


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
	import twitter
	import os, re
	import collections

	RETWEET_REGEX_PATTERN = r"RT @[\w]+:"

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
	#results = api.GetSearch(raw_query="q=%23uselessmutant", include_entities=True)
	results = api.GetSearch(term="#"+str(hashtag), result_type="recent", count=100)
	#print (str(len(results))+" were returned")


	## Start a list
	vote_text_list=[]

	## loop through results and add them to the list 1 by 1
	for i in range(len(results)):
		tweet_info = results[i]
		tweet_text = tweet_info.text

		## Only take text prior to the first hashtag regardless of what it is. 
		vote_text = tweet_text[:tweet_text.find("#")].strip()
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


	## Use the most_common method of the counter object to return the single most common item
	## Ties are sorted arbitrarily
	#most_popular_tuple = c.most_common(1)[0]
	#most_popular_vote = most_popular_tuple[0]
	#most_popular_count = most_popular_tuple[1]

	## For now return the whole thing and then get the count and most pop your self, so that if I want runner up info I can get it. 
	return c


def post_add_calc_fields(post,globals_dict):

	import datetime

	post.url 		= 	post.search_query.replace(' ','_') + "-" + str(post.created_at.strftime(globals_dict['DATE_FORMAT']))    
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
