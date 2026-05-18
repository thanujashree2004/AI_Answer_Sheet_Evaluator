# =========================================================
# MAIN AI ANSWER SHEET EVALUATION SYSTEM (DEBUG VERSION)
# =========================================================

from preprocess import preprocess_image
from line_segment import segment_lines
from ocr_module import extract_text
from clean_text import clean_text
from spell_correct import correct_spelling
from evaluation import evaluate_answer


# =========================================================
# LOAD ANSWER KEY
# =========================================================

with open("answer_key.txt", "r", encoding="utf-8") as file:
    reference_answer = file.read()

reference_answer = clean_text(reference_answer)

print("\n==============================")
print("ANSWER KEY")
print("==============================")
print(reference_answer)


# =========================================================
# IMAGE PATHS
# =========================================================

original_image = "images/student_answer.jpg"
processed_image = "images/processed.jpg"


# =========================================================
# IMAGE PREPROCESSING
# =========================================================

print("\n==============================")
print("IMAGE PREPROCESSING")
print("==============================")

preprocess_image(original_image, processed_image)


# =========================================================
# LINE SEGMENTATION (DEBUG ENHANCED)
# =========================================================

print("\n==============================")
print("LINE SEGMENTATION")
print("==============================")

segmented_output = segment_lines(processed_image)


# 🔴 DEBUG: CHECK SEGMENTATION OUTPUT
print("\n==============================")
print("SEGMENTATION DEBUG INFO")
print("==============================")

try:
    print("Total segmented files:", len(segmented_output))

    for i, box in enumerate(segmented_output):
        print(f"Line {i+1}: {box}")

except Exception as e:
    print("DEBUG ERROR: segment_lines() does not return boxes")
    print("Reason:", e)


# =========================================================
# OCR EXTRACTION
# =========================================================

print("\n==============================")
print("READING SEGMENTED LINES")
print("==============================")

ocr_text = extract_text("segmented_lines")


print("\n==============================")
print("RAW OCR TEXT")
print("==============================")
print(ocr_text)


# =========================================================
# SPELL CORRECTION
# =========================================================

corrected_text = correct_spelling(ocr_text)

print("\n==============================")
print("SPELL CORRECTED TEXT")
print("==============================")
print(corrected_text)


# =========================================================
# TEXT CLEANING
# =========================================================

cleaned_text = clean_text(corrected_text)

print("\n==============================")
print("CLEANED TEXT")
print("==============================")
print(cleaned_text)


# =========================================================
# Q4 SPECIFIC DEBUG CHECK
# =========================================================

print("\n==============================")
print("Q4 FAILURE DEBUG CHECK")
print("==============================")

lines = cleaned_text.split("\n")

for i, line in enumerate(lines):
    print(f"Line {i+1}: {line}")

    if "4" in line or "question 4" in line.lower():
        print("🔴 POSSIBLE Q4 LINE FOUND:", line)


# =========================================================
# AI ANSWER EVALUATION
# =========================================================

print("\n==============================")
print("AI ANSWER EVALUATION")
print("==============================")

result = evaluate_answer(cleaned_text)


# =========================================================
# FINAL OUTPUT
# =========================================================

print("\n==============================")
print("FINAL OUTPUT")
print("==============================")

print(f"Total Marks : {result['total_marks']}")

print("\nAI Evaluation Pipeline Executed Successfully!")