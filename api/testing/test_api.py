import requests

#URL = "http://nicholasblaskey.com:8080/api/"
URL = "http://127.0.0.1:8080/api/"

def output_route(route):
    res = requests.get(route)
    print(res.status_code, res.json())
    
# Really informal testing. Just getting results and making sure they appear valid.
def test_team():
    # team_get
    output_route(URL + "team")

    # team_team_id_get
    output_route(URL + "team/1610612764")
    output_route(URL + "team/9f")
    output_route(URL + "team/9")

def test_player():
    # player_get
    output_route(URL + "player")

    # player_player_idget
    output_route(URL + "player/blah")
    output_route(URL + "player/49")
    output_route(URL + "player/1962937827")

    # player_team_team_idget
    output_route(URL + "player/team/10")
    output_route(URL + "player/team/zz")
    output_route(URL + "player/team/1610612764")

    # player_season_season_get
    output_route(URL + "player/season/skajsa")
    output_route(URL + "player/season/10")    
    output_route(URL + "player/season/2015")

    # player_name_player_name_get
    output_route(URL + "player/name/fakename")
    output_route(URL + "player/name/lebron james")
    output_route(URL + "player/name/LEBRON JAMES")
    
    # season_stats_player_id_season_get
    output_route(URL + "seasonStats/1629026/2019")
    output_route(URL + "seasonStats/1629026/2000")
    output_route(URL + "seasonStats/5/2019")
    output_route(URL + "seasonStats/nonesense/nonesense")

def test_ranking():
    # ranking_get
    output_route(URL + "ranking")

    # ranking_ranking_idget
    output_route(URL + "ranking/dsjkaasdkj")
    output_route(URL + "ranking/999999999999999")
    output_route(URL + "ranking/100")

    # ranking_team_team_idget
    output_route(URL + "ranking/team/adjskjdsasa")
    output_route(URL + "ranking/team/23")
    output_route(URL + "ranking/team/1610612764")

    # ranking_from_date_to_date_get
    output_route(URL + "ranking/edjkejn/vflkjnver")
    output_route(URL + "ranking/1-1-2008/1-1-2009")
    output_route(URL + "ranking/1-1-2009/1-1-2008")

def test_game():
    # game_get
    output_route(URL + "game")

    # game_game_idget
    output_route(URL + "game/sd")
    output_route(URL + "game/41900402")
    output_route(URL + "game/1")


    # game_team_team_idget
    output_route(URL + "game/team/dcsnjds")
    output_route(URL + "game/team/4")
    output_route(URL + "game/team/1610612764")


    # game_from_date_to_date_get
    output_route(URL + "game/edjkejn/vflkjnver")
    output_route(URL + "game/1-1-2008/1-1-2009")
    output_route(URL + "game/1-1-2009/1-1-2008")

def test_player_game_details():
    # player_game_details_get
    output_route(URL + "player_game_details")

    # player_game_details_game_game_idget
    output_route(URL + "player_game_details/game/ted")
    output_route(URL + "player_game_details/game/3")
    output_route(URL + "player_game_details/game/41900402")

    # player_game_details_player_player_idget
    output_route(URL + "player_game_details/player/t9")
    output_route(URL + "player_game_details/player/9")
    output_route(URL + "player_game_details/player/2544")

    # player_game_details_player_player_idget
    output_route(URL + "player_game_details/3/5")
    output_route(URL + "player_game_details/abc/def")
    output_route(URL + "player_game_details/41900402/2544")

def test_models():
    '''
    # model_reinforcement_post
    res = requests.post(URL + "model/reinforcement", json = {
        "starting_money": 1000,
        "starting_date": "1-1-2018",
        "num_games": 100
        })
    print(res.status_code, res.json())
    
    # model_clustering_post
    res = requests.post(URL + "model/clustering",
                        json = {"season": 2019,
                                "player_ids": [202699, 203991, 203952, 2]})
    print(res.status_code, res.json())

    
    # model_neural_network_post
    res = requests.post(URL + "model/neuralNetwork", json = {
        "date": "1-1-2018",
        "tweet": "I am going to throw this game and lose intentionally!"
    })
    print(res.status_code, res.json())
    '''
    res = requests.post(URL + "model/neuralNetwork", json = {
        "date": "1-1-2019",
        "tweet": ""
    })
    print(res.status_code, res.json())
    
    res = requests.post(URL + "model/neuralNetwork", json = {
        "date": "2-3-2016"
    })
    print(res.status_code, res.json())

    # model_reinforcement_post
    '''
    res = requests.post(URL + "model/ensemble", json = {
        "starting_money": 2000,
        "starting_date": "1-5-2013",
        "num_games": 2,
        "tweets": ["good", "bad", "Great", "amazing", "terrible", "okay"]
    })
    print(res.status_code, res.json())
    
    res = requests.post(URL + "model/ensemble", json = {
        "starting_money": 1000,
        "starting_date": "3-2-2015",
        "num_games": 2
    })
    '''
    print(res.status_code, res.json())

    
def test_meta():
    # meta_tables_get
    output_route(URL + "meta/tables")

    # meta_nulls_table_name_get
    output_route(URL + "meta/nulls/player")
    output_route(URL + "meta/nulls/players")
    output_route(URL + "meta/nulls/3")

    
    
if __name__ == "__main__":
    #test_team()
    #test_player()
    #test_ranking()
    #test_game()
    #test_player_game_details()
    test_models()
    #test_meta()
    
