from flask import Blueprint, request, jsonify
from models.database import get_db_connection

users_bp = Blueprint('users', __name__)

@users_bp.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    user_id = data.get('user_id')
    username = data.get('username')

    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO users (user_id, username)
            VALUES (%s, %s)
        ''', (user_id, username))
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({"message": "User registered successfully."}), 201
    except Exception as e:
        print(f"Error registering user: {e}")
        return jsonify({"message": "Failed to register user."}), 500
