from spellchecker import SpellChecker

spell = SpellChecker()

def correct_spelling(text):

    words = text.split()

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

    return corrected_text