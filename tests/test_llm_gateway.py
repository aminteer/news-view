#!/usr/bin/env python
'''
This file is called test_llm_gateway.py
'''
from components.llm_gateway import LLM_gateway
import unittest
from unittest.mock import MagicMock

class TestLLM_Gateway(unittest.TestCase):
    def setUp(self):
        self.gateway = LLM_gateway()
        self.gateway.create_summary = MagicMock(return_value = "Generate a calm ocean scene")
        
    

if __name__ == '__main__':
    unittest.main()