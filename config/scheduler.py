from apscheduler.schedulers.background import BackgroundScheduler
from models.database import get_items
from flask import request
import requests
import os
from datetime import datetime, timedelta

scheduler = BackgroundScheduler()

def notify_users():
    # ここでデータベースからユーザー情報を取得し、賞味期限が近いアイテムを通知します
    try:
        users = []  # ユーザーリストをここに取得する処理が必要
        for user in users:
            items = get_items(user['user_id'])
            for item in items:
                expiration_date = item[1]
                if expiration_date - datetime.now().date() <= timedelta(days=3):
                    send_notification(user['user_id'], f"{item[0]}の賞味期限が近づいています（{expiration_date}まで）")

    except Exception as e:
        print(f"Error notifying users: {e}")

def send_notification(user_id, message):
    LINE_ACCESS_TOKEN = os.getenv("LINE_ACCESS_TOKEN")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_ACCESS_TOKEN}"
    }
    data = {
        "to": user_id,
        "messages": [
            {
                "type": "text",
                "text": message
            }
        ]
    }

    response = requests.post(
        "https://api.line.me/v2/bot/message/push",
        headers=headers,
        json=data
    )
    if response.status_code != 200:
        print(f"Failed to send notification: {response.status_code}, {response.text}")

# スケジュールにジョブを追加
scheduler.add_job(notify_users, 'interval', days=1)
