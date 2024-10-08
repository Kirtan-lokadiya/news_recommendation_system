from pymongo import MongoClient

def get_database():
    # Provide the MongoDB Atlas URL to connect Python to MongoDB
    CONNECTION_STRING = "mongodb+srv://Kirtan:Kirtan%40998@cluster0.uiyg63a.mongodb.net?retryWrites=true&w=majority"
    client = MongoClient(CONNECTION_STRING)
    return client['news_recommendation']

db = get_database()

# Function to test the connection and get the last 5 documents from 'behaviors' collection
def get_last_documents():
    try:
        # Access the 'behaviors' collection
        behaviors_collection = db['behaviors']
        
        # Fetch the last 5 documents, sorted by the '_id' in descending order
        last_documents = list(behaviors_collection.find().sort('_id', -1).limit(5))
        
        # Display the documents
        for doc in last_documents:
            print(doc)
    except Exception as e:
        print("Failed to retrieve documents")
        print("Error:", e)

if __name__ == "__main__":
    get_last_documents()
