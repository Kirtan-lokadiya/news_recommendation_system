

import sys
import os

# Append the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from News_Recommendation_System import logger  


logger.info("Welcome to   Kirtan' s  News Reccomendation System Project")


from News_Recommendation_System.pipeline.step1_data_ingestion import run_data_ingestion
from News_Recommendation_System.pipeline.step2_data_transformation import run_data_transformation
from News_Recommendation_System.pipeline.step3_model_training import run_model_trainer





run_data_ingestion()  # run data ingestion pipeline
run_data_transformation()  # run data transformation pipeline
run_model_trainer()  # run model trainer
