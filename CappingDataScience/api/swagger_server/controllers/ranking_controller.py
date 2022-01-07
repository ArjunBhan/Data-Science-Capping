import connexion
import six

from swagger_server.models.ranking import Ranking  # noqa: E501
from swagger_server import util
from swagger_server import cur, conn # Database 


def ranking_from_date_to_date_get(fromDate, toDate):  # noqa: E501
    """Get all rankings for a date range

    Return all rankings in a given date range # noqa: E501

    :param fromDate: Starting date range for rankings to get
    :type fromDate: str
    :param toDate: Ending date range for rankings to get
    :type toDate: str

    :rtype: List[Ranking]
    """
    try:
        fromDate = util.deserialize_datetime(fromDate)
        toDate = util.deserialize_datetime(toDate)
    except:
        return "Error parsing date", 400
        
    rankings = []
    try:
        cur.execute("SELECT * FROM team_ranking WHERE " +
                    "standings_date >= %s AND standings_date <= %s " +
                    "ORDER BY ranking_id", [fromDate, toDate])
        for i in cur.fetchall():
            rankings.append(Ranking(*i))
    except:
        conn.rollback()
        return "Database error", 500

    return rankings


def ranking_get():  # noqa: E501
    """Get all team rankings

     # noqa: E501


    :rtype: List[Ranking]
    """
    rankings = []

    try:
        cur.execute("SELECT * FROM team_ranking ORDER BY ranking_id")
        for i in cur.fetchall():
            rankings.append(Ranking(*i))
    except:
        conn.rollback()
        return "Database error", 500

    return rankings


def ranking_ranking_idget(rankingID):  # noqa: E501
    """Get ranking by ID

    Return ranking associated with ID # noqa: E501

    :param rankingID: ID of ranking to return
    :type rankingID: int

    :rtype: Ranking
    """
    try:
        cur.execute("SELECT * FROM team_ranking WHERE ranking_id = %s", [rankingID])
        ranking = cur.fetchone()
    except:
        conn.rollback()
        return "Database error", 500
        

    if not ranking:
        return "Ranking not found", 404
    return Ranking(*ranking)


def ranking_team_team_idget(teamID):  # noqa: E501
    """Get all rankings for a team

    Return all rankings associated with a team ID # noqa: E501

    :param teamID: ID of  the team to get all rankings for
    :type teamID: int

    :rtype: List[Ranking]
    """
    rankings = []

    try:
        cur.execute("SELECT * FROM team_ranking " +
                    "WHERE team_id = %s ORDER BY ranking_id", [teamID])
        for i in cur.fetchall():
            rankings.append(Ranking(*i))
    except:
        conn.rollback()
        return "Database error", 500
            
    return rankings
