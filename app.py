"""Flask backend API for the real-time plagiarism checker."""

from __future__ import annotations

import sys
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from algorithms.rabin_karp import RabinKarpDetector
from database.db import add_reference_code, delete_reference_code, init_db, list_reference_codes

FRONTEND_DIR = ROOT_DIR / "frontend"

app = Flask(__name__, static_folder=str(FRONTEND_DIR), static_url_path="")
init_db(seed=True)


@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET,POST,DELETE,OPTIONS"
    return response


@app.route("/")
def index():
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.route("/api/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/api/references", methods=["GET"])
def get_references():
    references = list_reference_codes()
    return jsonify([
        {
            "id": ref.id,
            "filename": ref.filename,
            "language": ref.language,
            "code": ref.code,
            "characters": len(ref.code),
        }
        for ref in references
    ])


@app.route("/api/references", methods=["POST"])
def create_reference():
    payload = request.get_json(force=True) or {}
    filename = (payload.get("filename") or "untitled.txt").strip()
    language = (payload.get("language") or "Text").strip()
    code = payload.get("code") or ""

    if not code.strip():
        return jsonify({"error": "Reference code cannot be empty."}), 400

    reference_id = add_reference_code(filename, language, code)
    return jsonify({"id": reference_id, "filename": filename, "language": language, "code": code}), 201


@app.route("/api/references/<int:reference_id>", methods=["DELETE"])
def remove_reference(reference_id: int):
    deleted = delete_reference_code(reference_id)
    if not deleted:
        return jsonify({"error": "Reference not found."}), 404
    return jsonify({"deleted": True})


@app.route("/api/check", methods=["POST"])
def check_plagiarism():
    payload = request.get_json(force=True) or {}
    submitted_code = payload.get("student_code") or ""
    chunk_size = int(payload.get("chunk_size") or 80)
    chunk_size = max(20, min(chunk_size, 200))

    if not submitted_code.strip():
        return jsonify({"error": "Student submitted code cannot be empty."}), 400

    references = list_reference_codes()
    detector = RabinKarpDetector(chunk_size=chunk_size)
    result = detector.find_matches(submitted_code, references)
    result["references_checked"] = len(references)
    result["chunk_size"] = chunk_size
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
