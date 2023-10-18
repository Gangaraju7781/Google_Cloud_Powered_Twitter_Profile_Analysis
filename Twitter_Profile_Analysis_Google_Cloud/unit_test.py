#where test is the file consists the code that has to be tested i.e source code--test.py
from test import *
import unittest

class Testaddition(unittest.TestCase):
    def test_volume(self):
        # to search for tweets which are not in range 
        search_tweets(userID,8740159846017860478181186018764085)
        #invalid usernmae
        userID("^^776435((*&&%%%^")
        #invalid Language - a language which doesnt exist in Google translate 
        tweet("&^*&*_(&^%$#@$%^&*()_(&^%$")
        #What if a tweet is infinitely long (very long)
        tweet(".........................................................................")
        #an error on the token's
        ACC_TOKEN('*******************^*************9************')