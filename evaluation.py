from sentence_transformers import SentenceTransformer, util
from sklearn.feature_extraction.text import TfidfVectorizer
import string
import re


# =========================================
# CLEAN TEXT
# =========================================

def clean_text(text):

    text = text.lower()

    for p in string.punctuation:
        text = text.replace(p, "")

    return text


# =========================================
# SPLIT MULTIPLE ANSWERS
# =========================================

def split_answers(text):

    # -------------------------------------
    # REMOVE PART HEADINGS
    # Example:
    # PART A — 2 × 3 = 6
    # -------------------------------------

    text = re.sub(
        r'part\s+[a-z]\s*[—\-:]*\s*\d+\s*[x×]\s*\d+\s*=\s*\d+',
        '',
        text,
        flags=re.IGNORECASE
    )


    # -------------------------------------
    # REMOVE STANDALONE MARK SCHEMES
    # Example:
    # 2 × 3 = 6
    # -------------------------------------

    text = re.sub(
        r'\d+\s*[x×]\s*\d+\s*=\s*\d+',
        '',
        text
    )


    # -------------------------------------
    # HANDLES:
    # 1.
    # 1 .
    # 1)
    # 1 )
    # -------------------------------------

    pattern = r'(\d+)\s*[\.\)]\s*'

    matches = list(
        re.finditer(pattern, text)
    )

    answers = {}


    # =====================================
    # NO QUESTION NUMBERS FOUND
    # =====================================

    if len(matches) == 0:

        answers["1"] = text.strip()

        return answers


    # =====================================
    # HANDLE MISSING FIRST QUESTION
    # =====================================

    first_match = matches[0]

    if first_match.start() > 0:

        first_answer = text[
            0:first_match.start()
        ].strip()

        if first_answer:

            answers["1"] = first_answer


    # =====================================
    # EXTRACT NORMAL QUESTIONS
    # =====================================

    for i in range(len(matches)):

        question_no = matches[i].group(1)

        start = matches[i].end()

        if i + 1 < len(matches):

            end = matches[i + 1].start()

        else:

            end = len(text)

        answer_text = text[start:end].strip()

        answers[question_no] = answer_text


    return answers


# =========================================
# EXTRACT QUESTION MARK SCHEME
# =========================================

def extract_mark_scheme(answer_key_text):

    lines = answer_key_text.splitlines()

    question_marks = {}

    current_marks = 10


    for line in lines:

        line = line.strip()


        # ---------------------------------
        # DETECT:
        # 2 × 5 = 10
        # 10 x 2 = 20
        # ---------------------------------

        match = re.search(
            r'(\d+)\s*[x×]\s*(\d+)',
            line.lower()
        )

        if match:

            current_marks = int(
                match.group(1)
            )


        # ---------------------------------
        # DETECT QUESTION NUMBERS
        # ---------------------------------

        q_match = re.match(
            r'(\d+)\.',
            line
        )

        if q_match:

            question_no = q_match.group(1)

            question_marks[
                question_no
            ] = current_marks


    return question_marks


# =========================================
# MAIN EVALUATION FUNCTION
# =========================================

def evaluate_answer(student_answer):

    # -------------------------------------
    # READ ANSWER KEY
    # -------------------------------------

    with open(
        "answer_key.txt",
        "r",
        encoding="utf-8"
    ) as file:

        answer_key = file.read()


    # -------------------------------------
    # SPLIT ANSWERS
    # -------------------------------------

    teacher_answers = split_answers(
        answer_key
    )

    student_answers = split_answers(
        student_answer
    )


    # -------------------------------------
    # EXTRACT MARK SCHEME
    # -------------------------------------

    question_marks = extract_mark_scheme(
        answer_key
    )


    # -------------------------------------
    # LOAD MODEL
    # -------------------------------------

    model = SentenceTransformer(
        'all-MiniLM-L6-v2'
    )


    # -------------------------------------
    # STORE RESULTS
    # -------------------------------------

    total_marks = 0

    question_results = []


    # -------------------------------------
    # QUESTION-WISE EVALUATION
    # -------------------------------------

    for question_no in teacher_answers:

        # =====================================
        # IF STUDENT ANSWER EXISTS
        # =====================================

        if question_no in student_answers:

            teacher_text = clean_text(
                teacher_answers[question_no]
            )

            student_text = clean_text(
                student_answers[question_no]
            )


            # =====================================
            # SEMANTIC SIMILARITY (70%)
            # =====================================

            emb1 = model.encode(
                teacher_text,
                convert_to_tensor=True
            )

            emb2 = model.encode(
                student_text,
                convert_to_tensor=True
            )

            similarity = util.cos_sim(
                emb1,
                emb2
            ).item()

            semantic_score = similarity * 70


            # =====================================
            # AUTOMATIC KEYWORD EXTRACTION
            # =====================================

            vectorizer = TfidfVectorizer(
                stop_words='english'
            )

            tfidf_matrix = vectorizer.fit_transform(
                [teacher_text]
            )

            keywords = vectorizer.get_feature_names_out()


            # =====================================
            # KEYWORD MATCHING (30%)
            # =====================================

            matched_keywords = 0

            for word in keywords:

                if word in student_text:

                    matched_keywords += 1


            keyword_score = (
                matched_keywords / len(keywords)
            ) * 30


            # =====================================
            # FINAL SCORE
            # =====================================

            final_score = (
                semantic_score + keyword_score
            )


            # =====================================
            # DYNAMIC MARK ALLOCATION
            # =====================================

            max_marks = question_marks.get(
                question_no,
                10
            )

            marks = round(
                (final_score / 100)
                * max_marks,
                1
            )


            # =====================================
            # EVALUATION CATEGORY
            # =====================================

            if final_score >= 90:

                evaluation = (
                    "Excellent Answer Match"
                )

            elif final_score >= 75:

                evaluation = (
                    "Good Answer Match"
                )

            elif final_score >= 55:

                evaluation = (
                    "Partial Answer Match"
                )

            else:

                evaluation = (
                    "Poor Answer Match"
                )


        # =====================================
        # IF STUDENT DID NOT ANSWER
        # =====================================

        else:

            similarity = 0

            semantic_score = 0

            keyword_score = 0

            final_score = 0

            max_marks = question_marks.get(
                question_no,
                10
            )

            marks = 0

            evaluation = "Question Not Answered"


        # =====================================
        # STORE TOTAL MARKS
        # =====================================

        total_marks += marks


        # =====================================
        # STORE QUESTION RESULTS
        # =====================================

        question_results.append({

            "question": question_no,

            "similarity": similarity,

            "semantic_score": semantic_score,

            "keyword_score": keyword_score,

            "final_score": final_score,

            "marks": marks,

            "max_marks": max_marks,

            "evaluation": evaluation
        })


    # -------------------------------------
    # DISPLAY QUESTION-WISE RESULTS
    # -------------------------------------

    print("\n==============================")
    print("QUESTION-WISE EVALUATION")
    print("==============================")

    for result in question_results:

        print(
            f"\nQuestion {result['question']}"
        )

        print(
            f"Similarity Score : "
            f"{result['similarity']:.4f}"
        )

        print(
            f"Semantic Score   : "
            f"{result['semantic_score']:.2f}/70"
        )

        print(
            f"Keyword Score    : "
            f"{result['keyword_score']:.2f}/30"
        )

        print(
            f"Final Score      : "
            f"{result['final_score']:.2f}/100"
        )

        print(
            f"Marks Awarded    : "
            f"{result['marks']}/"
            f"{result['max_marks']}"
        )

        print(
            f"Evaluation       : "
            f"{result['evaluation']}"
        )


    # -------------------------------------
    # DISPLAY TOTAL MARKS
    # -------------------------------------

    print("\n==============================")
    print("TOTAL MARKS")
    print("==============================")

    print(
        f"Total Marks : {total_marks:.2f}"
    )


    # -------------------------------------
    # RETURN RESULTS
    # -------------------------------------

    return {

        "total_marks": total_marks,

        "question_results": question_results
    }