from backend.utils.question_detector import (
    detect_question_numbers,
    find_missing_questions
)

sample_text = """
1. The earth revolves around the sun

3. DBMS manages data

4. Cloud computing provides storage
"""

questions = detect_question_numbers(
    sample_text
)

missing = find_missing_questions(
    questions
)

print("Detected Questions :", questions)

print("Missing Questions :", missing)