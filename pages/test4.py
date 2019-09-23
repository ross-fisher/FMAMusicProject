
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from app import app

df = pd.read_csv(
    'https://raw.githubusercontent.com/plotly/'
    'datasets/master/gapminderDataFiveYear.csv')

graph_and_slider = html.Div([
    dcc.Graph(id='graph-with-slider'),
    dcc.Slider(
        id='year-slider',
        min=df['year'].min(),
        max=df['year'].max(),
        value=df['year'].min(),
        marks={str(year): str(year) for year in df['year'].unique()},
        step=None
    )
])



@app.callback(
    Output('graph-with-slider', 'figure'),
    [Input('year-slider', 'value')])
def update_figure(selected_year):
    filtered_df = df[df.year == selected_year]
    traces = []
    for i in filtered_df.continent.unique():
        df_by_continent = filtered_df[filtered_df['continent'] == i]
        traces.append(go.Scatter(
            x=df_by_continent['gdpPercap'],
            y=df_by_continent['lifeExp'],
            text=df_by_continent['country'],
            mode='markers',
            opacity=0.7,
            marker={
                'size': 15,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name=i
        ))

    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'type': 'log', 'title': 'GDP Per Capita'},
            yaxis={'title': 'Life Expectancy', 'range': [20, 90]},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest'
        )
    }

multiple_outputs = html.Div([
    html.P(),
    html.P(),
    dbc.Row([
        dcc.Input(
            id='num',
            type='number',
            value=5
        ),
        html.P(),
        html.Table([
            html.Tr([html.Td(['x', html.Sup(1)]), html.Td(id='my-x')]),
            html.Tr([html.Td(['x', html.Sup(2)]), html.Td(id='square')]),
            html.Tr([html.Td(['x', html.Sup(3)]), html.Td(id='cube')]),
            html.Tr([html.Td([2, html.Sup('x')]), html.Td(id='twos')]),
            html.Tr([html.Td([3, html.Sup('x')]), html.Td(id='threes')]),
            html.Tr([html.Td(['x', html.Sup('x')]), html.Td(id='x^x')]),
        ]),

    ])
])


@app.callback(
    [Output('my-x', 'children'),
     Output('square', 'children'),
     Output('cube', 'children'),
     Output('twos', 'children'),
     Output('threes', 'children'),
     Output('x^x', 'children')],
    [Input('num', 'value')])
def callback_a(x):
    return x, x**2, x**3, 2**x, 3**x, x**x

layout = html.Div(children=[
    # Table
    html.H4(children='US Agriculture Exports (2011)'),
    graph_and_slider,
    html.Hr(),
    html.H3('Multi Output Callback'),
    multiple_outputs
    ])