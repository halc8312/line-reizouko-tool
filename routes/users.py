from flask import Blueprint, request, jsonify
from models.database import get_db_connection

users_bp = Blueprint('users', __name__)

@users_bp.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    user_id = data.get('user_id')
    username = data.get('username')
    
    if not user_id or not username:
        return jsonify({"error": "user_id and username are required"}), 400
    
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO users (user_id, username)
            VALUES (%s, %s)
            ON CONFLICT (user_id) DO NOTHING
        ''', (user_id, username))
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({"message": "User registered successfully."}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500