import psycopg2

db_login = {
    'database': 'basketball',
    'user': 'globetrotter',
    'password': 'alpacaalpaca',
    'host': 'blaskey.dev',
    # Set ten second timeout so my aws instance doesn't crash upon
    # very large queries.
    'options': "-c statement_timeout=10000", 
    'port': 5432    
}
conn = psycopg2.connect(**db_login)
cur = conn.cursor()
