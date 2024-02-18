#!/usr/bin/env python
'''
This file is called test.py
'''
from subprocess import Popen
from Client import Client

def test_server_client():
    '''
    We start the server and let it run in the background. Then we ask 
    the client to make a call to the server and we compare the expected value.
    '''
    print("\nStarting Server\n")
    server = Popen('./Server.py')
    print("\nStarting Client\n")
    client = Client()
    print("\nTesting Calc\n")
    sum = client.get_sum(3, 4)
    assert (sum == 7)