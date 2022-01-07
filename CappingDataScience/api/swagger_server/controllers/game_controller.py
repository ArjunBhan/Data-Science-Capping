import connexion
import six

from swagger_server.models.game import Game  # noqa: E501
from swagger_server import util
from swagger_server import cur, conn # Database 

import time

def game_from_date_to_date_get(fromDate, toDate):  # noqa: E501
    """Get all games in a date range

    Return games in a date range # noqa: E501

    :param fromDate: Starting date range for games to get
    :type fromDate: str
    :param toDate: Ending date range for games to get
    :type toDate: str

    :rtype: List[Game]
    """
    try:
        fromDate = util.deserialize_datetime(fromDate)
        toDate = util.deserialize_datetime(toDate)
    except:
        return "Error parsing date", 404

    games = []
    try:
        cur.execute("SELECT * FROM game WHERE " +
                    "game_date >= %s AND game_date <= %s", [fromDate, toDate])
        for i in cur.fetchall():
            games.append(Game(*i))
    except:
        conn.rollback()
        return "Database error", 500
    
    return games

def game_game_idget(gameID):  # noqa: E501
    """Get game by ID

    Return game associated with ID # noqa: E501

    :param gameID: ID of game to return
    :type gameID: int

    :rtype: Game
    """
    
    try:
        cur.execute("SELECT * FROM game WHERE game_id = %s", [gameID])
        game = cur.fetchone()
    
        if not game:
            print(game, "WAITING?")
            return "game not found " + str(gameID), 404
        return Game(*game)
    except:
        conn.rollback()
        return "Database error", 500



def game_get():  # noqa: E501
    """Get all games

     # noqa: E501


    :rtype: List[Game]
    """    
    games = []

    try:
        cur.execute("SELECT * FROM game ORDER BY game_id")
        for i in cur.fetchall():
            games.append(Game(*i))
    except:
        conn.rollback()
        return "Database error", 500
        

    return games
    

def game_team_team_idget(teamID):  # noqa: E501
    """Get all games from a given team

    Return games associated with a team # noqa: E501

    :param teamID: ID of the team for all games to return
    :type teamID: int

    :rtype: List[Game]
    """

    games = []
    try:
        cur.execute("SELECT * FROM game WHERE home_team_id = %s " +
                    "OR away_team_id = %s ORDER BY game_id", [teamID, teamID])
        for i in cur.fetchall():
            games.append(Game(*i))
    except:
        conn.rollback()
        return "Database error", 500

    return games
