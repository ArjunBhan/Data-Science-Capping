import psycopg2
import csv

db_login = {
    'database': 'basketball',
    'user': 'globetrotter',
    'password': 'alpacaalpaca',
    'host': 'blaskey.dev',
    'port': 5432
}
conn = psycopg2.connect(**db_login)
cur = conn.cursor()

def print_table(table_name, n = 25):
    cur.execute("SELECT * FROM " + table_name + " LIMIT " + str(n))

    print("Printing table ", table_name)
    for i in cur.fetchall():
        print(i)
    print()

print_table("team")


cur.execute("SELECT * from game WHERE game_id = 21200462")
print("GAME", cur.fetchone())


#print_table("player")
#print_table("game")
#print_table("team_ranking")
#print_table("player_game_detail")


#out = []
#for i in cur.fetchall():
#    print(i)#out.append(i)

#cur.execute("SELECT UNIQUE(*) FROM player ORDER BY player_id")

#out = []
#for i in cur.fetchall():
#    out.append(i)
    
#with open('updated_players.csv', 'w') as f:
#    write = csv.writer(f)
#    write.writerows(out)
