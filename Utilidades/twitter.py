# -*- coding: utf-8 -*-

import re
import json
import tweepy

consumer_key = ''
consumer_secret = ''

access_token_key = ''
access_token_secret = ''

auth1 = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth1.set_access_token(access_token_key, access_token_secret)

class StreamListener(tweepy.StreamListener):
    def on_status(self, tweet):
        print 'Ran on_status'

    def on_error(self, status_code):
        print 'Error: ' + repr(status_code)
        return False

    def on_data(self, data):
        #print 'Ok, this is actually running'
        #tweet = proc.split(',"text":"')[1].split('","source')[0]
        decoded = json.loads(data)
        tweet = decoded['text'].encode('utf-8', 'ignore')
        tweet = re.sub(r'http\S+', '', tweet)
        tweet = tweet.replace('\n',' ').replace('\r',' ')
        print type(tweet), tweet

        saveThis = tweet
        saveFile = open('Datasets/dumpCopaAmerica.txt','a')
        saveFile.write(saveThis)
        saveFile.write('\n')
        saveFile.close()

def getTweets():
    l = StreamListener()
    streamer = tweepy.Stream(auth=auth1, listener=l)
    setTerms = ['Copa America']
    setLanguages = ['es']
    streamer.filter(languages=setLanguages, track=setTerms)
