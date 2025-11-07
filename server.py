from flask import Flask, jsonify
from google.auth import default
from googleapiclient.discovery import build

app = Flask(__name__)

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
SPREADSHEET_ID = "1xp54tKOczklmT8uacW-HMxwV8r0VOR2ui33jYcE2pUQ"
RANGE_NAME = "可預約班次(web)!A1:Z"

# ✅ 使用 Cloud Run 內建服務帳號憑證
credentials, _ = default(scopes=SCOPES)
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
    import os
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
