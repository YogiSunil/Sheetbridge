# SheetBridge

A simple Flask app that converts Google Sheets and uploaded files to JSON format. Works as both a web interface and an API.

## What It Does

- **Google Sheets to JSON**: Paste a Google Sheets link and get the data as JSON
- **File Upload**: Upload .csv or .xlsx files and convert them to JSON
- **Download JSON**: Download the converted data as a .json file
- **API Access**: Use the API endpoint with authentication for programmatic access
- **Caching**: Responses are cached for 60 seconds to reduce API calls
- **Rate Limiting**: Limited to 30 requests per minute

## Setup

### 1. Install Required Packages

```bash
pip install -r requirements.txt
```

### 2. Create Environment File

Create a `.env` file in the `sheetbridge` folder:

```
API_KEY=your-secret-api-key-here
GOOGLE_CREDENTIALS_PATH=credentials/service_account.json
```

### 3. Add Google Service Account

You need Google credentials to access sheets:

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a service account with Google Sheets API enabled
3. Download the credentials JSON file
4. Save it as `credentials/service_account.json`

### 4. Share Your Google Sheet

Give your Google Sheet access to the service account:
- Find the `client_email` in your credentials file
- Share the sheet with that email
- Give it "Viewer" permission (read-only)

## How to Run

```bash
python app/main.py
```

Open http://127.0.0.1:5000 in your browser to use the web interface.

## Using the Web Interface

1. **Option 1: Google Sheets Link**
   - Paste your Google Sheets URL or spreadsheet ID
   - Optionally specify a cell range (e.g., A1:D100)
   - Click "Convert from Google Sheets"
   - Your JSON data will appear below
   - Click "Download JSON" to save it

2. **Option 2: Upload File**
   - Choose a .csv or .xlsx file
   - Click "Convert from File"
   - Your JSON data will appear below
   - Click "Download JSON" to save it

## Using the API

### Endpoint: GET `/api/sheets`

Get data from a Google Sheet via API.

**Required Header:**
```
X-API-Key: your-secret-api-key-here
```

**Parameters:**
- `spreadsheet_id` - The ID from your Google Sheets URL
- `range` - Cell range like `Sheet1!A1:D100` (required)

**Example:**
```bash
curl -H "X-API-Key: your-secret-api-key-here" \
  "http://127.0.0.1:5000/api/sheets?spreadsheet_id=YOUR_ID&range=Sheet1!A1:D10"
```

**Response:**
```json
{
  "data": [
    ["Name", "Email"],
    ["John", "john@example.com"],
    ["Jane", "jane@example.com"]
  ],
  "meta": {
    "cached": false
  }
}
```

## Demo Checklist
Project Structure

```
sheetbridge/
├── app/
│   ├── __init__.py              # Creates Flask app with config
│   ├── main.py                  # Starts the server
│   ├── routes.py                # API endpoint code
│   ├── web.py                   # Web interface routes
│   ├── auth.py                  # API key checking
│   ├── cache.py                 # Caching setup
│   ├── sheets_client.py         # Google Sheets API helper
│   └── utils.py                 # Helper functions
├── templates/
│   └── index.html               # Web interface HTML
├── credentials/
│   └── service_account.json     # Google credentials (keep secret!)
├── .env                         # Environment variables (keep secret!)
├── .gitignore                   # Files to ignore in git
├── requirements.txt             # Python packages needed
└── README.md                    # This file
```

## What Each File Does

- **app/__init__.py** - Sets up Flask with rate limiting and blueprints
- **app/main.py** - Entry point that runs the server
- **app/routes.py** - Handles `/api/sheets` endpoint for API access
- **app/web.py** - Handles web page routes and file conversion
- **app/sheets_client.py** - Connects to Google Sheets API
- **app/auth.py** - Checks if API key is valid
- **app/cache.py** - Stores responses to avoid repeating requests
- **app/utils.py** - Helper function to extract sheet ID from URL

## Important Notes

- Don't share your `.env` file or credentials with anyone
- Your Google credentials file should be kept secret
- The API key should be long and random
- This is for development/learning - not for production
- Responses are cached for 60 seconds (to save API calls)
- You can only make 30 requests per minute (rate limit)