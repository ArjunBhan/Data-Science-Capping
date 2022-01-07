# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.betting_bot_input import BettingBotInput  # noqa: E501
from swagger_server.models.betting_bot_output import BettingBotOutput  # noqa: E501
from swagger_server.models.todoin import TODOIN  # noqa: E501
from swagger_server.models.todoout import TODOOUT  # noqa: E501
from swagger_server.test import BaseTestCase


class TestModelController(BaseTestCase):
    """ModelController integration test stubs"""

    def test_model_clustering_post(self):
        """Test case for model_clustering_post

        Cluster a set of players
        """
        body = [List[int]()]
        response = self.client.open(
            '/api/model/clustering',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_model_reinforcement_post(self):
        """Test case for model_reinforcement_post

        Run a betting bot starting at a date
        """
        body = BettingBotInput()
        response = self.client.open(
            '/api/model/reinforcement',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_model_todo_post(self):
        """Test case for model_todo_post

        TODO
        """
        body = TODOIN()
        response = self.client.open(
            '/api/model/todo',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
