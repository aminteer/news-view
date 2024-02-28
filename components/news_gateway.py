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
        import requests
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
        
        # stories = []
        # #transform json into a list of story descriptions
        # for story in response_stories['articles']:
        #     title = story['title']
        #     description = story['description']
        #     if title!='[Removed]':
        #         #combine into responses list
        #         story_summary = f"title: {title}; description: {description}"
        #         logging.debug(story_summary)
        #         stories.append(story_summary)
        #return stories        
        return response_stories
    
            

if __name__ == "__main__":
    client = NewsGateway()
    #server = Server()
    #server.listen()