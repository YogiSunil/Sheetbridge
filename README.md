# SheetBridge

Convert Google Sheets and files to JSON format. Simple Flask web app with API support.

## Features

- **Google Sheets to JSON**: Convert sheets data by pasting a link
- **File Upload**: Upload CSV or Excel files for JSON conversion
- **Download JSON**: Download converted data as .json file
- **API Endpoint**: Programmatic access with API key authentication
- **Caching**: 60-second response caching to reduce API calls
- **Rate Limiting**: 30 requests per minute limit

## Installation

### Prerequisites
- Python 3.8 or higher
- Google Cloud service account with Sheets API enabled

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configuration

Create `.env` file in project root:

```
API_KEY=your-secret-api-key
GOOGLE_CREDENTIALS_PATH=credentials/service_account.json
```

### Google Sheets API Setup

1. Create service account at [Google Cloud Console](https://console.cloud.google.com)
2. Enable Google Sheets API
3. Download credentials JSON
4. Save as `credentials/service_account.json`
5. Share your sheet with service account email (viewer permission)

## Usage

### Running the Application

```bash
python app/main.py
```

Access the web interface at http://127.0.0.1:5000

### Web Interface

**Google Sheets Conversion:**
1. Paste Google Sheets URL or spreadsheet ID
2. Specify cell range (optional, e.g., A1:D100)
3. Click "Convert from Google Sheets"
4. Download JSON file

**File Upload:**
1. Select CSV or Excel file
2. Click "Convert from File"
3. Download JSON file

### API Access

**Endpoint:** `GET /api/sheets`

**Headers:**
```
X-API-Key: your-secret-api-key
```

**Query Parameters:**
- `spreadsheet_id` - Google Sheets ID
- `range` - Cell range (e.g., Sheet1!A1:D100)

**Example Request:**
```bash
curl -H "X-API-Key: your-key" \
  "http://127.0.0.1:5000/api/sheets?spreadsheet_id=YOUR_ID&range=Sheet1!A1:D10"
```

**Response:**
```json
{
  "data": [
    ["Name", "Email"],
    ["John", "john@example.com"]
  ],
  "meta": {
    "cached": false
  }
}
```

## Project Structure

```
sheetbridge/
├── app/
│   ├── __init__.py          # Flask app initialization
│   ├── main.py              # Application entry point
│   ├── routes.py            # API routes
│   ├── web.py               # Web interface routes
│   ├── auth.py              # API authentication
│   ├── cache.py             # Response caching
│   ├── sheets_client.py     # Google Sheets API client
│   └── utils.py             # Utility functions
├── templates/
│   └── index.html           # Web interface template
├── credentials/
│   └── service_account.json # Google credentials
├── .env                     # Environment variables
├── .gitignore
├── requirements.txt
└── README.md
```

## Technical Details

- **Framework:** Flask with blueprints architecture
- **Caching:** Flask-Caching with 60-second TTL
- **Rate Limiting:** Flask-Limiter (30 req/min)
- **Authentication:** API key validation
- **File Processing:** pandas, openpyxl

## Notes

- Keep `.env` and credentials files secure
- API key should be randomly generated
- Development use only - not production ready
- Cached responses expire after 60 seconds