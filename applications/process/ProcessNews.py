#!/usr/bin/env python
import logging
from datetime import datetime
from components.news_gateway import NewsGateway
import pika
import os
from dotenv import load_dotenv


# Configure logging to write to a file, making sure to append log messages
# and set the log level to DEBUG or higher
logging.basicConfig(filename='process_news.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG)

logging.debug("Launching news collecction job at UTC {}".format(datetime.utcnow))
logging.debug("Loading message server connections")
load_dotenv()
logging.debug("Grabbing news stories")

try:
    news = NewsGateway()
    top_stories = news.get_top_stories('general')
except:
    raise Exception("News retrieval failed")
    
#connect to message server and send on the json
mq_provider = os.environ('MESSAGE_Q_PROVIDER')
mq_url = os.environ(mq_provider)
try:
    params = pika.URLParameters(mq_url)
    connection = pika.BlockingConnection(params)
    channel = connection.channel() # start a channel
    channel.queue_declare(queue='news') # Declare a queue
    channel.basic_publish(exchange='',
                        routing_key='stories',
                        body=top_stories)
    connection.close()
except:
    raise Exception(f"Posting news to message queue failed at url: {mq_url}")