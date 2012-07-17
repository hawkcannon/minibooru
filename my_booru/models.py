from django.db import models

# Create your models here.
class Tag(models.Model):
	name = models.CharField(max_length=128)
	creator = models.BooleanField()
	series = models.BooleanField()
	
	def save(self):
		if(self.creator and self.series):
			raise ModelValidationError, "a tag cannot be both a creator and a series"
		else:
			super(Tag, self).save()
	
class Post(models.Model):
	RATING_SAFE = 0
	RATING_QUESTIONABLE = 1
	RATING_EXPLICIT = 2

	tags = models.ManyToManyField(Tag)
	path = models.CharField(max_length=256)
	rating = models.IntegerField()
	source = models.CharField(max_length=256)
	
	def save(self):
		if(self.rating > 2):
			raise ModelValidationError, "rating must be RATING_SAFE, RATING_QUESTIONABLE, or RATING_EXPLICIT"
		else:
			super(Post, self).save()