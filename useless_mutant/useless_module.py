
def google_image_search(search_query, num_result):
	from apiclient.discovery import build
	import os

	if num_result>99:
		num_result=99

	api_key = os.environ['USELESSMUTANT_CSE_APIKEY']
	service = build('customsearch','v1', developerKey = api_key)

	res = service.cse().list(	q=search_query                        ,
								cx=os.environ['USELESSMUTANT_CSE_CX'] , 
								searchType='image'                    , 
								num=1                                 , 
								start=num_result                      ,
								#imgType='clipart'                     , 
								#fileType='png'                        , 
								safe='off'                            ,   )

	res_ex = res.execute()

		
	#if res_ex['queries']['request'][0]['totalResults'] == 0:
	try:
		link_info=res_ex['items'][-1]
	except KeyError:
		link_info = {'error':{'error_message':'There were no results returned'}}

	return link_info #locals()



def tally_twitter_votes(hashtag):
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

	tweets = api.search_tweets('#'+hashtag, count = 100, tweet_mode = 'extended')

	## Start a list
	vote_text_list=[]

	for tweet in tweets:
		if 'retweeted_status' in dir(tweet):
			vote_text_list.append(tweet.retweeted_status.full_text)
		else:
			vote_text_list.append(tweet.full_text)

	## Use collections to create a counter object
	c = collections.Counter(vote_text_list) #access data with something like most_popular_tuple = c.most_common(1)[0]

	return c


def post_add_calc_fields(post,globals_dict):
	import datetime

	post.url  		=   post.hashtag.name.replace(' ','_') + "-" + str(post.created_at.strftime("%Y%m%d%H%M%S%f"))
	post.text_date 	= 	datetime.datetime.strftime(post.created_at, "%Y-%m-%d")
	post.text_time	=	datetime.datetime.strftime(post.created_at, "%H-%M-%S")	

	return post



if __name__ == "__main__":
	#q = "japan"
	i = 1

	q = tally_twitter_votes("japan").most_common(1)[0][0]

	print ("searching for "+q+" and returning info for result "+str(i))
	link_info = google_image_search(q, i)
	print(link_info["link"])
