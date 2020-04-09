from tqdm import tqdm
import pandas as pd
import constants
import pickle as pkl


def getSumRatingsForMovies(ratings_df: pd.DataFrame):
    sum_rating_for_movie = dict()
    for index, item in tqdm(ratings_df.iterrows()):
        mid = item["movieId"]
        cur_rating = item["rating"]
        if mid not in sum_rating_for_movie.keys():
            sum_rating_for_movie[mid] = cur_rating
        else:
            sum_rating_for_movie[mid] += cur_rating

    return sum_rating_for_movie


def getTopMoviesForGenreses(movies_df: pd.DataFrame, sum_rating_for_movie, topN):
    movies_for_genres = dict()
    movie_genres = dict()

    for index, item in tqdm(movies_df.iterrows()):
        cur_genres = item["genres"].split('|')
        movie_genres[item["movieId"]] = cur_genres

        for genre in cur_genres:
            if genre not in movies_for_genres.keys():
                if sum_rating_for_movie.get(item["movieId"]) is None:
                    movies_for_genres[genre] = [(item["movieId"], .0)]
                else:
                    movies_for_genres[genre] = [(item["movieId"], sum_rating_for_movie[item["movieId"]])]
            else:
                if sum_rating_for_movie.get(item["movieId"]) is None:
                    movies_for_genres[genre].append((item["movieId"], .0))
                else:
                    movies_for_genres[genre].append((item["movieId"], sum_rating_for_movie[item["movieId"]]))

    for key in movies_for_genres:
        element = movies_for_genres[key]
        element.sort(key=lambda x: x[1])
        movies_for_genres[key] = element[::-1][:topN]

    return movies_for_genres, movie_genres


def main():
    ratings_df = pd.read_csv(constants.PATH_TO_RATINGS_CSV)
    movies_df = pd.read_csv(constants.PATH_TO_MOVIES_CSV)

    sumRatingForMovies = getSumRatingsForMovies(ratings_df)
    moviesForGenres, movieGenres = getTopMoviesForGenreses(movies_df, sumRatingForMovies, constants.TOP_N_NUMBER)

    pklObject = open(constants.PATH_TO_MOVIES_FOR_GENRES_PICKLE, 'wb')
    pkl.dump(moviesForGenres, pklObject)
    pklObject.close()

    pklObject = open(constants.PATH_TO_MOVIE_GENRES, 'wb')
    pkl.dump(movieGenres, pklObject)
    pklObject.close()

    return


if __name__ == '__main__':
    main()

