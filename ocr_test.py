# =========================================================
# AI ANSWER SHEET EVALUATION SYSTEM
# LARGE ANSWER OPTIMIZED VERSION
# =========================================================

import ssl
import certifi

ssl._create_default_https_context = lambda: ssl.create_default_context(
    cafile=certifi.where()
)

# =========================================================
# IMPORT LIBRARIES
# =========================================================

import easyocr
from spellchecker import SpellChecker
from sentence_transformers import SentenceTransformer, util
import spacy
import re

# =========================================================
# LOAD MODELS
# =========================================================

print("Loading Models...")

reader = easyocr.Reader(['en'])

spell = SpellChecker()

nlp = spacy.load("en_core_web_sm")

model = SentenceTransformer('all-MiniLM-L6-v2')

print("Models Loaded Successfully!")

# =========================================================
# STEP 1: LOAD ANSWER KEY
# =========================================================

with open("answer_key.txt", "r", encoding="utf-8") as file:
    reference_answer = file.read()

reference_answer = reference_answer.lower()

print("\n==============================")
print("ANSWER KEY")
print("==============================")
print(reference_answer)

# =========================================================
# STEP 2: OCR STUDENT ANSWER SHEET
# =========================================================

image_path = "images/student_answer.jpg"

print("\nReading Student Answer Sheet...")

result = reader.readtext(image_path)

ocr_text = ""

for item in result:
    ocr_text += item[1] + " "

ocr_text = ocr_text.strip()

print("\n==============================")
print("RAW OCR TEXT")
print("==============================")
print(ocr_text)

# =========================================================
# STEP 3: CLEAN TEXT
# =========================================================

clean_text = ocr_text.lower()

clean_text = re.sub(r'[^a-zA-Z0-9\s.]', '', clean_text)

clean_text = re.sub(r'\s+', ' ', clean_text).strip()

print("\n==============================")
print("CLEANED TEXT")
print("==============================")
print(clean_text)

# =========================================================
# STEP 4: SPELL CORRECTION
# =========================================================

words = clean_text.split()

corrected_words = []

for word in words:

    if len(word) <= 2:
        corrected_words.append(word)
        continue

    corrected = spell.correction(word)

    if corrected is None:
        corrected = word

    corrected_words.append(corrected)

corrected_text = " ".join(corrected_words)

print("\n==============================")
print("SPELL CORRECTED TEXT")
print("==============================")
print(corrected_text)

# =========================================================
# STEP 5: SENTENCE SPLITTING
# =========================================================

student_sentences = [
    sent.text.strip()
    for sent in nlp(corrected_text).sents
]

reference_sentences = [
    sent.text.strip()
    for sent in nlp(reference_answer).sents
]

print("\n==============================")
print("STUDENT SENTENCES")
print("==============================")

for i, sentence in enumerate(student_sentences, 1):
    print(f"{i}. {sentence}")

print("\n==============================")
print("REFERENCE SENTENCES")
print("==============================")

for i, sentence in enumerate(reference_sentences, 1):
    print(f"{i}. {sentence}")

# =========================================================
# STEP 6: SENTENCE LEVEL SEMANTIC SCORING
# =========================================================

scores = []

print("\n==============================")
print("SENTENCE LEVEL ANALYSIS")
print("==============================")

for student, reference in zip(student_sentences, reference_sentences):

    emb1 = model.encode(student, convert_to_tensor=True)
    emb2 = model.encode(reference, convert_to_tensor=True)

    similarity = util.cos_sim(emb1, emb2)

    score = similarity.item()

    scores.append(score)

    print("\n--------------------------------")
    print("Student Sentence:")
    print(student)

    print("\nReference Sentence:")
    print(reference)

    print(f"\nSimilarity Score: {round(score, 4)}")

# =========================================================
# STEP 7: FINAL SCORE
# =========================================================

if len(scores) > 0:
    average_score = sum(scores) / len(scores)
else:
    average_score = 0

print("\n==============================")
print("FINAL AVERAGE SCORE")
print("==============================")
print(round(average_score, 4))

# =========================================================
# STEP 8: MARKS ALLOCATION
# =========================================================

if average_score >= 0.90:
    marks = 10
elif average_score >= 0.75:
    marks = 8
elif average_score >= 0.55:
    marks = 6
else:
    marks = 3

print("\n==============================")
print("MARKS ALLOCATED")
print("==============================")
print(f"Marks: {marks}/10")

# =========================================================
# STEP 9: FINAL EVALUATION
# =========================================================

print("\n==============================")
print("FINAL EVALUATION")
print("==============================")

if average_score >= 0.90:
    print("Excellent Answer Match")
elif average_score >= 0.75:
    print("Good Answer Match")
elif average_score >= 0.55:
    print("Partial Answer Match")
else:
    print("Poor Answer Match")

# =========================================================
# EXECUTION COMPLETED
# =========================================================

print("\nAI Evaluation Pipeline Executed Successfully!")