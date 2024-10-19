import unicodedata
from flask import Blueprint, request, jsonify
from models.database import get_db_connection

users_bp = Blueprint('users', __name__)

@users_bp.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    user_id = unicodedata.normalize('NFKC', data.get('user_id')).strip()
    username = unicodedata.normalize('NFKC', data.get('username')).strip()

    try:
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute('''
                    INSERT INTO users (user_id, username)
                    VALUES (%s, %s)
                ''', (user_id, username))
                connection.commit()
        return jsonify({"message": "User registered successfully."}), 201
    except Exception as e:
        print(f"Error registering user: {e}")
        return jsonify({"message": "Failed to register user."}), 500
