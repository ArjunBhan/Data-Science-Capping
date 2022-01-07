### Deps

```
pip3 install tweepy
```

### Authentication

You need an api key and a api secret to access the API.

You need to set these as enviroment variables by doing

```
export twitter_api_key=APIKEY; export twitter_api_secret=APISECRET
```

### downloadTweets.py

Download tweets will download all the tweets it can from a list of accounts. It expects a .csv with two rows the first being the player ID which is on our database and the second being their twitter handle. This is the id_to_handle.csv.

It will output a dataset called tweets.csv which is a raw dump of all the tweets downloaded.






