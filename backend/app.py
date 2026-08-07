from flask import Flask, request, jsonify, render_template
from backend.main import run_evaluation
import os
import uuid
import json
import threading
from threading import Lock

# =========================================================
# BASE DIRECTORY FIX (IMPORTANT)
# =========================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates")
)

# =========================================================
# SETUP
# =========================================================

UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
ANSWER_KEY_FOLDER = os.path.join(BASE_DIR, "answer_keys")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(ANSWER_KEY_FOLDER, exist_ok=True)

# =========================================================
# DISK-BACKED JOB STORE
# (Previously an in-memory dict "jobs = {}" — that gets wiped
# any time the Flask process restarts, which is what caused
# "Invalid job id" after the debug reloader or a manual
# restart. Persisting to a JSON file survives restarts.)
# =========================================================
JOBS_FILE = os.path.join(BASE_DIR, "jobs_store.json")
jobs_lock = Lock()


def load_jobs():
    if os.path.exists(JOBS_FILE):
        try:
            with open(JOBS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return {}
    return {}


def save_job(job_id, data):
    with jobs_lock:
        jobs = load_jobs()
        jobs[job_id] = data
        with open(JOBS_FILE, "w", encoding="utf-8") as f:
            json.dump(jobs, f)


def get_job(job_id):
    return load_jobs().get(job_id)

# =========================================================
# HOME PAGE
# =========================================================
@app.route("/")
def home():
    return render_template("index.html")


# =========================================================
# OPTIONAL: INDEX PAGE ROUTE (if you use index.html)
# =========================================================
@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/how-it-works")
def how_it_works():
    return render_template("howitworks.html")


@app.route("/file-upload")
def file_upload():
    return render_template("file_upload.html")


@app.route("/result/<job_id>")
def result(job_id):
    return render_template("result.html", job_id=job_id)

# =========================================================
# UPLOAD ENDPOINT
# =========================================================
@app.route("/upload", methods=["POST"])
def upload_file():

    file = request.files.get("file")

    if not file:
        return jsonify({"error": "No file received"}), 400

    job_id = str(uuid.uuid4())

    file_path = os.path.join(UPLOAD_FOLDER, f"{job_id}_{file.filename}")
    file.save(file_path)

    save_job(job_id, {
        "status": "processing",
        "result": None
    })

    thread = threading.Thread(
        target=process_file,
        args=(job_id, file_path)
    )
    thread.start()

    return jsonify({
        "job_id": job_id,
        "status": "started"
    })

# =========================================================
# ANSWER KEY UPLOAD
# =========================================================
@app.route("/upload-answer-key", methods=["POST"])
def upload_answer_key():

    file = request.files.get("answer_key")

    if not file:
        return jsonify({
            "error": "No answer key received"
        }), 400

    # Remove previous answer key
    for existing_file in os.listdir(ANSWER_KEY_FOLDER):

        file_path = os.path.join(
            ANSWER_KEY_FOLDER,
            existing_file
        )

        if os.path.isfile(file_path):
            os.remove(file_path)

    # Save new answer key
    save_path = os.path.join(
        ANSWER_KEY_FOLDER,
        file.filename
    )

    file.save(save_path)

    return jsonify({
        "message": "Answer key uploaded successfully"
    })
# =========================================================
# BACKGROUND PROCESSING
# =========================================================
def process_file(job_id, file_path):

    try:
        result = run_evaluation(file_path)

        save_job(job_id, {
            "status": "done",
            "result": result
        })

    except Exception as e:
        save_job(job_id, {
            "status": "error",
            "result": str(e)
        })


# =========================================================
# STATUS CHECK (POLLING)
# =========================================================
@app.route("/status/<job_id>", methods=["GET"])
def get_status(job_id):

    job = get_job(job_id)

    if not job:
        return jsonify({"error": "Invalid job id"}), 404

    return jsonify(job)


# =========================================================
# RUN SERVER
# =========================================================
if __name__ == "__main__":
    # use_reloader=False: the reloader watches every file in the project,
    # including images/segmented_lines/evaluation_output.json that the
    # pipeline writes to mid-job — those writes were triggering restarts
    # in the middle of an evaluation, wiping job state.
    app.run(debug=True, use_reloader=False)