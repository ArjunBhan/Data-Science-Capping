\c basketball


CREATE TABLE IF NOT EXISTS team (
   team_id INT,
   min_year_in_nba_champ INT,
   max_year_in_nba_champ INT,
   abbreviation VARCHAR,
   nickname VARCHAR,
   year_founded INT,
   city VARCHAR,
   arena_name VARCHAR,
   arena_capacity VARCHAR,
   owner VARCHAR,
   manager VARCHAR,
   head_coach VARCHAR,
   PRIMARY KEY(team_id)
);

CREATE TABLE IF NOT EXISTS player (
   auto_incr_key INT,
   player_id INT,
   player_name VARCHAR,
   height INT,
   weight INT,
   season INT,
   college VARCHAR,
   age INT,
   country VARCHAR,
   draft_year INT,
   draft_round INT,
   draft_number INT,
   team_id INT,
   PRIMARY KEY(auto_incr_key),
   FOREIGN KEY(team_id) REFERENCES team(team_id)
);

CREATE TABLE IF NOT EXISTS game (
   game_id INT,
   game_date DATE,
   home_team_id INT,
   away_team_id INT,
   season INT,
   home_team_won BOOLEAN,

   home_first INT,
   home_second INT,
   home_third INT,
   home_fourth INT,
   home_open INT,
   home_close INT,
   home_ml INT,
   home_two_h INT,
   
   away_first INT,
   away_second INT,
   away_third INT,
   away_fourth INT,
   away_open INT,
   away_close INT,
   away_ml INT,
   away_two_h INT,
   PRIMARY KEY(game_id),
   FOREIGN KEY(home_team_id) REFERENCES team(team_id),
   FOREIGN KEY(home_team_id) REFERENCES team(team_id)    
);

CREATE TABLE IF NOT EXISTS team_ranking (
   ranking_id INT,
   team_id INT,
   standings_date DATE,
   conference VARCHAR,
   games_played_season INT,
   winning_games_season INT,
   losing_games_seasons INT,
   home_record_wins INT,
   home_record_loses INT,
   away_record_wins INT,
   away_record_loses INT,
   PRIMARY KEY(ranking_id),
   FOREIGN KEY(team_id) REFERENCES team(team_id)
);

CREATE TABLE IF NOT EXISTS player_game_detail (
   game_id INT,
   player_id INT,
   team_id INT,
   start_position VARCHAR,
   did_not_play BOOLEAN,
   did_not_dress BOOLEAN,
   not_with_team BOOLEAN,
   seconds_played INT,
   field_goals_made INT,
   field_goals_attempted INT,
   three_pointers_made INT,
   three_pointers_attempted INT,
   free_throws_made INT,
   free_throws_attempted INT,
   offensive_rebounds INT,
   defensive_rebounds INT,
   assists INT,
   steals INT,
   blocked_shots INT,
   turonovers INT,
   personal_fouls INT,
   points INT,
   plus_minus INT,
   
   PRIMARY KEY(game_id, player_id),
   FOREIGN KEY(team_id) REFERENCES team(team_id)
--   FOREIGN KEY(player_id) REFERENCES player(player_id) TODO look into this https://stackoverflow.com/questions/34100293/psql-error-there-is-no-unique-constraint-matching-given-keys-for-referenced-tabl
);
