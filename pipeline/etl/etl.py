import pandas as pd
import os
import psycopg2
import numpy as np
import datetime
 
pd.options.mode.chained_assignment = None  # default='warn' ignore copy assignment warnings

SHOULD_COMMIT = True # Debug flag so we don't need to wipe database upon each run

db_login = {
    'database': 'basketball',
    'user': 'globetrotter',
    'password': 'alpacaalpaca',
    'host': '127.0.0.1', # Connecting locally for now
    'port': 5432
}
conn = psycopg2.connect(**db_login)
cur = conn.cursor()

data_dir = "./data/"

# Hold all of our data as seen in load_data()
# Just so we can pass this around easily across functions.
class BasketballData: 
    def __init__(self):
        pass

def insert_df_to_db(df, table_name, cols, needs_index):
    tuples = list(df[cols].itertuples(index = needs_index, name = None))
    cur.executemany("INSERT INTO " + table_name + " VALUES (" +
                    ("%s, " * len(tuples[0]))[:-2] + ")", tuples)
    if SHOULD_COMMIT:
        conn.commit()

    
def load_data():
    data = BasketballData()
    
    # Load all of our csv files    
    game_data_dir = data_dir + "games/"
    data.game_games = pd.read_csv(game_data_dir + "games.csv")
    data.game_details = pd.read_csv(game_data_dir + "games_details.csv")
    data.game_players = pd.read_csv(game_data_dir + "players.csv")
    data.game_rankings = pd.read_csv(game_data_dir + "ranking.csv")
    data.game_teams = pd.read_csv(game_data_dir + "teams.csv")

    #print(game_games, game_details, game_players, game_rankings, game_teams)

    players_data_dir = data_dir + "players/"
    data.players = pd.read_csv(players_data_dir + "all_seasons.csv")

    #print(players_data, players_players, players_season_stats)
    odds_data_dir = data_dir + "odds/"
    data.odds_data = []
    for odds_data_sheet in os.listdir(odds_data_dir):
       season = odds_data_sheet.split(" ")[-1].split("-")[0] # Get starting season year
       df = pd.read_excel(
           odds_data_dir + odds_data_sheet,
           engine='openpyxl')
       df["season"] = season
       data.odds_data.append(df)
    data.odds_data = pd.concat(data.odds_data)

    return data


def insert_team_data(data):
    team_abr_to_id = {}
    city_to_id = {}
    for abbr, t_id, city in zip(data.game_teams["ABBREVIATION"],
                          data.game_teams["TEAM_ID"],
                          data.game_teams["CITY"]):
        team_abr_to_id[abbr] = t_id
        city_to_id[city.replace(" ", "").lower()] = t_id


    cols = ["TEAM_ID", "MIN_YEAR", "MAX_YEAR", "ABBREVIATION", "NICKNAME",
            "YEARFOUNDED", "CITY", "ARENA", "ARENACAPACITY",
            "OWNER", "GENERALMANAGER", "HEADCOACH"]
    data.game_teams = data.game_teams.where(
        pd.notnull(data.game_teams), None) # Replace NAN with None
    
    insert_df_to_db(data.game_teams, "team", cols, False)
    
    return team_abr_to_id, city_to_id


def insert_players_data(data, team_abr_to_id):    
    clean = lambda x : x.replace("*", "").lower().strip()    
    data.players["player_name"] = data.players["player_name"].map(clean)
    data.game_players["PLAYER_NAME"] = data.game_players["PLAYER_NAME"].map(clean)

    # Convert season column from 2019-2020 to just 2019
    data.players["season"] = data.players["season"].map(lambda x: x.split("-")[0])
    
    # Find all players with same name
    name_to_id = {}
    duplicate_names = set()
    for name, pid in zip(data.game_players["PLAYER_NAME"],
                        data.game_players["PLAYER_ID"]):
        
        if name in name_to_id:
            if pid != name_to_id[name]:
                duplicate_names.add(name)

        name_to_id[name] = pid
    name_to_id = None # Free this memory

    #print(duplicate_names)
    
    out_df = pd.DataFrame(columns = list(data.players))
    processed_ids = set()
    for name, pid in zip(data.game_players["PLAYER_NAME"], data.game_players["PLAYER_ID"]):
        if pid in processed_ids:
            continue
        
        if name in duplicate_names: # If we have a duplicate player insert a null row
            out_df = out_df.append({"player_name": name, "PLAYER_ID": pid}, ignore_index = True)
            continue
        
        rows = data.players[data.players["player_name"] == name]
        if rows.empty: # If we can't find the player just insert a null row for them with their name
            out_df = out_df.append({"player_name": name, "PLAYER_ID": pid}, ignore_index = True)
        else:        
            rows["PLAYER_ID"] = pid        
            out_df = out_df.append(rows, ignore_index = True)        
        processed_ids.add(pid)

    def abr_to_id(x):
        if x in team_abr_to_id:
            return team_abr_to_id[x]
        return None
        
    out_df["TEAM_ID"] = out_df["team_abbreviation"].map(abr_to_id) # Add team ids
    out_df = out_df.replace("Undrafted", np.nan) # Replace undrafted with None
    cols = ["PLAYER_ID", "player_name", "player_height", "player_weight",
            "season", "college", "age", "country", "draft_year", "draft_round",
            "draft_number", "TEAM_ID"]
    out_df = out_df.where(
        pd.notnull(out_df), None) # Replace NAN with None

    insert_df_to_db(out_df, "player", cols, True)

        
def insert_game_data(data, city_to_id):
    # Get betting odds teams to ids
    city_to_id["newjersey"] = "1610612751" # Nets were in jersey
    city_to_id["seattle"] = "" # We will just ignore the seatle supersonics
    city_to_id["nan"] = "" # Ignore Nans too
    def city_to_id_func(x):
        x = str(x).replace(" ", "").lower()
        if x.find("la") != -1:
            if x.find("clipper") != -1:
                return 1610612746 # Clippers ID
            else:
                return 1610612747 # Lakers ID        
            
        return city_to_id[x]

    data.odds_data["Team"] = data.odds_data["Team"].map(city_to_id_func)
    data.odds_data["Date"] = data.odds_data["Date"].map(str) + "," + data.odds_data["season"]    
    
    def parse_date(x):
        if x.find("nan") != -1:
            return None
        
        x = x.split(",")
        year = int(x[1])

        days_month = x[0].split(".")[0]
        day = int(days_month[-2:])
        month = int(days_month[:-2])

        year += 1
        if month == 12: # Season for 2015 actually has games played in 2016 except for dec
            year -= 1

        
        return datetime.datetime(year, month, day)

    # Convert dates to pandas dates so we can merge
    data.odds_data["date_parsed"] = data.odds_data["Date"].map(parse_date)
    data.odds_data["date_parsed"] = pd.to_datetime(data.odds_data["date_parsed"])
    data.game_games["GAME_DATE_EST"] = pd.to_datetime(data.game_games["GAME_DATE_EST"])

    # Add betting odds for both home and visitor teams
    data.game_games = pd.merge(data.game_games,
                               data.odds_data[data.odds_data["VH"] == "H"], how = "left",
                               left_on = ["GAME_DATE_EST", "HOME_TEAM_ID"],
                               right_on = ["date_parsed", "Team"])
    data.game_games = pd.merge(data.game_games,
                               data.odds_data[data.odds_data["VH"] == "V"], how = "left",
                               left_on = ["GAME_DATE_EST", "VISITOR_TEAM_ID"],
                               right_on = ["date_parsed", "Team"])

    cols = ["GAME_ID", "GAME_DATE_EST", "HOME_TEAM_ID",
            "VISITOR_TEAM_ID", "SEASON", "HOME_TEAM_WINS",
            "1st_x", "2nd_x", "3rd_x", "4th_x", "Open_x", "Final_x", "ML_x", "2H_x",
            "1st_y", "2nd_y", "3rd_y", "4th_y", "Open_y", "Final_y", "ML_y", "2H_y"]

    data.game_games = data.game_games.replace(["PK", "pk", "NL", "nl"], np.nan)

    data.game_games["HOME_TEAM_WINS"] = data.game_games["HOME_TEAM_WINS"].astype("bool")
    data.game_games = data.game_games.where(
        pd.notnull(data.game_games), None) # Replace NAN with None
    # Drop duplicate rows
    data.game_games = data.game_games.drop_duplicates(subset = ["GAME_ID"])
    
    insert_df_to_db(data.game_games, "game", cols, False)

        
def insert_rankings_data(data):
    data.game_rankings = data.game_rankings.where(
        pd.notnull(data.game_rankings), None) # Replace NAN with None

    cols = ["TEAM_ID", "STANDINGSDATE", "CONFERENCE", "G", "W", "L",
            "HOME_W", "HOME_L", "AWAY_W", "AWAY_L"]

    data.game_rankings[["HOME_W", "HOME_L"]] = data.game_rankings[
        "HOME_RECORD"].str.split("-", expand = True)
    data.game_rankings[["AWAY_W", "AWAY_L"]] = data.game_rankings[
        "ROAD_RECORD"].str.split("-", expand = True)

    insert_df_to_db(data.game_rankings, "team_ranking", cols, True)
    

def insert_game_details(data):
    data.game_details = data.game_details.drop_duplicates(subset = ["GAME_ID", "PLAYER_ID"])
    
    data.game_details["COMMENT"] = data.game_details["COMMENT"].astype(str)
    data.game_details["MIN"] = data.game_details["MIN"].astype(str)

    data.game_details["did_not_play"] = data.game_details["COMMENT"].map(
        lambda x: x.find("DNP") != -1)
    data.game_details["did_not_dress"] = data.game_details["COMMENT"].map(
        lambda x: x.find("DND") != -1)
    data.game_details["not_with_team"] = data.game_details["COMMENT"].map(
        lambda x: x.find("NWT") != -1)
    
    def min_to_second(x):
        if x == "" or x == "nan":
            return 0
        x_split = x.split(":")
        
        if len(x_split) > 1:
            return int(x_split[0]) * 60 + int(x_split[1])
        return int(x_split[0]) 
        
    data.game_details["seconds_played"] = data.game_details["MIN"].map(min_to_second)

    data.game_details = data.game_details.where(
        pd.notnull(data.game_details), None) # Replace NAN with None
    
    cols = ["GAME_ID", "PLAYER_ID", "TEAM_ID", "START_POSITION", "did_not_play",
            "did_not_dress", "not_with_team", "seconds_played", 
            "FGM", "FGA", "FG3M", "FG3A", "FTM", "FTA", "OREB", "DREB",
            "AST", "STL", "BLK", "TO", "PF", "PTS", "PLUS_MINUS"]
    insert_df_to_db(data.game_details, "player_game_detail", cols, False)

    
if __name__ == "__main__":
    print("Starting ETL")

    data = load_data()
    print("<>Finished loading data into memory")
    
    team_abr_to_id, city_to_id = insert_team_data(data)
    print("<>Finished inserting team data into the database")
    
    insert_players_data(data, team_abr_to_id)
    print("<>Finished inserting player data into the database")
    
    insert_game_data(data, city_to_id)
    print("<>Finished inserting game data into the database")
    
    insert_rankings_data(data)
    print("<>Finished inserting ranking data into the database")
    
    insert_game_details(data)
    print("<>Finished inserting game_details into the database")

    print("Finished ETL\n")
