import re


# =========================================================
# NORMALIZE OCR QUESTION NUMBER ERRORS
# =========================================================

def normalize_ocr_question_line(line):

    line = line.strip()

    # OCR sometimes reads:
    # 1 -> I
    # only fix at question-number position
    line = re.sub(
        r'^I\s*[\.\)]',
        '1.',
        line
    )

    return line


# =========================================================
# DETECT QUESTION NUMBERS FROM OCR TEXT
# =========================================================

def detect_question_numbers(text):

    lines = text.split("\n")

    detected_questions = []

    for line in lines:

        # OCR normalization
        line = normalize_ocr_question_line(
            line
        )

        # OCR-tolerant question detection
        # Supports:
        # 1.
        # 1 .
        # 1)
        # 1 )
        match = re.match(
            r'^\s*(\d+)\s*[\.\)]',
            line
        )

        if match:

            question_num = int(
                match.group(1)
            )

            detected_questions.append(
                question_num
            )

    return detected_questions


# =========================================================
# FIND MISSING QUESTION NUMBERS
# =========================================================

def find_missing_questions(question_numbers):

    if not question_numbers:
        return []

    missing_questions = []

    start = min(question_numbers)
    end = max(question_numbers)

    for num in range(start, end + 1):

        if num not in question_numbers:

            missing_questions.append(num)

    return missing_questions