import pandas as pd
import numpy as np
from imdb import IMDb

ia = IMDb()
df = pd.read_csv("imdb_data.csv")
del df['Unnamed: 0']
del df['tmdbId']
del df['type'] #they are all movies this is unnecessary (other types include tv show, documentary, etc)
del df['rated'] #cannot get the MPAA rating from IMDb and most coming from omdb are blank so just delete
del df['metascore'] #cannot get this from IMDb and most are NaN so just delete

#for any data that could not be obtained from omdb, utilize IMDb
#+ this will not be an issue regarding speed because most values should be set
for i in range(0,20):
    if (pd.isna(df.loc[i, 'year']) or pd.isna(df.loc[i, 'genre']) or pd.isna(df.loc[i, 'director'])
        or pd.isna(df.loc[i, 'LeadActor']) or pd.isna(df.loc[i, 'country'])):
        
        try:
            movie = ia.get_movie(df.loc[i, 'imdbId'])
            this_director = movie['directors'][0]
            df.loc[i, 'director'] = this_director
            this_genre = movie['genres'][0]
            df.loc[i, 'genre'] = this_genre
            this_year = movie['year']
            df.loc[i, 'year'] = this_year
            this_actor = movie['actors'][0]
            df.loc[i, 'LeadActor'] = this_actor
            this_language = movie['language'][0]
            df.loc[i, 'language'] = this_language
            this_country = movie['country'][0]
            df.loc[i, 'country'] = this_country
        except:
            continue

#only include primary language
for i in range(0, 27277):
    try:
        df.loc[i, 'language'] = df.loc[i, 'language'].split(',')[0]
    except:
        continue #Any issues will be if language was 'NaN'

#Obtain avg ratings data and edit dataframes
df_avgratings = pd.read_csv("avg_ratings.csv")
del df_avgratings['Unnamed: 0']
del df_avgratings['total_rating']
del df['imdbId']

#merge two dataframes
df_final = pd.merge(df_avgratings, df, on='movieId', how='left')

#drop NaN values
df_final.dropna(axis=0, how='any', inplace=True)

#Removing any movies that were rated a low amount of times
#+this data can be skewed, 1 user's rating is not indicative of population
low_ratings = []
ind_list = []

for i in df_final['count']:
    if (i <= 5):
        low_ratings.append(df_final.index[ df_final['count'] == i ])

for ind in low_ratings:
    for num_of_ind in ind:
        ind_list.append(num_of_ind)

df_final.drop(ind_list, inplace=True)

#Finally, save the file
df.to_csv("final_data_removed_lowcounts.csv")