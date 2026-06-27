from bootstrap.server import start_application

def main():
    agent = start_application()

    print("=" * 50)
    print("Multi Agent Platform")
    print("Type 'exit' to quit.")
    print("=" * 50)

    while True:
        question = input("\nYou : ")

        if question.lower() == "exit":
            break

        print("AI : ", end="", flush=True)

        for token in agent.general_agent.stream(question):
            print(token, end="", flush=True)
        print()


if __name__ == "__main__":
    main()