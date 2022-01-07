import tweepy
import csv
import os

def get_players_and_handles():
    with open("id_to_handle.csv", newline = "") as f:
        reader = csv.reader(f)
        return list(reader)

def connect_to_api():
    api_key = os.getenv("twitter_api_key")
    api_secret = os.getenv("twitter_api_secret")

    auth = tweepy.OAuthHandler(api_key, api_secret)
    return tweepy.API(auth)
    

def get_tweets(api, user_name, player_id):
    print("Starting user", user_name)
    
    tweets = []

    # Get the most recent tweets and the id of the oldest tweet
    new_tweets = api.user_timeline(screen_name = user_name, count=200)
    tweets.extend(new_tweets)
    oldest = tweets[-1].id - 1

    # Repeat same process until we are unable to get older tweets 
    while len(new_tweets) > 0:
        new_tweets = api.user_timeline(screen_name = user_name, count=200, max_id = oldest)        
        tweets.extend(new_tweets)
        oldest = tweets[-1].id - 1
        
    out = []
    for i in tweets:
        out.append([player_id, user_name, i.id_str, i.created_at, "\"" + i.text + "\""])

    print("Finishing user", user_name, "\n")
    
    return out


def save_tweets_to_csv(tweets):
    with open(f'tweets.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(tweets)    


if __name__ == "__main__":
    players_and_handles = get_players_and_handles()

    tweets = []
    for player in players_and_handles:    
        api = connect_to_api()
        tweets.extend(get_tweets(api, player[1], player[0]))

    save_tweets_to_csv(tweets)


