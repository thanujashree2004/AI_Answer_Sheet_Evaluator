import json
from datetime import datetime

# =========================================================
# SAVE OUTPUT JSON
# =========================================================

def save_output_json(
    detected_questions,
    missing_questions,
    ocr_text,
    filtered_text,
    corrected_text,
    cleaned_text,
    result
):

    output_data = {

        "date": str(datetime.now()),

        "detected_questions": detected_questions,

        "missing_questions": missing_questions,

        "raw_ocr_text": ocr_text,

        "filtered_text": filtered_text,

        "corrected_text": corrected_text,

        "cleaned_text": cleaned_text,

        "total_marks": result["total_marks"]
    }

    with open(
        "evaluation_output.json",
        "w",
        encoding="utf-8"
    ) as json_file:

        json.dump(
            output_data,
            json_file,
            indent=4,
            ensure_ascii=False
        )

    print("\n==============================")
    print("JSON OUTPUT SAVED")
    print("==============================")