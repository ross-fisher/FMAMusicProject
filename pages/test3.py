import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
from app import app
import pandas as pd

df = pd.read_csv(
    'https://gist.githubusercontent.com/chriddyp/'
    'c78bf172206ce24f77d6363a2d754b59/raw/'
    'c353e8ef842413cae56ae3920b8fd78468aa4cb2/'
    'usa-agricultural-exports-2011.csv'
)


def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

dropdown_layout = html.Div([
    html.Label('Dropdown'),
    dcc.Dropdown(
        options=[
            {'label':'New York City', 'value':'NYC'},
            {'label': u'Montréal', 'value': 'MTL'},
            {'label': 'San Francisco', 'value': 'SF'}
        ],
        value='MTL'
    ),

    html.Label('Multi-Select Dropdown'),
    dcc.Dropdown(
        options=[
            {'label':'New York City', 'value':'NYC'},
            {'label': u'Montréal', 'value': 'MTL'},
            {'label': 'San Francisco', 'value': 'SF'}
        ],
        value=['MTL', 'SF'],
        multi=True
    ),


    html.Label('Radio Items'),
    dcc.RadioItems(
        options=[
            {'label':'New York City', 'value':'NYC'},
            {'label': u'Montréal', 'value': 'MTL'},
            {'label': 'San Francisco', 'value': 'SF'},
        ],
        value='MTL'),

    html.Label('Checkboxes'),
    dcc.Checklist(
        options=[
            {'label':'New York City', 'value':'NYC'},
            {'label': u'Montréal', 'value': 'MTL'},
            {'label': 'San Francisco', 'value': 'SF'},
        ],
        value=['MTF', 'SF']
    ),

    html.Label('Text Input'),
    dcc.Input(value='MTL', type='text'),

    html.Label('Slider'),
    dcc.Slider(
        min=0,
        max=9,
        marks={i: 'Label {}'.format(i) if i == 1 else str(i) for i in range(1, 6)},
        value=5,
    )],
    style={'columnCount' : 2}
    )



input_layout = html.Div([
    dcc.Input(id='my-input', value='initial_value', type='text'),
    html.Div(id='my-div')
])



@app.callback(
    Output(component_id='my-div', component_property='children'),
    [Input(component_id='my-input', component_property='value')]
) 
def update_output_div(input_value):
    return "You've entered '{}'".format(input_value)






layout = html.Div(children=[
    # Table
    html.H4(children='US Agriculture Exports (2011)'),
    generate_table(df),

    # Dropdown
    dropdown_layout,

    input_layout
])