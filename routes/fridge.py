from flask import Blueprint, request, jsonify
from models.database import add_item, delete_item, get_items

fridge_bp = Blueprint('fridge', __name__)

@fridge_bp.route('/add_item', methods=['POST'])
def add_item_endpoint():
    data = request.get_json()
    user_id = data.get('user_id')
    name = data.get('name')
    expiration_date = data.get('expiration_date')
    quantity = data.get('quantity')

    if add_item(user_id, name, expiration_date, quantity):
        return jsonify({"message": "Item added successfully."}), 201
    else:
        return jsonify({"message": "Failed to add item."}), 500

@fridge_bp.route('/delete_item', methods=['POST'])
def delete_item_endpoint():
    data = request.get_json()
    user_id = data.get('user_id')
    name = data.get('name')

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
