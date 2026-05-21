# =========================================================
# MAIN AI ANSWER SHEET EVALUATION SYSTEM
# FULL PAGE HANDWRITTEN OCR + NLP PIPELINE
# MULTIPLE QUESTION SUPPORT
# =========================================================

from preprocess import preprocess_image
from line_segment import segment_lines
from ocr_module import extract_text
from clean_text import clean_text
from spell_correct import correct_spelling
from evaluation import evaluate_answer

from utils.text_classifier import (
    is_meaningful_answer,
    is_strike_text
)

# =========================================================
# QUESTION DETECTOR IMPORT
# =========================================================

from utils.question_detector import (
    detect_question_numbers,
    find_missing_questions
)



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
reference_answer = clean_text(
    reference_answer
)

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

segment_lines(
    processed_image
)


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
# QUESTION NUMBER DETECTION
# =========================================================

detected_questions = detect_question_numbers(
    ocr_text
)

print("\n==============================")
print("DETECTED QUESTION NUMBERS")
print("==============================")
print(detected_questions)


# =========================================================
# FIND MISSING QUESTIONS
# =========================================================

missing_questions = find_missing_questions(
    detected_questions
)

print("\n==============================")
print("MISSING QUESTIONS")
print("==============================")

if missing_questions:
    print(missing_questions)

else:
    print("No Missing Questions")


# =========================================================
# INTELLIGENT ANSWER FILTERING
# =========================================================

filtered_lines = []

for line in ocr_text.split("\n"):

    if (
        is_meaningful_answer(line)
        and not is_strike_text(line)
    ):

        filtered_lines.append(line)

filtered_text = "\n".join(filtered_lines)

print("\n==============================")
print("FILTERED ANSWER TEXT")
print("==============================")
print(filtered_text)



# =========================================================
# SPELL CORRECTION
# =========================================================

corrected_text = correct_spelling(
    filtered_text
)

print("\n==============================")
print("SPELL CORRECTED TEXT")
print("==============================")
print(corrected_text)


# =========================================================
# TEXT CLEANING
# =========================================================

cleaned_text = clean_text(
    corrected_text
)

print("\n==============================")
print("CLEANED TEXT")
print("==============================")
print(cleaned_text)


# =========================================================
# AI ANSWER EVALUATION
# =========================================================

print("\n==============================")
print("AI ANSWER EVALUATION")
print("==============================")

result = evaluate_answer(
    cleaned_text
)


# =========================================================
# FINAL OUTPUT
# =========================================================

print("\n==============================")
print("FINAL OUTPUT")
print("==============================")

print(
    f"Total Marks : {result['total_marks']}"
)

print(
    "\nAI Evaluation Pipeline Executed Successfully!"
)