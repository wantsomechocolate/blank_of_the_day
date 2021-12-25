##import twitter
##import os, re
##import collections
##RETWEET_REGEX_PATTERN = r"RT @[\w]+:"
##consumer_key=os.environ["USELESSMUTANT_TWITTER_APIKEY"]
##consumer_secret=os.environ["USELESSMUTANT_TWITTER_SECRETKEY"]
##access_token=os.environ["USELESSMUTANT_TWITTER_ACCESSTOKEN"]
##access_token_secret=os.environ["USELESSMUTANT_TWITTER_SECRETTOKEN"]
##api = twitter.Api(
##                consumer_key=consumer_key, 
##                consumer_secret=consumer_secret, 
##                access_token_key=access_token, 
##                access_token_secret=access_token_secret
##                )
##
##hashtag = 'beautiful'
##results = api.GetSearch(term="#"+str(hashtag), result_type="recent", count=100)

import tweepy
import os
import collections

consumer_key=os.environ["USELESSMUTANT_TWITTER_APIKEY"]
consumer_secret=os.environ["USELESSMUTANT_TWITTER_SECRETKEY"]
access_token=os.environ["USELESSMUTANT_TWITTER_ACCESSTOKEN"]
access_token_secret=os.environ["USELESSMUTANT_TWITTER_SECRETTOKEN"]

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


tweets = api.search_tweets('#beautiful', count = 100, tweet_mode = 'extended')


vote_text_list = []

for tweet in tweets:
    if 'retweeted_status' in dir(tweet):
        vote_text_list.append(tweet.retweeted_status.full_text)
    else:
        vote_text_list.append(tweet.full_text)

c = collections.Counter(vote_text_list)
