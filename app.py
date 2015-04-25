# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, jsonify
from elasticsearch import Elasticsearch
import emoji, random, re, sqlite3, nltk

es = Elasticsearch()
app = Flask(__name__)
classifier = None
bannedWords = ['i', 'to', 'you', 'the', 'a', 'i\'m', 'and', 'it', 'for']

def getEmojiCategories():
    emojiDict = {}
    # all emoji categories with their list
    lines = [line.strip() for line in open('output')]
    # iterate by 2 at a time, getting category name and corresponding emojis
    it = iter(lines)
    for i in it:
        emojis = [] 
        category_name = i
        category_emojis = next(it)
        for emoji in category_emojis.split():
            emojis.append(emoji.decode('unicode-escape'))
        emojiDict[category_name] = emojis

    return emojiDict

def extract_features(message):
    counts = {}
    for word in re.sub('[^a-z]', ' ', message.lower()).split():
        w = word
        try:
            counts[w] += 1
        except KeyError:
            counts[w] = 1

    bigCounts = {}
    for (k, v) in counts.iteritems():
        if k not in bannedWords:
            bigCounts[k] = v

    return bigCounts

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/suggest', methods=['POST'])
def suggest():
    message = request.form['message']

    # create suggestions
    category = classifier.classify(extract_features(message))
    if (message.find("poop") != -1) :
       suggestions = [u'💩' for _ in range(1,random.randint(3, 10))] 
    else:
       suggestions = emojiCategories[category]

    return jsonify({'suggestions' : suggestions})

emojiCategories = getEmojiCategories();

if __name__ == '__main__':
    print "Making classifier..."
    db = sqlite3.connect('data.db')
    cursor = db.cursor()
    cursor.execute("SELECT text FROM message")
    rows = cursor.fetchall()

    messages = [row[0] for row in rows]

    labeled_messages = {}
    for msg in messages:
        for (category, emojis) in emojiCategories.iteritems():
            for emoji in emojis: 
                if (msg is not None and msg.find(emoji) != -1) :
                    labeled_messages[msg] = category
                    break

    db.close()

    # 2. create feature set dictionary in the form (func(data), classifer)
    featuresets = [(extract_features(msg), category) for (msg, category) in labeled_messages.iteritems()]

    # 4. create a classifier using the training set
    classifier = nltk.NaiveBayesClassifier.train(featuresets)
    print "Created classifier"
    print classifier.show_most_informative_features(10)
    app.run(debug = True)
