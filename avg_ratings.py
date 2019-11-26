import pandas as pd
import numpy as np

rating_df = pd.read_csv("ratings.csv")
count = rating_df['movieId'].value_counts()
movieset = list(set(rating_df['movieId']))
del rating_df['timestamp']

data = np.zeros((len(movieset),4))
j = 0
for i in movieset:
    rating_sum = rating_df.loc[rating_df['movieId'] == i]['rating'].sum()
    count_for_movie = count[i]
    avg_rating = rating_sum / count_for_movie
    data[j, 0] = i #set to movieId
    data[j, 1] = rating_sum
    data[j, 2] = count_for_movie
    data[j, 3] = avg_rating
    j = j + 1

df = pd.DataFrame(data, columns=['movieId', 'total_rating','count','avg_rating'])
df.to_csv("avg_ratings.csv")