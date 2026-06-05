from flask import Flask, request, jsonify
from backend.main import run_evaluation
import json
import threading
import uuid
import os

app = Flask(__name__)

# =========================================================
# GLOBAL JOB STORE (simple in-memory tracker)
# =========================================================

jobs = {}

# =========================================================
# HOME ROUTE
# =========================================================

@app.route("/")
def home():
    return "AI Answer Evaluator Backend Running"


# =========================================================
# BACKGROUND PROCESS FUNCTION
# =========================================================

def process_file(job_id, file_path):

    try:

        result = run_evaluation(file_path)

        # store result
        jobs[job_id]["status"] = "done"
        jobs[job_id]["result"] = result

        # also save to file (optional)
        with open("evaluation_output.json", "w", encoding="utf-8") as f:
            json.dump(result, f, indent=4)

    except Exception as e:

        jobs[job_id]["status"] = "error"
        jobs[job_id]["error"] = str(e)


# =========================================================
# UPLOAD ROUTE (FAST RESPONSE NOW)
# =========================================================

@app.route("/upload", methods=["POST"])
def upload_file():

    try:

        file = request.files["file"]

        file_path = f"uploads/{uuid.uuid4()}_{file.filename}"

        file.save(file_path)

        result = run_evaluation(file_path)

        return jsonify(result)

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# =========================================================
# STATUS CHECK ROUTE (FOR FRONTEND POLLING)
# =========================================================

@app.route("/status/<job_id>", methods=["GET"])
def get_status(job_id):

    job = jobs.get(job_id)

    if not job:
        return jsonify({"error": "Invalid job id"}), 404

    return jsonify(job)


# =========================================================
# RESULTS ROUTE (optional direct file read)
# =========================================================

@app.route("/results", methods=["GET"])
def get_results():

    try:
        with open("evaluation_output.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        return jsonify(data)

    except Exception as error:
        return jsonify({"error": str(error)})


# =========================================================
# RUN FLASK
# =========================================================

if __name__ == "__main__":
    app.run(debug=True)