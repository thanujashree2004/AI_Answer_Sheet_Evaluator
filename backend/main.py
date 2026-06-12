# =========================================================
# MAIN AI ANSWER SHEET EVALUATION SYSTEM
# FULL PAGE HANDWRITTEN OCR + NLP PIPELINE
# MULTIPLE QUESTION SUPPORT
# MULTI PAGE PDF SUPPORT
# =========================================================

from backend.preprocess import preprocess_image
from backend.line_segment import segment_lines
from backend.ocr_module import extract_text
from backend.clean_text import clean_text
from backend.spell_correct import correct_spelling
from backend.evaluation import evaluate_answer
from backend.pdf_module import convert_pdf_to_images
import os
# =========================================================
# UTILITY IMPORTS
# =========================================================

from backend.utils.cleanup import clear_old_files
from backend.utils.json_saver import save_output_json
from backend.utils.exception_handler import handle_exception

from backend.utils.text_classifier import (
    is_meaningful_answer,
    is_strike_text
)

# =========================================================
# QUESTION DETECTOR IMPORT
# =========================================================

from backend.utils.question_detector import (
    detect_question_numbers,
    find_missing_questions
)


# =========================================================
# MAIN EXECUTION FUNCTION
# =========================================================

def run_evaluation(pdf_path):

    try:

        # =====================================================
        # CLEAR OLD GENERATED FILES
        # =====================================================

        clear_old_files()

        # =====================================================
        # LOAD ANSWER KEY
        # =====================================================

        BASE_DIR = os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
            )
        )

        ANSWER_KEY_FOLDER = os.path.join(
            BASE_DIR,
            "answer_keys"
        )

        answer_key_files = os.listdir(
            ANSWER_KEY_FOLDER
        )

        if not answer_key_files:

            raise Exception(
                "No answer key uploaded. Please upload an answer key first."
            )

        answer_key_path = os.path.join(
            ANSWER_KEY_FOLDER,
            answer_key_files[0]
        )

        with open(
            answer_key_path,
            "r",
            encoding="utf-8"
        ) as file:

            reference_answer = file.read()

        reference_answer = clean_text(
            reference_answer
        )

        print("\n==============================")
        print("ANSWER KEY")
        print("==============================")
        print(reference_answer)

        # =====================================================
        # PDF INPUT
        # =====================================================

        page_images = convert_pdf_to_images(
            pdf_path
        )

        # =====================================================
        # MULTI PAGE PDF PROCESSING
        # =====================================================

        all_ocr_text = []

        for index, image_path in enumerate(page_images):

            print("\n==============================")
            print(f"PROCESSING PAGE {index + 1}")
            print("==============================")

            processed_image = (
                f"images/processed_{index + 1}.jpg"
            )

            # =================================================
            # IMAGE PREPROCESSING
            # =================================================

            print("\n==============================")
            print("IMAGE PREPROCESSING")
            print("==============================")

            preprocess_image(
                image_path,
                processed_image
            )

            # =================================================
            # LINE SEGMENTATION
            # =================================================

            print("\n==============================")
            print("LINE SEGMENTATION")
            print("==============================")

            segment_lines(
                processed_image,
                index + 1
            )

            # =================================================
            # OCR EXTRACTION USING TrOCR
            # =================================================

            print("\n==============================")
            print("READING SEGMENTED LINES")
            print("==============================")

            page_text = extract_text(
                f"segmented_lines/page_{index + 1}"
            )

            print("\n==============================")
            print("PAGE OCR TEXT")
            print("==============================")
            print(page_text)

            all_ocr_text.append(page_text)

        # =====================================================
        # COMBINED OCR TEXT
        # =====================================================

        ocr_text = "\n".join(all_ocr_text)

        print("\n==============================")
        print("RAW OCR TEXT")
        print("==============================")
        print(ocr_text)

        # =====================================================
        # QUESTION NUMBER DETECTION
        # =====================================================

        detected_questions = detect_question_numbers(
            ocr_text
        )

        print("\n==============================")
        print("DETECTED QUESTION NUMBERS")
        print("==============================")
        print(detected_questions)

        # =====================================================
        # FIND MISSING QUESTIONS
        # =====================================================

        missing_questions = find_missing_questions(
            detected_questions
        )

        print("\n==============================")
        print("MISSING QUESTIONS")
        print("==============================")

        if missing_questions:

            print(missing_questions)

        else:

            print("No Missing Questions")

        # =====================================================
        # INTELLIGENT ANSWER FILTERING
        # =====================================================

        filtered_lines = []

        for line in ocr_text.split("\n"):

            if (
                is_meaningful_answer(line)
                and not is_strike_text(line)
            ):

                filtered_lines.append(line)

        filtered_text = "\n".join(filtered_lines)

        print("\n==============================")
        print("FILTERED ANSWER TEXT")
        print("==============================")
        print(filtered_text)

        # =====================================================
        # SPELL CORRECTION
        # =====================================================

        corrected_text = correct_spelling(
            filtered_text
        )

        print("\n==============================")
        print("SPELL CORRECTED TEXT")
        print("==============================")
        print(corrected_text)

        # =====================================================
        # TEXT CLEANING
        # =====================================================

        cleaned_text = clean_text(
            corrected_text
        )

        print("\n==============================")
        print("CLEANED TEXT")
        print("==============================")
        print(cleaned_text)

        # =====================================================
        # AI ANSWER EVALUATION
        # =====================================================

        print("\n==============================")
        print("AI ANSWER EVALUATION")
        print("==============================")

        result = evaluate_answer(
            cleaned_text
        )

        # =====================================================
        # SAVE JSON OUTPUT
        # =====================================================

        save_output_json(
            detected_questions,
            missing_questions,
            ocr_text,
            filtered_text,
            corrected_text,
            cleaned_text,
            result
        )

        # =====================================================
        # FINAL OUTPUT
        # =====================================================

        print("\n==============================")
        print("FINAL OUTPUT")
        print("==============================")

        print(
            f"Total Marks : {result['total_marks']}"
        )

        print(
            "\nAI Evaluation Pipeline Executed Successfully!"
        )

        return result

    except Exception as error:

        handle_exception(error)

        return {
            "error": str(error)
        }


# =========================================================
# MANUAL TESTING
# =========================================================

if __name__ == "__main__":

    run_evaluation(
        "student_answer.pdf"
    )