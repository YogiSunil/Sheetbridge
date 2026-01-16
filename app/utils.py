import re

def extract_spreadsheet_id(sheet_value: str) -> str:
    """
    Accepts either a full Google Sheets URL or a raw spreadsheet ID.
    Returns the spreadsheet ID or empty string.
    """
    sheet_value = (sheet_value or "").strip()
    if not sheet_value:
        return ""

    # If it's already an ID (no slashes, reasonable length)
    if "/" not in sheet_value and len(sheet_value) >= 20:
        return sheet_value

    # Typical URL: https://docs.google.com/spreadsheets/d/<ID>/edit...
    m = re.search(r"/spreadsheets/d/([a-zA-Z0-9-_]+)", sheet_value)
    if m:
        return m.group(1)

    return ""
