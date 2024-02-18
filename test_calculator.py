#!/usr/bin/env python
'''
Import unittest framework and the Calculator class
'''
import unittest
from Calculator import Calculator
from unittest.mock import MagicMock


'''
Test cases are created by subclassing unittest.TestCase
'''
class TestCalculator(unittest.TestCase):
    '''
    setUp function is used to instantiate the object we are testing.
    '''
    def setUp(self):
        self.calculator = Calculator()
        self.calculator._get_exchange_rate = MagicMock(return_value=0.82)

    '''
    Test the add function.
    '''
    def test_add(self):
        add_result = self.calculator.add(1, 2)
        self.assertEqual(add_result, 3)

    '''
    Test the subtract function
    '''
    def test_subtract(self):
        subtract_result = self.calculator.subtract(1, 1)
        self.assertEqual(subtract_result, 0)

    '''
    Test currency conversion
    '''
    def test_currency_converter(self):
        conversion_result = self.calculator.usd_to_gbp(10)
        self.assertEqual(conversion_result, 8.2)


if __name__ == '__main__':
    unittest.main()