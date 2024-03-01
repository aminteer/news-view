#!/usr/bin/env python

import requests
from dotenv import load_dotenv
import os
import logging
from openai import OpenAI
import openai
from datetime import datetime

# Configure logging to write to a file, making sure to append log messages
# and set the log level to DEBUG or higher
logging.basicConfig(filename='news_gateway.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG)



class NewsGateway:

    def __init__(self):
        load_dotenv()
        self.ApiKey = os.getenv('NEWS_API_KEY')
        self.NewsURL = 'https://newsapi.org/v2/top-headlines?'

    def get_top_stories(self, category = 'business'):
        #categories can be:
        # business, entertainment, general,health, science, sports, technology.
        #url: https://newsapi.org/docs/endpoints/top-headlines
        #logging.debug(f"News api key: {news_api_key}")
        url = (self.NewsURL +
            'country=us&'
            'category={}&'
            'apiKey={}'.format(category,self.ApiKey))
        logging.debug("getting stories")
        response = requests.get(url)
        logging.debug("request complete")
        logging.debug(response.json())
        
        response_stories = response.json()
                
        return response_stories
    
    def get_everything_news(self,date_from, date_to, query_term='technology', category = 'business'):
        #data_from and date_to must be text and in the form of ISO standard yyyy-mm-dd, eg 2024-03-01
        url = (self.NewsURL +
            'country=us&'
            'from={}&'
            'to={}&'
            'q={}&'
            'category={}&'
            'apiKey={}'.format(date_from,date_to,query_term,category, self.ApiKey))
        logging.debug("getting stories")
        response = requests.get(url)
        logging.debug("request complete")
        logging.debug(response.json())
        
        response_stories = response.json()
        
        return response_stories
            

if __name__ == "__main__":
    client = NewsGateway()
    #server = Server()
    #server.listen()