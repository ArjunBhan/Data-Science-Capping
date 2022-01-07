# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util

from swagger_server.models.game import Game  # noqa: E501
from swagger_server.models.team import Team  # noqa: E501

class BettingBotOutput(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, games: List[Game]=None, teams: List[Team]=None, bet_on_games: List[bool]=None, ending_money: int=None):  # noqa: E501
        """BettingBotOutput - a model defined in Swagger

        :param games: The games of this BettingBotOutput.  # noqa: E501
        :type games: List[Game]
        :param teams: The teams of this BettingBotOutput.  # noqa: E501
        :type teams: List[Team]
        :param bet_on_games: The bet_on_games of this BettingBotOutput.  # noqa: E501
        :type bet_on_games: List[bool]
        :param ending_money: The ending_money of this BettingBotOutput.  # noqa: E501
        :type ending_money: int
        """
        self.swagger_types = {
            'games': List[Game],
            'teams': List[Team],
            'bet_on_games': List[bool],
            'ending_money': int
        }

        self.attribute_map = {
            'games': 'games',
            'teams': 'teams',
            'bet_on_games': 'bet_on_games',
            'ending_money': 'ending_money'
        }

        self._games = games
        self._teams = teams
        self._bet_on_games = bet_on_games
        self._ending_money = ending_money

    @classmethod
    def from_dict(cls, dikt) -> 'BettingBotOutput':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The BettingBotOutput of this BettingBotOutput.  # noqa: E501
        :rtype: BettingBotOutput
        """
        return util.deserialize_model(dikt, cls)

    @property
    def games(self) -> List[Game]:
        """Gets the games of this BettingBotOutput.


        :return: The games of this BettingBotOutput.
        :rtype: List[Game]
        """
        return self._games

    @games.setter
    def games(self, games: List[Game]):
        """Sets the games of this BettingBotOutput.


        :param games: The games of this BettingBotOutput.
        :type games: List[Game]
        """

        self._games = games

    @property
    def teams(self) -> List[Team]:
        """Gets the teams of this BettingBotOutput.


        :return: The teams of this BettingBotOutput.
        :rtype: List[Team]
        """
        return self._teams

    @teams.setter
    def teams(self, teams: List[Team]):
        """Sets the teams of this BettingBotOutput.


        :param teams: The teams of this BettingBotOutput.
        :type teams: List[Team]
        """

        self._teams = teams

    @property
    def bet_on_games(self) -> List[bool]:
        """Gets the bet_on_games of this BettingBotOutput.


        :return: The bet_on_games of this BettingBotOutput.
        :rtype: List[bool]
        """
        return self._bet_on_games

    @bet_on_games.setter
    def bet_on_games(self, bet_on_games: List[bool]):
        """Sets the bet_on_games of this BettingBotOutput.


        :param bet_on_games: The bet_on_games of this BettingBotOutput.
        :type bet_on_games: List[bool]
        """

        self._bet_on_games = bet_on_games

    @property
    def ending_money(self) -> int:
        """Gets the ending_money of this BettingBotOutput.


        :return: The ending_money of this BettingBotOutput.
        :rtype: int
        """
        return self._ending_money

    @ending_money.setter
    def ending_money(self, ending_money: int):
        """Sets the ending_money of this BettingBotOutput.


        :param ending_money: The ending_money of this BettingBotOutput.
        :type ending_money: int
        """

        self._ending_money = ending_money
