from flask import Flask, request, jsonify, render_template
from backend.main import run_evaluation
import os
import uuid
import threading

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
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

jobs = {}  # in-memory job tracker


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

    jobs[job_id] = {
        "status": "processing",
        "result": None
    }

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
# BACKGROUND PROCESSING
# =========================================================
def process_file(job_id, file_path):

    try:
        result = run_evaluation(file_path)

        jobs[job_id]["status"] = "done"
        jobs[job_id]["result"] = result

    except Exception as e:
        jobs[job_id]["status"] = "error"
        jobs[job_id]["result"] = str(e)


# =========================================================
# STATUS CHECK (POLLING)
# =========================================================
@app.route("/status/<job_id>", methods=["GET"])
def get_status(job_id):

    job = jobs.get(job_id)

    if not job:
        return jsonify({"error": "Invalid job id"}), 404

    return jsonify(job)


# =========================================================
# RUN SERVER
# =========================================================
if __name__ == "__main__":
    app.run(debug=True)