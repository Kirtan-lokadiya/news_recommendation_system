from News_Recommendation_System.constants import *
from News_Recommendation_System.utils.common import read_yaml, create_directories

from News_Recommendation_System.entity.config_entity import (DataIngestionConfig,
                                                        DataTransformationConfig,
                                                        ModelTrainerConfig,
                                                        TrendingAPIConfig,
                                                        FullNewsConfig)
                                                        

#  Updating Configuratiom Manager inside src/ config

class ConfigurationManager:                  
    def __init__(
        self,
        config_filepath = CONFIG_FILE_PATH,                     # These were all defined in constants
        params_filepath = PARAMS_FILE_PATH,
        schema_filepath = SCHEMA_FILE_PATH
    ):

        self.config = read_yaml(config_filepath) #read yaml file
        self.params = read_yaml(params_filepath)
        self.schema = read_yaml(schema_filepath)

        create_directories([self.config.artifact_root]) #create artifact folder



    def get_data_ingestion_config(self) -> DataIngestionConfig:   # return type is the entity we created

        config = self.config.data_ingestion

        create_directories([config.root_dir])     # data_ingestion is a root folder(directory)

        data_ingestion_configuration = DataIngestionConfig(
            root_dir= config.root_dir,
            local_data_file= config.local_data_file, #root_dir: artifacts/data_ingestion
                                                    #local_data_file: news.zip
                                                    #  unzip_dir: artifacts/data_ingestion
            unzip_dir= config.unzip_dir
        )

        return data_ingestion_configuration
    

    def get_data_transformation_config(self) -> DataTransformationConfig:

        config = self.config.data_transformation
        
        create_directories([config.root_dir])

        data_transformation_configuration = DataTransformationConfig(
            root_dir= config.root_dir,
            data_path_usr= config.data_path_usr,  # all variable answer you will get directly from artifacts / folder
            data_path_news= config.data_path_news,
            col_name= config.col_name
        )

        return data_transformation_configuration
    

    def get_model_trainer_config(self) -> ModelTrainerConfig:
        config = self.config.model_trainer
        params = self.params.Behaviour_model
        

        create_directories([config.root_dir])

        model_trainer_config = ModelTrainerConfig(
            root_dir= config.root_dir,                  # (model_trainer:
#   root_dir: artifacts/model_trainer
#   train_data_path: artifacts/data_transformation/train.tsv
#   test_data_path: artifacts/data_transformation/valid.tsv
#   news: artifacts/data_ingestion/news.tsv
#   col_name: ["itemId","category","subcategory","title","abstract","url","title_entities","abstract_entities"]
#   model_name: model_user.joblib
#   model_content: model_content_based.joblib
#   ind2user: artifacts/data_transformation/ind2user.json
  #ind2item: artifacts/data_transformation/ind2uitem.json)
            train_data_path= config.train_data_path,
            test_data_path= config.test_data_path,
            model_name= config.model_name,
            model_content= config.model_content,
            news= config.news,
            col_name= config.col_name,
            ind2user= config.ind2user,
            ind2item= config.ind2item,
            batch_size= params.batch_size
            
        )

        return model_trainer_config
    

    def get_trending_config(self) -> TrendingAPIConfig:

        config = self.config.trending_api

        trending_api_configuration = TrendingAPIConfig(
            training_data= config.training_data,
            validation_data= config.validation_data,
            news_data= config.news_data,
            col_name= config.col_name,
            item2ind_json= config.item2ind_json
        )

        return trending_api_configuration
    
    def get_fullnews_config(self) -> FullNewsConfig:

        config = self.config.fullnews

        fullnews_configuration = FullNewsConfig(
            news_data= config.news_data,
            col_name= config.col_name,
            item2ind_json= config.item2ind_json
        )

        return fullnews_configuration