import re

def clean_text(text):

    # ============================================
    # REPLACE OCR SYMBOL JOINS
    # Example:
    # Earth-REwolves -> Earth REwolves
    # ============================================

    text = re.sub(
        r'[-_/]',
        ' ',
        text
    )

    # ============================================
    # REMOVE SPECIAL SYMBOLS
    # KEEP LETTERS, NUMBERS, SPACES, DOTS
    # ============================================

    text = re.sub(
        r'[^a-zA-Z0-9\s.]',
        '',
        text
    )

    # ============================================
    # NORMALIZE MULTIPLE SPACES
    # ============================================

    text = re.sub(
        r'\s+',
        ' ',
        text
    ).strip()

    # ============================================
    # CONVERT TO LOWERCASE
    # KEEP THIS AT END
    # ============================================

    text = text.lower()

    return text