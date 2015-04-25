# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, jsonify
from elasticsearch import Elasticsearch
import emoji, random, re, sqlite3

es = Elasticsearch()
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/suggest', methods=['POST'])
def suggest():
    message = request.form['message']

    if (message.find("poop") != -1) :
       suggestions = [u'💩' for _ in range(1,random.randint(3, 10))] 
       return jsonify({'suggestions' : suggestions})

    try:
        res = es.search(index="emoji-index", body={
            "query": {
                "query_string": {
                    "query": message
                }
            }
        })
    except:
        return jsonify({'suggestions' : []})

    regExpr = re.compile(u'([\U00002600-\U000027BF])|([\U0001f300-\U0001f64F])|([\U0001f680-\U0001f6FF])')
    suggestions = set()
    for hit in res['hits']['hits']:
        emojisFound = regExpr.findall(hit['_source']['text'])
        for e in emojisFound:
            if e[1]:
                suggestions.add(e[1])

    return jsonify({'suggestions' : list(suggestions)})

if __name__ == '__main__':
    app.run(debug = True)
