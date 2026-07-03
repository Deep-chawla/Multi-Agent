from bootstrap.server import start_application
from langchain_core.messages import HumanMessage


def main():

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

        for message, metadata in app.workflow.graph.stream(
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
    main()