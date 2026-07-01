from abc import ABC
from langchain_core.messages import (
    BaseMessage,
    SystemMessage,
    ToolMessage,
)


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

    def _execute_tools(self, final_messages, response):

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

        return response

    def stream(self, messages: list[BaseMessage]):

        final_messages = self._build_messages(messages)

        for chunk in self.model.stream(final_messages):
            yield chunk