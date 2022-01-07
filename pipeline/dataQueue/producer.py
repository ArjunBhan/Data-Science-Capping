from kafka import KafkaProducer
from json import dumps

topic_name = "basketball"
producer = KafkaProducer(
   value_serializer = lambda m: dumps(m).encode("utf-8"), 
   bootstrap_servers = ["localhost:9092"])


player_example = {"type": "player", "data":
                  "999999999,Nick Blaskey,100,75,2020,Marist,22,US,2020,1,1,1610612740"}
producer.send(topic_name, value = player_example)


ranking_example = {"type": "team_ranking", "data":
                   "1610612740,2020-01-01,East,0,1,2,3,4,5"} 
producer.send(topic_name, value = ranking_example)

game_example = {"type": "game", "data":
                "392912,2020-01-01,1610612740,1610612740,2020,1,2,2,3,4," +
                "5,6,7,8,9,10,11,12,13,14,15,16"} 
producer.send(topic_name, value = game_example)

game_details_example = {"type": "player_game_details", "data":
                        "22000645,1629011,1610612752,0,0,1,2,3," +
                        "4,5,6,7,8,9,10,11,12,13,14,15,16"} 
producer.send(topic_name, value = game_details_example)

producer.flush()
