import os
import unittest
import requests
import pymongo
import datetime

class BasicTests(unittest.TestCase):

    ipAdd = '18.206.119.216'
    
    def test_saveBookLog(self):
        response = requests.get('http://'+self.ipAdd+':8000/logBook?book=Test Book')
        self.assertEqual(response.status_code, 200)

    def test_saveAuthorLog(self):
        response = requests.get('http://'+self.ipAdd+':8000/logAuthor?author=Test Author')
        self.assertEqual(response.status_code, 200)
        
if __name__ == "__main__":
    unittest.main()
