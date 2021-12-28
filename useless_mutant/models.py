from django.db import models
from datetime import datetime, timezone
from django.contrib.postgres.fields import JSONField


class Hashtag(models.Model):
	created_at           = models.DateTimeField(default = datetime.utcnow)
	last_post_added_time = models.DateTimeField(default = datetime(1988,1,29,3,1,0,0,timezone.utc))
	name                 = models.CharField(max_length=100)
	enabled              = models.BooleanField(default=True)

	def	__str__(self):
		return	"{0}\n".format(self.name)


def my_upload_func(instance, filename):
    return f"images/{instance.hashtag.name}/{filename}"

# Create your models here.
class Post(models.Model):
	created_at     =  models.DateTimeField(default=datetime.utcnow)
	search_query   =  models.TextField(max_length=500) #CharField(max_length=100)
	search_query_raw = models.TextField(max_length=500) #CharField(max_length=100)
	search_query_raw_with_links = models.TextField(max_length=500) #CharField(max_length=100)
	link           =  models.URLField(max_length=500)
	image          =  models.ImageField(upload_to=my_upload_func, blank=True, null=True)
	
	hashtag    =  models.ForeignKey(Hashtag, on_delete=models.CASCADE, default=1)

	## This could be a stats dict of voting stuff
	## I'll do this later though. 
	#voting_stats   =  models.JSONField()

	votes          =  models.IntegerField(default=0)
	current_streak =  models.IntegerField(default=0)
	max_streak     =  models.IntegerField(default=0)

	## this could be stats dict of visitors to the page
	## I'll do this later though
	#pageview_stats =  models.JSONField()

	views          =  models.IntegerField(default=0)

	#upload_to = hashtag.name

	def	__str__(self):
		return	"{0} - {1}\n".format(self.created_at, self.search_query[0:50])
	
	## Future dev for stats
	# https://docs.djangoproject.com/en/2.0/ref/contrib/postgres/fields/#django.contrib.postgres.fields.JSONField
	##stats = models.JSONField()

	@property
	def short_search_query(self):
		return self.search_query if len(self.search_query) < 50 else (self.search_query[:47] + '...')


