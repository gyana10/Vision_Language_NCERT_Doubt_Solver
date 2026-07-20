from backend.rag.rag_pipeline import ask_question


while True:

    query = input("\nAsk your question: ")

    if query.lower() == "exit":
        break

    response = ask_question(query)

    print("\n")
    print("=" * 60)
    print("ANSWER")
    print("=" * 60)

    print(response)