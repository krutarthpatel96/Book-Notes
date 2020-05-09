import os
import unittest
import requests
import pymongo
import datetime

class BasicTests(unittest.TestCase):

    ipAdd = '18.206.119.216'

    def setUp(self):
        myclient = pymongo.MongoClient("mongodb://krutarth:root@"+self.ipAdd+"/db")
        dbList = myclient.list_database_names()
        mydb = myclient["db"]
        mycol = mydb["assignment3_books"]
        mycolc = mydb["assignment3_catalogue"]
        mycol.insert_one({"book": "Test Book", "author": "Test Author"})
        mycolc.insert_one({"book": "Test Book", "author": "Test Author"})
         
    def tearDown(self):
        myclient = pymongo.MongoClient("mongodb://krutarth:root@"+self.ipAdd+"/db")
        dbList = myclient.list_database_names()
        mydb = myclient["db"]
        mycol = mydb["assignment3_books"]
        mycolc = mydb["assignment3_catalogue"]
        mycol.delete_many({"book": "Test Book"})
        mycolc.delete_many({"book": "Test Book"})

    def test_catalogueAuthor(self):
        response = requests.get('http://'+self.ipAdd+':8080/catAuthor?book=Test Book')
        self.assertEqual(response.status_code, 200)

    def test_catalogueBook(self):
        response = requests.get('http://'+self.ipAdd+':8080/catBook?author=Test Author')
        self.assertEqual(response.status_code, 200)
        
if __name__ == "__main__":
    unittest.main()
