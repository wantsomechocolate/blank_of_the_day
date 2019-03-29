from apiclient.discovery import build
import twitter
import os, re
import collections

consumer_key=os.environ["USELESSMUTANT_TWITTER_APIKEY"]
consumer_secret=os.environ["USELESSMUTANT_TWITTER_SECRETKEY"]
access_token=os.environ["USELESSMUTANT_TWITTER_ACCESSTOKEN"]
access_token_secret=os.environ["USELESSMUTANT_TWITTER_SECRETTOKEN"]

hashtag="bread"
RETWEET_REGEX_PATTERN = r"RT @[\w]+:"

api = twitter.Api(
	consumer_key=consumer_key, 
	consumer_secret=consumer_secret, 
	access_token_key=access_token, 
	access_token_secret=access_token_secret
	)

results = api.GetSearch(term="#"+str(hashtag), result_type="recent", count=50)

## Start a list
vote_text_list=[]

## loop through results and add them to the list 1 by 1
for i in range(len(results)):
	tweet_info = results[i]
	tweet_text = tweet_info.text

	## Only take text prior to the first hashtag regardless of what it is. 
	vote_text = tweet_text[:tweet_text.find("#")].strip()
	try:
		print("vote_text is: "+str(vote_text))
	except:
		pass
                
	if vote_text != '':
		# try to find retweet shit
		regex_result = re.search(RETWEET_REGEX_PATTERN, vote_text)
		if regex_result == None:
			vote_text_list.append(vote_text)
		else:
			vote_text = vote_text[regex_result.end():].strip()
			if vote_text!='':
				vote_text_list.append(vote_text)

## Use collections to create a counter object
c = collections.Counter(vote_text_list)

#return c

most_popular_tuple = c.most_common(1)[0]
most_popular_vote = most_popular_tuple[0]
most_popular_count= most_popular_tuple[1]


if most_popular_count == 1:
	print("There was no clear winner")
else:
	q_raw=most_popular_vote
	q = q_raw.replace('\n',' ')

	num_result=2

	api_key = os.environ['USELESSMUTANT_CSE_APIKEY']
	service = build('customsearch','v1', developerKey = api_key)

	res = service.cse().list(  q=q                                   ,
				   cx=os.environ['USELESSMUTANT_CSE_CX'] , 
				   searchType='image'                    , 
				   num=1                                 ,
				   start=num_result                      ,
				   safe='active'                         ,   )
	
	res_ex = res.execute()
	try:
		link_info=res_ex['items'][-1]
	except KeyError:
		print("The search didn't produce any results")

