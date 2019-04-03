from django.db import models
from datetime import datetime
from django.contrib.postgres.fields import JSONField

from django.core.files import File
from urllib.request import urlopen, urlretrieve
from tempfile import NamedTemporaryFile
import mimetypes


class Hashtag(models.Model):
	created_at           = models.DateTimeField(default = datetime.utcnow)
	last_post_added_time = models.DateTimeField(default = datetime.utcnow)
	name                 = models.CharField(max_length=100)
	enabled              = models.BooleanField(default=True)

	def	__str__(self):
		return	"{0}\n".format(self.name)


# Create your models here.
class Post(models.Model):
	created_at     =  models.DateTimeField(default=datetime.utcnow)
	search_query   =  models.TextField() #CharField(max_length=100)
	search_query_raw = models.TextField() #CharField(max_length=100)
	link           =  models.URLField()
	image          =  models.ImageField(upload_to="images", blank=True, null=True)
	#hashtag_name        =  models.CharField(max_length=100)
	
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

	#def	__str__(self):
	#	return	self.search_query

	def	__str__(self):
		return	"{0} - {1}\n".format(self.created_at, self.search_query)
	

	def save(self, *args, **kwargs):
		

		if self.link and not self.image:
			
			response = urlopen(self.link)
			#content_type = response.headers['content-type']
			content_type = response.info().get_content_subtype()
			#extension = mimetypes.guess_extension(content_type)
			extension = content_type

			img_temp = NamedTemporaryFile(delete=True)
			img_temp.write(response.read())
			img_temp.flush()

			self.image.save("image_{}-{}.{}".format(self.search_query[:50], 
													datetime.strftime(self.created_at,"%Y%m%d%H%M%S%f"), 
													extension) ,
					       	File(img_temp),)

		super().save(*args, **kwargs)  # Call the "real" save() method.

		

	# Will probably use JSON field for storing the stats
	# https://docs.djangoproject.com/en/2.0/ref/contrib/postgres/fields/#django.contrib.postgres.fields.JSONField
	##stats = models.JSONField()
