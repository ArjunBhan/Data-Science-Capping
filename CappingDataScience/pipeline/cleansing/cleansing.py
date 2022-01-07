import psycopg2
from nba_api.stats.endpoints import commonplayerinfo
from dateutil import parser
import random
import time
import operator

import numpy
from psycopg2.extensions import register_adapter, AsIs
def addapt_numpy_float64(numpy_float64):
    return AsIs(numpy_float64)
def addapt_numpy_int64(numpy_int64):
    return AsIs(numpy_int64)
register_adapter(numpy.float64, addapt_numpy_float64)
register_adapter(numpy.int64, addapt_numpy_int64)

SHOULD_COMMIT = True
UPDATE_DRAFT = True

db_login = {
    'database': 'basketball',
    'user': 'globetrotter',
    'password': 'alpacaalpaca',
    'host': '127.0.0.1', # Connecting locally for now
    'port': 5432
}
conn = psycopg2.connect(**db_login)
cur = conn.cursor()

def cleanse_teams():
    # The only thing missing for teams is the arena capacity for a handful of teams.
    data = [
        [16867, 1610612740], # Pelicans, smoothie king center
        [20478, 1610612755], # 76ers, wells fargo center
        [18422, 1610612756], # Suns, talking stick resort arena
        [18846, 1610612753], # Magic, amway center
        [17732, 1610612751], # Nets, barclays center
    ]
    
    cur.executemany("UPDATE team SET arena_capacity = %s WHERE team_id = %s", data)
    if SHOULD_COMMIT:
        conn.commit()
    
    
def get_player_info(player_id):    
    player_info = commonplayerinfo.CommonPlayerInfo(player_id = player_id, timeout = 10)  
    player_info = player_info.common_player_info.get_data_frame()
    clean = lambda x: x.replace("*", "").lower().strip()

    def convert_height(x):
        if x == "":
            return None
        
        x_split = x.split("-")
        if len(x_split) == 1:
            return int(x_split[0]) * 12
        return int(x_split[0]) * 12 + int(x_split[1])

    def handle_weight(x):
        if x == "":
            return None
        return x

    def get_age(x):
        try:
            parsed_date = parser.parse(x)
            return player_info["TO_YEAR"].values[0] - parsed_date.year
        except:
            return 2021 - parsed_date.year

    def handle_undraft(x):
        try:
            return int(x)
        except:
            return None

    def handle_team(x):
        if x == 0:
            return None
        return x
        
    out = (
        clean(player_info["FIRST_NAME"].values[0] + " "
              + player_info["LAST_NAME"].values[0]),           # player_name
        convert_height(player_info["HEIGHT"].values[0]),       # height
        handle_weight(player_info["WEIGHT"].values[0]),        # weight
        player_info["TO_YEAR"].values[0],                      # season
        player_info["SCHOOL"].values[0],                       # college
        get_age(player_info["BIRTHDATE"].values[0]),           # age
        player_info["COUNTRY"].values[0],                      # country
        handle_undraft(player_info["DRAFT_YEAR"].values[0]),   # draft_year
        handle_undraft(player_info["DRAFT_ROUND"].values[0]),  # draft_round
        handle_undraft(player_info["DRAFT_NUMBER"].values[0]), # draft_number
        handle_team(player_info["TEAM_ID"].values[0]),         # team_id
        player_id,                                             # player_id
    )
    
    return out

def cleanse_players():
    # Get a list of all missing players 
    player_ids = []
    cur.execute("SELECT DISTINCT player_id FROM player WHERE age IS NULL")
    for i in cur.fetchall():
        player_ids.append(i[0])

    for i, player_id in enumerate(player_ids):
        time.sleep(2)
                
        try:
            data = get_player_info(player_id)

            print("<>Got player info from stats API (" +
                  str(i) + " / " + str(len(player_ids)) + ")", data)
            
            cur.execute("""UPDATE player SET
            player_name = %s, height = %s, weight = %s, season = %s, 
            college = %s, age = %s, country = %s, draft_year = %s, 
            draft_round = %s, draft_number = %s,
            team_id = %s WHERE player_id = %s""", data)

            if SHOULD_COMMIT:
                conn.commit()

        except Exception as e: # Error upon finding the data delete row
            print("<>Ran into error (this is expected in some casses)", e)
            
            cur.execute("DELETE FROM player WHERE player_id = " + str(player_id))
            if SHOULD_COMMIT:
                conn.commit()

    if not UPDATE_DRAFT: # updating the draft takes awhile so we are adding a flag to skip it
        return
    
    # Update draft_year, draft_round, draft_number to be non null for all rows of a player id
    cur.execute("SELECT draft_year, draft_round, draft_number, player_id " +
                "FROM player WHERE draft_year IS NOT NULL AND " +
                "draft_round IS NOT NULL AND draft_number IS NOT NULL")
    draft_data = []
    for i in cur.fetchall():
        draft_data.append(i)

    cur.executemany("UPDATE player SET draft_year = %s, draft_round = %s, " +
                    "draft_number = %s WHERE player_id = %s", draft_data)
    if SHOULD_COMMIT:
        conn.commit()

def cleanse_game_details():
    # Set our players who we have no information on to be did not play
    # Despite only checking for assists is null, assists being null => all rows null
    cur.execute("UPDATE player_game_detail SET did_not_play = true " +
                "WHERE did_not_play = false AND did_not_dress = false "
                " AND not_with_team = false AND assists IS NULL")

    # Fill in positions
    # Get rows with a missing position
    player_ids = []
    cur.execute("SELECT DISTINCT player_id FROM player_game_detail WHERE " +
                "start_position IS NULL AND did_not_play = false " +
                "AND did_not_dress = false AND not_with_team = false")
    for i in cur.fetchall():
        player_ids.append(i[0])

    for player_id in player_ids:
        # Sample 97 (since it is prime and hopefully less ties occur this way)
        # of players games and what position they played. Then fill in games
        # with missing positions their most played position. 
        cur.execute("SELECT start_position FROM player_game_detail WHERE " +
                    "start_position IS NOT NULL AND " +
                    "player_id = %s LIMIT 97", [player_id])
        
        positions = {"F": 0, "G": 0, "C": 0} # I wish python dict had a default zero value...
        for i in cur.fetchall():
            positions[i[0]] += 1

        max_pos = max(positions.items(), key = operator.itemgetter(1))
        if max_pos[1] == 0: # Skip if we have no position data
            continue

        cur.execute("UPDATE player_game_detail SET start_position = %s " +
                    "WHERE did_not_play = false AND did_not_dress = false " +
                    "AND not_with_team = false AND start_position IS NULL " +
                    "AND player_id = %s", [max_pos[0], player_id])       
        
    if SHOULD_COMMIT:
        conn.commit()
    
if __name__ == "__main__":
    print("Starting cleansing")
    
    cleanse_teams()
    print("<>Finished cleansing teams")

    print("<>Starting cleansing players (this may take awhile)")
    cleanse_players()
    print("<>Finished cleansing players")

    print("<>Starting cleaning game_details (this may take awhile)")
    cleanse_game_details()
    print("<>Finished cleansing game details")

    print("Finished cleansings\n")
