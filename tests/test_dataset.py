from datasets import load_dataset
from jiwer import wer
import pandas as pd
import os
import shutil

from backend.ocr_module import extract_text

print("Loading Dataset...")

dataset = load_dataset("Teklia/IAM-line")

results = []

os.makedirs("temp_lines", exist_ok=True)

for i in range(50):

    print(f"\nProcessing Sample {i+1}")

    sample = dataset["test"][i]

    image = sample["image"]
    actual_text = sample["text"]

    # Clear old files
    shutil.rmtree("temp_lines", ignore_errors=True)
    os.makedirs("temp_lines")

    # Save image
    image_path = "temp_lines/line_1.jpg"
    image.save(image_path)

    # Run OCR
    predicted_text = extract_text("temp_lines")

    # Accuracy
    error = wer(actual_text, predicted_text)

    accuracy = max(0, (1 - error) * 100)

    results.append({
        "Sample": i + 1,
        "Ground Truth": actual_text,
        "OCR Output": predicted_text,
        "Accuracy": round(accuracy, 2)
    })

    print("GT :", actual_text)
    print("OCR:", predicted_text)
    print("Accuracy:", round(accuracy, 2), "%")

df = pd.DataFrame(results)

df.to_csv(
    "tests/ocr_report.csv",
    index=False
)

average_accuracy = df["Accuracy"].mean()

print("\n======================")
print("FINAL REPORT")
print("======================")
print("Average OCR Accuracy:", round(average_accuracy, 2), "%")
print("Report Saved: tests/ocr_report.csv")