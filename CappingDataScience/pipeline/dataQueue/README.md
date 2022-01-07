### Data queue

Our data queue utilizes Kafka to send messages to a broker in which one or many consumers can process the data and insert it into the database.

### Testing queue

To test the queue first start kafka
```
sudo docker-compose down && sudo docker-compose up --build
```

Run the consumer
```
python3 consumer.py
```

Run the producer
```
python3 producer.py
```

and you see messages indicating that the messages were inserted into the database. It may not save these inserts for debug purposes if ```SHOULD_COMMIT``` is set to false in consumer.

### Running Kafka

Kafka needs to be running for our queue to work. To start a kafka instance run

```
sudo docker-compose down && sudo docker-compose up --build
```

### Deps

```
pip3 install kafka kafka-python
```

### consumer.py

To run just do
```
python consumer.py
```

The consumer is responsible for getting messages sent to kafka and inserting them into the database. It will run continually and read and process messages when it is able to.

### producer.py

To run just do
```
python producer.py
```

Producer is a more example of how the queue would actually be set up. It demonstrates sending messages of the different possibilities to the consumer.

In a real production system there would likely be multiple forms of producers scraping sources of data all sending updates to Kafka when new data is possible.  

### message format

The messages will be sent in form of JSON. The JSON has two fields

#### type

```type``` indicates what kind of data is being sent. It can take the values

| type value          |
|---------------------|
| player              |
| team_ranking        |
| game                |
| player_game_details |

These correspond to tables in our database. Team is missing since a team being added to the NBA is rather rare and something that would likely not be worth setting up a queue for. 

#### data

data is a comma seperated list of all the data that each type expects.

The formats each type expects are below.

| type value          | data format                                                                                                                                                                                                                                                                                                           |
|---------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| player              | player_id,player_name,height,weight,season,college,age,country,draft_year,draft_round,draft_number,team_id                                                                                                                                                                                                            |
| team_ranking        | team_id,standings_date,conference,games_played_season,winning_games_season,home_record_wins,home_record_loses,away_record_wins,away_record_loses                                                                                                                                                                      |
| game                | game_id,game_date,home_team_id,away_team_id,season,home_team_won,home_first,home_second,home_third,home_fourth,home_open,home_close,home_ml,home_two_h,away_first,away_second,away_third,away_fourth,away_open,away_close,away_ml,away_two_h                                                                          |
| player_game_details | game_id,player_id,team_id,did_not_play,did_not_dress,minutes_played,field_goals_made,field_goals_attempted,three_pointers_made,three_pointers_attempted,free_throws_made,free_throws_attempted,offensive_rebounds,defensive_rebounds,assists,steals,blocked_shots,turnovers,personal_fouls,points,plus_minus |