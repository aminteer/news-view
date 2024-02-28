#!/usr/bin/env python
import logging
from datetime import datetime
import pika
import os
from dotenv import load_dotenv
import time
from components.transform import Transformations

# and set the log level to DEBUG or higher
logging.basicConfig(filename='generate_summary.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG)

logging.debug("Launching news summary generation job at UTC {}".format(datetime.utcnow))
load_dotenv()
logging.debug("Starting queue listener")

url_var = os.environ('MESSAGE_Q_PROVIDER') #'RABBITMQ_URL'
queue_name = 'news'

#establish connection
params = pika.URLParameters(os.environ(url_var))
connection = pika.BlockingConnection(params)
channel = connection.channel() # start a channel
channel.queue_declare(queue=queue_name, durable=True) # Declare a queue
print(' [*] Waiting for messages. To exit press CTRL+C')

def callback(ch, method, properties, body):
    #print(f" [x] Received {body.decode()}")
    #time.sleep(body.count(b'.'))
    news_json = body.decode()
    #print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)
    logging.debug("News stories message recieved. Starting transformations")
    trans = Transformations(news_json)
    Transformations.RunFullProcess()
    logging.debug("Transformations completed on the news stories message")


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=queue_name, on_message_callback=callback)

channel.start_consuming()