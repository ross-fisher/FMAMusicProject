import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app

column1 = dbc.Col(
    [
#        html.Audio(
#            src='assets/music/042048.mp3',
#            controls=True
#
#        ),

        dcc.Markdown(
            """
            ## Model
            The code for this project is available on my github at https://github.com/ross-fisher/unit2-portfolio-project. 
            In the notebooks you will find notebook.ipynb where you will find the code I used to train the model,
            to make the predictions, and to make the visualizations below. If you are interested in learning 
            more about this project, I would check there.

            We'll start by exploring the data, inluding the generated predictions, then we will look at some of the 
            inner workings of the model, and take a look at some visuals generated during the process.

            Let's start by taking a small look at the data that the model was trained on.
            """
        ),
        html.Hr(),
        html.H3('What the model predicts'),
        html.Img(
            src='assets/example_predict_data.png',
        ),
        html.P("""
            To reiterate this model aims to predict the number of track listens for a given song, which is the column 'track_listens'.
            This table shows the data we wanted to predict, listed under the column 'track_listens', and the prediction our model
            actually geneated, listed under the column 'predicted_track_listens'."""),
        html.P("""
            As you can see these predictions are in the ballpark but some are better or worse than others. It is somewhat surprising it
            gets close at all considering the model doesn't train on the actual music. Just by knowing aspects such as genre, and when 
            it was released, we can generate a rough prediction that gets pretty close most of the time.
        """),

        html.H3('Data used to train the model'),
        html.Img(
            src='assets/train_data_example.png',
        ),
        html.P("""This is what the data, taken from the fma dataset, looks like."""),
        html.P("""This data is fed into a Random Forest model,together with the the track listens, 
            and that is used to generate the predictions shown in the first table."""),
        
        html.H3('A Random Decision Tree in a Random Forest'),
        html.Img(
            src='assets/tree.png',
            width="1200",
        ),
        html.P("""
            In case you're wondering what a Random Forest looks like, this is part of one tree of the random forest model
            I used to generate the predictions for this project."""),
        html.P("""There are many trees in the forest, and they work together to generate a prediction. 
            In this case, how many people listened to the given track.
        """),


        html.Hr(),
        html.H3('What the data looks like'),
        html.Img(
            src='assets/actual.png',
            width="600"
        ),
        html.P("""
            This is a graph I made showing track duration and the number of listens. There are about 13 or so tracks with listens higher
            than this but the model doesn't predict outliers to these extremes.
            """),
        html.P("""
            It also color coded by the 'album'
            type for each song. One thing you could take away from this graph is for example that very long songs don't tend to 
            get very many listens. 
            You might also notice how the 'Albums' album_type sits on top of the other types when it comes to the number of listens, 
            generally speaking, and we might expect that our model take that information into account when generating its prediction.
        """),


        html.H3('What the predicted data looks like'),
        html.Img(
            src='assets/Predicted.png',
            width="600"
        ),
        html.P("""
            Here can we see the predicted result of the same data according to the model. As we would hope for the
            distribution looks quite similar to what it actually is in reality."""),

        html.H3('Other visuals'),
        html.H4('Shap Decision Plot'),
        html.Img(
            src='assets/dp_plot_track.png',
            style={'background-color':'#777777'}
        ),
        html.P("""One slightly confusing visual here. This is a shap decision plot that attemps to demonstrate the impact each
                variable this model had on a particular value's prediction. This graph tries to explain how the song 'Ente campestre',
                which is the song that plays by default, got its predicted value."""),
        html.P("""Right represents more listens, the left represents less.
                  You can see here for example, that, according to our model, the fact that this song was the 7th song on the album (track_number==7),
                  that the genre chosen was 38 (Experimental), lowered the predicted value for the number of listens for that particular song. 
                  However the fact that it was released in late 2015 raised the predicted number of listens, 2008 being the year of the earliest
                  tracks in the set."""),
        html.P("""I would say that all of that is naturally intuitive. Songs at the start of the album we would expect should have more listens.
                  It intuitively makes sense that Experimental music is on average less popular just by the meaning of the word 'experimental'. And it also
                  makes sense that more recent songs maybe get more exposure if the userbase for the service is larger now than it was before. Of course
                  time could go either way, something very recent could have very little views because people haven't had time to see it, for example,
                  and our tree-based model can account for some of these patterns."""),

        html.H5("""That's all I have to say here. Thank you for reading. If you would like to learn more about what I did check out my notebook,
             or try exploring the interactive page some more to see how the model performs."""),
    ],
    style={'margin-bottom' : '3em'}
)

layout = dbc.Row([column1])