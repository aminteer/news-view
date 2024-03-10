#!/usr/bin/env python

import logging
from datetime import datetime
from components.news_gateway import NewsGateway

# Configure logging to write to a file, making sure to append log messages
# and set the log level to DEBUG or higher
logging.basicConfig(filename='news_collector.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG)
MODULE_NAME = "news_collector.py"
MODULE_REFERENCE = f"({MODULE_NAME})"

class NewsCollector:

    def __init__(self):
        self.NewsGateway = NewsGateway()

    def get_top_stories(self, category = 'business'):
        #categories can be:
        # business, entertainment, general,health, science, sports, technology.
        url = ('top-headlines?'
            'country=us&'
            'category={}'.format(category))
        logging.debug(f"{MODULE_REFERENCE}getting top stories")
        response, status_code = self.NewsGateway.get_stories_from_url_request(url_request=url)
        logging.debug(f"{MODULE_REFERENCE}request for top stories complete")
        logging.debug(response)
                
        return response
    
    def get_everything_news(self,date_from, date_to, query_term='AI'):
        #data_from and date_to must be text and in the form of ISO standard yyyy-mm-dd, eg 2024-03-01
        url = ('everything?'
            'from={}&'
            'to={}&'
            'q={}&'
            'language=en'.format(date_from,date_to,query_term))
        logging.debug(f"{MODULE_REFERENCE}getting stories with this url: {url}")
        response, status_code = self.NewsGateway.get_stories_from_url_request(url_request=url)
        logging.debug(f"{MODULE_REFERENCE}request complete")
        logging.debug(response)
        
        return response
            

if __name__ == "__main__":
    client = NewsCollector()
