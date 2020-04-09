# VK Recommendation System

Recommendation system was built on the basis of matrix factorization of the dataset from the MovieLens website (http://files.grouplens.org/datasets/movielens/ml-25m.zip)

## How does it work?
Recommendation model consists of 2 parts, which are implemented in files `baseline.py` and `factorization.py`

### Factorization
The main goal of matrix factorization in our case is to divide `user-item matrix` to `user-factor matrix` and `item-factor matrix` with static number of features.

`NMF` method of factorization was chosen because of its fast work on the big datasets.
`W` - user-factor matrix and `H` - item-factor matrix were obtained.

Also added BallTree structure to try the `k-nearest-neighbor method` in predictor.

### Baseline
In case of a small number of chosen movies the main goal of this idea is to calculate for each genre list of movies they consists of, sorted by total rating amount for each movie, and then save `topN` positions for each genre.

### Predictor
The main problem in making our predictions is that we know nothing about a new user, who hasn't taken part in the training process. What can we do with this? 

Firstly, we have to build `user-item matrix`, which is similar with the factorization's one, but built for only one user. In general, to get recommendations list, we have to make matrix multiplying, getting row from `user-factor matrix` and multiply it on the whole `item-factor matrix` in case we want to get prediction for all movies, and multiply it on a current column from `item-factor matrix` in case we want to get rating for one current movie.

The problem is how to create a new row `W'` for new user, which is essentially the same row in the `user-factor matrix` and then, multiplying it on the `item-factor matrix` (which doesn't change), getting a list of predicted rating for all movies.

We need to come up with a matrix `W'` such that `W' * H = I`, where `I` is our interaction matrix of new user, `H` is already calculated matrix for items (`item-factor matrix`).

Well, here we can just say, that `W' = I x H^(-1)`, where `H^(-1)` is a pseudo-inverse matrix of `H`.
In this way we can  obtain `W'`, and then it's easy to get predicted raitings list for all movies, or for the few current ones.

Also, i had an idea to find the nearest neighbor for our `W'` row in the `W` matrix using BallTree structure which was implemented and fitted before, but results for neighbor was not better than for `W'` matrix.

Then, there were calculated recommendations by genres (picked first 3 popular genres caused by chosen movies), concatenate results and return it to front. 
  