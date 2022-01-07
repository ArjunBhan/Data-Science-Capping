import connexion
import six

import os

from tensorflow import keras
import tensorflow.compat.v1 as tf
tf.compat.v1.disable_eager_execution()
from collections import deque
import numpy as np
import random

from dateutil import parser
import pickle

from sklearn.preprocessing import OneHotEncoder, LabelEncoder, MinMaxScaler

from swagger_server.models.betting_bot_input import BettingBotInput  # noqa: E501
from swagger_server.models.betting_bot_output import BettingBotOutput  # noqa: E501
from swagger_server.models.ensemble_input import EnsembleInput  # noqa: E501
from swagger_server.models.ensemble_output import EnsembleOutput  # noqa: E501
from swagger_server import util
from swagger_server import util
from swagger_server import cur, conn # Database 

from swagger_server.models.cluster_input import ClusterInput  # noqa: E501
from swagger_server.models.cluster_output import ClusterOutput  # noqa: E501
from swagger_server.models.cluster_output_item import ClusterOutputItem  # noqa: E501

from swagger_server.models.nerual_net_input import NerualNetInput  # noqa: E501
from swagger_server.models.nerual_net_output import NerualNetOutput  # noqa: E501
from swagger_server.models.neural_net_features import NeuralNetFeatures  # noqa: E501


from swagger_server.models.player import Player  # noqa: E501
from swagger_server.models.game import Game  # noqa: E501
from swagger_server.models.team import Team  # noqa: E501

import nltk
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')
nltk.download('vader_lexicon')

from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.stem import WordNetLemmatizer 
from nltk.corpus import stopwords

def model_clustering_post(body):  # noqa: E501
    """Cluster a set of players

    Returns cluster IDs for the provided players # noqa: E501

    :param body: Player ids to cluster
    :type body: List[]

    :rtype: List[int]
    """

    if connexion.request.is_json:
        body = ClusterInput.from_dict(connexion.request.get_json())  # noqa: E501
    else:
        return "Got incorrect input", 400    

    # Get player stats.
    season = body.season
    player_ids = body.player_ids
    not_found_or_missing = []
    stats = []
    for i in player_ids:
        try:
            cur.execute("SELECT AVG(points), AVG(assists), AVG(steals), " +
                        "AVG(blocked_shots) FROM player_game_detail  " +
                        "INNER JOIN game ON player_game_detail.game_id = game.game_id " +
                        "WHERE player_id = %s AND season = %s", [i, season])
            res = list(cur.fetchone())
        except:
            conn.rollback()
            return "Database error", 500        
        
        has_none = False
        for j in range(len(res)):
            if res[j] == None:
                not_found_or_missing.append(i)
                has_none = True
                break
            else: # Convert to float
                res[j] = float(res[j])
        
        if not has_none:
            stats.append([i])
            stats[-1].extend(res)

    # Load our models
    with open("savedModels/offense_clustering.pkl", 'rb') as file:
        offense = pickle.load(file)
    with open("savedModels/defense_clustering.pkl", 'rb') as file:
        defense = pickle.load(file)

    # Find clusters for both offense and defense.
    if stats:    
        stats_np = np.array(stats)
        offense_classes = offense.predict(stats_np[:, 1:3])
        defense_classes = defense.predict(stats_np[:, 3:5])

    cluster_output = []
    for i in range(len(stats)):
        stats[i].extend([offense_classes[i], defense_classes[i]])
        for j in range(len(stats[i])): # Convert from numpy to int/float
            if j >= len(stats[i]) - 2 or j == 0:
                stats[i][j] = int(stats[i][j])
            else:
                stats[i][j] = float(stats[i][j])
                
        cluster_output.append(ClusterOutputItem(*stats[i]))

    # Get player_info for convenience of the api user and also the aws EC2
    # instance is has terrible performance. Calling 50+ calls to lookup each
    # player in the cluster is just simply not viable.
    players = []
    for i in player_ids:
        try:
            cur.execute("SELECT * FROM player WHERE player_id = %s LIMIT 1", [i])
            res = cur.fetchone()
        except:
            conn.rollback()
            return "Database error", 500        
            
        if res == None:
            players.append(None)
        else:        
            players.append(Player(*res))
    
    return ClusterOutput(cluster_output, players, not_found_or_missing)


def model_reinforcement_post(body):  # noqa: E501
    """Run a betting bot starting at a date

    Runs our betting bot based on input # noqa: E501

    :param body: Input to configure the betting bot
    :type body: dict | bytes

    :rtype: BettingBotOutput
    """

    # Make our body as input.
    if connexion.request.is_json:
        body = BettingBotInput.from_dict(connexion.request.get_json())  # noqa: E501
    else:
        return "Got incorrect input", 400
    
    games = []
    data = []
    game_ids = []
    bet_result = []
    try:
        cur.execute("SELECT * FROM game WHERE " +
                    "game_date >= %s AND home_ml IS NOT NULL AND " +
                    "away_ml IS NOT NULL ORDER BY game_date LIMIT %s",
                    [body.starting_date, body.num_games])
        for i in cur.fetchall():
            games.append(i)
    except:
        conn.rollback()
        return "Database error", 500        

    for i in games:
        data.extend([i[12], i[20]])
        game_ids.append(i[0])
        bet_result.extend([i[5], not i[5]])        
    
    initial_money = 10000
    window_size = 30
    skip = 1
    batch_size = 32
    model = Agent(state_size = window_size, 
                  window_size = window_size, 
                  data = data, 
                  skip = skip, 
                  batch_size = batch_size,
                  bet_results = bet_result)
    model.restore()

    bought, ending_money = model.run_model(body.starting_money, data, bet_result)

    teams_out, games_out = [], []
    for i in games:
        try:        
            cur.execute("SELECT * FROM team WHERE team_id = %s", [i[2]])
            teams_out.append(Team(*cur.fetchone()))

            cur.execute("SELECT * FROM team WHERE team_id = %s", [i[3]])
            teams_out.append(Team(*cur.fetchone()))
        except:
            conn.rollback()
            return "Database error", 500        

        games_out.append(Game(*i))

    return BettingBotOutput(games_out, teams_out, bought, ending_money)

def model_neural_network_post(body):  # noqa: E501
    """Runs a prediction on a given game using a possible supplied tweet.

    Gives the chance of team winning from the first game at the date supplied. Also provides features the nerual network is using to predict. # noqa: E501

    :param body: Input to the neural network
    :type body: dict | bytes

    :rtype: NerualNetOutput
    """
    if connexion.request.is_json:
        body = NerualNetInput.from_dict(connexion.request.get_json())  # noqa: E501
    else:
        return "Got incorrect input", 400


    # Get the game that occurs first after our date.
    # We are going to assume we will always predict the home team.
    try:
        is_home = True
        cur.execute("SELECT game_id, home_team_id, game_date, " +
                    "home_won_last, home_team_won FROM game WHERE " +
                    "game_date >= %s ORDER BY game_date LIMIT 1", [body._date])
        game_id, team_id, game_date, home_won_last, home_team_won = cur.fetchone()
    except:
        conn.rollback()
        return "Database error", 500

    try:
        body._date = parser.parse(body._date)
    except:
        pass
    
    return run_neural_net(game_id, team_id, game_date,
                          home_won_last, home_team_won, is_home, body.tweet,
                          body._date) 

def run_neural_net(game_id, team_id, game_date, home_won_last,
                   home_team_won, is_home, tweet, _date):
    # First we need to convert our tweet into a positivity score.
    # If we don't have a tweet set positivity to 0 and tweet to 0.
    tweet, positivity = 0.0, 0.0
    if tweet:
        ps = PorterStemmer()
        lemmatizer = WordNetLemmatizer()
        sia = SentimentIntensityAnalyzer()
        
        # tokenize and lower
        clean_tweet_bag = [t.lower() for t in nltk.word_tokenize(tweet)]
        # remove non alphanumeric stuff like punctuation and numbers
        clean_tweet_bag = [t for t in clean_tweet_bag if t.isalnum()]
        # remove stop words
        clean_tweet_bag = [t for t in clean_tweet_bag if t not in
                           nltk.corpus.stopwords.words("english")]
        # stem tokens
        clean_tweet_bag = [ps.stem(t) for t in clean_tweet_bag]
        # lemmatize tokens
        clean_tweet_bag = [lemmatizer.lemmatize(t) for t in clean_tweet_bag]

        # get sentiment of tweet
        tweet_sentiment = sia.polarity_scores(" ".join(clean_tweet_bag))
        print(tweet_sentiment)
        
        # If neutral leave tweet as 0.0.
        if tweet_sentiment["pos"] > tweet_sentiment["neg"]: # Positive tweet
            positivity = 1.0
        elif tweet_sentiment["pos"] < tweet_sentiment["neg"]: # Negative tweet
            positivity = 0.0
        tweet = 1.0 # Set that we do have a tweet.

    
    try:
        # Get the game which occured before the game.
        cur.execute("SELECT game_id FROM game WHERE " +
                    "game_date < %s AND " +
                    "(home_team_id = %s OR away_team_id = %s) " +
                    "ORDER BY game_date DESC LIMIT 1 ", [_date, team_id, team_id])
        prev_game_id = cur.fetchone()[0]

        # Get the statistics from previous game.
        cur.execute("SELECT SUM(points), " +
                    "AVG(field_goals_made) / AVG(field_goals_attempted), " +
                    "AVG(free_throws_made) / AVG(free_throws_attempted), " +
                    "AVG(three_pointers_made) / AVG(three_pointers_attempted), " +
                    "SUM(assists), SUM(offensive_rebounds) + SUM(defensive_rebounds) " +
                    "FROM player_game_detail " +
                    "WHERE game_id = %s AND team_id = %s", [prev_game_id, team_id])
        res = list(cur.fetchone())
        for i in range(len(res)):
            res[i] = float(res[i])
    except:
        conn.rollback()
        return "Database error", 500        
      
    
    # Assemble our feature vector.
    features = [int(_date.strftime("%m")), int(_date.strftime("%y")) + 2000, team_id]
    features.extend(res)
    features.extend([int(is_home), positivity, tweet, int(home_won_last)]) 
    
    f = open("savedModels/MinMaxScaler.pkl",'rb')
    minMax = pickle.load(f)
    f = open("savedModels/OneHotEncoder.pkl",'rb')
    oneHot = pickle.load(f)

    def transform(data):
        # I'm like 80% sure that this is a bug in the sklearn library.
        #oneHoted = oneHot.transform(
        #    data[::, 2].reshape(len(data), 1).astype(np.int))
        # So we are going to calculate this by ourself.
        vals = []
        for i in oneHot.categories_[0]:
            if i == int(data[0, 2]):
                vals.append(1)
            else:
                vals.append(0)
        oneHotted = np.array(vals).reshape(1, len(vals))

        minMaxed = minMax.transform(
            np.concatenate([data[::, 0:3], data[::, 3:9]], axis = 1)
        )
        return np.concatenate([minMaxed, oneHotted, data[::, 9:]], axis = 1)
    
    features_transformed = np.array(features).reshape(1, 13).astype(np.float)
    features_transformed = transform(features_transformed) # oneHot / min max scale
    
    # Load our neural network
    neural_model = keras.models.load_model("savedModels/neuralNet.h5")

    # Predict the probality
    prob_of_winning = float(neural_model.predict(features_transformed)[0][0])
    
    # Get the game data
    try:
        cur.execute("SELECT * FROM game WHERE game_id = %s", [game_id])
    
        return NerualNetOutput(Game(*cur.fetchone()), NeuralNetFeatures(*features),
                               prob_of_winning, home_team_won)
    except:
        conn.rollback()
        return "Database error", 500        

    

def model_ensemble_post(body):  # noqa: E501
    """Runs a prediction on a number of games using an ensemble approach.

    Utilizes an ensemble approach using both the reinforcement and the neural network. # noqa: E501

    :param body: Input for the ensemble model.
    :type body: dict | bytes

    :rtype: EnsembleOutput
    """
    tweets = None
    if connexion.request.is_json:
        #body = EnsembleInput.from_dict(connexion.request.get_json())  # noqa: E501
        # We need this since the from_dict is somehow losing the tweets.
        body = connexion.request.get_json()  # noqa: E501

        if "tweets" in body:
            tweets = body["tweets"]
        body = EnsembleInput.from_dict(body)

    
    betting_bot_res = model_reinforcement_post(body)
    games = betting_bot_res.games
    teams = betting_bot_res.teams
    betting_bot_on_games = betting_bot_res.bet_on_games
    
    if tweets == None:
        tweets = [""] * len(betting_bot_on_games)
        
    neural_probs = []
    for i, game in enumerate(games):
        res_home = run_neural_net(game.game_id, game.home_team_id, game.game_date,
                                  game.home_won_last, game.home_team_won, True,
                                  tweets[i * 2], game.game_date)
        res_away = run_neural_net(game.game_id, game.away_team_id, game.game_date,
                                  game.away_won_last, not game.home_team_won, False,
                                  tweets[i * 2 + 1], game.game_date)
        neural_probs.extend([res_home.chance_to_win, res_away.chance_to_win])        
    
    return EnsembleOutput(games, teams, betting_bot_on_games, neural_probs)

def get_return(ml, bet_amount): # Returns the profit + bet_amount.
  if ml < 0:
    return (100 / -ml) * bet_amount + bet_amount
  return (ml / 100) * bet_amount + bet_amount


class Agent:
    def __init__(self, state_size, window_size, data, skip, batch_size, bet_results):
        # Our model works with a sliding window. Essentially we consider
        # the past n betting observations (let's say n = 3 for example). 
        # These are our states. We consider each betting observation to be a state.
        # The stock market considered each day close to be a state. This makes sense
        # intuitively that each game we have an action to make (bet or not bet).
        self.state_size = state_size
        self.window_size = window_size
        self.half_window = window_size // 2

        self.bet_amount = 100
        self.bet_results = bet_results

        # Data is our actual data ie the moneylines.        
        self.data = data
        # Skip is the number of betting observations to advance.
        self.skip = skip
        # Action size is the number of actions we can take (bet or not bet on a game). 
        # Importantly a single game makes two betting observations.
        self.action_size = 2
        # Batch size is the amount of data in each batch
        self.batch_size = batch_size

        # Memory is used is the length of our memory queue
        self.memory = deque(maxlen = 1000)

        # Gamma is the amount of reward we give to future actions                
        self.gamma = 0.95

        # Epsilon is the value in which our model makes a completly random choice.
        # It starts off high and decays over time as our model learns.
        self.epsilon = 0.01 # Start epsilon off small since we are pretrained
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.999

        # Resets and creates a tensorflow session
        tf.reset_default_graph()
        self.sess = tf.InteractiveSession()

        # Our tensors defined used in calculating the probality of the actions
        self.X = tf.placeholder(tf.float32, [None, self.state_size])
        self.Y = tf.placeholder(tf.float32, [None, self.action_size])

        # Our logits used in calculating the probality.
        feed = tf.layers.dense(self.X, 256, activation = tf.nn.relu)
        self.logits = tf.layers.dense(feed, self.action_size)
        # Cost is how we determine how good our model is.
        self.cost = tf.reduce_mean(tf.square(self.Y - self.logits))
        # Our optimizer to help train our model
        self.optimizer = tf.train.GradientDescentOptimizer(1e-7).minimize(
            self.cost
        )

        self.sess.run(tf.global_variables_initializer())

    def restore(self):
        saver = tf.train.Saver()        
        saver.restore(self.sess, 'savedModels/my-checkpoints/my-checkpoints')

        init_op = tf.global_variables_initializer()
        self.sess.run(init_op)
        
    def act(self, state): # Choose an action to take based off our current window.
        if random.random() <= self.epsilon: # epsilon (0.5 default) of the time do a complete random action
            return random.randrange(self.action_size)
        # Otherwise get the maximum value from our model's logits.
        return np.argmax(
            self.sess.run(self.logits, feed_dict = {self.X: state})[0]
        )

    def get_state(self, t): # Get an array of amounts we would get if we bet 
        window_size = self.window_size 
        d = t - window_size 
        
        block = None
        if d >= 0:
          block = self.data[d : t]
        else: # If we are at the start of the data pad it with first values
          block = -d * [0] + self.data[0 : t]
        res = []

        return np.array([block])
    
    def run_model(self, initial_money, money_lines, bet_results):
        # Initialize buy function
        starting_money = initial_money
        bought = []
        self.data = money_lines
        self.bet_results = bet_results

        state = self.get_state(0)
        for t in range(0, len(self.data), self.skip):
            action = self.act(state)
            next_state = self.get_state(t + 1)
            # If we choose to bet and we have the money for it, and aren't betting too close to the end of our data.
            if action == 1 and starting_money >= self.bet_amount and t < (len(self.data) - self.half_window):
               starting_money -= self.bet_amount
               if self.bet_results[t]: # Won bet!
                  starting_money += get_return(self.data[t], self.bet_amount)
               bought.append(True)
            else:
              bought.append(False)
            state = next_state


        return bought, starting_money
