from flask import Flask, jsonify
from flask_cors import CORS  # ✅ 新增：CORS 支援
from google.auth import default
from googleapiclient.discovery import build
import json
import os

app = Flask(__name__)
CORS(app)  # ✅ 允許所有來源跨域（可改成指定來源）

# ====== Google Sheet 設定 ======
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
SPREADSHEET_ID = "1xp54tKOczklmT8uacW-HMxwV8r0VOR2ui33jYcE2pUQ"
RANGE_NAME = "可預約班次(web)!A1:Z"

# ✅ 使用 Cloud Run 內建服務帳號
credentials, _ = default(scopes=SCOPES)
service = build("sheets", "v4", credentials=credentials)

# ====== API 路由 ======
@app.route("/api/sheet")
def get_sheet_data():
    try:
        result = (
            service.spreadsheets()
            .values()
            .get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME)
            .execute()
        )
        # ✅ 用 ensure_ascii=False 讓中文直接顯示
        return app.response_class(
            response=json.dumps(result.get("values", []), ensure_ascii=False),
            status=200,
            mimetype="application/json",
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ====== 啟動 Flask ======
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
