import re


# =========================================================
# SMART OCR NORMALIZATION
# =========================================================

def normalize_ocr_question_line(line):

    line = line.strip()

    # =====================================================
    # REMOVE UNWANTED OCR SYMBOLS
    # =====================================================

    line = re.sub(
        r'^["\'`]+',
        '',
        line
    )

    # =====================================================
    # FIX SPACED OCR QUESTION NUMBER ERRORS
    # =====================================================

    # I . -> 1.
    line = re.sub(
        r'^\s*I\s*\.',
        '1.',
        line
    )

    # l . -> 1.
    line = re.sub(
        r'^\s*l\s*\.',
        '1.',
        line
    )

    # I ) -> 1)
    line = re.sub(
        r'^\s*I\s*\)',
        '1)',
        line
    )

    # l ) -> 1)
    line = re.sub(
        r'^\s*l\s*\)',
        '1)',
        line
    )

    # =====================================================
    # AUTO-CORRECT COMMON OCR CONFUSIONS
    # ONLY AT QUESTION NUMBER POSITION
    # =====================================================

    tokens = line.split()

    if not tokens:
        return line

    first_token = tokens[0]

    # =====================================================
    # OCR CONFUSION MAP
    # =====================================================

    confusion_map = {
        'I': '1',
        'l': '1',
        '|': '1',
        'O': '0',
        'o': '0',
        'S': '5'
    }

    corrected_token = ""

    for char in first_token:

        if char in confusion_map:
            corrected_token += confusion_map[char]

        else:
            corrected_token += char

    # Replace only first token
    tokens[0] = corrected_token

    corrected_line = " ".join(tokens)

    return corrected_line


# =========================================================
# DETECT QUESTION NUMBERS
# =========================================================

def detect_question_numbers(text):

    lines = text.split("\n")

    detected_questions = []

    for line in lines:

        # =================================================
        # SMART NORMALIZATION
        # =================================================

        line = normalize_ocr_question_line(line)

        # =================================================
        # FLEXIBLE QUESTION DETECTION
        # =================================================

        patterns = [

            # Q1 / Q.1
            r'^\s*Q\s*\.?\s*(\d+)',

            # Question 1
            r'^\s*Question\s*(\d+)',

            # 1. / 1)
            r'^\s*(\d+)\s*[\.\)]'
        ]

        for pattern in patterns:

            match = re.match(
                pattern,
                line,
                re.IGNORECASE
            )

            if match:

                question_num = int(
                    match.group(1)
                )

                detected_questions.append(
                    question_num
                )

                break

    return detected_questions


# =========================================================
# FIND MISSING QUESTIONS
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