# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util
from swagger_server.models.cluster_output_item import ClusterOutputItem  # noqa: E501
from swagger_server.models.player import Player  # noqa: E501

class ClusterOutput(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, players_clustered: List[ClusterOutputItem]=None, players: List[Player]=None, missing_or_not_found: List[int]=None):  # noqa: E501
        """ClusterOutput - a model defined in Swagger

        :param players_clustered: The players_clustered of this ClusterOutput.  # noqa: E501
        :type players_clustered: List[ClusterOutputItem]
        :param players: The players of this ClusterOutput.  # noqa: E501
        :type players: List[Player]
        :param missing_or_not_found: The missing_or_not_found of this ClusterOutput.  # noqa: E501
        :type missing_or_not_found: List[int]
        """
        self.swagger_types = {
            'players_clustered': List[ClusterOutputItem],
            'players': List[Player],
            'missing_or_not_found': List[int]
        }

        self.attribute_map = {
            'players_clustered': 'players_clustered',
            'players': 'players',
            'missing_or_not_found': 'missing_or_not_found'
        }

        self._players_clustered = players_clustered
        self._players = players
        self._missing_or_not_found = missing_or_not_found

    @classmethod
    def from_dict(cls, dikt) -> 'ClusterOutput':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The ClusterOutput of this ClusterOutput.  # noqa: E501
        :rtype: ClusterOutput
        """
        return util.deserialize_model(dikt, cls)

    @property
    def players_clustered(self) -> List[ClusterOutputItem]:
        """Gets the players_clustered of this ClusterOutput.


        :return: The players_clustered of this ClusterOutput.
        :rtype: List[ClusterOutputItem]
        """
        return self._players_clustered

    @players_clustered.setter
    def players_clustered(self, players_clustered: List[ClusterOutputItem]):
        """Sets the players_clustered of this ClusterOutput.


        :param players_clustered: The players_clustered of this ClusterOutput.
        :type players_clustered: List[ClusterOutputItem]
        """

        self._players_clustered = players_clustered

    @property
    def players(self) -> List[Player]:
        """Gets the players of this ClusterOutput.


        :return: The players of this ClusterOutput.
        :rtype: List[Player]
        """
        return self._players

    @players.setter
    def players(self, players: List[Player]):
        """Sets the players of this ClusterOutput.


        :param players: The players of this ClusterOutput.
        :type players: List[Player]
        """

        self._players = players

    @property
    def missing_or_not_found(self) -> List[int]:
        """Gets the missing_or_not_found of this ClusterOutput.


        :return: The missing_or_not_found of this ClusterOutput.
        :rtype: List[int]
        """
        return self._missing_or_not_found

    @missing_or_not_found.setter
    def missing_or_not_found(self, missing_or_not_found: List[int]):
        """Sets the missing_or_not_found of this ClusterOutput.


        :param missing_or_not_found: The missing_or_not_found of this ClusterOutput.
        :type missing_or_not_found: List[int]
        """

        self._missing_or_not_found = missing_or_not_found
