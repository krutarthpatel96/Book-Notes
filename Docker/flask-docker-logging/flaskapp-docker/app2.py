from flask import Flask, render_template, url_for, redirect
import os
import datetime
from flask import request
from flask import jsonify
import pymongo
import requests
#import logging
import json
#import sys

app = Flask(__name__)

ipAdd= requests.get("http://169.254.169.254/latest/meta-data/public-ipv4").content
#app.logger.warning(ipAdd)
myclient = pymongo.MongoClient("mongodb://krutarth:root@"+ipAdd+"/db")
mydb = myclient["db"]
mycolTime = mydb["assignment3_logging_time_book"]
mycolFreq = mydb["assignment3_logging_frequency_book"]

mycolTimeA = mydb["assignment3_logging_time_author"]
mycolFreqA = mydb["assignment3_logging_frequency_author"]

@app.route("/logBook", methods=['GET','POST'])
def saveBookLog():
    book = request.args.get('book').replace('"',"")
    '''
    myquery = {"book": book}
    mydoc = mycolFreq.find_one(myquery)
    
    if(mydoc is None):
        freq = 0
        myqueryFreq = {"book": book, "frequency": freq+1}
        mycolFreq.insert_one(myqueryFreq)
    else:
        freq = mydoc.get("frequency")
        mydoc["frequency"] = freq+1
        mycolFreq.save(mydoc)
        
    myqueryTime = {"book": book, "time": str(datetime.datetime.now())}
    mycolTime.insert_one(myqueryTime)
    '''

    data=[]
    try:
        with open('logs_time.json') as json_file:
            data = json.load(json_file)
    except IOError:
        msg = "File does not exist"

    valTime = {
        "keyword": book,
        "time": str(datetime.datetime.now())
    }
    data.append(valTime)
    writeTime(data)

    freq=1
    temp=[]
    flag=1
    try:
        with open('logs_frequency.json') as json_file:
            data = json.load(json_file)
            for val in data:
                if(val["keyword"] == book):
                    flag=0
                    val["frequency"] = val["frequency"]+1
                temp.append(val)
    except IOError:
        msg = "File does not exist"

    if(flag == 1):
        valFreq = {
            "keyword": book,
            "frequency": freq
        }
        temp.append(valFreq)

    writeFrequency(temp)
    
    return "true"

@app.route("/logAuthor", methods=['GET','POST'])
def saveAuthorLog():
    author = request.args.get('author').replace('"',"")
    '''
    myquery = {"author": author}
    mydoc = mycolFreqA.find_one(myquery)

    if(mydoc is None):
        freq = 0
        myqueryFreq = {"author": author, "frequency": freq+1}
        mycolFreqA.insert_one(myqueryFreq)
    else:
        freq = mydoc["frequency"]
        mydoc["frequency"] = freq+1
        
        mycolFreqA.save(mydoc)
        
    myqueryTime = {"author": author, "time": str(datetime.datetime.now())}
    mycolTimeA.insert_one(myqueryTime)
    '''

    data=[]
    try:
        with open('logs_time.json') as json_file:
            data = json.load(json_file)
    except IOError:
        msg = "File does not exist"
           
    valTime = {
        "keyword": author,
        "time": str(datetime.datetime.now())
    }
    data.append(valTime)
    writeTime(data)

    freq=1
    temp=[]
    flag=1
    try:
        with open('logs_frequency.json') as json_file:
            data = json.load(json_file)
            print(data)
            for val in data:
                if(val["keyword"] == author):
                    flag=0
                    val["frequency"] = val["frequency"]+1
                temp.append(val)
    except IOError:
        msg = "File does not exist"

    if(flag == 1):
        valFreq = {
            "keyword": author,
            "frequency": freq
        }
        temp.append(valFreq)

    writeFrequency(temp)
    
    return "true"

def writeTime(data, filename='logs_time.json'): 
    with open(filename,'w+') as file: 
        json.dump(data, file, indent=4)

def writeFrequency(data, filename='logs_frequency.json'): 
    with open(filename,'w+') as file: 
        json.dump(data, file, indent=4) 

if __name__ == "__main__":
    app.run(debug=True,
            host='0.0.0.0',
            port=int(os.getenv('PORT', '8000')))
