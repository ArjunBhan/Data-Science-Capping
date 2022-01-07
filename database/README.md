# Connecting to database

### Python

First install the database library with

```
pip install psycopg2-binary
```

Then you can connect by doing

```python
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

cur.execute("SELECT * FROM pg_catalog.pg_user")
for i in cur.fetchall():
    print(i)

# Make sure if changing any data you do 
# conn.commit() 
```

### R

If you use linux you need to run the command before installing the R package

```
sudo apt-get install libpq-dev
```

If you use mac you may need to run the command before installing the R package
```
brew install postgresql
```

Then in Rstudio install the package ```RPostgreSQL```

Then the following code should list out all the tables

```r
library(RPostgreSQL)
con <- dbConnect(PostgreSQL(), user= "globetrotter", password="alpacaalpaca", dbname="basketball", host="blaskey.dev", port="5432")
dbListTables(con) 
```

### Backup / restoring

To backup the database into a sql file run
```
sudo docker exec -it basketball_db pg_dump --clean -U globetrotter -d basketball > backup.sql
```

To restore this backup first copy the backup file to container
```
sudo docker cp backup.sql basketball_db:/backup.sql
```

Then run the command to restore the database
```
sudo docker exec -it basketball_db psql -U globetrotter -d basketball -f backup.sql
```