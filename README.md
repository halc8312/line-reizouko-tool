# LINE 冷蔵庫管理ツール

このプロジェクトは、LINE公式アカウントを使用してユーザーの冷蔵庫を管理するツールです。ユーザーは食品アイテムの追加や賞味期限の通知を受け取ることができます。

## プロジェクト構成

```
reizouko/
├── app.py                  # Flaskアプリケーションのメインエントリーポイント
├── requirements.txt        # 必要なパッケージを記述
├── .env                    # 環境変数を管理するファイル
├── config/
│   └── scheduler.py        # APSchedulerの設定、賞味期限の通知スケジューリング
├── models/
│   └── database.py         # データベース接続設定
├── routes/
│   ├── users.py            # ユーザー関連のルート
│   └── fridge.py           # 冷蔵庫関連のルート（食品の追加・編集など）
└── templates/              # HTMLテンプレートを置く場所（HTML UIが必要な場合）
```

## 必要なツールとセットアップ

1. **Python 3.8+**
2. **Virtual Environment**（仮想環境の使用を推奨）
3. **Railway.app アカウント**（ホスティング用）

### 仮想環境のセットアップ

1. プロジェクトのルートディレクトリで仮想環境を作成:

   ```sh
   python -m venv venv
   ```

2. 仮想環境をアクティベート:

   - Windows:
     ```sh
     .\venv\Scripts\activate
     ```
   - Mac/Linux:
     ```sh
     source venv/bin/activate
     ```

3. 必要なパッケージをインストール:

   ```sh
   pip install -r requirements.txt
   ```

### 環境変数の設定

`.env` ファイルを作成し、以下の情報を記入してください。

```
PGHOST=your_db_host
PGPORT=your_db_port
PGUSER=your_db_user
PGPASSWORD=your_db_password
PGDATABASE=your_db_name
LINE_ACCESS_TOKEN=your_line_access_token
```

## アプリケーションの起動

1. データベースの初期化とサーバーの起動を行います:

   ```sh
   python app.py
   ```

2. ブラウザで `http://127.0.0.1:5000/` にアクセスして、アプリケーションが正常に起動していることを確認してください。

## 主な機能

- **ユーザー登録と認証**: LINEアカウントを使ったユーザー登録。
- **食品アイテムの追加・管理**: 賞味期限や数量を設定し、食品を管理。
- **賞味期限の通知**: 賞味期限が近づいた食品をLINEで通知。

## 使用技術

- **Flask**: Pythonの軽量Webフレームワーク。
- **PostgreSQL**: データベース。
- **APScheduler**: タスクのスケジューリングに使用。
- **LINE Messaging API**: LINEを介したメッセージ送信。

## デプロイ

1. Railway.appにプロジェクトを作成し、リポジトリを接続します。
2. 環境変数をRailway.appの設定で登録してください。
3. 自動でデプロイが行われ、アプリケーションが公開されます。

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。

