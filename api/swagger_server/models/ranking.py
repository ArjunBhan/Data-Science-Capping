# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class Ranking(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, ranking_id: int=None, team_id: int=None, standings_date: datetime=None, conference: str=None, games_played_season: int=None, winning_games_season: int=None, losing_games_seasons: int=None, home_record_wins: int=None, home_record_loses: int=None, away_record_wins: int=None, away_record_loses: int=None, improved_since_last: bool=None):  # noqa: E501
        """Ranking - a model defined in Swagger

        :param ranking_id: The ranking_id of this Ranking.  # noqa: E501
        :type ranking_id: int
        :param team_id: The team_id of this Ranking.  # noqa: E501
        :type team_id: int
        :param standings_date: The standings_date of this Ranking.  # noqa: E501
        :type standings_date: datetime
        :param conference: The conference of this Ranking.  # noqa: E501
        :type conference: str
        :param games_played_season: The games_played_season of this Ranking.  # noqa: E501
        :type games_played_season: int
        :param winning_games_season: The winning_games_season of this Ranking.  # noqa: E501
        :type winning_games_season: int
        :param losing_games_seasons: The losing_games_seasons of this Ranking.  # noqa: E501
        :type losing_games_seasons: int
        :param home_record_wins: The home_record_wins of this Ranking.  # noqa: E501
        :type home_record_wins: int
        :param home_record_loses: The home_record_loses of this Ranking.  # noqa: E501
        :type home_record_loses: int
        :param away_record_wins: The away_record_wins of this Ranking.  # noqa: E501
        :type away_record_wins: int
        :param away_record_loses: The away_record_loses of this Ranking.  # noqa: E501
        :type away_record_loses: int
        :param improved_since_last: The improved_since_last of this Ranking.  # noqa: E501
        :type improved_since_last: bool
        """
        self.swagger_types = {
            'ranking_id': int,
            'team_id': int,
            'standings_date': datetime,
            'conference': str,
            'games_played_season': int,
            'winning_games_season': int,
            'losing_games_seasons': int,
            'home_record_wins': int,
            'home_record_loses': int,
            'away_record_wins': int,
            'away_record_loses': int,
            'improved_since_last': bool
        }

        self.attribute_map = {
            'ranking_id': 'ranking_id',
            'team_id': 'team_id',
            'standings_date': 'standings_date',
            'conference': 'conference',
            'games_played_season': 'games_played_season',
            'winning_games_season': 'winning_games_season',
            'losing_games_seasons': 'losing_games_seasons',
            'home_record_wins': 'home_record_wins',
            'home_record_loses': 'home_record_loses',
            'away_record_wins': 'away_record_wins',
            'away_record_loses': 'away_record_loses',
            'improved_since_last': 'improved_since_last'
        }

        self._ranking_id = ranking_id
        self._team_id = team_id
        self._standings_date = standings_date
        self._conference = conference
        self._games_played_season = games_played_season
        self._winning_games_season = winning_games_season
        self._losing_games_seasons = losing_games_seasons
        self._home_record_wins = home_record_wins
        self._home_record_loses = home_record_loses
        self._away_record_wins = away_record_wins
        self._away_record_loses = away_record_loses
        self._improved_since_last = improved_since_last

    @classmethod
    def from_dict(cls, dikt) -> 'Ranking':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Ranking of this Ranking.  # noqa: E501
        :rtype: Ranking
        """
        return util.deserialize_model(dikt, cls)

    @property
    def ranking_id(self) -> int:
        """Gets the ranking_id of this Ranking.


        :return: The ranking_id of this Ranking.
        :rtype: int
        """
        return self._ranking_id

    @ranking_id.setter
    def ranking_id(self, ranking_id: int):
        """Sets the ranking_id of this Ranking.


        :param ranking_id: The ranking_id of this Ranking.
        :type ranking_id: int
        """

        self._ranking_id = ranking_id

    @property
    def team_id(self) -> int:
        """Gets the team_id of this Ranking.


        :return: The team_id of this Ranking.
        :rtype: int
        """
        return self._team_id

    @team_id.setter
    def team_id(self, team_id: int):
        """Sets the team_id of this Ranking.


        :param team_id: The team_id of this Ranking.
        :type team_id: int
        """

        self._team_id = team_id

    @property
    def standings_date(self) -> datetime:
        """Gets the standings_date of this Ranking.


        :return: The standings_date of this Ranking.
        :rtype: datetime
        """
        return self._standings_date

    @standings_date.setter
    def standings_date(self, standings_date: datetime):
        """Sets the standings_date of this Ranking.


        :param standings_date: The standings_date of this Ranking.
        :type standings_date: datetime
        """

        self._standings_date = standings_date

    @property
    def conference(self) -> str:
        """Gets the conference of this Ranking.


        :return: The conference of this Ranking.
        :rtype: str
        """
        return self._conference

    @conference.setter
    def conference(self, conference: str):
        """Sets the conference of this Ranking.


        :param conference: The conference of this Ranking.
        :type conference: str
        """

        self._conference = conference

    @property
    def games_played_season(self) -> int:
        """Gets the games_played_season of this Ranking.


        :return: The games_played_season of this Ranking.
        :rtype: int
        """
        return self._games_played_season

    @games_played_season.setter
    def games_played_season(self, games_played_season: int):
        """Sets the games_played_season of this Ranking.


        :param games_played_season: The games_played_season of this Ranking.
        :type games_played_season: int
        """

        self._games_played_season = games_played_season

    @property
    def winning_games_season(self) -> int:
        """Gets the winning_games_season of this Ranking.


        :return: The winning_games_season of this Ranking.
        :rtype: int
        """
        return self._winning_games_season

    @winning_games_season.setter
    def winning_games_season(self, winning_games_season: int):
        """Sets the winning_games_season of this Ranking.


        :param winning_games_season: The winning_games_season of this Ranking.
        :type winning_games_season: int
        """

        self._winning_games_season = winning_games_season

    @property
    def losing_games_seasons(self) -> int:
        """Gets the losing_games_seasons of this Ranking.


        :return: The losing_games_seasons of this Ranking.
        :rtype: int
        """
        return self._losing_games_seasons

    @losing_games_seasons.setter
    def losing_games_seasons(self, losing_games_seasons: int):
        """Sets the losing_games_seasons of this Ranking.


        :param losing_games_seasons: The losing_games_seasons of this Ranking.
        :type losing_games_seasons: int
        """

        self._losing_games_seasons = losing_games_seasons

    @property
    def home_record_wins(self) -> int:
        """Gets the home_record_wins of this Ranking.


        :return: The home_record_wins of this Ranking.
        :rtype: int
        """
        return self._home_record_wins

    @home_record_wins.setter
    def home_record_wins(self, home_record_wins: int):
        """Sets the home_record_wins of this Ranking.


        :param home_record_wins: The home_record_wins of this Ranking.
        :type home_record_wins: int
        """

        self._home_record_wins = home_record_wins

    @property
    def home_record_loses(self) -> int:
        """Gets the home_record_loses of this Ranking.


        :return: The home_record_loses of this Ranking.
        :rtype: int
        """
        return self._home_record_loses

    @home_record_loses.setter
    def home_record_loses(self, home_record_loses: int):
        """Sets the home_record_loses of this Ranking.


        :param home_record_loses: The home_record_loses of this Ranking.
        :type home_record_loses: int
        """

        self._home_record_loses = home_record_loses

    @property
    def away_record_wins(self) -> int:
        """Gets the away_record_wins of this Ranking.


        :return: The away_record_wins of this Ranking.
        :rtype: int
        """
        return self._away_record_wins

    @away_record_wins.setter
    def away_record_wins(self, away_record_wins: int):
        """Sets the away_record_wins of this Ranking.


        :param away_record_wins: The away_record_wins of this Ranking.
        :type away_record_wins: int
        """

        self._away_record_wins = away_record_wins

    @property
    def away_record_loses(self) -> int:
        """Gets the away_record_loses of this Ranking.


        :return: The away_record_loses of this Ranking.
        :rtype: int
        """
        return self._away_record_loses

    @away_record_loses.setter
    def away_record_loses(self, away_record_loses: int):
        """Sets the away_record_loses of this Ranking.


        :param away_record_loses: The away_record_loses of this Ranking.
        :type away_record_loses: int
        """

        self._away_record_loses = away_record_loses

    @property
    def improved_since_last(self) -> bool:
        """Gets the improved_since_last of this Ranking.


        :return: The improved_since_last of this Ranking.
        :rtype: bool
        """
        return self._improved_since_last

    @improved_since_last.setter
    def improved_since_last(self, improved_since_last: bool):
        """Sets the improved_since_last of this Ranking.


        :param improved_since_last: The improved_since_last of this Ranking.
        :type improved_since_last: bool
        """

        self._improved_since_last = improved_since_last
