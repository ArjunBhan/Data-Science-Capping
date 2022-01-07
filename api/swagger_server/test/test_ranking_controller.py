# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.ranking import Ranking  # noqa: E501
from swagger_server.test import BaseTestCase


class TestRankingController(BaseTestCase):
    """RankingController integration test stubs"""

    def test_ranking_from_date_to_date_get(self):
        """Test case for ranking_from_date_to_date_get

        Get all rankings for a date range
        """
        response = self.client.open(
            '/api/ranking/{fromDate}/{toDate}'.format(fromDate='2013-10-20T19:20:30+01:00', toDate='2013-10-20T19:20:30+01:00'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_ranking_get(self):
        """Test case for ranking_get

        Get all team rankings
        """
        response = self.client.open(
            '/api/ranking',
            method='GET',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_ranking_ranking_idget(self):
        """Test case for ranking_ranking_idget

        Get ranking by ID
        """
        response = self.client.open(
            '/api/ranking/{rankingID}'.format(rankingID=789),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_ranking_team_team_idget(self):
        """Test case for ranking_team_team_idget

        Get all rankings for a team
        """
        response = self.client.open(
            '/api/ranking/team/{teamID}'.format(teamID=789),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
