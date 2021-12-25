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
	## Although I agree that it should. 

	## VIEWRIABLES #########################################################################	
	template 	=	'useless_mutant/hashtags_all.html'
	t 			= 	loader.get_template(template)


	## DB IO ###############################################################################
	hashtags_all 	= 	Hashtag.objects 							\
								.filter(enabled=True) 				\
								.order_by('name') 	#

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
	## Or when you get to the end of the list. 
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



#def	post(request, hashtag, post_url=None, created_at=None):
def	post(request, hashtag, hashtag_2 = None, created_at=None):

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
	if hashtag_2==None: ## If post_url is none we get the most recent post. 
		single_post = latest_posts.first()
	
	else: ## If the post_url isn't blank we need to get a specific post. 
		created_at_datetime = datetime.datetime.strptime(created_at,DATE_FORMAT)	
		#created_at_datetime = created_at_datetime - datetime.timedelta(hours=5) #Kludge

		## I have to do this because I haven't excatly figured out ms timestamps. 
		start = created_at_datetime - datetime.timedelta(seconds=1)
		end   = created_at_datetime + datetime.timedelta(seconds=1)

		try:

			single_post = Post.objects.get( hashtag = hashtag_record	 			, 
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



# Other function ideas
# def	instagram(request):
# 	return	HttpResponse(
# 		"Here is today's useless mutant as decided by instagram. Want to go back to the main page? <a href='/'>Back Home</a>"
# 		)

# def	twitter(request):
# 	return	HttpResponse(
# 		"Here is today's useless mutant as decided by twitter. Want to go back to the main page? <a href='/'>Back Home</a>"
# 		)

# def	better(request):
# 	t = loader.get_template('better_mutant.html')
# 	c = {'current_time': datetime.now(), }
# 	return HttpResponse(t.render(c))