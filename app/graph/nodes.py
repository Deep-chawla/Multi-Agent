from langchain_core.messages import HumanMessage,AIMessage

from app.graph.state import GraphState


class GraphNodes:

    def __init__(self, app):
        self.app = app

    def supervisor(self, state: GraphState):
        """
        Create the execution plan.
        """
        question = state["messages"]
        plan = self.app.supervisor.route(question)

        return {
            "plan": plan["plan"],          # or plan["steps"] if you haven't renamed it yet
            "current_step": 0,
            "results": {}
        }

    def dispatcher(self, state: GraphState):
        """
        Decide which agent to execute next.
        """
        plan = state["plan"]
        current_step = state["current_step"]

        if current_step >= len(plan):
            return {
                "next": "final_response"
            }

        return {
            "next": plan[current_step]["agent"]
        }

    # def general(self, state: GraphState):
    #     print("Executing General Agent...")

    #     messages = self._build_agent_messages(state)
    #     response = self.app.general_agent.invoke(messages)

    #     results = dict(state["results"])
    #     results["general"] = response.content

    #     return {
    #         "messages": [response],
    #         "results": results,
    #         "current_step": state["current_step"] + 1
    #     }
    


    async def general(self, state: GraphState):
        print("Executing General Agent...")

        messages = self._build_agent_messages(state)

        response = await self.app.general_agent.ainvoke(messages)

        results = dict(state["results"])
        results["general"] = response.content

        return {
            "messages": [response],
            "results": results,
            "current_step": state["current_step"] + 1,
        }

    async def coding(self, state: GraphState):
        print("Executing Coding Agent...")

        messages = self._build_agent_messages(state)
        response = await self.app.coding_agent.ainvoke(messages)

        results = dict(state["results"])
        results["coding"] = response.content

        return {
            "messages": [response],
            "results": results,
            "current_step": state["current_step"] + 1
        }

    async def research(self, state: GraphState):
        print("Executing Research Agent...")

        messages = self._build_agent_messages(state)
        response = await self.app.research_agent.ainvoke(messages)
        results = dict(state["results"])
        results["research"] = response.content

        return {
            "messages": [response],
            "results": results,
            "current_step": state["current_step"] + 1
        }
    

    async def knowledge(self, state: GraphState):
        print("Executing Knowledge Agent...")

        messages = self._build_agent_messages(state)

        response = await self.app.knowledge_agent.ainvoke(messages)

        results = dict(state["results"])
        results["knowledge"] = response.content

        return {
            "messages": [response],
            "results": results,
            "current_step": state["current_step"] + 1
        }
        

    # def final_response(self, state: GraphState):
    #     """
    #     Combine all agent outputs into a single response.
    #     """
    #     parts = []

    #     for agent, output in state["results"].items():
    #         parts.append(output)

    #     return {
    #         "messages": [
    #             AIMessage(content="\n\n".join(parts))
    #         ]
    #     }




    async def final_response(self, state: GraphState):
        """
        Generate the final response for the user.

        - If only one agent produced an answer, return it directly.
        - If multiple agents produced answers, use the LLM to merge them.
        """

        results = state["results"]

        # No response
        if not results:
            return {
                "messages": [
                    AIMessage(content="I'm sorry, I couldn't generate a response.")
                ]
            }

        # # Single agent -> No extra LLM call
        # if len(results) == 1:
        #     return {
        #         "messages": [
        #             AIMessage(
        #                 content=next(iter(results.values()))
        #             )
        #         ]
        #     }


        original_query = ""

        for message in reversed(state["messages"]):
            if isinstance(message, HumanMessage):
                original_query = message.content
                break

        combined_context = "\n\n".join(
            f"### {agent.upper()} AGENT\n{output}"
            for agent, output in results.items()
        )

        prompt = f"""
    You are the final response generator of a multi-agent AI assistant.

    Original User Question:
    {original_query}

    Outputs from different agents:

    {combined_context}

    Instructions:
    - Combine the agent outputs into one natural response.
    - Remove duplicate information.
    - Preserve all important technical details.
    - If code is present, keep the formatting exactly as it is.
    - Present the answer as if it comes from a single assistant.
    - Do NOT mention agents.
    - Do NOT add information that is not present in the agent outputs.
    """

        response = await self.app.llm.ainvoke(
            [
                HumanMessage(content=prompt)
            ]
        )

        return {
            "messages": [response]
        }
            
       

    def _build_agent_messages(self, state: GraphState):
        step = state["plan"][state["current_step"]]
        previous_results = state["results"]

        original_query = ""

        for message in reversed(state["messages"]):
            if isinstance(message, HumanMessage):
                original_query = message.content
                break

        prompt = f"""
    Your Assigned Task:
    {step["task"]}

    Results from Previous Agents:
    {previous_results}

    Complete only your assigned task.
    """
        

        prompt = f"""
Original User Request:
{original_query}

Your Assigned Task:
{step["task"]}

Results from Previous Agents:
{previous_results}

You are one agent in a multi-agent system.

IMPORTANT:
- Perform ONLY your assigned task.
- Ignore all parts of the request that belong to other agents.
- Do not answer anything outside your assigned task.
- Another agent will handle the remaining tasks.
"""

        return [
            HumanMessage(content=prompt),
        ]