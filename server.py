from flask import Flask, jsonify
from google.oauth2 import service_account
from googleapiclient.discovery import build

app = Flask(__name__)

SERVICE_ACCOUNT_FILE = "service-account.json"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
SPREADSHEET_ID = "1xp54tKOczklmT8uacW-HMxwV8r0VOR2ui33jYcE2pUQ"
RANGE_NAME = "可預約班次(web)!A1:Z"

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
service = build("sheets", "v4", credentials=credentials)

@app.route("/api/sheet")
def get_sheet_data():
    result = (
        service.spreadsheets()
        .values()
        .get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME)
        .execute()
    )
    return jsonify(result.get("values", []))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
