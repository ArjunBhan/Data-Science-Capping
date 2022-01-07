import psycopg2

db_login = {
    'database': 'basketball',
    'user': 'globetrotter',
    'password': 'alpacaalpaca',
    'host': 'blaskey.dev',
    'port': 5432
}
conn = psycopg2.connect(**db_login)
cur = conn.cursor()

def count_nulls(table_name, condition = ""):
    # Get column names of table
    cur.execute("SELECT column_name FROM information_schema.columns " +
                "WHERE table_name = %s", [table_name])
    cols = ["rows with any nulls"]
    for i in cur.fetchall():
        cols.append(i[0])

    # Get number of rows in total
    where_clause = ""
    if condition:
        where_clause = " WHERE " + condition
        
    cur.execute("SELECT COUNT(*) FROM " + table_name + where_clause)
    n = cur.fetchone()[0]

    if condition:
        condition = " AND " + condition
    
    # For each column count if there is a null value
    print(table_name, "table nulls (optional condition following)", condition)
    fmt_str = "{:<25} {:<15} {:<15} {:<15}"
    print(fmt_str.format("column name", "n", "number nulls", "null percentage"))
    
    counts = []
    for col in cols:
        if col == cols[0]:
            cur.execute("SELECT COUNT(*) FROM " + table_name + " WHERE NOT (" +
                        table_name + " IS NOT NULL)" + condition)
        else:
            cur.execute("SELECT COUNT(*) FROM " + table_name + " WHERE "
                        + col + " IS NULL" + condition)
        count = cur.fetchone()[0]
        print(fmt_str.format(col, n, count, str(round(float(count) / n, 2))))
    print()

def count_nulls_player_details():
    count_nulls("player_game_detail")
    
    count_nulls("player_game_detail", " did_not_play = false AND " +
                "did_not_dress = false AND not_with_team = false")

    cur.execute("SELECT distinct seconds_played FROM player_game_detail " +
                "WHERE did_not_play = false AND " +
                "did_not_dress = false AND not_with_team = false " +
                "AND assists IS NULL")
    for i in cur.fetchall():
        print(i)

    

def count_nulls_game():
    count_nulls("game")
    
    count_nulls("game", " home_first IS NULL")
    count_nulls("game", " away_first IS NULL")
    count_nulls("game", " home_first IS NOT NULL")

    cur.execute("SELECT COUNT(*) FROM game WHERE home_first IS NULL " +
                "AND home_second IS NULL AND home_third IS NULL " +
                "AND home_fourth IS NULL")
    print("Missing rows for home odds", cur.fetchone()[0])
    
    cur.execute("SELECT COUNT(*) FROM game WHERE away_first IS NULL " +
                "AND away_second IS NULL AND away_third IS NULL " +
                "AND away_fourth IS NULL")
    print("Missing rows for home odds", cur.fetchone()[0])

    
if __name__ == "__main__":

    count_nulls("team")
    count_nulls("player")
    
    count_nulls("team_ranking")
    count_nulls_player_details()
    count_nulls_game()
