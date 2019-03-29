
#http://python-twitter.readthedocs.io/en/latest/searching.html

## Use this to construct queries
#https://twitter.com/search-advanced

import twitter
import os
import collections

consumer_key=os.environ["USELESSMUTANT_TWITTER_APIKEY"]
consumer_secret=os.environ["USELESSMUTANT_TWITTER_SECRETKEY"]
access_token=os.environ["USELESSMUTANT_TWITTER_ACCESSTOKEN"]
access_token_secret=os.environ["USELESSMUTANT_TWITTER_SECRETTOKEN"]


api = twitter.Api(
	consumer_key=consumer_key, 
	consumer_secret=consumer_secret, 
	access_token_key=access_token, 
	access_token_secret=access_token_secret
	)

## Get all the tweets with the hashtag uselessmutant
results = api.GetSearch(raw_query="q=%23uselessmutant", include_entities=True)
#print (str(len(results))+" were returned")


## Start a list
vote_text_list=[]

## loop through results and add them to the list 1 by 1
for i in range(len(results)):
	tweet_info = results[i]
	tweet_text = tweet_info.text

	## Only take text prior to the first hashtag regardless of what it is. 
	vote_text = tweet_text[:tweet_text.find("#")].strip()
	vote_text_list.append(vote_text)

## Use collections to create a counter object
c = collections.Counter(vote_text_list)

## Use the most_common method of the counter object to return the single most common item
## Ties are sorted arbitrarily
most_popular_tuple = c.most_common(1)[0]
most_popular_vote = most_popular_tuple[0]
most_popular_count = most_popular_tuple[1]



#######################################################################################
## Other scratch work

#user="WantsomeChan"

## To see if your credentials are successful:
#print(api.VerifyCredentials())


#To fetch a single user's public status messages, where user is a Twitter user's screen name:
#statuses = api.GetUserTimeline(screen_name=user)
#print([s.text for s in statuses])

#most_recent=statuses[0].text

#index=most_recent.find("#uselessmutant")

#if index == -1:
#	content="Ajit Pai"
#else:
#	content=most_recent[0:most_recent.find("#uselessmutant")].strip()

#print(content)



## To fetch a list a user's friends:
#users = api.GetFriends()
#print([u.name for u in users])



## To post a Twitter status message: DOESN'T WORK BECUASE APPLICATION IS READ ONLY
#status = api.PostUpdate('This tweet made programmatically with python-twitter.')
#print(status.text)


## Search!
#results = api.GetSearch(raw_query="q=%23justchillin", include_entities=True)


