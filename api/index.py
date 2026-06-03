import os
import json
from flask import Flask, request, jsonify
import requests

BOT_TOKEN = os.environ["BOT_TOKEN"]
BASE_URL = f"https://tapi.bale.ai/bot{BOT_TOKEN}"

app = Flask(__name__)

def send_message(chat_id, text):
    requests.post(f"{BASE_URL}/sendMessage", json={"chat_id": chat_id, "text": text})

@app.route(f"/webhook/{BOT_TOKEN}", methods=["POST"])
def webhook():
    update = request.get_json()
    try:
        if "message" in update and "text" in update["message"]:
            if update["message"]["text"] == "/start":
                send_message(update["message"]["chat"]["id"], "سلام! 😊")
    except Exception as e:
        print("Error:", e)
    return jsonify({"ok": True})

@app.route("/", methods=["GET"])
def index():
    return "Bot is alive!"
