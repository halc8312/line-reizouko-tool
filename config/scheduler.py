from apscheduler.schedulers.background import BackgroundScheduler
from models.database import get_db_connection
import datetime
import requests
import os
from dotenv import load_dotenv

load_dotenv()

scheduler = BackgroundScheduler()

# Function to check items and send notifications
def check_expiration_dates():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        today = datetime.date.today()
        cursor.execute('''
            SELECT name, expiration_date, user_id FROM items
            WHERE expiration_date = %s
        ''', (today + datetime.timedelta(days=3),))
        items = cursor.fetchall()

        for item in items:
            name, expiration_date, user_id = item
            send_line_notification(user_id, name, expiration_date)

        cursor.close()
        connection.close()
    except Exception as e:
        print(f"Error checking expiration dates: {e}")

# Function to send notification to LINE
def send_line_notification(user_id, item_name, expiration_date):
    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {os.getenv('LINE_ACCESS_TOKEN')}"
        }
        message = f"Reminder: The item '{item_name}' will expire on {expiration_date}."
        data = {
            "to": user_id,
            "messages": [
                {
                    "type": "text",
                    "text": message
                }
            ]
        }
        response = requests.post("https://api.line.me/v2/bot/message/push", json=data, headers=headers)
        if response.status_code != 200:
            print(f"Failed to send notification: {response.text}")
    except Exception as e:
        print(f"Error sending LINE notification: {e}")

# Add job to scheduler
scheduler.add_job(check_expiration_dates, 'interval', days=1)

# Start the scheduler
scheduler.start()
