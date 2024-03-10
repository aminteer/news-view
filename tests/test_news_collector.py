#!/usr/bin/env python

import unittest
from components.news_collector import NewsCollector
from unittest.mock import MagicMock

'''
Test cases are created by subclassing unittest.TestCase
'''
class TestNewsGateway(unittest.TestCase):
    '''
    setUp function is used to instantiate the object we are testing.
    '''
    def setUp(self):
        self.news_collector = NewsCollector()
        self.news_collector.get_top_stories = MagicMock(return_value="Lots of news today")
    
    def test_get_everything(self):
        result = self.news_collector.get_top_stories()
        self.assertEqual(result, "Lots of news today")


if __name__ == '__main__':
    unittest.main()