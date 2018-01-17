from django.db import models

# Create your models here.
class User(models.Model):
	code =  models.CharField(max_length = 200)
	email = models.CharField(max_length = 100)
	password = models.CharField(max_length = 20)
	birth_date = models.DateTimeField()

class Profile(models.Model):
	name = models.CharField(max_length = 100)
	user = models.ForeignKey(User, on_delete=models.CASCADE)

class Timeline(models.Model):
	pass

class Relationship(models.Model):
	pass

class Post(models.Model):
	text = models.CharField(max_length = 255)
	created_date = models.DateTimeField()
	profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

class Comment(models.Model):
	text = models.CharField(max_length = 255)
	created_date = models.DateTimeField()
	profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
	post = models.ForeignKey(Post, on_delete=models.CASCADE)

class Reaction(models.Model):
	REACTION_TYPE_CHOICES  = (
		('LIKE', 'like'), 
		('LOVE', 'love'), 
		('LAUGH', 'laugh'), 
		('IMPRESSIVE', 'impressive'), 
		('SAD', 'sad'), 
		('ANGRY', 'angry')
	)
	
	reaction_type = models.CharField(max_length=2, choices=REACTION_TYPE_CHOICES, default=LIKE)
	created_date = models.DateTimeField(auto_now_add=True)
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
	weight = models.IntegerField()