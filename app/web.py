import io
import pandas as pd
from flask import Blueprint, current_app, jsonify, render_template, request
from app.sheets_client import get_sheets_service, fetch_range_as_rows
from app.utils import extract_spreadsheet_id

web_bp = Blueprint("web", __name__)

def rows_to_objects(rows):
    """Convert 2D array of rows into list of objects using first row as headers"""
    if not rows or len(rows) < 2:
        return []

    headers = [str(h).strip() for h in rows[0]]
    objects = []
    for row in rows[1:]:
        # Pad row if it's shorter than headers
        padded = row + [""] * (len(headers) - len(row))
        obj = {headers[i]: (padded[i].strip() if isinstance(padded[i], str) else padded[i])
               for i in range(len(headers))}
        # Only include rows that have at least one non-empty value
        if any(str(v).strip() for v in obj.values()):
            objects.append(obj)
    return objects

@web_bp.get("/")
def home():
    return render_template("index.html")

@web_bp.post("/convert_link")
def convert_link():
    data = request.get_json(silent=True) or {}
    sheet_value = (data.get("sheet") or "").strip()
    sheet_range = (data.get("range") or "").strip()
    header_row = (data.get("header_row") or "").strip()

    spreadsheet_id = extract_spreadsheet_id(sheet_value)
    if not spreadsheet_id:
        return jsonify({"error": "bad_request", "message": "Invalid Google Sheets URL or spreadsheet ID"}), 400

    try:
        service = get_sheets_service(current_app.config["GOOGLE_CREDENTIALS_PATH"])
        
        # If user doesn't provide a range, auto-detect the first sheet name
        if not sheet_range:
            from app.sheets_client import get_sheet_names
            sheet_names = get_sheet_names(service, spreadsheet_id)
            if not sheet_names:
                return jsonify({"error": "bad_request", "message": "No sheets found in spreadsheet"}), 400
            # Use first sheet with a default range
            first_sheet = sheet_names[0]
            sheet_range = f"{first_sheet}!A1:Z200"

        rows = fetch_range_as_rows(service, spreadsheet_id, sheet_range)

        # Optional: allow choosing header row inside the fetched range
        if header_row.isdigit():
            n = int(header_row)
            # header_row=1 means first row in range, so index 0
            idx = max(0, n - 1)
            if idx < len(rows):
                rows = [rows[idx]] + rows[idx+1:]

        objects = rows_to_objects(rows)

        return jsonify({
            "data": objects,
            "meta": {
                "spreadsheet_id": spreadsheet_id,
                "range": sheet_range,
                "rows_returned": len(objects)
            }
        })
    except Exception as e:
        return jsonify({"error": "conversion_failed", "message": str(e)}), 500

@web_bp.post("/convert")
def convert_file_to_json():
    """Legacy file upload endpoint"""
    if "file" not in request.files:
        return jsonify({"error": "bad_request", "message": "Missing file"}), 400

    f = request.files["file"]
    filename = (f.filename or "").lower()

    try:
        if filename.endswith(".csv"):
            df = pd.read_csv(f)
        elif filename.endswith(".xlsx"):
            content = f.read()
            df = pd.read_excel(io.BytesIO(content), engine="openpyxl")
        else:
            return jsonify({"error": "bad_request", "message": "Only .csv or .xlsx supported"}), 400

        df = df.dropna(how='all')
        
        if df.shape[0] > 1:
            first_row_text_count = sum(isinstance(val, str) for val in df.iloc[0])
            if first_row_text_count > len(df.columns) * 0.5:
                df.columns = df.iloc[0]
                df = df[1:].reset_index(drop=True)
        
        df.columns = [str(col).replace('\n', ' ').strip() for col in df.columns]
        df = df.dropna(axis=1, how='all')
        df = df.fillna("")
        
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
