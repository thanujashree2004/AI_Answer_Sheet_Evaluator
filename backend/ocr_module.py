from transformers import (
    TrOCRProcessor,
    VisionEncoderDecoderModel
)

from PIL import Image
import torch
import os
import cv2
import numpy as np

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
# IMAGE PREPROCESSING
# ============================================

def preprocess_image(image_path):

    # Read image using OpenCV
    img = cv2.imread(image_path)

    # Convert to grayscale
    gray = cv2.cvtColor(
        img,
        cv2.COLOR_BGR2GRAY
    )

    # Remove noise
    denoise = cv2.fastNlMeansDenoising(
        gray
    )

    # Improve contrast
    thresh = cv2.adaptiveThreshold(
        denoise,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2
    )

    # Convert back to RGB
    processed = cv2.cvtColor(
        thresh,
        cv2.COLOR_GRAY2RGB
    )

    # ============================================
    # RESIZE IMAGE FOR BETTER TrOCR READING
    # ============================================

    height, width = processed.shape[:2]

    new_width = 1024

    new_height = int(
        (new_width / width) * height
    )

    processed = cv2.resize(
        processed,
        (new_width, new_height)
    )

    return processed

# ============================================
# OCR FUNCTION
# ============================================

def extract_text_from_line(image_path):

    # Apply preprocessing
    processed_image = preprocess_image(
        image_path
    )

    # Convert OpenCV image to PIL image
    image = Image.fromarray(
        processed_image
    )

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
        os.listdir(folder_path),
        key=lambda x: int(
            x.split("_")[1].split(".")[0]
        )
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