### Deps

```
pip3 install psycopg2-binary nba_api
```

### analysis.py

analysis.py is a script which prints out information about the tables and how many values in each table are null.

This is not necessarly to run but is meant as a diagnostic tool to just guage how "cleansed" the database is. It is also important to note that some nulls are not necessarly bad and some bad nulls are necessary. A perfectly cleansed database isn't possible for us with the datasets and time constractions we have. More information on this in the specific tables and processes taken.

```
python3 analysis.py
```

### clease.py

cleanse.py actually performs all the action needed to clenase the database. These actions are described in detail in the sections for each table.

### player

The player table has a large amount of nulls in the columns. There are two kinds of missing data in the player table.

The first is completly missing people. These are people in which we have the player_id for but nothing more about them. The second is people we have information about but are missing information about them.

To cleanse the play database we utilized the official NBA statistics websites API. We went through for both missing players and players with missing information and called the NBA API to fill in information about them.

A few players had no record of their id (around 30) on the NBA statistics website. These players were dropped and are likely typos in the player_id value in the original dataset.

The vast majority of players with missing information we were able to find. However the dataset from even the NBA official statistics website is not complete. Around 300 or so players did not have statistics about their height and weight on the NBA API. Other fields were missing randomly too. If the NBA official source does not have the data we will just need to accept this and take care in the future when using the data in models to handle this appropiately.

These players who were completly missing are however missing historical data. We won't have information about all the teams they were on nor how their weight changed. This is important to keep note of in future analysis.

### team

The team table was relatively complete. The only issue was around 5 teams had missing arena capacities (or in one case an arena capacity of 0). These were looked up manually and are aentered in the cleanse script.

### team_ranking

The team ranking table was 100% complete so no action was needing for this table.

### game

The game table is 100% complete exluding the betting odds.

The betting odds has two types of nulls. The first is completly missing rows. These are games we could not find in our odds database. There were 13,277 games with no home betting odds and 13,267 with no away betting odds. This is a lot and something that needs to be taken care of. The best option we feel for this stage is to just leave these values missing. The ideal situation would be to find another dataset to fill in these values however we could not find a better dataset to utilize. We are however going to take note of these missing values and consider the best action to take handling them for the use case of the dataset going forward. Likely this dataset will be using in a NBA betting bot, and the bot could either just not bet on these games or these games could have these values inferred from previous games.

The second type of null is within row nulls. Every single of these within row nulls comes from the dataset used having values marked as pk. pk is a [betting term](https://www.bigal.com/articles/what-does-pk-mean-in-betting) meaning that the oddsmaker assumes the teams are equal strength. We are going to leave these rows as null and note in the future the meaning of these and handle these depending on the use case. 


### player_game_detail

The player game detail has two types of nulls. One are acceptable nulls. If a player did not dress or did not play then we expect all the values in the table to be null. 

Through cleansing we also discovered a bug within the ETL in which we did not consider NWT meaning not with team. We have added this to the database to account for this.

From this we found 402 rows which had row values for players who did not have a did_not_player, did_not_dress, not_with_team marked. However all these rows had a seconds_played value of 0. We marked all of these values as did_not_play.

This leads us to unacceptable nulls. These are where we expect a value (the player played a game but missing an entry). Every column besides start_position and plus_minus is 100% complete. 

To handle start_position we replaced the value with the mode start_position (an average of a sample to cut down on the script run time). There were still some players with no start_positions recorded ever. These are 3% of game_details that played. These were left null and up to future use of the data to decide how to handle this.

To handle the missing 5% of rows with a missing plus_minus statistics we choose to leave these values as null. Initially the plan was to calculate the plus_minus statistics indivudally however this is too complicated. This will be left for future use of the data to decide how to handle this.