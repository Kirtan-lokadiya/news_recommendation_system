import os
import urllib.request as request    # to download the file from the url
import zipfile
from News_Recommendation_System import logger
from News_Recommendation_System.utils.common import get_size

from pathlib import Path
from News_Recommendation_System.entity.config_entity import DataIngestionConfig

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def extract_zip_file(self):
        '''
        This will unzip the downloaded zip file
        '''
        zip_extract_to_path = self.config.unzip_dir
        os.makedirs(zip_extract_to_path, exist_ok=True)
        with zipfile.ZipFile(self.config.local_data_file, 'r') as zip_file:
            zip_file.extractall(zip_extract_to_path)