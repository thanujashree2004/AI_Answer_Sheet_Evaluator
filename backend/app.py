from flask import Flask, request, jsonify
from backend.main import run_evaluation

app = Flask(__name__)

@app.route("/")
def home():
    return "AI Answer Evaluator Backend Running"

@app.route("/upload", methods=["POST"])
def upload_file():

    file = request.files["file"]

    file.save(file.filename)

    result = run_evaluation(
        file.filename
    )

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)