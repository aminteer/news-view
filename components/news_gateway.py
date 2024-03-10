#!/usr/bin/env python

import requests
from dotenv import load_dotenv
import os
import logging
from datetime import datetime

# Configure logging to write to a file, making sure to append log messages
# and set the log level to DEBUG or higher
logging.basicConfig(filename='news_gateway.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG)
MODULE_NAME = "news_gateway.py"
MODULE_REFERENCE = f"({MODULE_NAME})"


class NewsGateway:

    def __init__(self):
        load_dotenv()
        self.ApiKey = os.getenv('NEWS_API_KEY')
        self.NewsURL = 'https://newsapi.org/v2/'

    def get_stories_from_url_request(self, url_request):
        #categories can be:
        # business, entertainment, general,health, science, sports, technology.
        #url: https://newsapi.org/docs/endpoints/top-headlines
        #logging.debug(f"News api key: {news_api_key}")
        url = (self.NewsURL +
            url_request +
            '&apiKey={}'.format(self.ApiKey))
        logging.debug(f"{MODULE_REFERENCE}getting stories")
        response = requests.get(url)
        logging.debug(f"{MODULE_REFERENCE}request complete")
        logging.debug(response.json())
        status_code = response.status_code
        response_stories = response.json()
                
        return response_stories, status_code
            

if __name__ == "__main__":
    client = NewsGateway()
