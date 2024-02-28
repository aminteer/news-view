#!/usr/bin/env python3
import requests
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from dotenv import load_dotenv
import os
import logging

# Configure logging to write to a file, making sure to append log messages
# and set the log level to DEBUG or higher
logging.basicConfig(filename='data_controller.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///News.sqlite3'


#get API key
logging.debug("preparing to get api key")
# Load environment variables from a .env file
load_dotenv()
# Get the NEWS_API_KEY environment variable
news_api_key = os.getenv('NEWS_API_KEY')
logging.debug("finished getting api key")


#checking on name 
logging.debug("Checking name and type of module")
logging.debug(f"{__name__}, {type(__name__)}")

'''
Define the database model
that is used to store
the top news stories.
'''


db = SQLAlchemy(app)
logging.debug("connected to SQL alchemy, SQLite")

class Articles(db.Model):
   id = db.Column(db.Integer, primary_key=True, autoincrement=True)
   datetime = db.Column(db.DateTime, default=datetime.utcnow())
   title = db.Column(db.String, nullable=False)
   description = db.Column(db.String, nullable=True)

        
with app.app_context():
    #drop and recreate tables - this is for initial test only, not production
    db.drop_all()
    db.create_all()       
        
'''
Helper function to get top news
using API
'''

def get_top_stories():
    import requests
    #logging.debug(f"News api key: {news_api_key}")
    url = ('https://newsapi.org/v2/top-headlines?'
        'country=us&'
        'category=business&'
        'apiKey={}'.format(news_api_key))
    logging.debug("getting stories")
    response = requests.get(url)
    logging.debug("request complete")
    logging.debug(response.json())
    return response.json()

def get_database_stories():
    with app.app_context():
        result2 = db.session.query(Articles.description).all()
        return result2


def count_words(text):
    # Split the text into words based on whitespace
    words = text.split()
    # Return the number of words
    return len(words)

def avg_words_per_description(descr_list):
    word_count = 0
    for row in descr_list:
        word_count += count_words(str(row))
    return word_count/len(descr_list)

'''
In main we first get the top stories and then
create a new object that we can add to the database.
'''
#if __name__ == "__main__":
logging.debug("preparing to get stories from if name main")
current_top_stories = get_top_stories()
#iterate through each top story and store result in the database
for story in current_top_stories['articles']:
    title = story['title']
    description = story['description']
    if title!='[Removed]':
        #add to database
        new_entry = Articles(title=title, description=description)
        with app.app_context():
            db.session.add(new_entry)
            db.session.commit()
            story_summary = f"title: {title}; description: {description}"
            print(story_summary)
            logging.debug(story_summary)
    
#print stories
history = get_database_stories()
logging.debug("*****Printing Stories****")
for row in history:
    logging.debug(str(row))

logging.debug("*****Avg word count per description****")   
avg_count = avg_words_per_description(history)
logging.debug(f"count: {avg_count}") 
