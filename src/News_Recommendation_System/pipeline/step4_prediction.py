import joblib
import numpy as np
import pandas as pd
from News_Recommendation_System import logger
from pathlib import Path
from box import ConfigBox 
from News_Recommendation_System.utils.common import load_json
from News_Recommendation_System.components.model_training import NewsMF, MindDataset
from News_Recommendation_System.pipeline.step5_trending_api import trending_api
import torch

class User_Based_Prediction:
    def __init__(self):
        self.model = joblib.load(Path('artifacts/model_trainer/model_user.joblib'))

    def to_records(self, df: pd.DataFrame):
        records = df.to_dict('records')
        records = list(map(lambda x: ConfigBox(x), records))
        return records

    def input_user_id(self, username):
        self.ind2item = load_json(Path('artifacts/data_transformation/ind2uitem.json'))
        self.item2ind = load_json(Path('artifacts/data_transformation/item2ind.json'))
        self.user2ind = load_json(Path('artifacts/data_transformation/user2ind.json'))
        user_id = self.user2ind[username]
        # print(ind2item)
        self.item_id = list(map(int, list(self.ind2item.keys())))
        self.userIdx =  [int(user_id)]*len(self.item_id)

    def get_news(self):
        df = pd.read_csv('artifacts/data_ingestion/news.tsv', 
                         sep= '\t',
                         names=["itemId","category",
                                "subcategory",
                                "title",
                                "abstract",
                                "url",
                                "title_entities",
                                "abstract_entities"])
        self.news = df


    def predict(self, category= None):

        preditions = self.model.forward(torch.IntTensor(self.userIdx), torch.IntTensor(self.item_id))

        # Select top 500 argmax
        top_index = torch.topk(preditions.flatten(), 5).indices  # change 500 to 5 only suggested news

        # Filter for top 500 suggested items
        filters = [self.ind2item[str(ix.item())] for ix in top_index]
        df = self.news[self.news["itemId"].isin(filters)]
        df['news_id'] = df['itemId'].apply(lambda x: self.item2ind[x] )
        if category:
            df = df[df['category'] == category]
        records = self.to_records(df= df)
        return records
    

class Content_Based_Prediction(User_Based_Prediction):
    def __init__(self):
        self.model = joblib.load(Path('artifacts/model_trainer/model_content_based.joblib'))

    def input(self, news_id:int):
        self.news_id = news_id
        


    def predict(self):
        
        newsid = load_json(Path('artifacts/data_transformation/item2ind.json'))
        self.news['news_id'] = self.news.itemId.apply(lambda x: newsid[x])
        df = self.news[self.news['news_id'] == self.news_id]
        self.news['full'] = self.news.apply(lambda row: str(row['title']) + str(row['abstract']), axis= 1)
        full_news = str(df['title']) + str(df['abstract'])
        reccomendations = []
        for i, doc in enumerate(self.model.recommend(text= full_news, n= 500)):
            # print(f'Recomed - {i+1}')
            # print(doc['text'])
            reccomendations.append(doc['text'])
        df = self.news[self.news["full"].isin(reccomendations)]

        records = self.to_records(df)

        return records



def user_based_rec_api(user_id, category=None):
    logger.info(f' >>>>>>> Step History Based Recommendation started <<<<<<<<<<<')

    obj = User_Based_Prediction()

    try:
        # Try to load the user's recommendation data
        obj.input_user_id(username=user_id)
    except KeyError as e:
        logger.warning(f'User {user_id} not found in the model: {str(e)}')

        # Fallback to trending news when the user is not in the model (cold start)
        return trending_api(category)

    # Proceed with personalized recommendations if the user is found
    try:
        obj.get_news()  # Load the news data for recommendations
        user_reccs = obj.predict(category=category)
        logger.info(f' >>>>>>> Step History Based Recommendation completed <<<<<<<<<<<\n\nx====================x')
        return user_reccs

    except IndexError as e:
        logger.error(f"IndexError during personalized recommendation for user {user_id}: {str(e)}")
        # Fall back to trending news in case of an error
        return trending_api(category)





def content_based_rec_api(news_id):

    logger.info(f' >>>>>>> Step Content Based Reccomedation started <<<<<<<<<<<')
    obj = Content_Based_Prediction()
    obj.input(news_id= news_id)
    obj.get_news()
    content_reccs = obj.predict()
    logger.info(f' >>>>>>> Step Content Based Reccomedation completed <<<<<<<<<<<\n\nx====================x')

    return content_reccs
    





