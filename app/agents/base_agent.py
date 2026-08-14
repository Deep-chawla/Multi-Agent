from abc import ABC
from pyexpat.errors import messages
from langchain_core.messages import (
    BaseMessage,
    SystemMessage,
    ToolMessage,
)

from collections import defaultdict

class BaseAgent(ABC):
    """
    Base class for all AI agents.
    """

    def __init__(self, llm, system_prompt, tools=None):
        self.llm = llm
        self.system_prompt = system_prompt
        self.tools = tools or []
    
        if self.tools:
            self.model = self.llm.client.bind_tools(self.tools)
        else:
            self.model = self.llm.client

    def _build_messages(self, messages: list[BaseMessage]):
        return [
            SystemMessage(content=self.system_prompt),
            *messages,
        ]

    def invoke(self, messages: list[BaseMessage]):
    
        final_messages = self._build_messages(messages)

        response = self.model.invoke(final_messages)
        
        if not self.tools or not response.tool_calls:
            return response

        return self._execute_tools(final_messages, response)
    
    async def ainvoke(self, messages: list[BaseMessage]):
        final_messages = self._build_messages(messages)

        response = await self.model.ainvoke(final_messages)

        if not self.tools or not response.tool_calls:
            return response

        return await self._aexecute_tools(
            final_messages,
            response,
        )

    def _execute_tools(self, final_messages, response, return_messages=False):
        tool_map = {
            tool.name: tool
            for tool in self.tools
        }

        messages = final_messages + [response]
        while response.tool_calls:

            tool_messages = []

            for tool_call in response.tool_calls:
                tool = tool_map.get(tool_call["name"])

                if tool is None:
                    tool_messages.append(
                        ToolMessage(
                            content=f"Tool '{tool_call['name']}' not found.",
                            tool_call_id=tool_call["id"],
                        )
                    )
                    continue

                try:
                    result = tool.invoke(tool_call["args"])

                except Exception as e:
                    result = f"Tool Error: {e}"

                tool_messages.append(
                    ToolMessage(
                        content=str(result),
                        tool_call_id=tool_call["id"],
                    )
                )

            messages.extend(tool_messages)
            response = self.model.invoke(messages)
            messages.append(response)
            if return_messages:
                return messages

        return response
    


    async def _aexecute_tools(
        self,
        final_messages,
        response,
        return_messages=False,
    ):
        tool_map = {
            tool.name: tool
            for tool in self.tools
        }

        messages = final_messages + [response]

        # Prevent infinite tool loops
        MAX_TOOL_ITERATIONS = 5

        # Per-tool limits
        TOOL_LIMITS = {
            "web_search": 1,
            # "url_reader": 5,
            # "calculator": 10,
        }

        tool_usage = defaultdict(int)

        for _ in range(MAX_TOOL_ITERATIONS):

            if not response.tool_calls:
                break

            tool_messages = []

            for tool_call in response.tool_calls:
                tool_name = tool_call["name"]

                tool = tool_map.get(tool_name)

                if tool is None:
                    tool_messages.append(
                        ToolMessage(
                            content=f"Tool '{tool_name}' not found.",
                            tool_call_id=tool_call["id"],
                        )
                    )
                    continue

                # ---------- Tool limit ----------
                tool_usage[tool_name] += 1

                limit = TOOL_LIMITS.get(tool_name)

                if limit is not None and tool_usage[tool_name] > limit:
                    tool_messages.append(
                        ToolMessage(
                            content=(
                                f"The tool '{tool_name}' has already been used "
                                f"{limit} time(s). Use the previous tool results "
                                f"to answer the user."
                            ),
                            tool_call_id=tool_call["id"],
                        )
                    )
                    continue

                # ---------- Execute Tool ----------
                try:
                    result = tool.invoke(tool_call["args"])

                except Exception as e:
                    result = f"Tool Error: {e}"

                tool_messages.append(
                    ToolMessage(
                        content=str(result),
                        tool_call_id=tool_call["id"],
                    )
                )

            messages.extend(tool_messages)

            try:
                response = await self.model.ainvoke(messages)
            except Exception:
                break
            messages.append(response)

        if return_messages:
            return messages

        return response

    def stream(self, messages: list[BaseMessage]):
        final_messages = self._build_messages(messages)
        response = self.model.invoke(final_messages)
        # No tools
        if not self.tools or not response.tool_calls:
            yield from self.model.stream(final_messages)
            return

        # Execute tools
        history = self._execute_tools(
            final_messages,
            response,
            return_messages=True,
        )
        # Remove the last AIMessage
        history = history[:-1]
        # Stream final answer
        yield from self.model.stream(history)



    async def astream(self, messages):
        final_messages = self._build_messages(messages)
        response = await self.model.ainvoke(final_messages)
        if not self.tools or not response.tool_calls:
            async for chunk in self.model.astream(final_messages):
                yield chunk
            return
        history = await self._aexecute_tools(
            final_messages,
            response,
            return_messages=True,
        )
        history = history[:-1]
        async for chunk in self.model.astream(history):
            yield chunk