from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os
# Create your models here.
class DataSample(models.Model):
	location = models.ForeignKey('Location', 
					on_delete=models.CASCADE)
	dataType = models.CharField(max_length=42)
	dataFile = models.FileField()
	createdAt = models.DateTimeField(auto_now_add=True)
	def delete(self):
		fs = FileSystemStorage()
		if os.path.exists(fs.path(self.dataFile.name)):
			os.remove(fs.path(self.dataFile.name))
		super(DataSample,self).delete()
class DataFeature(models.Model):
	dataSample = models.ForeignKey('DataSample',
					on_delete=models.CASCADE)
	featureType = models.CharField(max_length=42)
	featureFile = models.FilePathField(path=settings.FEAT_ROOT)
	classificationResult = models.TextField(null=True)
	def delete(self):
		if os.path.exists(featureFile.path):
			os.remove(featureFile.path)
		super(DataFeature,self).delete()
class Location(models.Model):
	name = models.CharField(max_length=42)
	labelConfidenceVals = models.TextField(null=True)


