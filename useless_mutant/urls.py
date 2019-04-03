from django.conf.urls import url
from useless_mutant import views

urlpatterns	=	[

	# The naked url goes to index, pretty standard
	url(r'^$', views.index, name='index'),

	# The only special pages are admin and hashtags_all 
	#(that means that I can't setup those two words to be hashtags in the system)
	# So I guess I could set it up, but the hashtag index page would load something else, 
	# although specific pages in the hashtag would point at the right place. same with admin?
	# Admin is already taken care of
	url(r'^hashtags_all/$', views.hashtags_all, name = 'hashtags_all'),


	# match hashtag/post_url-created_at
	url(r'^(?P<hashtag>\w+)/(?P<post_url>[^/]+)-(?P<created_at>\d+)/$',	views.post,	name='post'),


	# if that doesn't match, check it see if it's hashtag/archive, which would show all posts
	# for that hashtag.    
	url(r'^(?P<hashtag>\w+)/archive/$', views.archive, name = 'archive'),


	# If that doesn't match, check to see if it's just a hashtag, which would show the first
	# post for that hashtag. 
	url(r'^(?P<hashtag>\w+)/$', views.post, name = 'hashtag_index'),





	# This is the special view for displaying the result of running the function that is to be scheduled to 
	# create posts. It doesn't actually need a view. 
	#url(r'^create_new_post_from_votes_twitter/(?P<hashtag>\w+)/$', views.create_new_post_from_votes_twitter, name = 'create_new_post_from_votes_twitter'),



	##########################################################
	# Sandbox
	#url(r'^instagram/', views.instagram, name='instagram'),
	#url(r'^twitter/', views.twitter, name='twitter'),
	# match create_new_post
	#url(r'^create_new_post/', views.create_new_post, name = 'create_new_post'),
	# match create_new_post from twitter
	#url(r'^create_new_post_from_twitter/', views.create_new_post_from_twitter, name = 'create_new_post_from_twitter'),



	##########################################################
	# Older
	# match mutant/#
	#url(r'^mutant/(?P<post_id>\d+)/$',	views.post,	name='post'),

]