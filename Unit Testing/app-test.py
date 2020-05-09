import os
import unittest
import requests
import pymongo

class BasicTests(unittest.TestCase):

    ipAdd = '18.206.119.216'

    def setUp(self):
        myclient = pymongo.MongoClient("mongodb://krutarth:root@"+self.ipAdd+"/db")
        dbList = myclient.list_database_names()
        mydb = myclient["db"]
        mycol = mydb["assignment3_books"]
        mycol.insert_one({"book": "Test Book", "author": "Test Author"})
        
    def tearDown(self):
        myclient = pymongo.MongoClient("mongodb://krutarth:root@"+self.ipAdd+"/db")
        dbList = myclient.list_database_names()
        mydb = myclient["db"]
        mycol = mydb["assignment3_books"]
        mycolc = mydb["assignment3_catalogue"]
        mycol.delete_many({"book": "Test Book"})
        mycolc.delete_many({"book": "Test Book"})

    def test_searchAuthor(self):
        response = requests.get('http://'+self.ipAdd+':5000/searchAuthor?book=Test Book')
        self.assertEqual(response.status_code, 200)

    def test_searchBook(self):
        response = requests.get('http://'+self.ipAdd+':5000/searchBook?author=Test Author')
        self.assertEqual(response.status_code, 200)

    def test_submitNote(self):
        response = requests.get('http://'+self.ipAdd+':5000/submitNote?keyword=Test Keyword&note=Test Note')
        self.assertEqual(response.status_code, 200)

    def test_retrieveNote(self):
        response = requests.get('http://'+self.ipAdd+':5000/retrieveNote?keyword=Test Keyword')
        self.assertEqual(response.status_code, 200)

        
if __name__ == "__main__":
    unittest.main()
