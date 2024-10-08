import sys
import os
import pandas as pd

# Add the src directory to the Python path so that the News_Reccomendation_System module can be found
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from News_Recommendation_System.mongodb import db

def insert_data_in_batches(collection, data, batch_size=1000):
    for i in range(0, len(data), batch_size):
        try:
            collection.insert_many(data[i:i + batch_size])
        except Exception as e:
            print(f"Error inserting batch {i // batch_size + 1}: {e}")

def store_tsv_data():
    # Load behaviors.tsv
    behaviors_df = pd.read_csv(os.path.join('../../../artifacts/data_ingestion/behaviors.tsv'), sep='\t', names=["impressionId", "userId", "timestamp", "click_history", "impressions"])
    
    # Load news.tsv
    news_df = pd.read_csv(os.path.join('../../../artifacts/data_ingestion/news.tsv'), sep='\t', names=["newsId", "category", "subcategory", "title", "abstract", "url", "entities", "sentiment"])
    
    # Store data in MongoDB
    behaviors_collection = db['behaviors']
    news_collection = db['news']
    
    # Convert data to dictionaries
    behaviors_data = behaviors_df.to_dict(orient='records')
    news_data = news_df.to_dict(orient='records')
    
    # Insert data into MongoDB in batches
    try:
        insert_data_in_batches(behaviors_collection, behaviors_data)
        print("Behaviors data inserted successfully.")
    except Exception as e:
        print("Error inserting behaviors data:", e)
    
    try:
        insert_data_in_batches(news_collection, news_data)
        print("News data inserted successfully.")
    except Exception as e:
        print("Error inserting news data:", e)

if __name__ == "__main__":
    store_tsv_data()
