from flask import Flask, render_template, url_for, redirect
import os
from flask import request
from flask import jsonify
import pymongo
import requests
import json
#import logging

app = Flask(__name__)

#ipAdd= requests.get("http://169.254.169.254/latest/meta-data/public-ipv4").content
ipAdd="localhost"
#app.logger.warning(ipAdd)
myclient = pymongo.MongoClient("mongodb://krutarth:root@"+ipAdd+"/db")
mydb = myclient["db"]
mycol = mydb["assignment3_books"]
mycolCat = mydb["assignment3_catalogue"]
mycolNote = mydb["assignment3_notes"]

@app.route("/submitNote", methods=['GET','POST'])
def submitNote():
    keyword = request.args.get('keyword')
    note = request.args.get('note')
    #myquery = {"$or": [{"book": keyword }, {"author": keyword}]}
    ''' search from books
    mydoc = mycol.find_one(myquery,{"book":1, "author":1, "_id": False})
    mydocc = mycol.find_one(myquery,{"book":1, "author":1, "_id": False})
    if(mydocc is None):
        myqueryNote = {"keyword": keyword, "note": note}
        mycolNote.insert_one(myqueryNote)
    '''
    ''' search from catalogue
    mydoc2 = mycolCat.find_one(myquery,{"book":1, "author":1, "_id": False})
    mydocc2 = mycolCat.find_one(myquery,{"book":1, "author":1, "_id": False})
    if(mydocc2 is None):
        return "Keyword not found!"
    else:
        myqueryNote = {"keyword": keyword, "note": note}
        mycolNote.insert_one(myqueryNote)
        return "Note Submitted!"
    '''

    data=[]
    try:
        with open('notes.json') as json_file:
            data = json.load(json_file)
    except IOError:
        msg = "File does not exist"

    valTime = {
        "keyword": keyword,
        "note": note
    }
    data.append(valTime)
    writeTime(data)
    
    return "Note Submitted!"

@app.route("/retrieveNote", methods=['GET','POST'])
def retrieveNote():
    keyword = request.args.get('keyword')
    '''
    myquery = {"keyword": keyword }
    mydoc = mycolNote.find(myquery,{"keyword":1, "note":1, "_id": False})
    mydocc = mycolNote.find(myquery,{"keyword":1, "note":1, "_id": False})
    if(len(list(mydocc)) == 0):
        return "No notes found!"
    else:
        return jsonify(list(mydoc))
    '''

    temp=[]
    try:
        with open('notes.json') as json_file:
            data = json.load(json_file)
            for val in data:
                if(val["keyword"] == keyword):
                    temp.append(val)
    except IOError:
        msg = "File does not exist"

    return jsonify(temp)

def writeTime(data, filename='notes.json'): 
    with open(filename,'w+') as file: 
        json.dump(data, file, indent=4)


if __name__ == "__main__":
    app.run(debug=True,
            host='0.0.0.0',
            port=int(os.getenv('PORT', '5050')))
