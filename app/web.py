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

    try:
        if filename.endswith(".csv"):
            df = pd.read_csv(f)
        elif filename.endswith(".xlsx"):
            # read Excel from uploaded file bytes
            content = f.read()
            df = pd.read_excel(io.BytesIO(content), engine="openpyxl")
        else:
            return jsonify({"error": "bad_request", "message": "Only .csv or .xlsx supported"}), 400

        # Clean the data
        # 1. Remove completely empty rows
        df = df.dropna(how='all')
        
        # 2. Try to detect if first row should be header
        # If more than 50% of first row is text and subsequent rows are different, use first row as header
        if df.shape[0] > 1:
            first_row_text_count = sum(isinstance(val, str) for val in df.iloc[0])
            if first_row_text_count > len(df.columns) * 0.5:
                # Use first row as headers
                df.columns = df.iloc[0]
                df = df[1:].reset_index(drop=True)
        
        # 3. Clean column names - remove newlines and extra spaces
        df.columns = [str(col).replace('\n', ' ').strip() for col in df.columns]
        
        # 4. Remove columns that are completely empty
        df = df.dropna(axis=1, how='all')
        
        # 5. Fill NaN with empty string for cleaner JSON
        df = df.fillna("")
        
        # Convert to list of dicts (objects)
        records = df.to_dict(orient="records")

        return jsonify({
            "data": records, 
            "meta": {
                "rows": len(records),
                "columns": list(df.columns)
            }
        })
    except Exception as e:
        return jsonify({"error": "conversion_failed", "message": str(e)}), 500
