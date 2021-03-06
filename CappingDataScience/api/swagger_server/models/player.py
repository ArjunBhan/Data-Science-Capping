# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class Player(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, player_auto_key: int=None, player_id: int=None, player_name: str=None, height: int=None, weight: int=None, season: int=None, college: str=None, age: int=None, country: str=None, draft_year: int=None, draft_round: int=None, draft_number: int=None, team_id: int=None, season_range: int=None):  # noqa: E501
        """Player - a model defined in Swagger

        :param player_auto_key: The player_auto_key of this Player.  # noqa: E501
        :type player_auto_key: int
        :param player_id: The player_id of this Player.  # noqa: E501
        :type player_id: int
        :param player_name: The player_name of this Player.  # noqa: E501
        :type player_name: str
        :param height: The height of this Player.  # noqa: E501
        :type height: int
        :param weight: The weight of this Player.  # noqa: E501
        :type weight: int
        :param season: The season of this Player.  # noqa: E501
        :type season: int
        :param college: The college of this Player.  # noqa: E501
        :type college: str
        :param age: The age of this Player.  # noqa: E501
        :type age: int
        :param country: The country of this Player.  # noqa: E501
        :type country: str
        :param draft_year: The draft_year of this Player.  # noqa: E501
        :type draft_year: int
        :param draft_round: The draft_round of this Player.  # noqa: E501
        :type draft_round: int
        :param draft_number: The draft_number of this Player.  # noqa: E501
        :type draft_number: int
        :param team_id: The team_id of this Player.  # noqa: E501
        :type team_id: int
        :param season_range: The season_range of this Player.  # noqa: E501
        :type season_range: int
        """
        self.swagger_types = {
            'player_auto_key': int,
            'player_id': int,
            'player_name': str,
            'height': int,
            'weight': int,
            'season': int,
            'college': str,
            'age': int,
            'country': str,
            'draft_year': int,
            'draft_round': int,
            'draft_number': int,
            'team_id': int,
            'season_range': int
        }

        self.attribute_map = {
            'player_auto_key': 'player_auto_key',
            'player_id': 'player_id',
            'player_name': 'player_name',
            'height': 'height',
            'weight': 'weight',
            'season': 'season',
            'college': 'college',
            'age': 'age',
            'country': 'country',
            'draft_year': 'draft_year',
            'draft_round': 'draft_round',
            'draft_number': 'draft_number',
            'team_id': 'team_id',
            'season_range': 'season_range'
        }

        self._player_auto_key = player_auto_key
        self._player_id = player_id
        self._player_name = player_name
        self._height = height
        self._weight = weight
        self._season = season
        self._college = college
        self._age = age
        self._country = country
        self._draft_year = draft_year
        self._draft_round = draft_round
        self._draft_number = draft_number
        self._team_id = team_id
        self._season_range = season_range

    @classmethod
    def from_dict(cls, dikt) -> 'Player':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Player of this Player.  # noqa: E501
        :rtype: Player
        """
        return util.deserialize_model(dikt, cls)

    @property
    def player_auto_key(self) -> int:
        """Gets the player_auto_key of this Player.


        :return: The player_auto_key of this Player.
        :rtype: int
        """
        return self._player_auto_key

    @player_auto_key.setter
    def player_auto_key(self, player_auto_key: int):
        """Sets the player_auto_key of this Player.


        :param player_auto_key: The player_auto_key of this Player.
        :type player_auto_key: int
        """

        self._player_auto_key = player_auto_key

    @property
    def player_id(self) -> int:
        """Gets the player_id of this Player.


        :return: The player_id of this Player.
        :rtype: int
        """
        return self._player_id

    @player_id.setter
    def player_id(self, player_id: int):
        """Sets the player_id of this Player.


        :param player_id: The player_id of this Player.
        :type player_id: int
        """

        self._player_id = player_id

    @property
    def player_name(self) -> str:
        """Gets the player_name of this Player.


        :return: The player_name of this Player.
        :rtype: str
        """
        return self._player_name

    @player_name.setter
    def player_name(self, player_name: str):
        """Sets the player_name of this Player.


        :param player_name: The player_name of this Player.
        :type player_name: str
        """

        self._player_name = player_name

    @property
    def height(self) -> int:
        """Gets the height of this Player.


        :return: The height of this Player.
        :rtype: int
        """
        return self._height

    @height.setter
    def height(self, height: int):
        """Sets the height of this Player.


        :param height: The height of this Player.
        :type height: int
        """

        self._height = height

    @property
    def weight(self) -> int:
        """Gets the weight of this Player.


        :return: The weight of this Player.
        :rtype: int
        """
        return self._weight

    @weight.setter
    def weight(self, weight: int):
        """Sets the weight of this Player.


        :param weight: The weight of this Player.
        :type weight: int
        """

        self._weight = weight

    @property
    def season(self) -> int:
        """Gets the season of this Player.


        :return: The season of this Player.
        :rtype: int
        """
        return self._season

    @season.setter
    def season(self, season: int):
        """Sets the season of this Player.


        :param season: The season of this Player.
        :type season: int
        """

        self._season = season

    @property
    def college(self) -> str:
        """Gets the college of this Player.


        :return: The college of this Player.
        :rtype: str
        """
        return self._college

    @college.setter
    def college(self, college: str):
        """Sets the college of this Player.


        :param college: The college of this Player.
        :type college: str
        """

        self._college = college

    @property
    def age(self) -> int:
        """Gets the age of this Player.


        :return: The age of this Player.
        :rtype: int
        """
        return self._age

    @age.setter
    def age(self, age: int):
        """Sets the age of this Player.


        :param age: The age of this Player.
        :type age: int
        """

        self._age = age

    @property
    def country(self) -> str:
        """Gets the country of this Player.


        :return: The country of this Player.
        :rtype: str
        """
        return self._country

    @country.setter
    def country(self, country: str):
        """Sets the country of this Player.


        :param country: The country of this Player.
        :type country: str
        """

        self._country = country

    @property
    def draft_year(self) -> int:
        """Gets the draft_year of this Player.


        :return: The draft_year of this Player.
        :rtype: int
        """
        return self._draft_year

    @draft_year.setter
    def draft_year(self, draft_year: int):
        """Sets the draft_year of this Player.


        :param draft_year: The draft_year of this Player.
        :type draft_year: int
        """

        self._draft_year = draft_year

    @property
    def draft_round(self) -> int:
        """Gets the draft_round of this Player.


        :return: The draft_round of this Player.
        :rtype: int
        """
        return self._draft_round

    @draft_round.setter
    def draft_round(self, draft_round: int):
        """Sets the draft_round of this Player.


        :param draft_round: The draft_round of this Player.
        :type draft_round: int
        """

        self._draft_round = draft_round

    @property
    def draft_number(self) -> int:
        """Gets the draft_number of this Player.


        :return: The draft_number of this Player.
        :rtype: int
        """
        return self._draft_number

    @draft_number.setter
    def draft_number(self, draft_number: int):
        """Sets the draft_number of this Player.


        :param draft_number: The draft_number of this Player.
        :type draft_number: int
        """

        self._draft_number = draft_number

    @property
    def team_id(self) -> int:
        """Gets the team_id of this Player.


        :return: The team_id of this Player.
        :rtype: int
        """
        return self._team_id

    @team_id.setter
    def team_id(self, team_id: int):
        """Sets the team_id of this Player.


        :param team_id: The team_id of this Player.
        :type team_id: int
        """

        self._team_id = team_id

    @property
    def season_range(self) -> int:
        """Gets the season_range of this Player.


        :return: The season_range of this Player.
        :rtype: int
        """
        return self._season_range

    @season_range.setter
    def season_range(self, season_range: int):
        """Sets the season_range of this Player.


        :param season_range: The season_range of this Player.
        :type season_range: int
        """

        self._season_range = season_range
