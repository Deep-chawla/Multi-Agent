from langchain_core.messages import HumanMessage,AIMessage

from app.graph.state import GraphState,PlanStep
import time

from app.config.settings import Settings


class GraphNodes:

    def __init__(self, app):
        self.app = app

    def _get_step(self, state, agent: str):
        return next(
            step
            for step in state["plan"]
                if step["agent"] == agent
            )

    def supervisor(self, state: GraphState):
        """
        Create the execution plan.
        """
        # start = time.perf_counter()
        # print(f"SuperVisor Start : {start}")
        question = state["messages"][-3:]
        plan = self.app.supervisor.route(question)
        # print(f"Supervisor: {time.perf_counter()-start:.2f}s")

        return {
            "plan": plan["plan"],          # or plan["steps"] if you haven't renamed it yet
            "results": {}
        }

    def dispatcher(self, state: GraphState):
        """
        Decide which agent to execute next.
        """
        plan = state["plan"]
        current_step = state["current_step"]

        if current_step >= len(plan):

            if len(plan) == 1:
                return {
                    "next": "__end__"
                }
            return {
                "next": "final_response"
            }

        return {
            "next": plan[current_step]["agent"]
        }


    async def general(self, state: GraphState):
        start = time.perf_counter()
        print("General : ",start)
        # print(f"General Start : {start}")

        step = self._get_step(state,"general")
        messages = self._build_agent_messages(state,step)
        response = await self.app.general_agent.ainvoke(messages)


        return {
            "results":{
                "general": response.content
            },
        }
    
    async def coding(self, state: GraphState):
        # start = time.perf_counter()
        start = time.perf_counter()
        print("Coding : ",start)
        step = self._get_step(state,"coding")
        messages = self._build_agent_messages(state,step)
        response = await self.app.coding_agent.ainvoke(messages)

        # results = dict(state["results"])
        # results["coding"] = response.content
        # print(f"Supervisor: {time.perf_counter()-start:.2f}s")

        return {
            # "messages": [response],
            "results": {
                "coding":response.content
            },
        }

    async def research(self, state: GraphState):
        # print("Executing Research Agent...")
        start = time.perf_counter()
        print("Research : ",start)

        step = self._get_step(state,"research")
        messages = self._build_agent_messages(state,step)
        try:
            response = await self.app.research_agent.ainvoke(messages)
        except Exception as e:
            print(e)
            raise
        results = dict(state["results"])
        results["research"] = response.content

        return {
            # "messages": [response],
            "results": {
                "research":response.content
            },
            # "current_step": state["current_step"] + 1
        }
    

    async def knowledge(self, state: GraphState):
        # print("Executing Knowledge Agent...")
        start = time.perf_counter()
        print("Knowledge : ",start)
        step = self._get_step(state,"knowledge")
        messages = self._build_agent_messages(state,step)

        response = await self.app.knowledge_agent.ainvoke(messages)

        # results = dict(state["results"])
        # results["knowledge"] = response.content

        return {
            # "messages": [response],
            "results": {
                "knowledge":response.content
            },
        }
        

    async def final_response(self, state: GraphState):
        """
        Generate the final response for the user.

        - If only one agent produced an answer, return it directly.
        - If multiple agents produced answers, use the LLM to merge them.
        """
        start = time.perf_counter()
    
        results = state["results"]

        # No response
        if not results:
            return {
                "messages": [
                    AIMessage(content="I'm sorry, I couldn't generate a response.")
                ]
            }

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

        # print(response)
        # for i in state["messages"]:
        #     print(i)
        # print(f"Final: {time.perf_counter()-start:.2f}s")
        # print(response.content)
        return {
            "messages": [response]
        }
            
       

    def _build_agent_messages(self, state: GraphState,step :PlanStep):
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
        history = state["messages"][-Settings.MAX_HISTORY:]
        return [
            HumanMessage(content=prompt),
            *history
        ]