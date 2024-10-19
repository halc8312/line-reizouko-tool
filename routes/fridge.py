import unicodedata
import re
from flask import Blueprint, request, jsonify
from models.database import add_item, delete_item, get_items

fridge_bp = Blueprint('fridge', __name__)

@fridge_bp.route('/add_item', methods=['POST'])
def add_item_endpoint():
    data = request.get_json()
    user_id = unicodedata.normalize('NFKC', data.get('user_id')).strip()
    name = unicodedata.normalize('NFKC', data.get('name')).strip()
    expiration_date = unicodedata.normalize('NFKC', data.get('expiration_date')).strip()
    quantity = unicodedata.normalize('NFKC', data.get('quantity')).strip()

    # 入力チェック
    if not re.match(r'^\d{4}-\d{2}-\d{2}$', expiration_date):
        return jsonify({"message": "Invalid expiration date format. Use YYYY-MM-DD."}), 400

    try:
        quantity = int(quantity)
    except ValueError:
        return jsonify({"message": "Quantity must be a number."}), 400

    if add_item(user_id, name, expiration_date, quantity):
        return jsonify({"message": "Item added successfully."}), 201
    else:
        return jsonify({"message": "Failed to add item."}), 500

@fridge_bp.route('/delete_item', methods=['POST'])
def delete_item_endpoint():
    data = request.get_json()
    user_id = unicodedata.normalize('NFKC', data.get('user_id')).strip()
    name = unicodedata.normalize('NFKC', data.get('name')).strip()

    if delete_item(user_id, name):
        return jsonify({"message": "Item deleted successfully."}), 200
    else:
        return jsonify({"message": "Failed to delete item."}), 500

@fridge_bp.route('/get_items', methods=['GET'])
def get_items_endpoint():
    user_id = request.args.get('user_id')
    items = get_items(user_id)

    if items:
        return jsonify({"items": items}), 200
    else:
        return jsonify({"message": "No items found."}), 404
