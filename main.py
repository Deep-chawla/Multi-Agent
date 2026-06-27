from bootstrap.server import start_application


def main():
    app = start_application()

    print("=" * 50)
    print("Multi Agent Platform")
    print("Type 'exit' to quit.")
    print("=" * 50)

    while True:
        question = input("\nYou : ")

        if question.lower() == "exit":
            break

        # Ask supervisor which agent should handle the request
        route = app.super_visor.route(question)

        if route == "coding":
            agent = app.coding_agent
        else:
            agent = app.general_agent

        print("AI : ", end="", flush=True)

        for token in agent.stream(question):
            print(token, end="", flush=True)

        print()


if __name__ == "__main__":
    main()