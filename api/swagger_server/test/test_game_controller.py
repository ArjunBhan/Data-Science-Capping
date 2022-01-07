# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.game import Game  # noqa: E501
from swagger_server.test import BaseTestCase


class TestGameController(BaseTestCase):
    """GameController integration test stubs"""

    def test_game_from_date_to_date_get(self):
        """Test case for game_from_date_to_date_get

        Get all games in a date range
        """
        response = self.client.open(
            '/api/game/{fromDate}/{toDate}'.format(fromDate='2013-10-20T19:20:30+01:00', toDate='2013-10-20T19:20:30+01:00'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_game_game_idget(self):
        """Test case for game_game_idget

        Get game by ID
        """
        response = self.client.open(
            '/api/game/{gameID}'.format(gameID=789),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_game_get(self):
        """Test case for game_get

        Get all games
        """
        response = self.client.open(
            '/api/game',
            method='GET',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_game_team_team_idget(self):
        """Test case for game_team_team_idget

        Get all games from a given team
        """
        response = self.client.open(
            '/api/game/team/{teamID}'.format(teamID=789),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
