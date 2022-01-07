import connexion
import six

from swagger_server.models.team import Team  # noqa: E501
from swagger_server import util
from swagger_server import cur, conn # Database 


def team_get():  # noqa: E501
    """Get all teams

     # noqa: E501


    :rtype: List[Team]
    """
    teams = []

    try:
        cur.execute("SELECT * FROM team ORDER BY team_id")
        for i in cur.fetchall():
            teams.append(Team(*i))
    except:
        conn.rollback()
        return "Database error", 500            

    return teams


def team_team_idget(teamID):  # noqa: E501
    """Get team by ID

    Returns a single team # noqa: E501

    :param teamID: ID of team to return
    :type teamID: int

    :rtype: Team
    """

    try:
        cur.execute("SELECT * FROM team WHERE team_id = %s", [teamID])
        res = cur.fetchone()
    except:
        conn.rollback()
        return "Database error", 500        
    
    if res == None:
        return "", 404

    return Team(*res)
    
    
