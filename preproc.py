import pandas as pd
import numpy as np
from imdb import IMDb

ia = IMDb()
df_links = pd.read_csv("links.csv")
df_ratings = pd.read_csv("ratings.csv")
#df_movies = pd.read_csv("movies.csv") #I don't think this is necessary
#+ we can get genre from imdbpy, and movie title isnt important

#remove unnecessary columns
del df_links['tmdbId']
del df_ratings['timestamp']

#add columns for movie director, two actors, and genre
df_links['director'] = 0
df_links['lead_actor'] = 0
df_links['genre'] = 0

for i in range(0,df_links.size):
    movie = ia.get_movie(df_links.loc[i, 'imdbId'])
    lead = movie['actors'][0]
    director = movie['directors'][0]
    genre = movie['genres'][0]
    df_links.loc[i, 'director'] = int(director.personID)
    df_links.loc[i, 'lead_actor'] = int(lead.personID)
    df_links.loc[i, 'genre'] = genre

print(df_links.head())

#df = pd.merge(df_ratings, df_links, on='movieId', how='left')