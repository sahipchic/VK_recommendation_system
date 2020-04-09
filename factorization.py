import numpy as np
import pandas as pd
import pickle as pkl
import scipy.sparse as sps
from sklearn.decomposition import NMF
from tqdm import tqdm
import sklearn
import constants


def createDictMovieIdx(movies_df: pd.DataFrame):
    movieId2Idx = {}
    movieIdx2Id = []

    for movieId in movies_df['movieId']:
        if not movieId in movieId2Idx.keys():
            movieId2Idx[int(movieId)] = len(movieId2Idx.keys())
            movieIdx2Id.append(movieId)

    return movieId2Idx, movieIdx2Id


def buildUserMovieMatrix(movies: pd.DataFrame, ratings: pd.DataFrame, movieId2Idx):
    print("Building user-movie matrix...")

    users = ratings.userId.unique()
    matrix = np.full((len(users), len(movies)), 0.0, dtype=np.float32)

    for userRowIdx, userId in tqdm(enumerate(users)):
        ratingsForUser = ratings[ratings['userId'] == userId]
        for idx, rating in ratingsForUser.iterrows():
            movieIdx = int(movieId2Idx[rating['movieId']])
            ratingVal = int(rating['rating'])
            matrix[userRowIdx][movieIdx] = ratingVal

    print("Saving user movie matrix...")

    return matrix


def writeComponentsToPickle(W, H, pathW, pathH):
    print("Starting writing components")

    pklObject = open(pathW, 'wb')
    pkl.dump(W, pklObject)
    pklObject.close()
    pklObject = open(pathH, 'wb')
    pkl.dump(H, pklObject)
    pklObject.close()

    print("Finished writing components")

    return


def main():
    ratings_df = pd.read_csv(constants.PATH_TO_RATINGS_CSV)
    movies_df = pd.read_csv(constants.PATH_TO_MOVIES_CSV)

    movieId2Idx, movieIdx2Id = createDictMovieIdx(movies_df)
    matrix = buildUserMovieMatrix(movies_df, ratings_df, movieId2Idx)

    print("Starting sparsing")

    sparsedMatrix = sps.csr_matrix(matrix)

    print("Finished sparsing")
    print("Starting fitting")

    nmf = NMF(n_components=50)
    nmf.fit(sparsedMatrix)

    print("Finished fitting")
    print("Starting transforming")

    W = nmf.transform(sparsedMatrix)

    print("Finished transforming")

    H = nmf.components_
    writeComponentsToPickle(W, H, constants.PATH_TO_W_PICKLE, constants.PATH_TO_H_PICKLE)

    print("Starting training BallTree")

    tree = sklearn.neighbors.BallTree(W, leaf_size=0.6*len(W))

    print("Finished training BallTree")

    pklObject = open(constants.PATH_TO_BALL_TREE_PICKLE, 'wb')
    pkl.dump(tree, pklObject)
    pklObject.close()

    return


if __name__ == '__main__':
    main()
