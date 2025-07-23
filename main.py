from flask import Flask, request, jsonify
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

app = Flask(__name__)

# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)
sheet = client.open("Trading Alerts").sheet1  # Ensure this exists

# Telegram setup
TELEGRAM_BOT_TOKEN = "7767603804:AAHAIIWhjo3sjCQinRLTQVmybGvZe_G4QmE"
TELEGRAM_CHAT_ID = "665594180"

@app.route('/')
def home():
    return "TradingView Webhook Bot is Live"

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.json
        symbol = data.get("symbol", "N/A")
        price = data.get("price", "N/A")
        note = data.get("note", "")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Telegram alert
        message = f"📈 *Swing Alert*\n\n*Symbol:* {symbol}\n*Price:* {price}\n*Note:* {note}\n🕐 {timestamp}"
        telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        requests.post(telegram_url, json={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "Markdown"
        })

        # Google Sheets logging
        sheet.append_row([timestamp, symbol, price, note])
        return jsonify({"status": "success"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
