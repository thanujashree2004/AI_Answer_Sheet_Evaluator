from utils.question_detector import (
    detect_question_numbers
)


# =====================================================
# REALISTIC OCR OUTPUT TEST
# =====================================================

sample_text = """
1. Artificial Intelligence is the simulation
of human intelligence processes by machines.

These systems can learn and reason.

Q2 Machine Learning is a subset of AI
which helps systems learn automatically.

Question 3 OCR converts image text
into editable machine-readable text.

I) Deep Learning uses neural networks.

l. Natural Language Processing helps
machines understand human language.
"""


# =====================================================
# RUN DETECTOR
# =====================================================

detected_questions = detect_question_numbers(
    sample_text
)

print("\nDetected Question Numbers:")
print(detected_questions)