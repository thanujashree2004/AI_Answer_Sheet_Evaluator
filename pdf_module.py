import fitz
import os

# ============================================
# PDF TO IMAGE CONVERSION
# ============================================

def convert_pdf_to_images(pdf_path):

    output_folder = "pdf_pages"

    os.makedirs(
        output_folder,
        exist_ok=True
    )

    # Clear old pages

    for file in os.listdir(output_folder):

        file_path = os.path.join(
            output_folder,
            file
        )

        if os.path.isfile(file_path):
            os.remove(file_path)

    # Open PDF

    pdf_document = fitz.open(pdf_path)

    image_paths = []

    # Convert each page

    for page_number in range(len(pdf_document)):

        page = pdf_document[page_number]

        pix = page.get_pixmap(
            matrix=fitz.Matrix(2, 2)
        )

        image_path = os.path.join(
            output_folder,
            f"page_{page_number + 1}.jpg"
        )

        pix.save(image_path)

        image_paths.append(image_path)

        print(f"Saved: {image_path}")

    pdf_document.close()

    return image_paths