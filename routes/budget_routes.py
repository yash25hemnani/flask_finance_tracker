from flask import Blueprint, request, jsonify
from lib import db_connect
from bson import ObjectId

budget_bp = Blueprint('budget_bp', __name__)

# MongoDB setup
db = db_connect.connectToDB()
budget_collection = db["budgets"]

# Helper Function
def object_id_to_str(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    return obj


# GET: Fetch budget items
@budget_bp.route("/", methods=["GET"])
def get_budget():
    month = request.args.get("month")
    year = request.args.get("year")
    category = request.args.get("category")

    if not month or not year:
        return jsonify({"error": "Both month and year are required."}), 400

    query = {"month": month, "year": year}
    if category:
        query["category"] = category

    data = list(budget_collection.find(query, {"_id": 0}))

    if data:
        return jsonify(data), 200
    else:
        return jsonify({"message": "No Budget Yet"}), 404

# PATCH: Update or insert a budget entry
@budget_bp.route("/", methods=["PATCH"])
def update_budget():
    data = request.get_json()

    month = data.get("month")
    year = data.get("year")
    category = data.get("category")

    if not month or not year or not category:
        return jsonify({"error": "Month, Year, and Category required"}), 400

    update_fields = {k: v for k, v in data.items() if k not in ["month", "year", "category"]}

    updated_budget = budget_collection.find_one_and_update(
        {"month": month, "year": year, "category": category},
        {"$set": update_fields},
        upsert=True,
        return_document=True
    )

    if updated_budget:
            updated_budget = {k: object_id_to_str(v) for k, v in updated_budget.items()}

            return jsonify({
                "message": "Budget updated successfully",
                "data": updated_budget
            }), 200
    else:
        return jsonify({
            "message": "Budget not found"
        }), 404

# DELETE: Delete a budget entry
@budget_bp.route("/", methods=["DELETE"])
def delete_budget():
    data = request.get_json()

    month = data.get("month")
    year = data.get("year")

    if not month or not year:
        return jsonify({"error": "Month and Year required"}), 400

    result = budget_collection.delete_one({"month": month, "year": year})

    return jsonify({"message": "Budget Deleted Successfully"}), 200
