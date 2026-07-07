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

        start = time.perf_counter()

        # Get or create conversation
        conversation = conversation_service.get_or_create_conversation(
            conversation_id=conversation_id,
            user_id=user_id,
        )

        # Save user message
        conversation_service.add_user_message(
            conversation_id=conversation.id,
            content=question,
        )

        # Load complete conversation history
        history = conversation_service.get_history(
            conversation.id
        )

        # Convert domain messages -> LangChain messages
        langchain_messages = LangChainMessageAdapter.to_langchain(
            history
        )

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

        # Save assistant response
        conversation_service.add_assistant_message(
            conversation_id=conversation.id,
            content=final_response,
            agent="multi-agent",  # Temporary
        )

        end = time.perf_counter()

        print(f"\n\n[Execution Time: {end - start:.2f}s]")
        print()


if __name__ == "__main__":
    asyncio.run(main())