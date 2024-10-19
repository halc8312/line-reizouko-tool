from flask import Blueprint, request, jsonify
from models.database import get_db_connection
import datetime

fridge_bp = Blueprint('fridge', __name__)

@fridge_bp.route('/add_item', methods=['POST'])
def add_item():
    data = request.get_json()
    name = data.get('name')
    expiration_date = data.get('expiration_date')
    quantity = data.get('quantity')
    user_id = data.get('user_id')
    
    if not name or not expiration_date or not quantity or not user_id:
        return jsonify({"error": "All fields are required."}), 400
    
    try:
        expiration_date = datetime.datetime.strptime(expiration_date, '%Y-%m-%d').date()
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO items (name, expiration_date, quantity, user_id)
            VALUES (%s, %s, %s, %s)
        ''', (name, expiration_date, quantity, user_id))
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({"message": "Item added successfully."}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
