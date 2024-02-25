#!/usr/bin/env python
'''
This file is called test_llm_gateway.py
'''
from components import llm_gateway
import unittest
from unittest.mock import MagicMock

class TestLLM_Gateway(unittest.TestCase):
    def setUp(self):
        self.gateway = llm_gateway.LLM_gateway()
        
    

if __name__ == '__main__':
    unittest.main()