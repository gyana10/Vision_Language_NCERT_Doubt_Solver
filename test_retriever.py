from backend.rag.retriever import retrieve_docs


query = "What is integers?"


results = retrieve_docs(query)


for i, doc in enumerate(results):

    print("\n")
    print("=" * 60)

    print(f"RESULT {i+1}")

    print("=" * 60)

    print(doc.page_content)