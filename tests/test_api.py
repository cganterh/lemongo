"""Define and test lemongo's API."""


from argparse import ArgumentParser
from unittest.mock import patch

import lemongo
from pymongo import MongoClient
from pkg_resources import iter_entry_points

from tests.lemongo_test_case import LeMongoTestCase


class TestLeMongoModuleRequirements(LeMongoTestCase):
    """Test lemongo's module requirements."""

    def test_module_attribute_number(self):
        """Test that the module has the correct number of attributes."""
        number_of_attributes = len(
            [a for a in dir(lemongo) if not a.startswith('_')])

        self.assertEqual(
            number_of_attributes,
            1,
            'lemongo module has zero or more than one attributes.'
        )

    def test_get_client_is_attribute_of_lemongo(self):
        """Test that ``get_client`` is an attribute of lemongo."""
        get_client_exists = hasattr(lemongo, 'get_client')

        self.assertTrue(
            get_client_exists,
            'There is no attribute called get_client in lemongo module.'
        )

    def test_that_get_client_is_callable(self):
        """Test that ``get_client`` is callable."""
        is_callable = callable(object)
        self.assertTrue(is_callable, 'lemongo.get_client is not callable.')


class TestGetClientFunctionBehavior(LeMongoTestCase):
    """Test ``lemongo.get_client()`` behavior."""

    def test_get_client_returns_mongo_client_object(self):
        """Test that get_client() returns a MongoClient object."""
        client = lemongo.get_client()

        self.assertIsInstance(
            client,
            MongoClient,
            'lemongo.get_client() did not return an instance of MongoClient.'
        )

    def test_multiple_calls_to_get_client_return_the_same_object(self):
        """Test that multiple calls to get_client() return the same object."""
        client1 = lemongo.get_client()
        client2 = lemongo.get_client()

        self.assertIs(
            client1,
            client2,
            'Two calls to lemongo.get_client() did not return the same object.'
        )


class TestArgumentParserEntryPoint(LeMongoTestCase):
    """Test argument parser entry point behavior."""

    def test_advertised_object_is_instance_of_argument_parser(self):
        """Test that the advertised object is an instance of ArgumentParser."""
        entry_point_iterator = iter_entry_points(
            group='le.parsers', name='lemongo_parser')

        entry_point = next(entry_point_iterator)
        argument_parser = entry_point.load()

        self.assertIsInstance(
            argument_parser,
            ArgumentParser,
            'The advertised lemongo_parser object is not an instance of '
            'ArgumentParser.'
        )

    @patch('lemongo._MongoClient')
    @patch('argparse._sys.argv', ['dfsuf', '--mongodb-uri', 'mongodb://mongo'])
    def test_mongo_client_is_called_with_parsed_uri(self, MongoClient):
        """Test that the MongoClient is constructed using the given URI."""
        lemongo.get_client()
        MongoClient.assert_called_with('mongodb://mongo')
