import pandas as pd
import numpy as np
import requests
import threading
import time

df_links = pd.read_csv("imdb_data.csv")

BASE_URL = "http://www.omdbapi.com/?apikey=[APIKEY]&i=tt"
THREADS = 10

def movie_url(imdbId):
    if (imdbId < 10):
        addon = "000000"
    elif (imdbId < 100):
        addon = "00000"
    elif (imdbId < 1000):
        addon = "0000"
    elif (imdbId < 10000):
        addon = "000"
    elif (imdbId < 100000):
        addon = "00"
    elif (imdbId < 1000000):
        addon = "0"
    else:
        addon = ""
    new_url = BASE_URL + addon + str(imdbId)
    return new_url

def worker(start, end):
    while (start < end):
            try:
                movie_id = df_links.loc[start, 'imdbId']

                m_url = movie_url(movie_id)
                request = requests.get(m_url)
                info = request.json()
                director = info['Director'].split(',')[0]
                genre = info['Genre'].split(',')[0]
                rated = info['Rated']
                year = info['Year']
                df_links.loc[start, 'director'] = director
                df_links.loc[start, 'rated'] = rated
                df_links.loc[start, 'genre'] = genre
                df_links.loc[start, 'year'] = year
            except:
                print("Skipping  " + str(start))
                start = start + 1
                continue
            start = start + 1

threads = []
t = threading.Thread(target= worker, args=(0,2700,))
threads.append(t)
t.start()

t = threading.Thread(target= worker, args=(2700,5400,))
threads.append(t)
t.start()

t = threading.Thread(target= worker, args=(5400,8100,))
threads.append(t)
t.start()

t = threading.Thread(target= worker, args=(8100,10800,))
threads.append(t)
t.start()

t = threading.Thread(target= worker, args=(10800,13500,))
threads.append(t)
t.start()

t = threading.Thread(target= worker, args=(13500,16200,))
threads.append(t)
t.start()

t = threading.Thread(target= worker, args=(16200,18900,))
threads.append(t)
t.start()

t = threading.Thread(target= worker, args=(18900,21600,))
threads.append(t)
t.start()

t = threading.Thread(target= worker, args=(21600,24300,))
threads.append(t)
t.start()

t = threading.Thread(target= worker, args=(24300,27279,))
threads.append(t)
t.start()

for j in threads:
    j.join()


df_links.to_csv("imdb_data.csv")
