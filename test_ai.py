import easyocr
from sentence_transformers import SentenceTransformer, util

print("Libraries loaded successfully!")

# semantic model
model = SentenceTransformer('all-MiniLM-L6-v2')

teacher_answer = "Data redundancy means duplication of data."

student_answer = "Repeated storage of same information."

# Convert text to embeddings
emb1 = model.encode(teacher_answer, convert_to_tensor=True)
emb2 = model.encode(student_answer, convert_to_tensor=True)

# Calculate similarity

score = util.cos_sim(emb1, emb2)

print("Similarity Score:")
print(score)