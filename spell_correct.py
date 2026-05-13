# =========================================================
# CONTEXTUAL SPELL CORRECTION USING T5
# =========================================================

from transformers import AutoTokenizer
from transformers import AutoModelForSeq2SeqLM

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(
    "vennify/t5-base-grammar-correction"
)

model = AutoModelForSeq2SeqLM.from_pretrained(
    "vennify/t5-base-grammar-correction"
)

# =========================================================
# SPELL CORRECTION FUNCTION
# =========================================================

def correct_spelling(text):

    input_text = "grammar: " + text

    input_ids = tokenizer.encode(
        input_text,
        return_tensors="pt",
        max_length=256,
        truncation=True
    )

    outputs = model.generate(
        input_ids,
        max_length=256,
        num_beams=4,
        early_stopping=True
    )

    corrected_text = tokenizer.decode(
        outputs[0],
        skip_special_tokens=True
    )

    return corrected_text