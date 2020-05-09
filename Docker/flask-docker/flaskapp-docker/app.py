from flask import Flask, render_template, url_for, redirect
import os
from flask import request
from flask import jsonify
import requests
#import logging

app = Flask(__name__)

@app.route("/searchAuthor", methods=['GET','POST'])
def searchAuthor():
    book = request.args.get('book')
    ipAdd= requests.get("http://169.254.169.254/latest/meta-data/public-ipv4").content
    #app.logger.warning(ipAdd)
    r = requests.get('http://'+ipAdd+':8000/logBook?book='+book)
    r = requests.get('http://'+ipAdd+':8080/catAuthor?book='+book)
    data = r.json()

    return jsonify(data)

@app.route("/searchBook", methods=['GET','POST'])
def searchBook():
    author = request.args.get('author')
    ipAdd= requests.get("http://169.254.169.254/latest/meta-data/public-ipv4").content
    #app.logger.warning(ipAdd)
    r = requests.get('http://'+ipAdd+':8000/logAuthor?author='+author)
    r = requests.get('http://'+ipAdd+':8080/catBook?author='+author)
    data = r.json()
        
    return jsonify(data)

@app.route("/submitNote", methods=['GET','POST'])
def submitNote():
    keyword = request.args.get('keyword')
    note = request.args.get('note')
    ipAdd= requests.get("http://169.254.169.254/latest/meta-data/public-ipv4").content
    #app.logger.warning(ipAdd)
    r = requests.get('http://'+ipAdd+':5050/submitNote?keyword='+keyword+'&note='+note)
        
    return r.content

@app.route("/retrieveNote", methods=['GET','POST'])
def retrieveNote():
    keyword = request.args.get('keyword')
    ipAdd= requests.get("http://169.254.169.254/latest/meta-data/public-ipv4").content
    #app.logger.warning(ipAdd)
    r = requests.get('http://'+ipAdd+':5050/retrieveNote?keyword='+keyword)
    data = r.json()
    
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True,
            host='0.0.0.0',
            port=int(os.getenv('PORT', '5000')))
