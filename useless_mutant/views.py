from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context, loader
from django.shortcuts import get_object_or_404

#from datetime import datetime
import datetime

from useless_mutant.models import Post, Hashtag
import useless_mutant.useless_module as um

DATE_FORMAT = "%Y%m%d%H%M%S%f"
NUM_RECENT_POSTS = 6
MAX_NUM_RESULT = 100

MESSAGE_NO_HASHTAGS_SETUP = "It looks like no hashtags have been setup yet. Email wantsomechocolate @ gmail.com to start '____ of the day' for your hashtag!"
MESSAGE_HASHTAG_NOT_SETUP = "It looks like this hashtag isn't setup in the system yet. Email wantsomechocolate @ gmail.com to start '____ of the day' for your hashtag!" 
MESSAGE_NO_POSTS_ON_HASHTAG = "It looks like this hashtag is setup but hasn't produced any posts yet! Try making a publicly available tweet using the hashtag and come back later."
MESSAGE_POST_DOES_NOT_EXIST = "It looks like no post exists matching the given URL, sorry!"
MESSAGE_NOTHING_TO_EXPLORE = "It looks like there isn't anything to explore yet, sorry!"

GLOBALS_DICT = {	'DATE_FORMAT'					:	DATE_FORMAT						, 
					'NUM_RECENT_POSTS'				:	NUM_RECENT_POSTS				,
					'MAX_NUM_RESULT'				:	MAX_NUM_RESULT 					,
					'MESSAGE_NO_HASHTAGS_SETUP'		:	MESSAGE_NO_HASHTAGS_SETUP 		,
					'MESSAGE_HASHTAG_NOT_SETUP' 	:	MESSAGE_HASHTAG_NOT_SETUP 		,
					'MESSAGE_NO_POSTS_ON_HASHTAG'	:	MESSAGE_NO_POSTS_ON_HASHTAG 	, 	
					'MESSAGE_POST_DOES_NOT_EXIST'	:	MESSAGE_POST_DOES_NOT_EXIST 	, 	
					'MESSAGE_NOTHING_TO_EXPLORE'	:	MESSAGE_NOTHING_TO_EXPLORE		,	}

# Create your views here.



def hashtags_all(request):

	## A view to show viewers all the active hashtags - doesn't guaruntee that each post shown has a post. 

	## VIEWRIABLES #########################################################################	
	template 	=	'useless_mutant/hashtags_all.html'
	t 			= 	loader.get_template(template)


	## DB IO ###############################################################################
	hashtags_all 	= 	Hashtag.objects 							\
								.filter(enabled=True) 				\
								.order_by('-last_post_added_time') 	#

	if len(hashtags_all)==0: 	## Check to see if any items came back. if not you're done! 
		c 	=	{	'query_returned_none'	:	True						,		#
					'message'				:	MESSAGE_NO_HASHTAGS_SETUP	,	}	#
		return HttpResponse(t.render(c))


	## VIEW LOGIC ##########################################################################
	c	= 	{	'hashtags_all'	:	hashtags_all	,	}	#


	## FINAL RETURN ########################################################################
	return HttpResponse(t.render(c))



def	index(request):

	## The main welcome page - explains the project and gets the user started on some examples
	## Right now this grabs the three hashtags that have most recently been added to
	## But it's possible that they could no longer have any posts (deleting posts doesn't 
	## currently do anything. So maybe a more robust way would be to grab all the hashtags
	## and then when you get a certain number with at least one post then you move on. 
	## Of when you get to the end of the list. 
	## The other thing I can do is mark a hashtag enabled=False by default and then 
	## again if it ever gets to a point where it has no children. 


	## VIEWRIABLES #########################################################################
	template 	=	'useless_mutant/index.html'
	t 			=	loader.get_template(template)


	## DB IO ###############################################################################
	hashtags_with_most_recent_posts = Hashtag.objects \
												.filter(enabled=True) \
												.order_by('-last_post_added_time')[0:3]
	
	if len(hashtags_with_most_recent_posts)==0:  ## If there are not hashtags setup yet (fresh db)
		c 	=	{	'query_returned_none'	:	True						,		#
					'message'				:	MESSAGE_NO_HASHTAGS_SETUP	,	}	#		
		return	HttpResponse(t.render(c))
	
	## If there are some hashtags to work with. 
	latest_posts=[]  ## Loop through each hashtag and get the most recent post. 
	for hashtag in hashtags_with_most_recent_posts:

		most_recent_posts 	= 	Post.objects.filter(hashtag=hashtag) \
											.order_by('-created_at')
		
		## If you actually have a post on the hashtag, add most recent to list
		if len(most_recent_posts)!=0: 
			most_recent_post 				= 	most_recent_posts[0]
			most_recent_post.hashtag_name 	=	hashtag.name  
			latest_posts.append(most_recent_post)

	if len(latest_posts) == 0: ## If there are no posts and any of the most recent hashtags. 
		c 	=	{	'query_returned_none'	:	True						,		#
					'message'				:	MESSAGE_NOTHING_TO_EXPLORE	,	}	#
		return	HttpResponse(t.render(c))


	## VIEW LOGIC ##########################################################################
	for post in latest_posts: ## Add some information to the post objects. Is this necessary in this view?
		um.post_add_calc_fields(post, GLOBALS_DICT)

	c	=	{	'latest_posts'	:	latest_posts	,	}	#


	## FINAL RETURN ########################################################################	
	return	HttpResponse(t.render(c))



def	post(request, hashtag, post_url=None, created_at=None):

	## Show (for a given hashtag) a specific post or show the most recent post depending on post_url

	## VIEWRIABLES #########################################################################
	template = 'useless_mutant/post.html'
	t = loader.get_template(template)


	## DB IO ###############################################################################
	try: 		## Check to see that the hashtag exists in the hashtag table
		hashtag_record = Hashtag.objects.get(name=hashtag, enabled=True)
	except Hashtag.DoesNotExist: ## If the record turned out not to exist, then you're done!
		c 	=	{	'query_returned_none'	:	True						, 
					'message'				:	MESSAGE_HASHTAG_NOT_SETUP	,	}
		return	HttpResponse(t.render(c))
		
	## Get all the posts related to that hashtag (up to NUM_RECENT_POSTS) 
	latest_posts = Post.objects 										\
						.filter(hashtag=hashtag_record.id) 				\
						.order_by('-created_at')[0:NUM_RECENT_POSTS]	#

	if len(latest_posts) == 0: ## If there are no posts under the hashtag, you're done! 
		c 	=	{	'query_returned_none'	: 	True 						, 
					'message'				: 	MESSAGE_NO_POSTS_ON_HASHTAG ,	}
		return	HttpResponse(t.render(c))

	## Lets see if this is for index or a specific post
	if post_url==None: ## If post_url is none we get the most recent post. 
		single_post = latest_posts.first()
	
	else: ## If the post_url isn't blank we need to get a specific post. 
		created_at_datetime = datetime.datetime.strptime(created_at,DATE_FORMAT)	
		created_at_datetime = created_at_datetime - datetime.timedelta(hours=4) #Kludge

		## I have to do this because I haven't excatly figured out ms timestamps. 
		start = created_at_datetime - datetime.timedelta(seconds=1)
		end   = created_at_datetime + datetime.timedelta(seconds=1)

		try:
			single_post = Post.objects.get( search_query=post_url.replace('_',' ')	, 
											created_at__range = (start, end) 		,	)
		except Post.DoesNotExist:
			c 	=	{	'query_returned_none'	: 	True 						, 
						'message'				: 	MESSAGE_POST_DOES_NOT_EXIST ,	}
			return	HttpResponse(t.render(c))

		## VIEW LOGIC ######################################################################
		um.post_add_calc_fields(single_post, GLOBALS_DICT)
	

	## VIEW LOGIC ##########################################################################
	for post in latest_posts: 
		um.post_add_calc_fields(post, GLOBALS_DICT)

	c	=	{	'single_post' 	:	single_post		,
			 	'hashtag'		:	hashtag 		, 
			 	'latest_posts'	:	latest_posts 	,	}


	## FINAL RETURN ########################################################################
	return	HttpResponse(t.render(c))



def	archive(request, hashtag):

	## Shows all the items for a given hashtag. 

	## VIEWRIABLES #########################################################################
	template = 'useless_mutant/archive.html'
	t = loader.get_template(template)


	## DB IO ###############################################################################
	try: 	## Check to see that the hashtag exists in the hashtag table
 		hashtag_record = Hashtag.objects.get(name=hashtag, enabled=True)
	except Hashtag.DoesNotExist:	
		c = {	'query_returned_none' 	:	True 						, 
				'message'				:	MESSAGE_HASHTAG_NOT_SETUP	,	}
		return HttpResponse(t.render(c))

	## If it does get the associated posts
	latest_posts = Post.objects 							\
						.filter(hashtag=hashtag_record.id)	\
						.order_by('-created_at')			#

	if len(latest_posts) == 0: ## If there are no posts!
		t = loader.get_template(template)
		c = { 	'query_returned_none' 	: 	True 						, 
				'message'				: 	MESSAGE_NO_POSTS_ON_HASHTAG	,	}
		return HttpResponse(t.render(c))


	## VIEW LOGIC ##########################################################################	
	for post in latest_posts:
		um.post_add_calc_fields(post, GLOBALS_DICT)
		
	c = { 'latest_posts': latest_posts ,
		  'hashtag'     : hashtag      , }


	## FINAL RETURN ########################################################################
	return	HttpResponse(t.render(c))



## Should be scheduled, should require admin priveldges to run
def create_new_post_from_votes_twitter(request, hashtag):

	from collections import Counter
	import random
	
	#from useless_mutant.useless_module import tally_twitter_votes
	c = um.tally_twitter_votes(hashtag)

	# If there are no votes than don't create a post!
	if c == Counter():
		return	HttpResponse('<html><body>There are no votes to create a post</body></html>')
	
	
	most_popular_tuple = c.most_common(1)[0]
	most_popular_vote = most_popular_tuple[0]
	most_popular_count= most_popular_tuple[1]

	if most_popular_count == 1:
		return	HttpResponse('<html><body>No one rose above the rest</body></html>')


	q_raw=most_popular_vote
	q = q_raw.replace('\n',' ')

	## Might consider randomizing this in the future. 
	i = random.randrange(0,MAX_NUM_RESULT)

	link_info = um.google_image_search(q,i)
	
	if 'error' in link_info.keys():
		return	HttpResponse('<html><body>The search query'+'<br>'+str(q)+'<br>'+'did not return any results</body></html>')

	img_link=link_info['link']

	h, h_created_tf = Hashtag.objects.get_or_create(name = hashtag)
	if not h_created_tf:
		h.last_post_added_time=datetime.datetime.utcnow()
	h.save()

	## I need to download the image from the link and than save it into the image field!


	p = Post(	search_query 		=	q 					, 
				search_query_raw	=	q_raw 				, 
				link 				= 	img_link			, 
				votes 				= 	most_popular_count 	, 
				hashtag 			= 	h 					, 	)
	p.save()

	return	HttpResponse('<html><body>Successfully created post using'+'<br>'+str(q)+'<br>'+'!</body></html>')

	#most_popular_tuple = c.most_common(1)[0]
	#most_popular_vote = most_popular_tuple[0]
	#most_popular_count = most_popular_tuple[1]	






##############################################################################
## Older functions
##############################################################################


## Currently index just loads the most recent mutant, at some point the search should be more specific.
# def	hashtag_index(request, hashtag):
# 	from datetime import datetime

# 	## try to get all the posts for this hashtag
# 	## if the variable for the posts is empty, then the view will get a variable telling it so
# 	## In the view, the first post will be treated a special way!, if there are other items
# 	## they will be looped through and placed in a differenct section. 

# 	template = 'useless_mutant/post.html'
#     hashtag_modified = hashtag #.replace("_"," ")

# 	## Get all the posts
# 	latest_posts = Post.objects.filter(hashtag=hashtag).order_by('-created_at')

# 	## If there are no posts!
# 	if latest_posts == None:
# 		t = loader.get_template(template)
# 		c = { 'hashtag_not_setup' : True, }
# 		return HttpResponse(t.render(c))

# 	## If there are posts!

# 	#latest_post = latest_posts.first()
# 	#latest_post.url = latest_post.search_query.replace(' ','_')
	
# 	string_date = datetime.strftime(latest_post.created_at, "%Y-%m-%d")


# 	## For the other posts
# 	for post in latest_posts:
# 		post.url = post.search_query.replace(' ','_') + "-" + str(post.created_at.strftime(DATE_FORMAT))

# 	t	=	loader.get_template(template)
# 	c	=	{ 'single_post'         : latest_post      ,
# 			  'hashtag_modified'    : hashtag_modified , 
# 			  'string_date'         : string_date      , 
# 			  'latest_posts'        : latest_posts     , }

# 	return	HttpResponse(t.render(c))





## Function to add a new post, this is mostly for testing purposes and to keep the google search engine api at the top of my mind
def create_new_post(request):

	from apiclient.discovery import build
	import os

	search_query=request.GET.get('q')

	search_query=search_query.replace('_',' ')

	# api_key = os.environ['USELESSMUTANT_APIKEY']
	# service = build('customsearch','v1', developerKey = api_key)

	# res = service.cse().list(q=search_query ,cx=os.environ['USELESSMUTANT_CX'], searchType='image', num=1, imgType='clipart', fileType='png',safe='high')
	# res_ex = res.execute()

	i = 30

	link_info = um.google_image_search(q,i)

	#img_link=res_ex['items'][0]['link']

	img_link=link_info['link']

	#print (img_link)

	p = Post(search_query=search_query, link=img_link)
	p.save()

	return	HttpResponse('<html><body>Success!</body></html>')




## Function to add a new post, this is mostly for testing purposes and to keep the google search engine api at the top of my mind
def create_new_post_from_twitter(request):

	## The twitter stuff. 
	import twitter
	import os
	from django.shortcuts import redirect

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

	user="WantsomeChan"
	statuses = api.GetUserTimeline(screen_name=user)
	most_recent=statuses[0].text
	index=most_recent.find("#uselessmutant")

	## Get the search query
	if index == -1:
		content="Snooki"
	else:
		content=most_recent[0:most_recent.find("#uselessmutant")].strip()


	## The google stuff. 
	from apiclient.discovery import build
	import os

	#search_query=request.GET.get('q')
	#search_query=search_query.replace('_',' ')

	search_query=content

	api_key = os.environ['USELESSMUTANT_APIKEY']
	service = build('customsearch','v1', developerKey = api_key)

	res = service.cse().list(q=search_query ,cx=os.environ['USELESSMUTANT_CX'], searchType='image', num=1, imgType='clipart', fileType='png',safe='high')
	res_ex = res.execute()

	img_link=res_ex['items'][0]['link']

	#print (img_link)

	p = Post(search_query=search_query, link=img_link)
	p.save()

	#return	HttpResponse('<html><body>Success!</body></html>')	
	return redirect("index")





# Other function ideas
def	instagram(request):
	return	HttpResponse(
		"Here is today's useless mutant as decided by instagram. Want to go back to the main page? <a href='/'>Back Home</a>"
		)

def	twitter(request):
	return	HttpResponse(
		"Here is today's useless mutant as decided by twitter. Want to go back to the main page? <a href='/'>Back Home</a>"
		)

def	better(request):
	t = loader.get_template('better_mutant.html')
	c = {'current_time': datetime.now(), }
	return HttpResponse(t.render(c))