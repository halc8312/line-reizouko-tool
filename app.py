import os
import unicodedata  # ユニコードの正規化を行うモジュールをインポート
from flask import Flask, request, jsonify
from models.database import init_db, add_item, get_items
from routes.users import users_bp
from routes.fridge import fridge_bp
from config.scheduler import scheduler
from urllib.parse import quote as url_quote
import requests
import re  # 正規表現を使って賞味期限のフォーマットをチェック

app = Flask(__name__)

# Blueprintを登録
app.register_blueprint(users_bp, url_prefix='/users')
app.register_blueprint(fridge_bp, url_prefix='/fridge')

# データベースを初期化
init_db()

# スケジューラが既に動作していない場合にのみ開始
if not scheduler.running:
    scheduler.start()

# ユーザーごとの状態を追跡するための辞書
user_states = {}

@app.route('/')
def hello():
    return "Hello, LINE Refrigerator Management Tool!"

# LINEのWebhookエンドポイント
@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        body = request.get_json()

        # LINEプラットフォームからのイベントを処理
        for event in body['events']:
            if event['type'] == 'message' and event['message']['type'] == 'text':
                # ユーザーメッセージを正規化して前後の空白を削除
                user_message = unicodedata.normalize('NFKC', event['message']['text']).strip()
                user_id = event['source']['userId']
                reply_token = event['replyToken']

                # ユーザーの状態に基づいて応答を生成
                if user_id in user_states:
                    state = user_states[user_id]

                    if state['action'] == 'adding_item':
                        # ユーザーがアイテムの名前を送った段階
                        user_states[user_id]['item_name'] = user_message
                        reply_message = "賞味期限を教えてください（例: 2024-12-31）"
                        user_states[user_id]['next_step'] = 'expiration_date'

                    elif state.get('next_step') == 'expiration_date':
                        # ユーザーが賞味期限を送った段階
                        expiration_date = user_message
                        # 正しいフォーマットかをチェック
                        if re.match(r'^\d{4}-\d{2}-\d{2}$', expiration_date):
                            user_states[user_id]['expiration_date'] = expiration_date
                            reply_message = "数量を教えてください（例: 2）"
                            user_states[user_id]['next_step'] = 'quantity'
                        else:
                            # フォーマットが間違っている場合、再度入力を促す
                            reply_message = "賞味期限の形式が正しくありません。例: 2024-12-31 のように入力してください。"

                    elif state.get('next_step') == 'quantity':
                        # ユーザーが数量を送った段階でアイテムを追加
                        try:
                            quantity = int(user_message)  # 数量を整数として取得
                            item_name = state['item_name']
                            expiration_date = state['expiration_date']

                            if add_item(user_id, item_name, expiration_date, quantity):
                                reply_message = f"{item_name}を追加しました。"
                            else:
                                reply_message = "アイテムの追加に失敗しました。"

                            # 状態をクリア
                            del user_states[user_id]
                        except ValueError:
                            # 数量が整数でない場合、再度入力を促す
                            reply_message = "数量は数字で入力してください。例: 2"

                    else:
                        reply_message = "すみません、その操作はわかりません。"
                else:
                    # 新しい操作の開始
                    if "食品を追加" in user_message:
                        reply_message = "追加したい食品の名前を教えてください。"
                        user_states[user_id] = {'action': 'adding_item'}
                    elif "冷蔵庫の中身" in user_message:
                        items = get_items(user_id)
                        if items:
                            items_list = "\n".join([f"{item[0]} - {item[1]} - {item[2]}個" for item in items])
                            reply_message = f"現在の冷蔵庫の中身は以下の通りです:\n{items_list}"
                        else:
                            reply_message = "冷蔵庫には何も入っていません。"
                    else:
                        reply_message = "すみません、その操作はわかりません。「食品を追加」や「冷蔵庫の中身」などを教えてください。"

                # LINEに応答を送信
                reply_to_user(reply_token, reply_message)

        return jsonify({"status": "success"}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "error"}), 500

def reply_to_user(reply_token, message):
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
