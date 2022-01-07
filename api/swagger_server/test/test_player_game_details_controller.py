# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.player_game_details import PlayerGameDetails  # noqa: E501
from swagger_server.test import BaseTestCase


class TestPlayerGameDetailsController(BaseTestCase):
    """PlayerGameDetailsController integration test stubs"""

    def test_player_game_details_game_game_idget(self):
        """Test case for player_game_details_game_game_idget

        Get all player game details for a given game
        """
        response = self.client.open(
            '/api/player_game_details/game/{gameID}'.format(gameID=789),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_player_game_details_game_id_player_idget(self):
        """Test case for player_game_details_game_id_player_idget

        Get player game details for a given player and a given game
        """
        response = self.client.open(
            '/api/player_game_details/{gameID}/{playerID}'.format(gameID=789, playerID=789),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_player_game_details_get(self):
        """Test case for player_game_details_get

        Get all player game details
        """
        response = self.client.open(
            '/api/player_game_details',
            method='GET',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_player_game_details_player_player_idget(self):
        """Test case for player_game_details_player_player_idget

        Get all player game details for a given player
        """
        response = self.client.open(
            '/api/player_game_details/player/{playerID}'.format(playerID=789),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
