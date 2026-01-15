import io
import pandas as pd
from flask import Blueprint, jsonify, request, render_template

web_bp = Blueprint("web", __name__)

@web_bp.get("/")
def home():
    return render_template("index.html")

@web_bp.post("/convert")
def convert_file_to_json():
    if "file" not in request.files:
        return jsonify({"error": "bad_request", "message": "Missing file"}), 400

    f = request.files["file"]
    filename = (f.filename or "").lower()

    if filename.endswith(".csv"):
        df = pd.read_csv(f)
    elif filename.endswith(".xlsx"):
        # read Excel from uploaded file bytes
        content = f.read()
        df = pd.read_excel(io.BytesIO(content), engine="openpyxl")
    else:
        return jsonify({"error": "bad_request", "message": "Only .csv or .xlsx supported"}), 400

    # Convert to list of dicts (objects)
    records = df.fillna("").to_dict(orient="records")

    return jsonify({"data": records, "meta": {"rows": len(records)}})
