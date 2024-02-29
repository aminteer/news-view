#!/usr/bin/env python
'''
This file is called test_data_gateway.py
'''
from data.data_gateway import DataGateway
import unittest
from unittest.mock import MagicMock
from PIL import Image

TEST_IMAGE_PATH="tests/test_image.png"

class TestLLM_Gateway(unittest.TestCase):
    def setUp(self):
        self.gateway = DataGateway()
        #self.gateway.create_summary = MagicMock(return_value = "Generate a calm ocean scene")
        self.test_image = Image.open(TEST_IMAGE_PATH)
        
    def test_save_image(self, img = None):
        if img==None : img = self.test_image
        dg = self.gateway
        assert(dg.save_image_as_file(img=img)==True)   
        
    

if __name__ == '__main__':
    unittest.main()


