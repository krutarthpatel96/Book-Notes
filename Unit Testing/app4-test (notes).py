import os
import unittest
import requests
import pymongo

class BasicTests(unittest.TestCase):
    ipAdd = '18.206.119.216'
    
    def test_submitNote(self):
        response = requests.get('http://'+self.ipAdd+':5050/submitNote?keyword=Test Keyword&note=Test Note')
        self.assertEqual(response.status_code, 200)

    def test_retrieveNote(self):
        response = requests.get('http://'+self.ipAdd+':5050/retrieveNote?keyword=Test Keyword')
        self.assertEqual(response.status_code, 200)

        
if __name__ == "__main__":
    unittest.main()
