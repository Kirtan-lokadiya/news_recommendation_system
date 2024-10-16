import sys
import os

# Append the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))


from flask import Flask, render_template, url_for, request, redirect, session
from pymongo import MongoClient
from flask import jsonify
from datetime import datetime
import json
from pathlib import Path
from flask import flash
from News_Recommendation_System.pipeline.step4_prediction import user_based_rec_api, content_based_rec_api
from News_Recommendation_System.pipeline.step5_trending_api import trending_api
from News_Recommendation_System.pipeline.step6_fullnews_api import get_fullnews_api
from News_Recommendation_System.utils.user_interaction import update_user_interaction


def get_database():
    CONNECTION_STRING = "mongodb+srv://Kirtan:Kirtan%40998@cluster0.uiyg63a.mongodb.net?retryWrites=true&w=majority"
    client = MongoClient(CONNECTION_STRING)
    return client['news_recommendation']

db = get_database()

# Define collections
users_collection = db['behaviors'] 
user_interactions_collection = db['behaviors']

app = Flask(__name__)
app.secret_key = '11111'

@app.route('/')
def home():
    home_news_data = trending_api()
    return render_template('home.html',home_news= home_news_data, user_logged_in=session.get('user_logged_in', False), current_user=session.get('current_user', '') )

@app.route('/category/<category>')
def category(category):   # if the user is logged in, the user_based_rec_api() fetches personalized news. If not, trending_api() is called to show the trending news.
    if session.get('user_logged_in', False):
        personalized_news_data = user_based_rec_api(session['current_user'], category)
        return render_template('category.html', category=category, category_news= personalized_news_data, user_logged_in=session.get('user_logged_in', False), current_user=session.get('current_user', ''))
    # If not logged in, show trending news in the category
    category_news_data = trending_api(category)
    return render_template('category.html', category=category, category_news= category_news_data, user_logged_in=session.get('user_logged_in', False), current_user=session.get('current_user', ''))


@app.route('/full_news/<news_id>')
def full_news(news_id):
    full_news_data = get_fullnews_api(news_id)
    content_recommendation_news = content_based_rec_api(news_id=news_id)

    # Assuming the user is logged in, update the click history
    if session.get('user_logged_in', False):
        user_id = session['current_user']
        update_user_interaction(user_id=user_id, new_click=news_id, new_impression="")
    
    return render_template('full_news.html', full_news=full_news_data, news_id=news_id, 
                           content_recc=content_recommendation_news, 
                           user_logged_in=session.get('user_logged_in', False), 
                           current_user=session.get('current_user', ''))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        userId = request.form.get('username')
        password = request.form.get('password')

        # Query the MongoDB collection to find the user
        user = users_collection.find_one({"userId": userId})

        if user and user.get('password') == password:
            session['user_logged_in'] = True
            session['current_user'] = userId
            return redirect(url_for('personalized', username=userId))
        else:
            error_message = 'Please check your login credentials'
            return render_template('login.html', error_message=error_message)
    
    return render_template('login.html', user_logged_in=session.get('user_logged_in', False), current_user=session.get('current_user', ''))



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        existing_user = users_collection.find_one({"userId": username})

        if existing_user:
            flash('Username already exists. Please choose a different username.')
            return render_template('signup.html')

        users_collection.insert_one({"userId": username, "password": password})

        flash('Account created successfully! Please log in.')
        return redirect(url_for('login'))

    return render_template('signup.html')


@app.route('/logout')
def logout():
    session.pop('user_logged_in', None)
    session.pop('current_user', None)
    return redirect(url_for('home'))

@app.route('/personalized/<username>')
def personalized(username, category=None):
    personalized_news_data = user_based_rec_api(username, category=category)

    return render_template('personalized.html', username=username, 
                           personalized_news=personalized_news_data, 
                           user_logged_in=session.get('user_logged_in', False), 
                           current_user=session.get('current_user', ''), 
                           category=category)


# @app.route('/update_interaction', methods=['POST'])
# def update_interaction():
#     data = request.json
#     user_id = data.get('userId')
#     clicked_news = data.get('clicked_news')
#     impressions = data.get('impressions')

#     if not user_id or not clicked_news or not impressions:
#         return jsonify({"error": "Missing userId, clicked_news, or impressions"}), 400

#     # Fetch the user's interaction data
#     user_interaction = user_interactions_collection.find_one({"userId": user•••••_id})

#     if not user_interaction:
#         return jsonify({"error": "User not found"}), 404

#     # Update the user's click history and impressions
#     updated_click_history = f"{user_interaction['click_history']} {clicked_news}".strip()
#     updated_impressions = f"{user_interaction['impressions']} {impressions}".strip()

#     user_interactions_collection.update_one(
#         {"userId": user_id},
#         {
#             "$set": {
#                 "click_history": updated_click_history,
#                 "impressions": updated_impressions,
#                 "timestamp": datetime.now().strftime("%m/%d/%Y %I:%M:%S %p")
#             }
#         }
#     )

#     return jsonify({"message": "User interaction updated successfully"}), 200

if __name__ == "__main__":
    app.run(debug=True)

