import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app

column1 = dbc.Col(
    [
        html.H3('About'),
        html.H6("This is a project exploring the fma dataset, available here https://github.com/mdeff/fma/.\n"),
        html.H6('The fma dataset is a dataset concerning the audio tracks freely available at https://freemusicarchive.org/.\n'),
        html.H6('The goal of the project is to predict the number of listens for each song.'),
        html.P(),
        html.P("""Click on the link below if you would like to see the predictions generated for each track, while listening to it,
             and check out the model page if you're interested in the process behind it."""),
        html.Center(dcc.Link(dbc.Button('Listen to Music 🥍', color='#00a5c2', outline=True, style={'font-size' :'1.07em'}), href='/interact')),
        html.Hr(),
        html.P("Many thanks to the artists who made their work freely available and to the people who made the information accessible.")
    ],
    style={'font-size' : '1.1em'}
)

layout = dbc.Row([column1])