import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
import util
import pandas as pd


# none of these change
df          = util.df
genre_csv   = pd.read_csv('assets/fma_metadata/genres.csv')
features    = util.features 
# Used for sliders
year_min    = df['track_date_created_dt'].dt.year.min()
year_max    = df['track_date_created_dt'].dt.year.max()
bitrate_min = df['track_bit_rate'].min()
bitrate_max = df['track_bit_rate'].max()

print( bitrate_min )
print( bitrate_max )


def get_dropdown_options(df, key):
    my_list = df[key].unique()
    dropdown_options = [
        {'label' : my_list[i],
         'value' : my_list[i]
        }
            for i in range(0, len(my_list))]
    dropdown_options.append({'label' : 'All', 'value' : 'All'})
    return dropdown_options


def get_genre_from_id(id):
    entry =  genre_csv[ genre_csv['genre_id'] == id]
    if len(entry) > 0:
        return entry.iloc[0]['title']
    else:
        return 'Not Listed'


input_col = dbc.Col(
    [
        html.H3('Select Song:'),
        dcc.Dropdown(
            id    = 'song-dropdown',
            value = 122256
        ),

        html.Hr(),
        html.H4('Play Music'),
        html.Iframe(
            id     = "embeded-song",
            width  = "300",
            height = "150",
        ),
        html.P('Track may or may not be available through FMA site.'),

        html.Hr(),
        html.H5('Select Genres:'),
        dcc.Dropdown(
            id      = 'genre-dropdown',
            options = get_dropdown_options(df, 'genre_title'),
            value   = ['All'],
            multi   = True
        ),

        
        html.H6('Date Created'),
        dcc.RangeSlider(
            id='date-range-slider',
            min   = year_min,
            max   = year_max,
            step  = 1,
            value = [year_min, year_max]
        ),
        html.Div(id='output-date-range-slider'),

        html.H6('Bitrate'),
        dcc.RangeSlider(
            id='bitrate-range-slider',
            min   = bitrate_min,
            max   = bitrate_max,
            step  = int((bitrate_max - bitrate_min) / 10),
            value = [bitrate_min, bitrate_max]
        ),
        html.Div(id='output-bitrate-range-slider'),


        html.H5("Select Track Type:"),
        dcc.Dropdown(
            id      = 'album-dropdown',
            options = get_dropdown_options(df, 'album_type'),
            value   = ['All'],
            multi   = True
        ),
    ],
)

# TODO don't use the index of the dropdown, use an actual identifier for the track
@app.callback(
    Output('embeded-song','src'),
    [Input('song-dropdown', 'value')]
)
def update_embeded_song(song_idx):
    return util.GetSongLink(song_idx) 

# could probably be in a class with date-range
@app.callback(
    Output('output-bitrate-range-slider', 'children'),
    [Input('bitrate-range-slider', 'value')]
)
def update_bitrange_slider(slider_range):
    return f"{slider_range[0]} : {slider_range[1]}"


@app.callback(
    Output('output-date-range-slider', 'children'),
    [Input('date-range-slider'       , 'value')]
)
def update_daterange_slider(date_range):
    return f"{date_range[0]} : {date_range[1]}"


# TODO updating song-dropdown options should update its value if
#   the previous value is not in the dropdown options
@app.callback(
    Output(component_id='song-dropdown'    , component_property='options'),
    [ Input('genre-dropdown'   ,'value'),
      Input('album-dropdown'   ,'value'),
      Input('date-range-slider','value'),
      Input('bitrate-range-slider','value'),
    ]
)
def update_song_dropdown(selected_genres, selected_album_types, date_range, bitrate_range):
    # filter by genre
    if 'All' in selected_genres:
        selected_genres      = df['genre_title'].unique()
    if 'All' in selected_album_types:
        selected_album_types = df['album_type'].unique()

    filtered_df = df
    filtered_df = filtered_df[ filtered_df['genre_title'].isin( selected_genres) ]
    filtered_df = filtered_df[ filtered_df['album_type'] .isin( selected_album_types) ]

    # filter by date
    year_min = str(date_range[0])
    year_max = str(date_range[1])
    mask = (df['track_date_created_dt'] >= year_min) & (df['track_date_created_dt'] <= year_max)
    filtered_df = filtered_df.loc[mask]

    # filter by bitrate
    mask = (df['track_bit_rate'] >= bitrate_range[0]) & (df['track_bit_rate'] <= bitrate_range[1])
    filtered_df = filtered_df.loc[mask]

    # return song dropdown options
    return [ {'label' : filtered_df['track_title'].iloc[i], 
              'value' : filtered_df['track_id'].iloc[i]} 
                for i in range(0, filtered_df.shape[0]) ]
















def identity(x): 
    return x

















@app.callback(
    Output('output-col'   , 'children'),
    [Input('song-dropdown', 'value')]
)
def update_output_col(current_song):
    song_entity = util.get_song_entity(current_song)
    children = [
        html.H2(                                                song_entity['track_title']),
        html.H5(format(                                         song_entity['artist_name'])),
        html.H5('Released: {}'.format(                          song_entity['track_date_created_dt'])),
        html.Hr(),
        html.H3('Predicted Listens: {}'.format(                 song_entity['y_pred'])),
        html.H4('Actual Listens: {}'.format(                    song_entity['track_listens'] )),
        html.H5('Bitrate: {}'.format(                           song_entity['track_bit_rate'])),
        html.H5('Track Type: {}'.format(                        song_entity['album_type'])),
        html.H5('Genre: {}'.format(                             song_entity['genre_title'])),
        html.H5('Parent Genre: {}'.format(  get_genre_from_id(  song_entity['genre_top_level'] ))),
        html.H5('Related Genre: {}'.format(  get_genre_from_id( song_entity['genre_parent'] ))),

        html.Hr(),
    ]

    return children 


output_col = dbc.Col(
    [
        html.Div(
            id='output-col',
        )
    ]
)

layout = dbc.Row([input_col, output_col])