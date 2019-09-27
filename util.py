import dash_html_components as html
import requests
from lxml import etree
from lxml import html as lhtml
import pandas as pd
import pickle

df = pd.read_csv('assets/final.csv')
df['track_date_created_dt'] = pd.to_datetime(df['track_date_created_dt'], infer_datetime_format=True)
features= ['track_bit_rate', 'track_date_created', 'track_date_recorded', 'track_duration',
           'track_instrumental', 'track_language_code', 'track_number', 'genre_id', 'album_type',
           'genre_parent', 'genre_top_level', 'genre_#tracks', 'track_explicit']


def get_song_entity( track_id ):
    return df[ df['track_id'] == track_id ].iloc[0]

def GetSongLink( track_id ):
    url = get_song_entity( track_id )['track_url']
    url = url.replace('http', 'https')
    req = requests.get(url)
    print( url )


    if req.status_code == 404:
        print('Site 404')
        return "Site 404"

    page = req.content
    tree = lhtml.fromstring(page)
    xpath = '/html/body/div[2]/div[4]/div[2]/div[2]/div/div[1]/div[1]/div/span[3]/a'

    etree_obj = etree.HTML(page)
    output_html = etree.tostring(etree_obj, pretty_print=True, encoding='unicode')

    f = open('output.html', "w+")
    f.write(output_html)
    f.close()
    elements = tree.xpath(xpath)

    if len(elements) == 0:
        print('Unavailable')
        return 'Unavailable'

    download_link_element = dict(elements[0].items())

    return download_link_element['href']