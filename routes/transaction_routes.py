from flask import Blueprint, request, jsonify
from lib import db_connect
from bson import ObjectId
from datetime import datetime

transaction_bp = Blueprint('transaction_bp', __name__)

# MongoDB setup
db = db_connect.connectToDB()
transactions_collection = db["transactions"]


# Helper Function
def object_id_to_str(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    return obj

# POST - Create Transaction
@transaction_bp.route('/', methods=['POST'])
def create_transaction():
    try:
        data = request.get_json()
        amount = data.get('amount')
        description = data.get('description', "")
        date = data.get('date')
        category = data.get('category')
        color = data.get('color', "#000000")

        if not amount or not date or not category:
            return jsonify({"error": "Required Fields Missing"}), 400

        # Convert date to datetime object
        date_obj = datetime.fromisoformat(date)

        transaction = {
            "amount": amount,
            "description": description,
            "date": date_obj,
            "category": category,
            "color": color,
            "createdAt": datetime.now(),
            "updatedAt": datetime.now()
   
        }
        
        result = transactions_collection.insert_one(transaction)
        
        saved_transaction = transactions_collection.find_one({"_id": result.inserted_id})
        
        saved_transaction = {k: object_id_to_str(v) for k, v in saved_transaction.items()}
        
        return jsonify(saved_transaction), 201


    except Exception as e:
        print(e)
        return jsonify({"error": "Internal Server Error"}), 500

# GET All
@transaction_bp.route('/', methods=['GET'])
def get_transactions():
    try:
        fetched_data = list(transactions_collection.find().sort("date", -1))
        if fetched_data:
            fetched_data = [
                {k: object_id_to_str(v) for k, v in txn.items()}
                for txn in fetched_data
            ]
            return jsonify(fetched_data), 200
        else:
            return jsonify({"message": "No Transaction Yet"}), 404
    except Exception as e:
        print(e)
        return jsonify({"error": "Failed to fetch transactions"}), 500

# GET by ID
@transaction_bp.route('/<string:id>', methods=['GET'])
def get_transaction_by_id(id):
    try:
        if not ObjectId.is_valid(id):
            return jsonify({"error": "Invalid ID"}), 400

        transaction = transactions_collection.find_one({"_id": ObjectId(id)})
        if not transaction:
            return jsonify({"error": "Transaction Not Found"}), 404

        transaction = {k: object_id_to_str(v) for k, v in transaction.items()}
        return jsonify(transaction), 200

    except Exception as e:
        print(e)
        return jsonify({"error": "Internal Server Error"}), 500


# PATCH: Update a Transaction
@transaction_bp.route('/', methods=['PATCH'])
def update_transaction():
    try:
        data = request.get_json()
        _id = data.get('_id')

        if not _id or not ObjectId.is_valid(_id):
            return jsonify({"error": "Valid _id is required"}), 400

        update_fields = {k: v for k, v in data.items() if k != '_id'}

        updated = transactions_collection.find_one_and_update(
            {"_id": ObjectId(_id)},
            {"$set": update_fields},
            return_document=True
        )

        if not updated:
            return jsonify({"error": "Transaction Not Found"}), 404

        updated = {k: object_id_to_str(v) for k, v in updated.items()}
        return jsonify(updated), 200

    except Exception as e:
        print(e)
        return jsonify({"error": "Internal Server Error"}), 500


# DELETE by ID
@transaction_bp.route('/<string:id>', methods=['DELETE'])
def delete_transaction(id):
    try:
        if not id or not ObjectId.is_valid(id):
            return jsonify({"error": "Valid ID Required"}), 400

        deleted = transactions_collection.find_one_and_delete({"_id": ObjectId(id)})

        if not deleted:
            return jsonify({"error": "Transaction Not Found"}), 404

        deleted = {k: object_id_to_str(v) for k, v in deleted.items()}
        return jsonify(deleted), 200

    except Exception as e:
        print(e)
        return jsonify({"error": "Internal Server Error"}), 500
