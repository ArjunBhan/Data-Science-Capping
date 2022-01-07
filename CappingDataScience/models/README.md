### Models

We have three models in this folder and a combination of two of the models as an ensemble in the API.

##### Clustering

Clustering aims to cluster the players based on either offensive stats or defensive stats. It uses K-means.

##### Reinforcement

Reinforcement uses money lines to try and find patterns in betting data and predict good or bad bets. It uses a time series sliding window along with the Q learning algorithm.

##### Neural network and text analysis

The text analysis uses NLTK to analyize tweets from players. This analysis is then fed into a neural network along with other data from a given team's previous matches to try and predict the likelhood of winning.

##### Ensemble

The ensemble model is primarily implmeneted in the API. However there is a notebook implemneted it and testing the preformance of it in the ensemble folder. It uses both the reinforcemnet along with the neural network to try and predict game outcomes for the purpose of betting.

### Saved

These models all are saved after training in ```./api/savedModels```. These models are saved here since the API is the primary user of the models and this can simplify the deployment if dockerization is going to be used.