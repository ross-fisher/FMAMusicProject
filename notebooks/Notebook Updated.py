#%%
import pandas as pd
import numpy as np
import ast

#%%
import category_encoders as ce
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from sklearn.metrics import r2_score
from pdpbox.pdp import pdp_isolate, pdp_plot
from sklearn.linear_model import RidgeCV, LogisticRegression
from sklearn.model_selection import cross_val_predict
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor

#%% [markdown]
# Import files
#%%
!pwd
#%%
!pwd
tracks_df = pd.read_csv('external/fma_metadata/raw_tracks.csv')
# data needs to be shuffeled it was orderd sequentially 
tracks_df = tracks_df.sample(frac=1)#.reset_index()
tracks_df = tracks_df[pd.notnull(tracks_df['track_genres'])]
tracks_df_old1 = tracks_df.copy()

#%%
def get_sec(time_str):
    if type(time_str) != type(""): return time_str # not super effecient
    time_list = [*time_str.split(':')]
    if len(time_list)==3:
        return int(time_list[0]) * 3600 + int(time_list[1]) * 60 + int(time_list[2])
        # h, m, s
    else: 
        return int(time_list[0]) * 60 + int(time_list[1])
        # m, s
    
def get_genres(value):
    genre_ids = []
    # evaluates the string as python code. it's a dict.
    fixed = ast.literal_eval(value)
    # just return the first genre listed and predict with that
    return int(fixed[0]['genre_id'])

l = []
for i, val in enumerate(tracks_df['track_genres']):
    l.append(get_genres(val))

#%%
tracks_df['genre_id'] = l
meta_features = ['album_title', 'license_parent_id','track_copyright_c', 'track_copyright_p','track_composer', 'track_title', ]
cols_to_keep= ['album_id',  'artist_id', 'track_bit_rate',
'track_date_created', 'track_date_recorded', 'track_duration',
'track_explicit', 'track_instrumental', 'track_interest', 'track_language_code', 'track_listens',
'track_number', 'genre_id']

# %%
new_tracks_df = tracks_df[cols_to_keep].copy() # to avoid the warning 
old_tracks_df = tracks_df
tracks_df = new_tracks_df

#%% 
tracks_df['track_date_created'] = pd.to_datetime(tracks_df['track_date_created'], infer_datetime_format=True)
tracks_df['track_date_recorded'] = pd.to_datetime(tracks_df['track_date_recorded'], infer_datetime_format=True)
tracks_df['track_duration'] =  tracks_df['track_duration'].apply(get_sec)
tracks_df['track_listens_log'] = np.log(tracks_df['track_listens'])

#%%
tracks_df['track_date_created'].head()

#%%
from sklearn.model_selection import train_test_split
target =  'track_listens_log'
numeric_features = tracks_df.drop(target,axis=1).select_dtypes('number').columns
# drop the columns that would leak information
features = tracks_df.drop([target, 'track_listens', 'track_interest'],axis=1).columns
tracks_df 
train, test = train_test_split(tracks_df, test_size=0.15)
train.shape, test.shape

#%% 
using_features = features.copy()
# TODO address
# removing date time for now since pandas didn't like it. Could probably replace with time delta from the start instead.
using_features = using_features.drop(['track_date_recorded', 'track_date_created'])

(train[target] - train[target].mean()).abs().mean()

#%%
from sklearn.linear_model import Ridge, LinearRegression
from xgboost import XGBRegressor

xpipeline = make_pipeline(
    ce.OrdinalEncoder(),
    SimpleImputer(strategy='mean'),
    XGBRegressor(n_estimators=200, objective='reg:squarederror', n_jobs=-1)
)

xpipeline.fit(train[using_features], train[target])
y_pred = cross_val_predict(xpipeline, train[using_features], train[target], cv=3)

#%%
print('R2 Square for model', r2_score(train[target], y_pred))
















#%% [markdown]
# Testing Code
#%%
# %matplotlib inline
import matplotlib.pyplot as plt

plt_fig = plt.figure()
x = [10,  8, 13,  9, 11, 14,  6,  4, 12,  7,  5]
y = [ 8,  6,  7,  8,  8,  9,  7,  4, 10,  4,  5]
plt.scatter(x, y)

#%% [markdown]
# How to convert matplotlib graph to plotly so it can be used in the heroku web app.
#%%
from plotly.tools import mpl_to_plotly
ploty_fig = mpl_to_plotly(plt_fig)
ploty_fig.show()

#%%
# layout = dcc.Graph(id='graph-name', figure=ploty_fig)

#%% [markdown]
# Dash stuff
#%%
import dash_html_components as html
dir(html)

