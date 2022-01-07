import connexion
import six

from swagger_server.models.player_game_details import PlayerGameDetails  # noqa: E501
from swagger_server import util
from swagger_server import cur, conn # Database 


def player_game_details_game_game_idget(gameID):  # noqa: E501
    """Get all player game details for a given game

    Return all player&#39;s game details for a given game # noqa: E501

    :param gameID: ID of the game for which to return all details for
    :type gameID: int

    :rtype: List[PlayerGameDetails]
    """
    details = []
    try:
        cur.execute("SELECT * FROM player_game_detail WHERE game_id = %s", [gameID])
        for i in cur.fetchall():
            details.append(PlayerGameDetails(*i))
    except:
        conn.rollback()
        return "Database error", 500

    return details
    


def player_game_details_game_id_player_idget(gameID, playerID):  # noqa: E501
    """Get player game details for a given player and a given game

    Return player game details for a given game and a given player # noqa: E501

    :param gameID: ID of the game
    :type gameID: int
    :param playerID: ID of the player
    :type playerID: int

    :rtype: PlayerGameDetails
    """

    try:
        cur.execute("SELECT * FROM player_game_detail WHERE " +
                    "game_id = %s AND player_id = %s", [gameID, playerID])
        detail = cur.fetchone()
    except:
        conn.rollback()
        return "Database error", 500

    if not detail:
        return "Game detail not found", 404
    return PlayerGameDetails(*detail)


def player_game_details_get():  # noqa: E501
    """Get all player game details

     # noqa: E501


    :rtype: List[PlayerGameDetails]
    """
    details = []
    try:
        cur.execute("SELECT * FROM player_game_detail ORDER BY game_id")
        for i in cur.fetchall():
            details.append(PlayerGameDetails(*i))
    except:
        conn.rollback()
        return "Database error", 500

    return details
    


def player_game_details_player_player_idget(playerID):  # noqa: E501
    """Get all player game details for a given player

    Return all player&#39;s game details for a given player # noqa: E501

    :param playerID: ID of the player for which to return all details for
    :type playerID: int

    :rtype: List[PlayerGameDetails]
    """
    details = []

    try:
        cur.execute("SELECT * FROM player_game_detail WHERE player_id = %s", [playerID])
        for i in cur.fetchall():
            details.append(PlayerGameDetails(*i))
    except:
        conn.rollback()
        return "Database error", 500

    return details
