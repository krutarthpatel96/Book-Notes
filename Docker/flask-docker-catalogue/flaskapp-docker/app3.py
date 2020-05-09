from flask import Flask, render_template, url_for, redirect
import os
from flask import request
from flask import jsonify
import pymongo
import requests
#import logging

app = Flask(__name__)

ipAdd= requests.get("http://169.254.169.254/latest/meta-data/public-ipv4").content
#app.logger.warning(ipAdd)
myclient = pymongo.MongoClient("mongodb://krutarth:root@"+ipAdd+"/db")
mydb = myclient["db"]
mycol = mydb["assignment3_books"]
mycolCat = mydb["assignment3_catalogue"]

@app.route("/catAuthor", methods=['GET','POST'])
def catalogueAuthor():
    book = request.args.get('book')
    myquery = {"book": book}
    mydoc = mycol.find(myquery,{"book":1, "author":1, "_id": False})
    mydocc = mycol.find_one(myquery,{"book":1, "author":1, "_id": False})

    if(list(mydocc) is not None):
        myquery = {"book": book}
        mydoc2 = mycolCat.find_one(myquery)
        if(mydoc2 is None):
            myqueryCat = {"author": mydocc["author"], "book": book}
            mycolCat.insert_one(myqueryCat)

    return jsonify(list(mydoc))

@app.route("/catBook", methods=['GET','POST'])
def catalogueBook():
    author = request.args.get('author')
    myquery = {"author": author}
    mydoc = mycol.find(myquery,{"book":1, "author":1, "_id": False})
    mydocc = mycol.find(myquery,{"book":1, "_id": False})
    checkdoc = mycol.find(myquery,{"book":1, "_id": False})
    if(list(checkdoc) is not None):
        for val in mydocc:
            myquery = {"author": author, "book": val.get("book")}
            mydoc2 = mycolCat.find_one(myquery)
            if(mydoc2 is None):
                myqueryCatA = {"author": author, "book": val.get("book")}
                mycolCat.insert_one(myqueryCatA)
    #print(jsonify(mydoc), file=sys.stderr)
    return jsonify(list(mydoc))

if __name__ == "__main__":
    app.run(debug=True,
            host='0.0.0.0',
            port=int(os.getenv('PORT', '8080')))
