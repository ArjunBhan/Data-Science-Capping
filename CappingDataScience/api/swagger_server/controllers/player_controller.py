import connexion
import six

from swagger_server.models.player import Player  # noqa: E501
from swagger_server import util
from swagger_server import cur, conn # Database 

from swagger_server.models.season_statistics import SeasonStatistics  # noqa: E501


def player_get():  # noqa: E501
    """Get all players

     # noqa: E501


    :rtype: List[Player]
    """
    players = []

    try:
        cur.execute("SELECT * FROM player ORDER BY player_id")
        for i in cur.fetchall():
            players.append(Player(*i))
    except:
        conn.rollback()
        return "Database error", 500        
    
    return players


def player_name_player_name_get(playerName):  # noqa: E501
    """Get player by player name

    Returns all rows matching the player name # noqa: E501

    :param playerName: Name of the player to return (first last)
    :type playerName: str

    :rtype: List[Player]
    """
    playerName = playerName.replace("*", "").lower().strip()
    
    players = []

    try:
        cur.execute("SELECT * FROM player WHERE player_name = %s", [playerName])
        for i in cur.fetchall():
            players.append(Player(*i))
    except:
        conn.rollback()
        return "Database error", 500

    if not players:
        return "No player found for name", 404        
    return players

                                                              

def player_player_idget(playerID):  # noqa: E501
    """Get player by ID

    Returns all rows associated with playerID # noqa: E501

    :param playerID: ID of player to return
    :type playerID: int

    :rtype: List[Player]
    """
    players = []

    try:
        cur.execute("SELECT * FROM player WHERE player_id = %s", [playerID])
        for i in cur.fetchall():
            players.append(Player(*i))
    except:
        conn.rollback()
        return "Database error", 500

    if not players:
        return "No players found", 404
    return players


def player_season_season_get(season):  # noqa: E501
    """Get all players in a season

    Returns all players in a season # noqa: E501

    :param season: year of the season of all players to return
    :type season: int

    :rtype: List[Player]
    """
    players = []

    try:
        cur.execute("SELECT * FROM player WHERE season = %s", [season])
        for i in cur.fetchall():
            players.append(Player(*i))
    except:
        conn.rollback()
        return "Database error", 500

    return players


def player_team_team_idget(teamID):  # noqa: E501
    """Get all players on a team

    Returns all players on the provided team # noqa: E501

    :param teamID: ID of the team which to get all players on
    :type teamID: int

    :rtype: List[Player]
    """
    players = []

    try:
        cur.execute("SELECT * FROM player WHERE team_id = %s", [teamID])
        for i in cur.fetchall():
            players.append(Player(*i))
    except:
        conn.rollback()
        return "Database error", 500

    return players
    
def season_stats_player_id_season_get(playerID, season):  # noqa: E501
    """Get season statistics of a player and season

    Returns statistics of a player for a given season # noqa: E501

    :param playerID: ID of player to return statistics for
    :type playerID: int
    :param season: season (year) to consider statistics for
    :type season: int

    :rtype: List[SeasonStatistics]
    """

    # Get number of games played
    try:
        cur.execute("SELECT COUNT(*) " +
                    "FROM player_game_detail " +
                    "INNER JOIN game ON player_game_detail.game_id = game.game_id " + 
                    "WHERE player_id = %s AND season = %s AND " +
                    "did_not_play = false AND did_not_dress = false AND " +
                    "not_with_team = false", [playerID, season])
        res = [cur.fetchone()[0]]
    
        # Get rest of season statistics
        cur.execute("SELECT AVG(seconds_played), AVG(field_goals_made), " +
                    "AVG(field_goals_attempted), AVG(three_pointers_made), " +
                    "AVG(three_pointers_attempted), AVG(free_throws_made), " +
                    "AVG(free_throws_attempted), AVG(offensive_rebounds), " +
                    "AVG(defensive_rebounds), AVG(assists), AVG(steals), " +
                    "AVG(blocked_shots), AVG(turonovers), AVG(personal_fouls), " +
                    "AVG(points), AVG(plus_minus) FROM player_game_detail " +
                    "INNER JOIN game ON player_game_detail.game_id = game.game_id " + 
                    "WHERE player_id = %s AND season = %s", [playerID, season])    
        res.extend(cur.fetchone())
    except:
        conn.rollback()
        return "Database error", 500


    return SeasonStatistics(*res)
