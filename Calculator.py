#!/usr/bin/env python

import requests


class Calculator:
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b
    
    '''
    Get the value of 1 USD to GBP
    '''
    def _get_exchange_rate(self):
        response = requests.get("https://api.frankfurter.app/latest?from=USD&to=GBP")
        return response.json()['rates']['GBP']
    
    '''
    Do the conversion
    '''
    def usd_to_gbp(self, amt_in_usd):
        exchange_rate = self._get_exchange_rate()
        return amt_in_usd * exchange_rate