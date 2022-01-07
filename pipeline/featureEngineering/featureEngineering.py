import psycopg2

db_login = {
    'database': 'basketball',
    'user': 'globetrotter',
    'password': 'alpacaalpaca',
    'host': '127.0.0.1',
    'port': 5432
}
conn = psycopg2.connect(**db_login)
cur = conn.cursor()

# Limit queries to make runtime managable. When trying to run inserts or updates
# against the blaskey.dev performance of the database is atrocious. The best way to
# solve this is to just run our scripts that insert and update locally then pg_dump
# a backup over and run the backup created on the blaskey.dev host.
LIMIT = 2147483647 

SHOULD_COMMIT = True

def create_won_last_game_feature():
    '''
    This feature will two boolean values to each game showing if 
    both the home team or away team won the previous game.
    '''

    # Select needed information to build the data
    GAME_ID, GAME_DATE, HOME_TEAM_ID, AWAY_TEAM_ID, HOME_TEAM_WON = 0, 1, 2, 3, 4
    HOME_TEAM_WON_LAST, AWAY_TEAM_WON_LAST = 5, 6
    data = []
    cur.execute("SELECT game_id, game_date, home_team_id, away_team_id, " +
                "home_team_won FROM game ORDER BY game_date LIMIT " + str(LIMIT))
    for i in cur.fetchall():
        data.append(list(i))
        data[-1].extend([False, False]) # Add two entries for home and away won last

    # For each game we will mark the next game played for both the home team
    # and away team.
    def mark_next_team(index, team_index, won_last):
        while index < len(data):
            if data[index][HOME_TEAM_ID] == team_index:
                data[index][HOME_TEAM_WON_LAST] = won_last
                return
            elif data[index][AWAY_TEAM_ID] == team_index:
                data[index][AWAY_TEAM_WON_LAST] = won_last
                return
            index += 1

    out = []
    for i, row in enumerate(data):
        mark_next_team(i + 1, row[HOME_TEAM_ID], row[HOME_TEAM_WON])
        mark_next_team(i + 1, row[AWAY_TEAM_ID], not row[HOME_TEAM_WON])
        out.append((row[HOME_TEAM_WON_LAST], row[AWAY_TEAM_WON_LAST], row[GAME_ID]))

    # Update our game table with columns for the features
    cur.execute("ALTER TABLE game " +
                "ADD COLUMN home_won_last BOOLEAN, " +
                "ADD COLUMN away_won_last BOOLEAN")

    # Update our table
    cur.executemany("UPDATE game SET home_won_last = %s, away_won_last = %s " +
                "WHERE game_id = %s", out)
    if SHOULD_COMMIT:
        conn.commit()

        
def create_season_range():
    '''
    This feature is the max(season) - min(season) for each player. 
    Technically it is not years in the NBA since off years will
    still be counted. However this should still provide a useful feature. 
    '''

    # Get all player ids.
    data = []
    cur.execute("SELECT DISTINCT player_id " +
                "FROM player LIMIT " + str(LIMIT))
    for i in cur.fetchall():
        data.append(list(i))

    # For each player id get the min and max age.
    for i, player_id in enumerate(data):
        cur.execute("SELECT min(season), max(season) FROM player " +
                    "WHERE player_id = %s", player_id)        

        min_season, max_season = cur.fetchone()
        if min_season == None:
            data[i].insert(0, None)
        else:
            data[i].insert(0, max_season - min_season)

    # Update our game table with a column for the feature
    cur.execute("ALTER TABLE player ADD COLUMN season_range int")

    # Update our table with all the values
    cur.executemany("UPDATE player SET season_range = %s " +
                    " WHERE player_id = %s", data)
    if SHOULD_COMMIT:
        conn.commit()

    
def create_ranking_improved():
    ''' 
    This feature is whether a given teams ranking improved from the last one.
    Improved is defined as having an overall higher win percentage than the previous
    ranking. In the case of equal win percentages then ranking improved will be false.
    '''

    # Get needed data.
    RANKING_ID, TEAM_ID, DATE, GAMES_PLAYED, GAMES_WON, IMPROVED = 0, 1, 2, 3, 4, 5
    data = []
    cur.execute("SELECT ranking_id, team_id, standings_date, " +
                "games_played_season, winning_games_season " +
                "FROM team_ranking ORDER BY standings_date " +
                "LIMIT " + str(LIMIT))
    for i in cur.fetchall():
        data.append(list(i))
        data[-1].append(False)

    # Calculate if the ranks improved from the previous ranking.
    def calc_win_perc(index):
        if data[index][GAMES_PLAYED] == 0:
            return 0        
        return data[index][GAMES_WON] / data[index][GAMES_PLAYED]
        
    def mark_next_as_improved(index, team_id, prev_win_perc):
        while index < len(data):
            if data[index][TEAM_ID] == team_id:
                data[index][IMPROVED] = prev_win_perc < calc_win_perc(index)
                return
            index += 1

    out = []
    for i, row in enumerate(data):
        mark_next_as_improved(i + 1, row[TEAM_ID], calc_win_perc(i))
        out.append((row[IMPROVED], row[RANKING_ID]))

    # Add a new column for our new feature.
    cur.execute("ALTER TABLE team_ranking ADD COLUMN improved_since_last BOOLEAN")

    # Update our table
    cur.executemany("UPDATE team_ranking SET improved_since_last = %s " +
                    "WHERE ranking_id = %s", out)
    if SHOULD_COMMIT:
        conn.commit()


def create_is_top_scorer():
    ''' 
    This feature is for each game and each player that played the game if 
    they were the person that scored the most amount of points. There can
    be multiple people if there is a tie.
    '''
    
    # Get all the game_ids
    data = []
    cur.execute("SELECT game_id FROM game LIMIT " + str(LIMIT))
    for i in cur.fetchall():
        data.append(i)

    # For each game find the top scoring player(s)
    PLAYER_ID, POINTS = 0, 1
    out = []    
    for game_id in data:
        # Select all the players and points scored during a game
        cur.execute("SELECT player_id, points FROM player_game_detail " +
                    "WHERE game_id = %s", game_id)

        # Find the max player(s)
        max_players = []
        max_points = -1
        for i in cur.fetchall():
            if i[POINTS] == None or i[PLAYER_ID] == None:
                continue
            
            if i[POINTS] > max_points:
                max_points = i[POINTS]
                max_players = [i[PLAYER_ID]]
            elif i[1] == max_points:
                max_players.append(i[PLAYER_ID])
        
        for max_player in max_players:
            out.append([game_id[0], max_player])

    # Add a new column for our feature.
    cur.execute("ALTER TABLE player_game_detail ADD COLUMN is_top_scorer " +
                "BOOLEAN DEFAULT FALSE")
    
    # Update our new column
    cur.executemany("UPDATE player_game_detail SET is_top_scorer = true " +
                    "WHERE game_id = %s AND player_id = %s", out)
    if SHOULD_COMMIT:
        conn.commit()

def create_players_been_on_team():
    '''
    This feature is a count of all players in our dataset that have been on a 
    given team. It could be useful for cases in which a team might have high
    churn or trying to determine how active a team is in recruiting talent.
    '''

    # Get team ids
    data = []
    cur.execute("SELECT team_id FROM team LIMIT " + str(LIMIT))
    for i in cur.fetchall():
        data.append([i[0]])

    # Count players on each team
    for i, team_id in enumerate(data):
        cur.execute("SELECT COUNT(*) FROM player WHERE team_id = %s", team_id)

        data[i].insert(0, cur.fetchone())

    # Create new column for our feature.
    cur.execute("ALTER TABLE team ADD COLUMN players_been_on_team INT")

    cur.executemany("UPDATE team SET players_been_on_team = %s " +
                    "WHERE team_id = %s", data)
    if SHOULD_COMMIT:
        conn.commit()    

        
if __name__ == "__main__":
    print("Starting feature engineering")
    
    create_won_last_game_feature()
    print("<>Finished creating won last feature")
    
    create_season_range()
    print("<>Finished creating season range feature")
    
    create_ranking_improved()
    print("<>Finished creating ranking improved feature")
    
    create_is_top_scorer()
    print("<>Finished creating is top scorer feature")
    
    create_players_been_on_team()
    print("<>Finished creating players been on team feature")

    print("Finished feature engineering\n")





    
