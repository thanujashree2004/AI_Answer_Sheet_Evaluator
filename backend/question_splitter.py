import re

def split_questions(text):
    """
    Splits OCR cleaned text into individual questions
    based on numbering like 1. 2. 3.
    """

    # split when number + dot appears
    parts = re.split(r'(?=\d+\.)', text)

    # remove empty parts
    questions = [p.strip() for p in parts if p.strip()]

    return questions