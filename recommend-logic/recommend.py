# import os
# print(os.getcwd())
# from ydata_profiling import ProfileReport
# import pandas as pd

# df = pd.read_csv("recommend-logic/data-set/data/ratings.csv")

# # Generate the data profiling report
# report = ProfileReport(df, title='Ratings')
# report.to_file("recommend-logic/data-set/reports/ratings.html")

import pandas as pd
import json
ratings = pd.read_csv("recommend-logic/data-set/data/ratings.csv")
movies = pd.read_csv("recommend-logic/data-set/data/movies.csv")
links = pd.read_csv("recommend-logic/data-set/data/links.csv", converters={'imdbId': str})

# Preprocessing
import re

def clean_title(title):
    title = re.sub("[^a-zA-Z0-9 ]", "", title)
    return title

movies["clean_title"] = movies["title"].apply(clean_title)

from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer(ngram_range=(1,2))

tfidf = vectorizer.fit_transform(movies["clean_title"])

from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def search(title):
    title = clean_title(title)
    query_vec = vectorizer.transform([title])
    similarity = cosine_similarity(query_vec, tfidf).flatten()
    indices = np.argpartition(similarity, -5)[-5:]
    results = movies.iloc[indices].iloc[::-1]

    return results

def find_sim_user_recs(movie_id):
    similar_users = ratings[(ratings["movieId"] == movie_id) & (ratings["rating"] > 4)]["userId"].unique()
    similar_user_recs = ratings[(ratings["userId"].isin(similar_users)) & (ratings["rating"] > 4)]["movieId"]
    similar_user_recs = similar_user_recs.value_counts() / len(similar_users)
    return similar_user_recs[similar_user_recs > .10]

def find_all_user_recs(sim_user_recs):
    all_users = ratings[(ratings["movieId"].isin(sim_user_recs.index)) & (ratings["rating"] > 4)]
    return all_users["movieId"].value_counts() / len(all_users["userId"].unique())

def find_percentage_difference(sim_user_rec, all_user_rec):
    rec_percentages = pd.concat([sim_user_rec, all_user_rec], axis=1)
    rec_percentages.columns = ["similar", "all"]
    rec_percentages["score"] = rec_percentages["similar"] / rec_percentages["all"]
    return rec_percentages.sort_values("score", ascending=False)

def find_similar_movies(movie_id):
    similar_user_recs = find_sim_user_recs(movie_id)
    all_user_recs = find_all_user_recs(similar_user_recs)
    percentage_difference = find_percentage_difference(similar_user_recs, all_user_recs)
    return percentage_difference.head(10).merge(movies, left_index=True, right_on="movieId").merge(links)[["score", "title", "genres", "imdbId"]]

def get_recommendations(title):
    results = search(title)
    movie_id = results.iloc[0]["movieId"]
    print(movie_id)
    similar_movies = find_similar_movies(movie_id)
    similar_movies["imdbLink"] = similar_movies['imdbId'].apply(lambda x: "http://www.imdb.com/title/tt"+x+"/")
    similar_movies = similar_movies.drop("imdbId", axis=1)
    if not similar_movies.empty:
        similar_movies = similar_movies.drop(0)
    similar_movies = similar_movies.to_json(orient='records')
    return json.loads(similar_movies)


def get_average_rating_desc():
    average_rating = ratings.groupby("movieId").agg({"rating":["mean"]})
    average_rating.columns = ["avg_rating"]
    average_rating.reset_index(inplace=True)
    return average_rating.sort_values("avg_rating", ascending=False).merge(movies, left_on="movieId", right_on="movieId")

def get_recommendations_by_genre(genre):
    average_rating_desc = get_average_rating_desc()
    average_rating_desc["boolean"] = average_rating_desc['genres'].apply(lambda x: 1 if all(i.casefold() in x.casefold() for i in genre) else 0)
    recommedation_by_genre = average_rating_desc[(average_rating_desc.boolean == 1)]
    recommedation_by_genre = recommedation_by_genre.merge(links)[["title", "genres", "imdbId"]]
    recommedation_by_genre["imdbLink"] = recommedation_by_genre['imdbId'].apply(lambda x: "http://www.imdb.com/title/tt"+x+"/")
    recommedation_by_genre = recommedation_by_genre.drop("imdbId", axis=1)
    recommedation_by_genre = recommedation_by_genre.to_json(orient='records')
    return json.loads(recommedation_by_genre)