# SheetBridge - Google Sheets API Bridge

A Flask API that provides authenticated access to Google Sheets data with caching and rate limiting.

## Features

- ✅ Fetch data from Google Sheets and return as JSON
- ✅ API Key authentication
- ✅ Response caching (60 second TTL)
- ✅ Rate limiting (30 requests per minute)

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the `sheetbridge` directory:

```
API_KEY=change-me-to-a-long-random-string
GOOGLE_CREDENTIALS_PATH=credentials/service_account.json
```

### 3. Add Google Service Account Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a service account with Google Sheets API access
3. Download the JSON key file
4. Save it as `credentials/service_account.json`

### 4. Share Your Google Sheet

Share your Google Sheet with the service account email (found in the credentials JSON):
- Email: `client_email` from your credentials file
- Access level: **Viewer**

## Running the Application

```bash
cd sheetbridge
python app/main.py
```

The server will start at `http://127.0.0.1:5000`

## API Usage

### Endpoint: GET `/api/sheets`

Fetches data from a Google Sheet.

**Required Headers:**
- `X-API-Key`: Your API key from `.env`

**Query Parameters:**
- `spreadsheet_id`: The Google Sheets spreadsheet ID
- `range`: The sheet range (e.g., `Sheet1!A1:D10` or `Order Tracker!A1:D10`)

### Example Requests

**Without Authentication (401 Error):**
```bash
curl "http://127.0.0.1:5000/api/sheets?spreadsheet_id=YOUR_SHEET_ID&range=Sheet1!A1:D10"
```

**With Authentication (Success):**
```bash
curl -H "X-API-Key: change-me-to-a-long-random-string" \
  "http://127.0.0.1:5000/api/sheets?spreadsheet_id=YOUR_SHEET_ID&range=Sheet1!A1:D10"
```

**Response (Success):**
```json
{
  "data": [
    ["Name", "Email", "Phone"],
    ["John Doe", "john@example.com", "555-1234"],
    ["Jane Smith", "jane@example.com", "555-5678"]
  ],
  "meta": {
    "cached": false
  }
}
```

**Response (Cached):**
```json
{
  "data": [...],
  "meta": {
    "cached": true
  }
}
```

## Demo Checklist

### Objective 1: Fetch Google Sheets Data ✅
- [x] Connects to Google Sheets API
- [x] Returns data as JSON
- [x] Handles sheet names with spaces

### Objective 2: API Key Authentication ✅
- [x] Requires `X-API-Key` header
- [x] Returns 401 for invalid/missing keys
- [x] Returns 200 for valid keys

### Objective 3: Caching + Rate Limiting ✅
- [x] Caches responses for 60 seconds
- [x] Returns `cached: true` for cached responses
- [x] Rate limits to 30 requests per minute
- [x] Returns 429 when rate limit exceeded

## Project Structure

```
sheetbridge/
├── app/
│   ├── __init__.py          # Flask app factory with rate limiting
│   ├── main.py              # Entry point
│   ├── routes.py            # API endpoints
│   ├── auth.py              # API key authentication
│   ├── cache.py             # Response caching
│   └── sheets_client.py     # Google Sheets API client
├── credentials/
│   └── service_account.json # Google service account credentials
├── .env                     # Environment variables
├── .gitignore              # Git ignore rules
└── requirements.txt         # Python dependencies
```

## Security Notes

- Never commit `.env` or `credentials/` to version control
- Use a strong, random API key in production
- Consider using environment-specific API keys
- The development server is not suitable for production use
