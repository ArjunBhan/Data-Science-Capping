from kafka.admin import KafkaAdminClient, NewTopic
from kafka import KafkaConsumer
import json
import psycopg2

# Connect to database
SHOULD_COMMIT = False
db_login = {
    'database': 'basketball',
    'user': 'globetrotter',
    'password': 'alpacaalpaca',
    'host': 'blaskey.dev',
    'port': 5432
}
conn = psycopg2.connect(**db_login)
cur = conn.cursor()

def insert_comma_seperated(table_name, data):
    cur.execute("INSERT INTO " + table_name + " VALUES (" +
                ("%s, " * len(data))[:-2] + ")", tuple(data))
    if SHOULD_COMMIT:
        conn.commit()

def insert_player(data):
    # Get highest auto_incr_key + 1
    cur.execute("SELECT max(auto_incr_key) FROM player")
    for i in cur.fetchall():
        data = str(i[0] + 1) + "," + data
    
    data = data.split(",")
    insert_comma_seperated("player", data)    
    print("Sucessfully inserted player message")


def insert_ranking(data):
    # Get highest auto_incr_key + 1
    cur.execute("SELECT max(ranking_id) FROM team_ranking")
    for i in cur.fetchall():
        data = str(i[0] + 1) + "," + data
        
    data = data.split(",")
    insert_comma_seperated("team_ranking", data)    
    print("Sucessfully inserted team ranking message")
        
def insert_game(data):
    data = data.split(",")
        
    insert_comma_seperated("game", data)    
    print("Sucessfully inserted game message")


def insert_game_details(data):
    data = data.split(",")
    
    insert_comma_seperated("player_game_detail", data)    
    print("Sucessfully inserted game details message")

    
if __name__ == "__main__":
    # Create topic
    try:
        admin_client = KafkaAdminClient(
            bootstrap_servers="localhost:9092", 
            client_id='test'
        )
        topic_list = []
        topic_list.append(NewTopic(name = "basketball", num_partitions=1, replication_factor=1))
        admin_client.create_topics(new_topics=topic_list, validate_only=False)
    except Exception as e:
        print(e)
    
    # Create consumer
    consumer = KafkaConsumer(
        'basketball',
        auto_offset_reset = 'earliest',
        enable_auto_commit = True,
        group_id = 'my-group-1',
        value_deserializer = lambda m: json.loads(m.decode('utf-8')),
        bootstrap_servers = "localhost:9092")

    # Listen for messages
    msg_type_to_handler = {"player": insert_player, "team_ranking": insert_ranking,
                           "game": insert_game, "player_game_details": insert_game_details}
    print("Listening for messages")
    for m in consumer:
        val = m.value
        if not val["type"] in msg_type_to_handler:
            print("Got invalid message type", val)
        else:
            try:
                msg_type_to_handler[val["type"]](val["data"])
            except Exception as e:
                conn.rollback()
                print(e)
        
