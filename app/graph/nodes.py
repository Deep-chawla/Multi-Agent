from langchain_core.messages import HumanMessage,AIMessage,SystemMessage

from app.graph.state import GraphState,PlanStep
import time
from app.agents.superviser.schema import TaskExecution
from app.config.settings import Settings
from app.config.settings import logger


class GraphNodes:

    def __init__(self, app):
        self.app = app

    def supervisor(self, state: GraphState):
        start = time.perf_counter()
        latest_question = ""

        for message in reversed(state["messages"]):
            if isinstance(message, HumanMessage):
                latest_question = message.content
                break

        plan = self.app.supervisor.route(latest_question)["plan"]

        executions = {
            step["id"]: TaskExecution(step=PlanStep(**step))
            for step in plan
        } 
        

        logger.info(f"Supervisor: {time.perf_counter()-start:.2f}s")

        return {
            "plan": plan,
            "executions": executions,
            "results": {},
        }


    def scheduler(self, state: GraphState):

        executions = dict(state["executions"])

        for execution in executions.values():
            if execution.status != "PENDING":
                continue
            deps = execution.step.depends_on
            if all(
                executions[d].status == "COMPLETED"
                for d in deps
            ):
                execution.status = "READY"

        return {
            "executions": executions
        }


    async def general(self, state: GraphState):
        start = time.perf_counter()
        step = state["current_task"]
        executions = state["executions"]

        messages = self._build_agent_messages(state, step)

        try:
            response = await self.app.general_agent.ainvoke(messages)

            executions[step.id].status = "COMPLETED"
            executions[step.id].result = response.content
            
            logger.info(f"General: {time.perf_counter()-start:.2f}s")

            return {
                "results": {
                    "general": response.content
                },
                "executions": executions,
            }

        except Exception as e:


            executions[step.id].status = "FAILED"
            executions[step.id].error = str(e)

            logger.info(f"General: {time.perf_counter()-start:.2f}s")

            return {
                "executions": executions
            }
    
    async def coding(self, state: GraphState):
        start = time.perf_counter()

        step = state["current_task"]
        executions = state["executions"]

        messages = self._build_agent_messages(state, step)

        try:
            response = await self.app.coding_agent.ainvoke(messages)

            executions[step.id].status = "COMPLETED"
            executions[step.id].result = response.content

            logger.info(f"coding: {time.perf_counter()-start:.2f}s")


            return {
                "results": {
                    "coding": response.content
                },
                "executions": executions,
            }

        except Exception as e:
            executions[step.id].status = "FAILED"
            executions[step.id].error = str(e)

            logger.info(f"coding: {time.perf_counter()-start:.2f}s")


            return {
                "executions": executions
            }
        

    async def research(self, state: GraphState):
    
        start = time.perf_counter()
        step = state["current_task"]
        executions = state["executions"]

        messages = self._build_agent_messages(state, step)

        try:
            response = await self.app.research_agent.ainvoke(messages)

            executions[step.id].status = "COMPLETED"
            executions[step.id].result = response.content

            logger.info(f"research: {time.perf_counter()-start:.2f}s")


            return {
                "results": {
                    "research": response.content
                },
                "executions": executions,
            }

        except Exception as e:
            executions[step.id].status = "FAILED"
            executions[step.id].error = str(e)
            logger.info(f"research: {time.perf_counter()-start:.2f}s")

            return {
                "executions": executions
            }
                

    async def knowledge(self, state: GraphState):

        start = time.perf_counter()
        step = state["current_task"]
        executions = state["executions"]

        messages = self._build_agent_messages(state, step)

        try:
            response = await self.app.knowledge_agent.ainvoke(messages)

            executions[step.id].status = "COMPLETED"
            executions[step.id].result = response.content

            logger.info(f"Knoweldge: {time.perf_counter()-start:.2f}s")


            return {
                "results": {
                    "knowledge": response.content
                },
                "executions": executions,
            }

        except Exception as e:
            executions[step.id].status = "FAILED"
            executions[step.id].error = str(e)
            logger.info(f"Knowledge: {time.perf_counter()-start:.2f}s")

            return {
                "executions": executions
            }
                    

    async def final_response(self, state: GraphState):
        """
        Generate the final response for the user.

        - If only one agent produced an answer, return it directly.
        - If multiple agents produced answers, use the LLM to merge them.
        """
        start = time.perf_counter()
        logger.info(f"Final : {start:.2f}s")
    
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
    - The response Text should be in markDown (.md) format for better rendering.
    """
        

        response = await self.app.final_llm.ainvoke(
            [
                HumanMessage(content=prompt)
            ]
        )

        logger.info(f"Final : {time.perf_counter()-start:.2f}s")

        return {
            "messages": [response]
        }
            
       

    def _build_agent_messages(self, state: GraphState, step: PlanStep):
        previous_results = state["results"]

        original_query = ""

        for message in reversed(state["messages"]):
            if isinstance(message, HumanMessage):
                original_query = message.content
                break

        prompt = f"""
    Original User Request:
    {original_query}

    Your Assigned Task:
    {step.task}

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
            SystemMessage(content=prompt),
            *history,
        ]