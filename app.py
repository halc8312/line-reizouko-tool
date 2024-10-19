import os
from flask import Flask, request, jsonify
from models.database import init_db
from routes.users import users_bp
from routes.fridge import fridge_bp
from config.scheduler import scheduler
from urllib.parse import quote as url_quote  # 修正

app = Flask(__name__)

# Register blueprints
app.register_blueprint(users_bp, url_prefix='/users')
app.register_blueprint(fridge_bp, url_prefix='/fridge')

# Initialize the database
init_db()

# Start the scheduler only if it's not already running
if not scheduler.running:
    scheduler.start()

@app.route('/')
def hello():
    return "Hello, LINE Refrigerator Management Tool!"

# Webhook endpoint for LINE
@app.route('/webhook', methods=['POST'])
def webhook():
    # LINEからのリクエストを受け取るエンドポイント
    try:
        body = request.get_json()

        # LINEプラットフォームからのイベントを処理
        for event in body['events']:
            if event['type'] == 'message' and event['message']['type'] == 'text':
                user_message = event['message']['text']
                reply_token = event['replyToken']

                # ユーザーのメッセージに応じて応答を生成
                if "食品を追加" in user_message:
                    reply_message = "追加したい食品の名前を教えてください。"
                elif "冷蔵庫の中身" in user_message:
                    reply_message = "現在の冷蔵庫の中身は以下の通りです。"  # ここでデータベースからアイテムを取得して応答する
                elif "食品を削除" in user_message:
                    reply_message = "削除したい食品の名前を教えてください。"
                else:
                    reply_message = "すみません、その操作はわかりません。「食品を追加」や「冷蔵庫の中身」などを教えてください。"

                # LINEに応答を送信
                reply_to_user(reply_token, reply_message)

        return jsonify({"status": "success"}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "error"}), 500

def reply_to_user(reply_token, message):
    # LINEの返信APIを使用してユーザーにメッセージを返す
    import requests

    LINE_ACCESS_TOKEN = os.getenv("LINE_ACCESS_TOKEN")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_ACCESS_TOKEN}"
    }
    data = {
        "replyToken": reply_token,
        "messages": [
            {
                "type": "text",
                "text": message
            }
        ]
    }

    response = requests.post(
        "https://api.line.me/v2/bot/message/reply",
        headers=headers,
        json=data
    )
    if response.status_code != 200:
        print(f"Failed to send message: {response.status_code}, {response.text}")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
