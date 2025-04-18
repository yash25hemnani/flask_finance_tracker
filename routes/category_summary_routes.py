from flask import Blueprint, request, jsonify
from configure import db_connect
from bson import ObjectId
from datetime import datetime

category_summary_bp = Blueprint('category_summary_bp', __name__)

# MongoDB setup
db = db_connect.connectToDB()
transactions_collection = db["transactions"]
budget_collection = db["budgets"]


# Helper Function
def object_id_to_str(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    return obj

# GET Current-Month Category Summary
@category_summary_bp.route('/current-month', methods=['GET'])
def get_category_wise_spending():
    try:
        month = request.args.get("month")
        year = request.args.get("year")

        if not month or not year:
            return jsonify({ "error": "Both month and year are required." }), 400

        print("Month:", month, "Year:", year)

        category_wise_spending = list(transactions_collection.aggregate([
            {
                "$match": {
                    "$expr": {
                        "$and": [
                            { "$eq": [{ "$month": "$date" }, int(month)] },
                            { "$eq": [{ "$year": "$date" }, int(year)] }
                        ]
                    }
                }
            },
            {
                "$group": {
                    "_id": "$category",
                    "totalAmount": { "$sum": "$amount" },
                    "color": { "$first": "$color" }
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "category": "$_id",
                    "totalAmount": 1,
                    "fill": "$color"
                }
            },
            {
                "$sort": { "totalAmount": -1 }
            }
        ]))

        print(category_wise_spending)

        return jsonify(category_wise_spending), 200

    except Exception as e:
        print(e)
        return jsonify({ "error": "Failed to fetch budgets" }), 500