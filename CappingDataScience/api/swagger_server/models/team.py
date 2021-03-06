# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class Team(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, team_id: int=None, min_year_in_nba_champ: int=None, max_year_in_nba_champ: int=None, abbreviation: str=None, nickname: str=None, year_founded: int=None, city: str=None, arena_name: str=None, arena_capacity: int=None, owner: str=None, manager: str=None, head_coach: str=None, players_been_on_team: int=None):  # noqa: E501
        """Team - a model defined in Swagger

        :param team_id: The team_id of this Team.  # noqa: E501
        :type team_id: int
        :param min_year_in_nba_champ: The min_year_in_nba_champ of this Team.  # noqa: E501
        :type min_year_in_nba_champ: int
        :param max_year_in_nba_champ: The max_year_in_nba_champ of this Team.  # noqa: E501
        :type max_year_in_nba_champ: int
        :param abbreviation: The abbreviation of this Team.  # noqa: E501
        :type abbreviation: str
        :param nickname: The nickname of this Team.  # noqa: E501
        :type nickname: str
        :param year_founded: The year_founded of this Team.  # noqa: E501
        :type year_founded: int
        :param city: The city of this Team.  # noqa: E501
        :type city: str
        :param arena_name: The arena_name of this Team.  # noqa: E501
        :type arena_name: str
        :param arena_capacity: The arena_capacity of this Team.  # noqa: E501
        :type arena_capacity: int
        :param owner: The owner of this Team.  # noqa: E501
        :type owner: str
        :param manager: The manager of this Team.  # noqa: E501
        :type manager: str
        :param head_coach: The head_coach of this Team.  # noqa: E501
        :type head_coach: str
        :param players_been_on_team: The players_been_on_team of this Team.  # noqa: E501
        :type players_been_on_team: int
        """
        self.swagger_types = {
            'team_id': int,
            'min_year_in_nba_champ': int,
            'max_year_in_nba_champ': int,
            'abbreviation': str,
            'nickname': str,
            'year_founded': int,
            'city': str,
            'arena_name': str,
            'arena_capacity': int,
            'owner': str,
            'manager': str,
            'head_coach': str,
            'players_been_on_team': int
        }

        self.attribute_map = {
            'team_id': 'team_id',
            'min_year_in_nba_champ': 'min_year_in_nba_champ',
            'max_year_in_nba_champ': 'max_year_in_nba_champ',
            'abbreviation': 'abbreviation',
            'nickname': 'nickname',
            'year_founded': 'year_founded',
            'city': 'city',
            'arena_name': 'arena_name',
            'arena_capacity': 'arena_capacity',
            'owner': 'owner',
            'manager': 'manager',
            'head_coach': 'head_coach',
            'players_been_on_team': 'players_been_on_team'
        }

        self._team_id = team_id
        self._min_year_in_nba_champ = min_year_in_nba_champ
        self._max_year_in_nba_champ = max_year_in_nba_champ
        self._abbreviation = abbreviation
        self._nickname = nickname
        self._year_founded = year_founded
        self._city = city
        self._arena_name = arena_name
        self._arena_capacity = arena_capacity
        self._owner = owner
        self._manager = manager
        self._head_coach = head_coach
        self._players_been_on_team = players_been_on_team

    @classmethod
    def from_dict(cls, dikt) -> 'Team':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Team of this Team.  # noqa: E501
        :rtype: Team
        """
        return util.deserialize_model(dikt, cls)

    @property
    def team_id(self) -> int:
        """Gets the team_id of this Team.


        :return: The team_id of this Team.
        :rtype: int
        """
        return self._team_id

    @team_id.setter
    def team_id(self, team_id: int):
        """Sets the team_id of this Team.


        :param team_id: The team_id of this Team.
        :type team_id: int
        """

        self._team_id = team_id

    @property
    def min_year_in_nba_champ(self) -> int:
        """Gets the min_year_in_nba_champ of this Team.


        :return: The min_year_in_nba_champ of this Team.
        :rtype: int
        """
        return self._min_year_in_nba_champ

    @min_year_in_nba_champ.setter
    def min_year_in_nba_champ(self, min_year_in_nba_champ: int):
        """Sets the min_year_in_nba_champ of this Team.


        :param min_year_in_nba_champ: The min_year_in_nba_champ of this Team.
        :type min_year_in_nba_champ: int
        """

        self._min_year_in_nba_champ = min_year_in_nba_champ

    @property
    def max_year_in_nba_champ(self) -> int:
        """Gets the max_year_in_nba_champ of this Team.


        :return: The max_year_in_nba_champ of this Team.
        :rtype: int
        """
        return self._max_year_in_nba_champ

    @max_year_in_nba_champ.setter
    def max_year_in_nba_champ(self, max_year_in_nba_champ: int):
        """Sets the max_year_in_nba_champ of this Team.


        :param max_year_in_nba_champ: The max_year_in_nba_champ of this Team.
        :type max_year_in_nba_champ: int
        """

        self._max_year_in_nba_champ = max_year_in_nba_champ

    @property
    def abbreviation(self) -> str:
        """Gets the abbreviation of this Team.


        :return: The abbreviation of this Team.
        :rtype: str
        """
        return self._abbreviation

    @abbreviation.setter
    def abbreviation(self, abbreviation: str):
        """Sets the abbreviation of this Team.


        :param abbreviation: The abbreviation of this Team.
        :type abbreviation: str
        """

        self._abbreviation = abbreviation

    @property
    def nickname(self) -> str:
        """Gets the nickname of this Team.


        :return: The nickname of this Team.
        :rtype: str
        """
        return self._nickname

    @nickname.setter
    def nickname(self, nickname: str):
        """Sets the nickname of this Team.


        :param nickname: The nickname of this Team.
        :type nickname: str
        """

        self._nickname = nickname

    @property
    def year_founded(self) -> int:
        """Gets the year_founded of this Team.


        :return: The year_founded of this Team.
        :rtype: int
        """
        return self._year_founded

    @year_founded.setter
    def year_founded(self, year_founded: int):
        """Sets the year_founded of this Team.


        :param year_founded: The year_founded of this Team.
        :type year_founded: int
        """

        self._year_founded = year_founded

    @property
    def city(self) -> str:
        """Gets the city of this Team.


        :return: The city of this Team.
        :rtype: str
        """
        return self._city

    @city.setter
    def city(self, city: str):
        """Sets the city of this Team.


        :param city: The city of this Team.
        :type city: str
        """

        self._city = city

    @property
    def arena_name(self) -> str:
        """Gets the arena_name of this Team.


        :return: The arena_name of this Team.
        :rtype: str
        """
        return self._arena_name

    @arena_name.setter
    def arena_name(self, arena_name: str):
        """Sets the arena_name of this Team.


        :param arena_name: The arena_name of this Team.
        :type arena_name: str
        """

        self._arena_name = arena_name

    @property
    def arena_capacity(self) -> int:
        """Gets the arena_capacity of this Team.


        :return: The arena_capacity of this Team.
        :rtype: int
        """
        return self._arena_capacity

    @arena_capacity.setter
    def arena_capacity(self, arena_capacity: int):
        """Sets the arena_capacity of this Team.


        :param arena_capacity: The arena_capacity of this Team.
        :type arena_capacity: int
        """

        self._arena_capacity = arena_capacity

    @property
    def owner(self) -> str:
        """Gets the owner of this Team.


        :return: The owner of this Team.
        :rtype: str
        """
        return self._owner

    @owner.setter
    def owner(self, owner: str):
        """Sets the owner of this Team.


        :param owner: The owner of this Team.
        :type owner: str
        """

        self._owner = owner

    @property
    def manager(self) -> str:
        """Gets the manager of this Team.


        :return: The manager of this Team.
        :rtype: str
        """
        return self._manager

    @manager.setter
    def manager(self, manager: str):
        """Sets the manager of this Team.


        :param manager: The manager of this Team.
        :type manager: str
        """

        self._manager = manager

    @property
    def head_coach(self) -> str:
        """Gets the head_coach of this Team.


        :return: The head_coach of this Team.
        :rtype: str
        """
        return self._head_coach

    @head_coach.setter
    def head_coach(self, head_coach: str):
        """Sets the head_coach of this Team.


        :param head_coach: The head_coach of this Team.
        :type head_coach: str
        """

        self._head_coach = head_coach

    @property
    def players_been_on_team(self) -> int:
        """Gets the players_been_on_team of this Team.


        :return: The players_been_on_team of this Team.
        :rtype: int
        """
        return self._players_been_on_team

    @players_been_on_team.setter
    def players_been_on_team(self, players_been_on_team: int):
        """Sets the players_been_on_team of this Team.


        :param players_been_on_team: The players_been_on_team of this Team.
        :type players_been_on_team: int
        """

        self._players_been_on_team = players_been_on_team
