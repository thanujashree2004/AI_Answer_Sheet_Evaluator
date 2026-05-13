# =========================================================
# MAIN AI ANSWER SHEET EVALUATION SYSTEM
# FULL PAGE HANDWRITTEN OCR + NLP PIPELINE
# =========================================================

from preprocess import preprocess_image
from line_segment import segment_lines
from ocr_module import extract_text
from clean_text import clean_text
from spell_correct import correct_spelling
from similarity import calculate_similarity
from evaluation import evaluate_score

# =========================================================
# LOAD ANSWER KEY
# =========================================================

with open(
    "answer_key.txt",
    "r",
    encoding="utf-8"
) as file:

    reference_answer = file.read()

# Clean reference answer
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

preprocess_image(
    original_image,
    processed_image
)

# =========================================================
# LINE SEGMENTATION
# =========================================================

print("\n==============================")
print("LINE SEGMENTATION")
print("==============================")

segment_lines(processed_image)

# =========================================================
# OCR EXTRACTION USING TrOCR
# =========================================================

print("\n==============================")
print("READING SEGMENTED LINES")
print("==============================")

ocr_text = extract_text(
    "segmented_lines"
)

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
# SIMILARITY ANALYSIS
# =========================================================

average_score = calculate_similarity(
    cleaned_text,
    reference_answer
)

print("\n==============================")
print("FINAL AVERAGE SCORE")
print("==============================")
print(round(average_score, 4))

# =========================================================
# EVALUATION
# =========================================================

marks, evaluation = evaluate_score(
    average_score
)

print("\n==============================")
print("MARKS ALLOCATED")
print("==============================")
print(f"Marks: {marks}/10")

print("\n==============================")
print("FINAL EVALUATION")
print("==============================")
print(evaluation)

# =========================================================
# FINAL OUTPUT
# =========================================================

print("\nAI Evaluation Pipeline Executed Successfully!")