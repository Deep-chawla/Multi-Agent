from bootstrap.server import start_application
from app.adapters.langchain.message_adapter import LangChainMessageAdapter
from app.graph.state import GraphState

import asyncio
import time


async def main():

    app = start_application()
    conversation_service = app.conversation_service

    # Temporary values
    user_id = "user-1"
    conversation_id = "chat-1"

    config = {
        "configurable": {
            "thread_id": conversation_id
        }
    }

    print("=" * 50)
    print("Multi Agent Platform")
    print("Type 'exit' to quit.")
    print("=" * 50)

    while True:

        question = input("\nYou : ")
        if question.lower() == "exit":
            break


        # Get or create conversation
        conversation = conversation_service.get_or_create_conversation(
            conversation_id=conversation_id,
            user_id=user_id,
        )

        # t0 = time.perf_counter()

        # Save user message
        conversation_service.add_user_message(
            conversation_id=conversation.id,
            content=question,
        )

        # t1 = time.perf_counter()
        # Load complete conversation history
        history = conversation_service.get_history(
            conversation.id
        )

        # t2 = time.perf_counter()

        # Convert domain messages -> LangChain messages
        langchain_messages = LangChainMessageAdapter.to_langchain(
            history
        )
        # t3 = time.perf_counter()

        print("AI : ", end="", flush=True)
        response_chunks = []

       
        async for message, metadata in app.workflow.graph.astream(
            {
                "messages": langchain_messages
            },
            config=config,
            stream_mode="messages",
        ):


            # Ignore intermediate nodes
            if metadata.get("langgraph_node") != "final_response":
                continue

            if message.content:
                print(message.content, end="", flush=True)
                response_chunks.append(message.content)

        final_response = "".join(response_chunks)

        # t4 = time.perf_counter()

        # Save assistant response
        conversation_service.add_assistant_message(
            conversation_id=conversation.id,
            content=final_response,
            agent="multi-agent",  # Temporary
        )

        # t5 = time.perf_counter()

        # print(f"""
        #     Add User Message      : {(t1-t0):.3f}s
        #     Load History          : {(t2-t1):.3f}s
        #     Adapter               : {(t3-t2):.3f}s
        #     LangGraph + LLM       : {(t4-t3):.3f}s
        #     Save Assistant        : {(t5-t4):.3f}s
        #     Total                 : {(t5-t0):.3f}s
        #     """)
        print()


if __name__ == "__main__":
    asyncio.run(main())