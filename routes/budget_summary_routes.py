from flask import Blueprint, request, jsonify
from configure import db_connect
from bson import ObjectId
from datetime import datetime

budget_summary_bp = Blueprint('budget_summary_bp', __name__)

# MongoDB setup
db = db_connect.connectToDB()
transactions_collection = db["transactions"]
budget_collection = db["budgets"]

# GET BUDGET SUMMARY
@budget_summary_bp.route('/', methods=['GET'])
def get_budget_summary():
    try:
        month = request.args.get('month')
        year = request.args.get('year')
        category = request.args.get('category')

        if not month or not year:
            return jsonify({"error": "Both month and year are required."}), 400

        print(month, year, category)

        # Budget Fetch
        budget_data = budget_collection.find_one(
            {"month": month, "year": year, "category": category},
            {"_id": 0, "amount": 1}
        )

        # Aggregation for actual amount
        amount_agg = transactions_collection.aggregate([
            {
                "$match": {
                    "$expr": {
                        "$and": [
                            { "$eq": [{ "$month": "$date" }, int(month)] },
                            { "$eq": [{ "$year": "$date" }, int(year)] }
                        ]
                    },
                    "category": category
                }
            },
            {
                "$group": {
                    "_id": None,
                    "totalAmount": { "$sum": "$amount" }
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "totalAmount": 1
                }
            }
        ])

        amount_result = list(amount_agg)
        print(amount_result)

        return jsonify({
            "budget": budget_data.get("amount", 0) if budget_data else 0,
            "actual": amount_result[0]["totalAmount"] if amount_result else 0
        }), 200

    except Exception as e:
        print(e)
        return jsonify({"error": "Failed to fetch budgets"}), 500