from django.core.management.base import BaseCommand
class Command(BaseCommand):
    help = "This command doesn't take any arguments. It loops through all the ACTIVE hashtags and tries to create a post for it"
    def handle(self, *args, **options):

    	## I tried making the timezones not nieve and now of course they are slightly different than 
    	## the timezones before. I'll probably just end up deleting all the old posts and see what the deal is
    	from collections import Counter
    	import random, datetime
    	from useless_mutant.models import Post, Hashtag
    	import useless_mutant.useless_module as um
    	#from datetime import datetime, timezone

    	MAX_NUM_RESULT = 100

    	active_hashtags = Hashtag.objects.filter(enabled = True)

    	for hashtag in active_hashtags:

    		## Not sure where to put it but I want to put this try except somewhere and let it fail three times
    		## before moving on
    		#urllib.error.HTTPError: HTTP Error 403: Forbidden

    		self.stdout.write("Starting to create a post for "+str(hashtag.name))

    		c = um.tally_twitter_votes(hashtag.name)
    		# If there are no votes than don't create a post!
    		if c == Counter():
    			self.stdout.write("There are no votes to create a post")
    			continue
    		
    		most_popular_tuple = c.most_common(1)[0]
    		most_popular_vote = most_popular_tuple[0]
    		most_popular_count= most_popular_tuple[1]

    		if most_popular_count == 1:
    			self.stdout.write("No one rose above the rest")
    			continue

    		q_raw=most_popular_vote

    		## I should probably do some more work here to take out chars that can't be in URLs
    		q = q_raw.replace('\n',' ')
    		q = q.replace('?', '')
    		q = q.replace('"', '')

    		## Can I import the value of MAX_NUM_RESULT to this sheet?
    		i = random.randrange(0,MAX_NUM_RESULT)

    		link_info = um.google_image_search(q,i)

    		if 'error' in link_info.keys():
    			self.stdout.write("The search query: "+str(q)+" did not return any results")
    			continue

    		img_link=link_info['link']

    		h, h_created_tf = Hashtag.objects.get_or_create(name = hashtag.name)

    		if not h_created_tf:
    			h.last_post_added_time=datetime.datetime.now(datetime.timezone.utc)
    			#datetime.datetime.utcnow()


    		h.save()

    		p = Post(	search_query 		=	q 												, 
    					search_query_raw	=	q_raw 											, 
    					link 				= 	img_link										, 
    					votes 				= 	most_popular_count 								, 
    					hashtag 			= 	h 												,
    					created_at			=	datetime.datetime.now(datetime.timezone.utc)	, 	)

    		p.save()

    		self.stdout.write("Successfully created a post with: "+str(q))

    	#self.stdout.write("Finished "+hashtag.name)


