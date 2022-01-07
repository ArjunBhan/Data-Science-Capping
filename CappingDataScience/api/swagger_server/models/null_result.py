# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class NullResult(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, row_count: int=None, columns: List[str]=None, nulls_in_columns: List[int]=None, rows_with_any_nulls: int=None):  # noqa: E501
        """NullResult - a model defined in Swagger

        :param row_count: The row_count of this NullResult.  # noqa: E501
        :type row_count: int
        :param columns: The columns of this NullResult.  # noqa: E501
        :type columns: List[str]
        :param nulls_in_columns: The nulls_in_columns of this NullResult.  # noqa: E501
        :type nulls_in_columns: List[int]
        :param rows_with_any_nulls: The rows_with_any_nulls of this NullResult.  # noqa: E501
        :type rows_with_any_nulls: int
        """
        self.swagger_types = {
            'row_count': int,
            'columns': List[str],
            'nulls_in_columns': List[int],
            'rows_with_any_nulls': int
        }

        self.attribute_map = {
            'row_count': 'row_count',
            'columns': 'columns',
            'nulls_in_columns': 'nulls_in_columns',
            'rows_with_any_nulls': 'rows_with_any_nulls'
        }

        self._row_count = row_count
        self._columns = columns
        self._nulls_in_columns = nulls_in_columns
        self._rows_with_any_nulls = rows_with_any_nulls

    @classmethod
    def from_dict(cls, dikt) -> 'NullResult':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The NullResult of this NullResult.  # noqa: E501
        :rtype: NullResult
        """
        return util.deserialize_model(dikt, cls)

    @property
    def row_count(self) -> int:
        """Gets the row_count of this NullResult.


        :return: The row_count of this NullResult.
        :rtype: int
        """
        return self._row_count

    @row_count.setter
    def row_count(self, row_count: int):
        """Sets the row_count of this NullResult.


        :param row_count: The row_count of this NullResult.
        :type row_count: int
        """

        self._row_count = row_count

    @property
    def columns(self) -> List[str]:
        """Gets the columns of this NullResult.


        :return: The columns of this NullResult.
        :rtype: List[str]
        """
        return self._columns

    @columns.setter
    def columns(self, columns: List[str]):
        """Sets the columns of this NullResult.


        :param columns: The columns of this NullResult.
        :type columns: List[str]
        """

        self._columns = columns

    @property
    def nulls_in_columns(self) -> List[int]:
        """Gets the nulls_in_columns of this NullResult.


        :return: The nulls_in_columns of this NullResult.
        :rtype: List[int]
        """
        return self._nulls_in_columns

    @nulls_in_columns.setter
    def nulls_in_columns(self, nulls_in_columns: List[int]):
        """Sets the nulls_in_columns of this NullResult.


        :param nulls_in_columns: The nulls_in_columns of this NullResult.
        :type nulls_in_columns: List[int]
        """

        self._nulls_in_columns = nulls_in_columns

    @property
    def rows_with_any_nulls(self) -> int:
        """Gets the rows_with_any_nulls of this NullResult.


        :return: The rows_with_any_nulls of this NullResult.
        :rtype: int
        """
        return self._rows_with_any_nulls

    @rows_with_any_nulls.setter
    def rows_with_any_nulls(self, rows_with_any_nulls: int):
        """Sets the rows_with_any_nulls of this NullResult.


        :param rows_with_any_nulls: The rows_with_any_nulls of this NullResult.
        :type rows_with_any_nulls: int
        """

        self._rows_with_any_nulls = rows_with_any_nulls
