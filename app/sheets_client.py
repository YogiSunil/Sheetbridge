from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

def get_sheets_service(credentials_path: str):
    creds = service_account.Credentials.from_service_account_file(
        credentials_path, scopes=SCOPES
    )
    return build("sheets", "v4", credentials=creds)

def get_sheet_names(service, spreadsheet_id: str):
    """Get list of sheet names in the spreadsheet"""
    spreadsheet = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
    sheets = spreadsheet.get('sheets', [])
    return [sheet['properties']['title'] for sheet in sheets]

def fetch_range_as_rows(service, spreadsheet_id: str, sheet_range: str):
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=sheet_range
    ).execute()
    return result.get("values", [])
