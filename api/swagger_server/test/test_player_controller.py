# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.player import Player  # noqa: E501
from swagger_server.test import BaseTestCase


class TestPlayerController(BaseTestCase):
    """PlayerController integration test stubs"""

    def test_player_get(self):
        """Test case for player_get

        Get all players
        """
        response = self.client.open(
            '/api/player',
            method='GET',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_player_name_player_name_get(self):
        """Test case for player_name_player_name_get

        Get player by player name
        """
        response = self.client.open(
            '/api/player/name/{playerName}'.format(playerName='playerName_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_player_player_idget(self):
        """Test case for player_player_idget

        Get player by ID
        """
        response = self.client.open(
            '/api/player/{playerID}'.format(playerID=789),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_player_season_season_get(self):
        """Test case for player_season_season_get

        Get all players in a season
        """
        response = self.client.open(
            '/api/player/season/{season}'.format(season=789),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_player_team_team_idget(self):
        """Test case for player_team_team_idget

        Get all players on a team
        """
        response = self.client.open(
            '/api/player/team/{teamID}'.format(teamID=789),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
