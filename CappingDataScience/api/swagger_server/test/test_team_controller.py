# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.team import Team  # noqa: E501
from swagger_server.test import BaseTestCase


class TestTeamController(BaseTestCase):
    """TeamController integration test stubs"""

    def test_team_get(self):
        """Test case for team_get

        Get all teams
        """
        response = self.client.open(
            '/api/team',
            method='GET',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_team_team_idget(self):
        """Test case for team_team_idget

        Get team by ID
        """
        response = self.client.open(
            '/api/team/{teamID}'.format(teamID=789),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
