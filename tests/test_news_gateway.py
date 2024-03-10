#!/usr/bin/env python

import unittest
from components.news_gateway import NewsGateway
from unittest.mock import MagicMock

TEST_URL = 'top-headlines?country=us&category=business'
FAKE_API = 'fake_api'

'''
Test cases are created by subclassing unittest.TestCase
'''
class TestNewsGateway(unittest.TestCase):
    '''
    setUp function is used to instantiate the object we are testing.
    '''
    def setUp(self):
        self.gateway = NewsGateway()
    
    def test_api_return_success(self):
        #test that a request gets an expected response
        url = TEST_URL
        response, status = self.gateway.get_stories_from_url_request(url)
        self.assertEqual(status, 200)
        self.assertGreaterEqual(response['totalResults'], 1)
        
    def test_api_key_change(self):
        #test that api key change is kept and accurate
        self.gateway.ApiKey = FAKE_API
        self.assertEqual(self.gateway.ApiKey, FAKE_API)


if __name__ == '__main__':
    unittest.main()