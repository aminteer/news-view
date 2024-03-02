# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, dcc, html, Input, Output, State, callback
import plotly.express as px
import pandas as pd
import os
import time
#from flask import jsonify
from flask import jsonify, Flask, render_template, request, url_for, redirect
import flask
from flask_sqlalchemy import SQLAlchemy
import logging
from datetime import datetime
import requests
from data.data_gateway import DataGateway
from PIL import Image
from io import BytesIO
from __appsignal__ import appsignal
from opentelemetry import trace
from appsignal import set_category, set_gauge, increment_counter

MODULE_NAME = "app.py"
MODULE_REFERENCE = f"({MODULE_NAME})"


#appsignal Heroku addon used for metrics tracking.  The below has to be before Flask app start
appsignal.start()

app = flask.Flask(__name__)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

dash_app = Dash(__name__, external_stylesheets=external_stylesheets, server=app)
dash_app.title = "NewsView"

# Register the Dash app with the Flask app
app.add_url_rule('/dash', view_func=dash_app.server.wsgi_app)
#app.add_url_rule('/dash', view_func=dash_app.server)

server = dash_app.server

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///News.sqlite3'

'''
Define the database model
that is used to store
the top news stories.
'''


db = SQLAlchemy(app=app)
logging.debug("connected to SQL alchemy, SQLite")

class Articles(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    datetime = db.Column(db.DateTime, default=datetime.utcnow())
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    source_name = db.Column(db.String, nullable=True)

        
# with app.app_context():
#     #drop and recreate tables - this is for initial test only, not production
#     db.drop_all()
#     db.create_all()  

def load_summary_data ():
    #load new summary info
        #Get latest news summary and images ready
    dg = DataGateway()
    news_summary = dg.get_news_summary_txt()
    news_summary_image = dg.get_news_summary_image()
    image_path = "assets/news_summary.png"

    news_summary_image.save(image_path)
    
    return news_summary, image_path

def get_top_10_news_sources():
    # Perform the query and group by 'news_source'
    results = db.session.query(
        Articles.source_name,
        db.func.count(Articles.source_name).label('count')
    ).group_by(
        Articles.source_name
    ).order_by(
        db.desc('count')
    ).limit(10).all()
    
    # Convert the result into a pandas DataFrame
    df = pd.DataFrame(results, columns=['source_name', 'count'])
    logging.debug(f"{MODULE_NAME}: Top news sources query result | {str(df)}")
    
    return df

def get_all_stories_into_log():
    #dump all existing stories in Article table into the log file
    articles_query = Articles.query.all()
    # Transform the query result into a list of dictionaries
    articles_list = [{'id': article.id, 'datetime': article.datetime, 'source_name': article.source_name, 'title': article.title, 'description': article.description} for article in articles_query]
    # Convert the list of dictionaries into a pandas DataFrame
    articles_df = pd.DataFrame(articles_list)
    # Print the DataFrame to log
    logging.debug(f"{MODULE_NAME}: all news in Article table | {str(df)}")


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

tracer = trace.get_tracer(__name__)
with tracer.start_as_current_span("News summaries load"):
    news_summary, image_path = load_summary_data()
    set_category("data.summaries_page_load")    


colors = {
    'background': '#FFFFFF',     #black is '#111111',  gray is #808080, white is #FFFFFF
    'text': '#111111'
}

comment_history = "Comments: /n"

# # assume you have a "long-form" data frame
# # see https://plotly.com/python/px-arguments/ for more options
# df = pd.DataFrame({
#     "Sources": ["New York Times", "The Economist", "Wall Street Journal", "The Atlantic", "Guardian", "The Financial Times"],
#     "Amount": [4, 1, 2, 2, 4, 5],
#     "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
# })

#get historical data for analysis in chart
with app.app_context():
    logging.debug(f"{MODULE_REFERENCE}getting history of top 10 news stories")
    df = get_top_10_news_sources()
    
# #for debugging, dump all contents into log file
# with app.app_context():
#     get_all_stories_into_log()

fig = px.bar(df, x="source_name", y="count", barmode="group")

fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

dash_app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='NewsView',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(children='NewsView: Know what is going on with one glance.', style={
        'textAlign': 'center',
        'color': colors['text']
    }),
    
    html.Br(),
    
    html.Div(children = news_summary, 
             id = 'daily_summary_text',
             style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
       
    html.Div([
        html.H4("Top Stories in one Image"),
        #html.Img(src="/assets/news_summary.png", alt="News of the day as an image"),
        html.Img(src=image_path, alt="News of the day as an image",
            id = 'daily_summary_image',
            style={
            'height': '50%',
            'width': '50%'
            })
        ], style={'textAlign': 'center'}
    ),
 
    html.Br(),
    
    html.Div([
        dcc.Textarea(
            id='comment',
            value='Type your comment\nhere.  Replace this text.',
            style={'width': '100%', 'height': 100},
        ),
        html.Button('Submit', id='comment-button', n_clicks=0),
        html.Br(),
        dcc.Markdown("""
                ## Comments
                """, id="comments_markdown"),
        html.Div('Test sentence', id='textarea-comments', style={'whiteSpace': 'pre-line'}),
    ]),
    
    dcc.Graph(
        id='example-graph-2',
        figure=fig
    ),
    dcc.Interval(
        id='interval-component',
        interval=60*1000, # in milliseconds
        n_intervals=0
        ),
])

@callback(
    Output('textarea-comments', 'children'),
    Input('comment-button', 'n_clicks'),
    State('comment', 'value')
)
def update_output_div(n_clicks, value):
    if n_clicks > 0:
        #comment_history2 = comment_history + " \n{}".format(value)
        comment_history2 = value
        logging.debug("Comment added")
        #print(comment_history)
        #comment_markdown = "### Comments \n {}".format(comment_history)
        #comment_history = comment_history2
        return comment_history2

#text and image refresh
@callback(
        Output('daily_summary_text', 'children'),
        Output('daily_summary_image', 'src'),
        [Input('interval-component', 'n_intervals')]
)
def update_summary_data(n_intervals):
    new_text, new_image_path = load_summary_data()
    logging.debug("Web app refreshed image and summary")
    return new_text, new_image_path 

#testing out for monitoring purposes
@app.route('/health')
def report_healthy():
    return "OK", 200

@app.route('/metrics')
def metrics():
    return jsonify({
        "requests_per_second": 5
    }), 200

@app.route('/addstories',methods=('GET', 'POST'))
def add_new_stories():
    with tracer.start_as_current_span("Stories save to database"):
        if request.method=='POST':
            current_top_stories = request.json
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
                        increment_counter("stories.saved",1)
    return {'status': 'success', 'message': 'updated'}
 
    
if __name__ == '__main__':    
    #app.run(debug=True)
    dash_app.run_server(debug=True)
    

