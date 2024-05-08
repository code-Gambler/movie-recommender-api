from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import numpy as np
import re
import json

ratings = pd.read_csv("recommend-logic/data-set/data/ratings.csv")
movies = pd.read_csv("recommend-logic/data-set/data/movies.csv")
links = pd.read_csv("recommend-logic/data-set/data/links.csv", converters={'imdbId': str})

def clean_title(title):
    """Cleans title of the movies file by removing all the character except
       space and alphanumeric characters.

    Args:
        title: The title of the movie to clean.

    Returns:
        The cleaned title string.
    """
    title = re.sub("[^a-zA-Z0-9 ]", "", title)
    return title

# Preprocessing
movies["clean_title"] = movies["title"].apply(clean_title)
vectorizer = TfidfVectorizer(ngram_range=(1,2))
vectorized_movies = vectorizer.fit_transform(movies["clean_title"])

def search(title):
    """Searches for similar movies based on the provided title using TF-IDF vectorizer.

    Args:
        title: The title of the movie to search.

    Returns:
        A pandas DataFrame containing the top 5 most similar movies based on title.
    """
    title = clean_title(title)
    query_vec = vectorizer.transform([title])
    similarity = cosine_similarity(query_vec, vectorized_movies).flatten()
    indices = np.argpartition(similarity, -5)[-5:]
    results = movies.iloc[indices].iloc[::-1]
    return results

def find_sim_user_recs(movie_id):
    """Finds movie recommendations based on similar user ratings.

    This function identifies users who gave high ratings (above 4) to the provided movie
    and then recommends other movies that these users also rated highly (above 4).

    Args:
        movie_id: The ID of the movie to use as a base for recommendations.

    Returns:
        A pandas DataFrame containing movie IDs as index and recommendation scores (percentage) as values
        for movies recommended based on similar user ratings.
    """
    similar_users = ratings[(ratings["movieId"] == movie_id) & (ratings["rating"] > 4)]["userId"].unique()
    similar_user_recs = ratings[(ratings["userId"].isin(similar_users)) & (ratings["rating"] > 4)]["movieId"]
    similar_user_recs = similar_user_recs.value_counts() / len(similar_users)
    return similar_user_recs[similar_user_recs > .10]

def find_all_user_recs(movies):
    """Finds all user ratings higher that 4 for the movies.

    Args:
        movies: A pandas DataFrame containing movies.

    Returns:
        A pandas DataFrame containing movie IDs as index and overall rating percentages as values
        for all users who rated the movies recommended.
    """
    all_users_rating = ratings[(ratings["movieId"].isin(movies.index)) & (ratings["rating"] > 4)]
    return all_users_rating["movieId"].value_counts() / len(all_users_rating["userId"].unique())

def find_percentage_difference(sim_user_rec, all_user_rec):
    """Calculates the percentage difference between recommendation scores based on similar users
       and overall user ratings.

    Args:
        sim_user_rec: A pandas DataFrame containing movie IDs as index and recommendation scores based on similar users as values.
        all_user_rec: A pandas DataFrame containing movie IDs as index and recommendation scores based on all users as values.

    Returns:
        A pandas DataFrame containing movie IDs, recommendation scores based on similar users and overall users, and imdb id.
    """
    rec_percentages = pd.concat([sim_user_rec, all_user_rec], axis=1)
    rec_percentages.columns = ["similar", "all"]
    rec_percentages["score"] = rec_percentages["similar"] / rec_percentages["all"]
    return rec_percentages.sort_values("score", ascending=False)

def find_similar_movies(movie_id):
    """Finds similar movies based on a combination of user ratings and movie content.

    This function first finds movies recommended based on similar user ratings for the provided movie_id.
    Then, it calculates a score indicating the recommendation strength based on the difference between
    recommendation scores from similar users and overall user ratings. Finally, it retrieves details
    like title, genres, and imdb link for the top 10 recommended movies.

    Args:
        movie_id: The ID of the movie to use as a base for recommendations.

    Returns:
        A pandas DataFrame containing details (title, genres, imdb link, score) for the top 10 recommended movies.
    """
    similar_user_recs = find_sim_user_recs(movie_id)
    all_user_recs = find_all_user_recs(similar_user_recs)
    percentage_difference = find_percentage_difference(similar_user_recs, all_user_recs)
    return percentage_difference.head(10).merge(movies, left_index=True, right_on="movieId").merge(links)[["score", "title", "genres", "imdbId"]]

def get_recommendations(title):
    """Recommends similar movies based on user ratings and content.

    This function searches for movies similar to the provided title, finds recommendations based on
    a combination of user ratings and movie content for the most similar movie, and converts
    the results to a JSON dictionary.

    Args:
        title: The title of the movie to use for recommendations.

    Returns:
        A dictionary containing a list of recommended movies with details
        including title, genres, imdb link, and a score indicating recommendation
        strength.
    """
    results = search(title)
    movie_id = results.iloc[0]["movieId"]
    similar_movies = find_similar_movies(movie_id)
    similar_movies_with_link = covert_imdb_id_to_link(similar_movies)
    similar_movies_with_link = remove_element(similar_movies_with_link, 0)
    return covert_to_json(similar_movies_with_link)


def get_average_rating_desc():
    """Calculates average rating for each movie and merges with movie details.

    This function groups movie ratings by movie ID, calculates the average rating for each movie,
    and merges the results with the original movie data including title and genres.
    Sorts the results in descending order by average rating.

    Returns:
        A pandas DataFrame containing movie details (title, genres) merged with average rating.
    """
    average_rating = ratings.groupby("movieId").agg({"rating":["mean"]})
    average_rating.columns = ["avg_rating"]
    average_rating.reset_index(inplace=True)
    return average_rating.sort_values("avg_rating", ascending=False).merge(movies, left_on="movieId", right_on="movieId")

def covert_imdb_id_to_link(movies):
    """Converts imdb ID to a full IMDB link.

    This function adds a new column 'imdbLink' to the provided DataFrame. The new column
    contains the full IMDB link for each movie using the existing 'imdbId' column. Removing the 'imdbId' column.

    Args:
        movies: A pandas DataFrame containing movie data.

    Returns:
        A pandas DataFrame with an additional 'imdbLink' column containing full IMDB links.
    """
    movies["imdbLink"] = movies['imdbId'].apply(lambda x: "http://www.imdb.com/title/tt"+x+"/")
    return movies.drop("imdbId", axis=1)

def remove_element(df, index):
    """Removes a row from a pandas DataFrame at the specified index.

    This function checks if the DataFrame is not empty and then removes the row at the provided index.

    Args:
        df: The pandas DataFrame to remove the element from.
        index: The index of the row to remove.

    Returns:
        A pandas DataFrame with the row at the specified index removed (if the DataFrame was not empty).
    """
    if not df.empty:
        return df.drop(index)
    
def covert_to_json(df):
    """Converts a pandas DataFrame to a JSON Object.

    This function uses the `to_json` method of the DataFrame to convert it to a JSON string
    and then loads the JSON string into a Python dictionary.

    Args:
        df: The pandas DataFrame to convert to JSON.

    Returns:
        A Python dictionary representing the JSON format of the DataFrame.
    """
    json_string = df.to_json(orient='records')
    return json.loads(json_string)

def get_movies_by_genre(movies, genre):
    """Filters movies based on a specific genre.

    This function creates a new boolean column indicating whether a movie belongs to the specified genre
    based on case-insensitive string matching. It then filters the DataFrame to include only movies
    where the boolean column is True. Finally, it merges the results with the links DataFrame
    to include the 'imdbId' for each movie.

    Args:
        movies: A pandas DataFrame containing movie data.
        genre: The genre to filter movies by (case-insensitive).

    Returns:
        A pandas DataFrame containing details (title, genres, imdb link) for movies belonging to the specified genre.
    """
    movies["boolean"] = movies['genres'].apply(lambda x: 1 if all(i.casefold() in x.casefold() for i in genre) else 0)
    recommendation_by_genre = movies[(movies.boolean == 1)]
    return recommendation_by_genre.head(10).merge(links)[["title", "genres", "imdbId"]]

def get_recommendations_by_genre(genre):
    """Recommends movies based on a specified genre.

    This function first retrieves the top movies with high average ratings using `get_average_rating_desc`.
    Then, it filters those movies based on the provided genre using `get_movies_by_genre`. Finally,
    it converts the recommendations to JSON format using `covert_to_json`.

    Args:
        genre: The genre to recommend movies from (case-insensitive).

    Returns:
        A dictionary containing a list of recommended movies with details
        including title, genres, imdb link, in JSON format.
    """
    average_rating_desc = get_average_rating_desc()
    recommendation_by_genre = get_movies_by_genre(average_rating_desc, genre)
    recommendation_by_genre_with_links = covert_imdb_id_to_link(recommendation_by_genre)
    return covert_to_json(recommendation_by_genre_with_links)