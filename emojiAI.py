# -*- coding: utf-8 -*-

import nltk
import random
import sqlite3
import os
import sys

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
      #print emojiDict 

   return emojiDict

def word_freq(message):
   counts = {}
   for word in message.split(' '):
      try:
         counts[word] += 1
      except KeyError:
         counts[word] = 1

   return counts


if __name__ == '__main__':

   reload(sys)
   sys.setdefaultencoding('utf-8')

   emojiCategories = getEmojiCategories();

   db = sqlite3.connect('data.db')
   cursor = db.cursor()
   cursor.execute("SELECT text FROM message")
   rows = cursor.fetchall()

   messages = [row[0] for row in rows]

#   print emojiCategories
   labeled_messages = {}
   for msg in messages:
      for(category, emojis) in emojiCategories.iteritems():
         #print "category: ", category
         #print "emojis: ", emojis
         for emoji in emojis: 
            #print "emoji: ", emoji
            if (msg is not None and msg.find(emoji) != -1) :
               #print "\nmsg: ", msg
               #print "emoji found", emoji
               
               labeled_messages[msg] = category
               break
         else:
            hi = 4
            #print "emoji not found"

   db.close()

   #print "labeled_messages", labeled_messages

   # shuffle because we are making both train and test sets from this list
   random.shuffle(labeled_messages.keys())
   print labeled_messages

   # 2. create feature set dictionary in the form (func(data), classifer)
   featuresets = [(word_freq(msg), category) for (msg, category) in labeled_messages.iteritems()]
   #print "featuresets", featuresets

   # 3. create a training set from the feature set
   train_set = featuresets[1000:]
   test_set = featuresets[:1000]

   # 4. create a classifier using the training set
   classifier = nltk.NaiveBayesClassifier.train(train_set)

   # 5. classify a specific result
   print classifier.classify(word_freq('You are cute.'))

   # 6. (optional) gather statistics 
   print "Accuracy: %f" % (nltk.classify.accuracy(classifier, test_set))
   print (classifier.show_most_informative_features(50))

