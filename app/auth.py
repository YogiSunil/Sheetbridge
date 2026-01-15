from flask import current_app, request, jsonify

def require_api_key():
    expected = current_app.config.get("API_KEY", "")
    provided = request.headers.get("X-API-Key", "")

    if not expected or provided != expected:
        return jsonify({"error": "unauthorized", "message": "Invalid or missing API key"}), 401

    return None
