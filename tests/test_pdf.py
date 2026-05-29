from backend.pdf_module import convert_pdf_to_images

pdf_path = "student_answer.pdf"

image_paths = convert_pdf_to_images(
    pdf_path
)

print("\nGenerated Images:\n")

for path in image_paths:
    print(path)