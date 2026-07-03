from bootstrap.server import start_application
from langchain_core.messages import HumanMessage
import asyncio


async def main():

    app = start_application()

    config = {
        "configurable": {
            "thread_id": "user-1"
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

        print("AI : ", end="", flush=True)

        async for message, metadata in app.workflow.graph.astream(
            {
                "messages": [
                HumanMessage(content=question)
                ]
            },
            config=config,
            stream_mode="messages",
        ):

    # Ignore supervisor output
            if metadata["langgraph_node"] != "final_response":
                continue

            if message.content:
                print(message.content, end="", flush=True)

        print()


if __name__ == "__main__":
    asyncio.run(main())