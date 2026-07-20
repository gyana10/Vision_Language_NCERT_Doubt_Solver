from backend.ocr.vision import extract_text_from_image


image_path = "test_images/question.png"


text = extract_text_from_image(image_path)


print("\n")
print("=" * 60)
print("EXTRACTED TEXT")
print("=" * 60)

print(text)