from sentence_transformers import SentenceTransformer, util
import spacy

print("Loading Similarity Model...")

model = SentenceTransformer(
    'all-MiniLM-L6-v2'
)

nlp = spacy.load("en_core_web_sm")

print("Similarity Model Loaded!")

def calculate_similarity(student_text, reference_text):

    student_sentences = [
        sent.text.strip()
        for sent in nlp(student_text).sents
    ]

    reference_sentences = [
        sent.text.strip()
        for sent in nlp(reference_text).sents
    ]

    scores = []

    print("\n==============================")
    print("SENTENCE LEVEL ANALYSIS")
    print("==============================")

    for student, reference in zip(
        student_sentences,
        reference_sentences
    ):

        emb1 = model.encode(
            student,
            convert_to_tensor=True
        )

        emb2 = model.encode(
            reference,
            convert_to_tensor=True
        )

        similarity = util.cos_sim(
            emb1,
            emb2
        )

        score = similarity.item()

        scores.append(score)

        print("\n--------------------------------")
        print("Student Sentence:")
        print(student)

        print("\nReference Sentence:")
        print(reference)

        print(f"\nSimilarity Score: {round(score, 4)}")

    if len(scores) > 0:
        average_score = sum(scores) / len(scores)
    else:
        average_score = 0

    return average_score