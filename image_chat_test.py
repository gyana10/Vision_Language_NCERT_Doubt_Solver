from backend.rag.rag_pipeline import ask_image_question


image_path = "test_images/question.png"


response = ask_image_question(
    image_path=image_path,
    selected_class="class9",
    selected_subject="science"
)


print("\n")
print("=" * 60)
print("AI ANSWER")
print("=" * 60)

print(response)