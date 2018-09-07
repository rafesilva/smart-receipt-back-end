from django.db import models

class Image(models.Model):
  	image = models.FileField(blank=False, null=False)
  	query = models.CharField(max_length=20)
  	timestamp = models.DateTimeField(auto_now_add=True)