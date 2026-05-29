import re
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')

STOP_WORDS = set(stopwords.words('english'))


# =========================================================
# DETECT MEANINGFUL ANSWER CONTENT
# =========================================================

def is_meaningful_answer(text):

    text = text.strip()

    # Empty text
    if not text:
        return False

    # Very short text
    if len(text.split()) <= 1:
        return False

    # Uppercase heading detection
    if text.isupper() and len(text.split()) <= 5:
        return False

    # Instruction-like patterns
    instruction_patterns = [
        r'answer',
        r'question',
        r'section',
        r'part\s+[a-z]',
        r'choose',
        r'any\s+\d+',
        r'all\s+questions',
        r'marks'
    ]

    lower_text = text.lower()

    instruction_score = 0

    for pattern in instruction_patterns:

        if re.search(pattern, lower_text):
            instruction_score += 1

    # Ignore instruction-like lines
    if instruction_score >= 1:
        return False

    # Extract words
    words = re.findall(
        r'\b[a-zA-Z]+\b',
        lower_text
    )

    # Keep meaningful words only
    meaningful_words = [

        word for word in words

        if (
            word not in STOP_WORDS
            and len(word) > 2
        )
    ]

    # Too few meaningful words
    if len(meaningful_words) < 2:
        return False

    return True


# =========================================================
# DETECT STRIKE / CANCELLED / NOISY TEXT
# =========================================================

def is_strike_text(text):

    text = text.strip()

    if not text:
        return False

    total_chars = len(text)

    # Count alphabets
    alpha_chars = sum(
        c.isalpha() for c in text
    )

    # Count symbols
    symbol_chars = sum(

        not c.isalnum()
        and not c.isspace()

        for c in text
    )

    # Ratio calculations
    alpha_ratio = alpha_chars / total_chars
    symbol_ratio = symbol_chars / total_chars

    # Detect repeated noisy characters
    repeated_noise = (

        text.count("/") +
        text.count("\\") +
        text.count("x") +
        text.count("-") +
        text.count("_")
    )

    # Detect low character diversity
    unique_chars = set(
        text.replace(" ", "").lower()
    )

    # Repeated same-character noise
    if (
        len(unique_chars) <= 2
        and total_chars > 8
    ):
        return True

    # Intelligent noisy strike detection
    if (
        symbol_ratio > 0.35
        and alpha_ratio < 0.5
        and repeated_noise > 5
    ):
        return True

    return False