import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

from app import app

"""
https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout

Layout in Bootstrap is controlled using the grid system. The Bootstrap grid has 
twelve columns.

There are three main layout components in dash-bootstrap-components: Container, 
Row, and Col.

The layout of your app should be built as a series of rows of columns.

We set md=4 indicating that on a 'medium' sized or larger screen each column 
should take up a third of the width. Since we don't specify behaviour on 
smaller size screens Bootstrap will allow the rows to wrap so as not to squash 
the content.
"""

        #    """
        
        #    ## Value Proposition

        #    Emphasize how the app will benefit users. Don't emphasize the underlying technology.

        #    ✅ RUN is a running app that adapts to your fitness levels and designs personalized workouts to help you improve your running.

        #    ❌ RUN is the only intelligent running app that uses sophisticated deep neural net machine learning to make your run smarter because we believe in ML driven workouts.

        #    """
column1 = dbc.Col(
    [ # it's possible to add style= parameter to dcc.Markdown
        dcc.Markdown(
            """
            The dash_core_components includes a set of higher-level components like dropdowns, graphs, markdown blocks, and more.
            ## Put Words here\n
            > Block quotes are used to highlight text
            [Dash User Guide](https://dash.plot.ly)

            Inline code snippet: `True`
            Block Code snippet:
            ```py
            import dash
            app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
            """
        ),
        dcc.Link(dbc.Button('Call To Action', color='primary'), href='/predictions')
    ],
    md=4,
)

buttons = html.Div(
    [
        dbc.Row([
            dbc.Button('Play', color='primary', className='mr-1', id='play-button'),
            dbc.Button('Pause', color='secondary', className='mr-1', block=True),

        ]),
       #  html.Div(
       #      dcc.Markdown(dir(dbc))
       #  ),
        dbc.Row([
            dbc.Button('Next', color='tertiary', className='mr-1', outline=True),
            dbc.Button('Link', color='link')
        ]),
        html.Span(id='example-layout', style={'vertical-align':'middle'})
    ]
)

@app.callback(
    Output('example-output', 'children'), [Input('play-button', "n_clicks")]
)

def on_button_click(n):
    if n is None:
        return 'Guy'
    else:
        return 'Yo'

gapminder = px.data.gapminder()
fig = px.scatter(gapminder.query("year==2007"), x="gdpPercap", y="lifeExp", size="pop", color="continent",
           hover_name="country", log_x=True, size_max=60)

column2 = dbc.Col(
    [
        dcc.Graph(figure=fig),
    ]
)

graphs = html.Div([
    html.Div(
        dcc.Graph(
            id='g1',
            config={'displayModeBar' : False}
        ), className='column'
    )
], className='row')

image = html.Img(src='assets/Soundwave.png', className='img-fluid')

# row = html.Div(
#     [
#         dbc.Row(dbc.Col(html.Div('A single column', width='auto'))),
#         dbc.Row(
#             [
#                dbc.Col(html.Div('A single column', width=3)),
#                # Order can be used to reorder the colmuns, 1 to 12
#                dbc.Col(html.Div('A single column', width=dict(size=3, order="last", offset=3))),
#                dbc.Col(html.Div('A single column', width=4)),
#             ],
#           # or 'start' and 'end'
#           align="center") 
#     ]
# )

layout = dbc.Row([column1, buttons, image, column2])