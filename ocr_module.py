from transformers import (
    TrOCRProcessor,
    VisionEncoderDecoderModel
)

from PIL import Image
import torch
import os

# ============================================
# LOAD TrOCR MODEL
# ============================================

print("Loading TrOCR Model...")

processor = TrOCRProcessor.from_pretrained(
    "microsoft/trocr-base-handwritten"
)

model = VisionEncoderDecoderModel.from_pretrained(
    "microsoft/trocr-base-handwritten"
)

device = (
    "cuda"
    if torch.cuda.is_available()
    else "cpu"
)

model.to(device)

print("TrOCR Loaded Successfully!")

# ============================================
# OCR FUNCTION
# ============================================

def extract_text_from_line(image_path):

    image = Image.open(
        image_path
    ).convert("RGB")

    pixel_values = processor(
        image,
        return_tensors="pt"
    ).pixel_values.to(device)

    generated_ids = model.generate(
        pixel_values,
        max_new_tokens=100
    )

    generated_text = processor.batch_decode(
        generated_ids,
        skip_special_tokens=True
    )[0]

    return generated_text

# ============================================
# MAIN OCR PIPELINE
# ============================================

def extract_text(folder_path):

    extracted_lines = []

    # Get all segmented line images
    files = sorted(
        os.listdir(folder_path)
    )

    for file in files:

        if file.endswith(".jpg"):

            line_path = os.path.join(
                folder_path,
                file
            )

            print(f"\nReading: {file}")

            text = extract_text_from_line(
                line_path
            )

            print("Extracted Text:", text)

            extracted_lines.append(text)

    # Combine all lines
    final_text = "\n".join(
        extracted_lines
    )

    return final_text