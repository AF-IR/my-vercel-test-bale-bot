import os
import json
from flask import Flask, request, jsonify
import requests

# توکن ربات از متغیر محیطی میاد (بعداً توی Vercel تنظیم می‌کنیم)
BOT_TOKEN = os.environ["BOT_TOKEN"]
BASE_URL = f"https://tapi.bale.ai/bot{BOT_TOKEN}"

app = Flask(__name__)

def send_message(chat_id, text):
    """یه پیام ساده می‌فرسته به کاربر"""
    url = f"{BASE_URL}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": text})

# آدرس وب‌هوک: هر پیامی که از بله بیاد، این تابع صدا زده می‌شه
@app.route(f"/webhook/{BOT_TOKEN}", methods=["POST"])
def webhook():
    update = request.get_json()
    try:
        # پیام متنی
        if "message" in update:
            msg = update["message"]
            if "text" in msg:
                text = msg["text"]
                chat_id = msg["chat"]["id"]
                
                # فقط به /start جواب می‌ده
                if text == "/start":
                    send_message(chat_id, "سلام! 😊")
    except Exception as e:
        print("Error:", e)
    return jsonify({"ok": True})

# یه صفحه ساده برای اینکه Vercel تابع رو زنده نگه داره
@app.route("/", methods=["GET"])
def index():
    return "Bot is alive!"

# این بخش برای تست روی کامپیوتر خودمونه (نه روی Vercel)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
