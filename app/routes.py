from flask import Blueprint, current_app, jsonify, request
from app.sheets_client import get_sheets_service, fetch_range_as_rows
from app.auth import require_api_key
from app.cache import sheet_cache

api_bp = Blueprint("api", __name__)

@api_bp.route("/api/sheets", methods=["GET"])
def read_sheet():
    auth_error = require_api_key()
    if auth_error:
        return auth_error

    spreadsheet_id = request.args.get("spreadsheet_id", "").strip()
    sheet_range = request.args.get("range", "").strip()

    if not spreadsheet_id or not sheet_range:
        return jsonify({"error": "bad_request", "message": "Missing spreadsheet_id or range"}), 400

    cache_key = f"{spreadsheet_id}:{sheet_range}"
    if cache_key in sheet_cache:
        return jsonify({"data": sheet_cache[cache_key], "meta": {"cached": True}})

    service = get_sheets_service(current_app.config["GOOGLE_CREDENTIALS_PATH"])
    rows = fetch_range_as_rows(service, spreadsheet_id, sheet_range)

    sheet_cache[cache_key] = rows
    return jsonify({"data": rows, "meta": {"cached": False}})
