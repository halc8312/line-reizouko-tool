import os
from flask import Flask
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

# Start the scheduler
scheduler.start()

@app.route('/')
def hello():
    return "Hello, LINE Refrigerator Management Tool!"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
