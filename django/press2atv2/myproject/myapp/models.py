from django.db import models

# Create your models here.
class User(models.Model):
	code =  models.CharField(max_length = 200)
	email = models.CharField(max_length = 100)
	password = models.CharField(max_length = 20)
	birth_date = models.DateTimeField()

class Profile(models.Model):
	name = models.CharField(max_length = 100)

	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="profiles")
	relationship = models.ManyToManyField("self")

class Reaction(models.Model):
	REACTION_TYPE_CHOICES  = (
		('LIKE', 'like'), 
		('LOVE', 'love'), 
		('LAUGH', 'laugh'), 
		('IMPRESSIVE', 'impressive'), 
		('SAD', 'sad'), 
		('ANGRY', 'angry')
	)
	
	reaction_type = models.CharField(max_length=2, choices=REACTION_TYPE_CHOICES, default='LIKE')
	profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name = "reactions")

class Post(models.Model):
	text = models.CharField(max_length = 255)
	created_date = models.DateTimeField(auto_now_add=True)

	profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name = "posts")
	reactions = models.ManyToManyField(Reaction, through='PostReaction')

class Comment(models.Model):
	text = models.CharField(max_length = 255)
	created_date = models.DateTimeField(auto_now_add=True)

	profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name = "comments")
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name = "comments")

class PostReaction(models.Model):
	weight = models.IntegerField()
	created_date = models.DateTimeField(auto_now_add=True)

	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	reaction = models.ForeignKey(Reaction, on_delete=models.CASCADE) 

def get_date(day, month, year):
	from django.utils import timezone
	import datetime, pytz
	return datetime.datetime(year, month, day, tzinfo=pytz.UTC)