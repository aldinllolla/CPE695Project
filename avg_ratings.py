import pandas as pd
import numpy as np
import requests
import threading
import time

rating_df = pd.read_csv('ratings.csv')

global new_df
new_df = pd.DataFrame(columns=['movieId', 'total_rating','count','avg_rating'])
count = rating_df['movieId'].value_counts()

#print(count)
#print(rating_df.loc[rating_df['movieId'] == 123607]['rating'].sum())
j = 0
movie_dict = {}

def worker(start, end):
    global new_df
    j = 0
    for i in range (start, end):
        row = rating_df.iloc[i]
        if not row['movieId'] in movie_dict:
            movieId = row['movieId']
            movie_dict[movieId] = i
            rating_sum = rating_df.loc[rating_df['movieId'] == movieId]['rating'].sum()
            count_for_this_movie = count[movieId]
            new_df = new_df.append({'movieId' : movieId, 'total_rating' : rating_sum,'count' : count_for_this_movie,'avg_rating' : rating_sum/ count_for_this_movie}, ignore_index=True)
            #new_df.loc[movieId] = [movieId,rating_sum,count_for_this_movie,rating_sum/ count_for_this_movie]
            print(i)

# worker(0,19967646)
i = 0
threads = []
while (i < 19967646):
    t = threading.Thread(target= worker, args=(i,i+1996764,))
    threads.append(t)
    t.start()
    i = i + 1996764

for j in threads:
    j.join()

new_df.to_csv("new_data.csv")
# new_dict = {}
# for i in rating_df['movieId']:
#     new_dict[i] = rating_df.loc[i, 'rating']
