from utils.text_classifier import is_meaningful_answer

samples = [
    "PART A",
    "Answer all questions",
    "SECTION B",
    "Artificial Intelligence simulates human intelligence",
    "Choose any five",
    "Machine learning uses data"
]

for text in samples:
    result = is_meaningful_answer(text)
    print(f"{text} --> {result}")