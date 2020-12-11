
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
from fuzzywuzzy import process

#storing file
movies='movies.csv'
ratings='ratings.csv'

#Extracting file data
df_movies=pd.read_csv(movies, usecols=['movieId','title'], dtype={'movieId':'int32','title':'str'})
df_ratings=pd.read_csv(ratings, usecols=['userId','movieId','rating'],dtype={'userId':'int32','movieId':'int32','rating':'float32'})

#Creating spare Matrix
movies_users=df_ratings.pivot(index='movieId', columns='userId',values='rating').fillna(0)
mat_movies_users=csr_matrix(movies_users.values)



# Cosine Similarity
model_knn= NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=20)
model_knn.fit(mat_movies_users)



# List of Movies recommended

def recommender(movie_name, data, model, n_recommendations):
    model.fit(data)
    idx = process.extractOne(movie_name, df_movies['title'])[2]
    print('Movie Selected: ', df_movies['title'][idx], 'Index: ', idx)
    print('Searching for recommendations.....')
    distances, indices = model.kneighbors(data[idx], n_neighbors=n_recommendations)
    for i in indices:
        print(df_movies['title'][i].where(i != idx))


movie_name=str(input("Enter Movie Name : "))
recommender(movie_name, mat_movies_users, model_knn, 20)
