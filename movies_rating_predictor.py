#!/usr/bin/env python

import argparse
import constants
import pandas as pd
import pickle as pkl
from tqdm import tqdm
import numpy as np


def getObjectFromPickle(path):
    pklObject = open(path, 'rb')
    obj = pkl.load(pklObject)
    pklObject.close()

    return obj


def buildUserChosenMoviesMatrix(movies: pd.DataFrame, argsIdx, movieIdx):
    userChosenMoviesMatrix = []

    for i in tqdm(range(len(movies))):
        if movieIdx[i] in argsIdx:
            userChosenMoviesMatrix.append(5.0)
        else:
            userChosenMoviesMatrix.append(0.0)

    return userChosenMoviesMatrix


def main():
    parser = argparse.ArgumentParser(description='Movies Rating Predictor')
    parser.add_argument('--chosen_movie_idx', required=True)
    args = parser.parse_args()

    movies_df = pd.read_csv(constants.PATH_TO_MOVIES_CSV)
    movieIdx = [0 for i in range(len(movies_df))]
    for index, item in movies_df.iterrows():
        movieIdx[index] = item["movieId"]

    W = getObjectFromPickle(constants.PATH_TO_W_PICKLE)
    H = getObjectFromPickle(constants.PATH_TO_H_PICKLE)

    tree = getObjectFromPickle(constants.PATH_TO_BALL_TREE_PICKLE)
    moviesForGenres = getObjectFromPickle(constants.PATH_TO_MOVIES_FOR_GENRES_PICKLE)
    movieGenres = getObjectFromPickle(constants.PATH_TO_MOVIE_GENRES)

    args.chosen_movie_idx = eval(args.chosen_movie_idx)
    userChosenMoviesMatrix = buildUserChosenMoviesMatrix(movies_df, args.chosen_movie_idx, movieIdx)
    userChosenMoviesMatrix = np.expand_dims(np.array(userChosenMoviesMatrix), axis=0)

    newRowInW = np.dot(userChosenMoviesMatrix, np.linalg.pinv(H))
    totalNumberOfRecommendations = constants.TOP_N_NUMBER * 2
    recommendedIdx = np.argsort(np.dot(newRowInW, H))[::-1][0][:constants.TOP_N_NUMBER]


    # For the k-nearest-neighbors method
    #
    # dist, ind = tree.query(newRowInW, k=1)
    # neighborIndex = ind[0][0]
    # recommendedIdx = np.argsort(np.dot(W[neighborIndex], H))[::-1][0][:constants.TOP_N_NUMBER]


    chosenMoviesIdx = args.chosen_movie_idx
    numRecommendationsPerId = totalNumberOfRecommendations // len(chosenMoviesIdx)
    recommendedIdxFromTopByGenre = []

    storedIdx = set()

    for chosenId in chosenMoviesIdx:
        curGenres = movieGenres[chosenId]
        numRecommendationsPerGenre = numRecommendationsPerId // len(curGenres)

        for genre in curGenres:
            topIdxPerGenre = moviesForGenres[genre]
            cnt = 0

            for _id in topIdxPerGenre:
                if _id[0] not in storedIdx:
                    recommendedIdxFromTopByGenre.append((genre, _id[0]))
                    storedIdx.add(_id[0])
                    cnt += 1
                if cnt >= numRecommendationsPerGenre:
                    break

    recommendMovieIdx = []
    for i in recommendedIdx:
        recommendMovieIdx.append(('Personal', movieIdx[i]))

    recommendedIdxFromTopByGenre.sort(key=lambda x: x[0])
    resultArray = recommendMovieIdx + recommendedIdxFromTopByGenre
    strResult = ''
    for i in resultArray:
        strResult += str(i[0]) + ':' + str(i[1]) + ' '
    print(strResult.rstrip())


if __name__ == '__main__':
    main()
