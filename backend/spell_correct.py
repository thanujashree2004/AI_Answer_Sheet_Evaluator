# =========================================================
# CONTEXTUAL SPELL CORRECTION USING T5
# IMPROVED FOR MULTIPLE QUESTION ANSWERS
# =========================================================

from transformers import AutoTokenizer
from transformers import AutoModelForSeq2SeqLM
import re


# =========================================================
# LOAD TOKENIZER AND MODEL
# =========================================================

tokenizer = AutoTokenizer.from_pretrained(
    "vennify/t5-base-grammar-correction"
)

model = AutoModelForSeq2SeqLM.from_pretrained(
    "vennify/t5-base-grammar-correction"
)


# =========================================================
# FIX QUESTION NUMBER FORMATTING
# =========================================================

def fix_question_format(text):

    # Converts:
    # 1 .
    # 2 .
    # 3 )
    # into:
    # 1.
    # 2.
    # 3.

    text = re.sub(
        r'(\d+)\s*[\.\)]\s*',
        r'\1. ',
        text
    )

    return text


# =========================================================
# REBUILD QUESTION NUMBER SEQUENCE
# =========================================================

def rebuild_question_sequence(text):

    # Find all question numbers
    pattern = r'(\d+)\.\s'

    matches = list(
        re.finditer(pattern, text)
    )

    # If no numbers found
    if len(matches) == 0:

        return text


    rebuilt_text = ""

    expected_number = 1

    current_position = 0


    # =====================================
    # HANDLE TEXT BEFORE FIRST QUESTION
    # =====================================

    first_match = matches[0]

    if first_match.start() > 0:

        first_answer = text[
            0:first_match.start()
        ].strip()

        if first_answer:

            rebuilt_text += (
                f"{expected_number}. "
                + first_answer
                + " "
            )

            expected_number += 1


    # =====================================
    # REBUILD NORMAL QUESTION FLOW
    # =====================================

    for i in range(len(matches)):

        actual_number = int(
            matches[i].group(1)
        )

        start = matches[i].end()

        if i + 1 < len(matches):

            end = matches[i + 1].start()

        else:

            end = len(text)

        answer_text = text[
            start:end
        ].strip()


        # Fill missing sequence
        while expected_number < actual_number:

            rebuilt_text += (
                f"{expected_number}. "
            )

            expected_number += 1


        rebuilt_text += (
            f"{actual_number}. "
            + answer_text
            + " "
        )

        expected_number = actual_number + 1


    return rebuilt_text.strip()


# =========================================================
# SPELL CORRECTION FUNCTION
# =========================================================

def correct_spelling(text):

    # -------------------------------------
    # FIX QUESTION NUMBER FORMATTING
    # -------------------------------------

    text = fix_question_format(text)


    # -------------------------------------
    # PREPARE INPUT
    # -------------------------------------

    input_text = "grammar: " + text


    # -------------------------------------
    # TOKENIZE
    # -------------------------------------

    input_ids = tokenizer.encode(
        input_text,
        return_tensors="pt",
        max_length=512,
        truncation=True
    )


    # -------------------------------------
    # GENERATE CORRECTED TEXT
    # -------------------------------------

    outputs = model.generate(
        input_ids,
        max_length=512,
        num_beams=4,
        early_stopping=True
    )


    # -------------------------------------
    # DECODE OUTPUT
    # -------------------------------------

    corrected_text = tokenizer.decode(
        outputs[0],
        skip_special_tokens=True
    )


    # -------------------------------------
    # FIX QUESTION FORMAT AGAIN
    # -------------------------------------

    corrected_text = fix_question_format(
        corrected_text
    )


    # -------------------------------------
    # REBUILD QUESTION SEQUENCE
    # -------------------------------------

    corrected_text = rebuild_question_sequence(
        corrected_text
    )


    return corrected_text