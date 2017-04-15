from __future__ import unicode_literals

from django.db import models

# Create your models here.
class DataSample(models.Model):
	location = models.ForeignKey('Location', 
					on_delete=models.CASCADE)
	dataType = models.CharField(max_length=42)
	dataFile = models.FileField()
	createdAt = models.DateTimeField(auto_now_add=True)

class Location(models.Model):
	name = models.CharField(max_length=42)
	labelConfidenceVals = models.TextField(null=True)


