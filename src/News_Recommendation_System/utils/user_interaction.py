from datetime import datetime
from flask import jsonify
from News_Recommendation_System.mongodb import db


user_interactions_collection = db['user_interactions']
def update_user_interaction(user_id, new_click, new_impression):
    # Fetch the user's interaction data
    user_interaction = user_interactions_collection.find_one({"userId": user_id})

    if not user_interaction:
        return jsonify({"error": "User not found"}), 404

    # Update the user's click history and impressions
    updated_click_history = f"{user_interaction.get('click_history', '')} {new_click}".strip()

    # To avoid duplicates, ensure that only new impressions are added
    existing_impressions = user_interaction.get('impressions', '').split()
    new_impressions_list = new_impression.split()

    updated_impressions = " ".join(
        [imp for imp in new_impressions_list if imp not in existing_impressions]
    )

    user_interactions_collection.update_one(
        {"userId": user_id},
        {
            "$set": {
                "click_history": updated_click_history,
                "impressions": updated_impressions,
                "timestamp": datetime.now().strftime("%m/%d/%Y %I:%M:%S %p")
            }
        }
    )

    return jsonify({"message": "User interaction updated successfully"}), 200

