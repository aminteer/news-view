import logging
from datetime import datetime, timedelta
from components.news_gateway import NewsGateway
from sqlalchemy import Column, Integer, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import Articles
from time import time
import sqlalchemy as db

# Configure logging to write to a file, making sure to append log messages
# and set the log level to DEBUG or higher
logging.basicConfig(filename='rebuild_database.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG)

#below is not needed since it is now imported from App
# class Articles(db.Model):
#    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#    datetime = db.Column(db.DateTime, default=datetime.utcnow())
#    title = db.Column(db.String, nullable=False)
#    description = db.Column(db.String, nullable=True)
#    source_name = db.Column(db.String, nullable=True)

def drop_and_recreate_db_schema(engine):        
        #drop and recreate tables - this is for initial test only, not production
        Articles.metadata.drop_all(bind=engine)
        Articles.metadata.create_all(bind=engine)
        
def add_new_stories(db_session, stories=None):
    if stories != None:
        current_top_stories = stories
        for story in current_top_stories['articles']:
            title = story['title']
            description = story['description']
            source = story['source']
            source_name = source['name']
            if title!='[Removed]':
                #add to database
                new_entry = Articles(title=title, description=description, source_name=source_name)

                db_session.add(new_entry)
                db_session.commit()
                story_summary = f"title: {title}; source: {source_name}; description: {description}"
                print(story_summary)
                logging.debug(story_summary)

def grab_some_starter_data(include_prior_number_of_days = 4):
    logging.debug("Launching news collecction job at UTC {}".format(datetime.utcnow))
    
    today = datetime.now()

    # Calculate the date the required number of days ago
    datetime_from = today - timedelta(days=include_prior_number_of_days) # can change this date

    # Convert the date to a string in ISO format (yyyy-mm-dd)
    date_from = datetime_from.strftime('%Y-%m-%d')
    date_to = date_from = today.strftime('%Y-%m-%d')
    
    try:
        news = NewsGateway()
        stories = news.get_everything_news(date_from=date_from, date_to=date_to,category='general')
        return stories
    except:
        raise Exception("News retrieval failed")

if __name__ == '__main__':
    #run through a sample process of obtaining top stories and creating prompts
    SQLALCHEMY_DB_URL = 'sqlite:///instance/News.sqlite3'
    engine = db.create_engine(SQLALCHEMY_DB_URL)
    connection = engine.connect()
    metadata = db.MetaData()

    #metadata.create_all(engine) #Creates the table

    logging.debug("connected to SQL alchemy, SQLite")
    t = time()

    #Create the session
    session = sessionmaker()
    session.configure(bind=engine)
    s = session()
    
    print('\nRecreating the news top stories database')
    logging.debug("Recreating the news top stories database")
    logging.debug("Dropping and recreating database")
    drop_and_recreate_db_schema(engine=engine)
    logging.debug("Grabbing some starter stories")
    stories = grab_some_starter_data(2)
    logging.debug("Adding new stories to database")
    add_new_stories(s, stories)
    logging.debug("Stories added to database after rebuild")
    #this is ugly and will fix better later
    logging.debug("Time elapsed: " + str(time() - t) + " s.")
    
