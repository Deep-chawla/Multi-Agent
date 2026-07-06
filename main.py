from bootstrap.server import start_application
from langchain_core.messages import HumanMessage
import asyncio
import time


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
        start = time.perf_counter()

        if question.lower() == "exit":
            break

        print("AI : ", end="", flush=True)

        t1 = time.perf_counter()
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

        t2 = time.perf_counter()
        print(f"\n\n[Execution Time: {t2 - t1:.2f}s]")
        print()


if __name__ == "__main__":
    asyncio.run(main())