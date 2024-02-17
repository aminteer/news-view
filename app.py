# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, dcc, html, Input, Output, State, callback
import plotly.express as px
import pandas as pd
import os


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

colors = {
    'background': '#FFFFFF',     #black is '#111111',  gray is #808080, white is #FFFFFF
    'text': '#111111'
}

comment_history = "Comments: /n"

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame({
    "Sources": ["New York Times", "The Economist", "Wall Street Journal", "The Atlantic", "Guardian", "The Financial Times"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig = px.bar(df, x="Sources", y="Amount", color="City", barmode="group")

fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
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
    )
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
        #print(comment_history)
        #comment_markdown = "### Comments \n {}".format(comment_history)
        #comment_history = comment_history2
        return comment_history2

if __name__ == '__main__':
    app.run(debug=True)

