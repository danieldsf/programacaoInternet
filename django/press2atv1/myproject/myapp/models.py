from django.db import models

# Create your models here.
class Blog(models.Model):
	name = models.CharField(max_length = 50)

class Entry(models.Model):
	headline = models.CharField(max_length = 60)
	body_text = models.CharField(max_length = 255)
	pub_date = models.DateTimeField(auto_now_add=True)
	blog = models.ForeignKey(Blog, on_delete=models.CASCADE)

