from django.core.files.storage import FileSystemStorage
from SherlockServer.models import *
from mfcc import *
import scipy.io.wavfile as wav
import numpy as np
from django.core.files import File
import FeatureExtractor as fe
import classifier
import json
from django.conf import settings

def extractFeatures():
	samples = DataSample.objects.filter(datafeature=None)
	fs = FileSystemStorage()
	for i in samples:
		ftype = i.dataType
		print ftype
		if ftype == 'audio':
			[mfcc_path, diff_path, stft_path] = fe.extractAudioFeatures(fs.path(i.dataFile.name))
			with open(mfcc_path) as ff:
				f1 = DataFeature(dataSample = i,
								featureType = 'audio-mfcc',
								featureFile = File(ff))
				f1.save()
			with open(diff_path) as ff:
				f1 = DataFeature(dataSample = i,
								featureType = 'audio-mfcc-diff',
								featureFile = File(ff))
				f1.save()
			with open(stft_path) as ff:
				f2 = DataFeature(dataSample = i,
								featureType = 'audio-stft',
								featureFile = File(ff))
				f2.save()
		if ftype == 'image':
			file_paths = fe.extractImageFeatures([fs.path(i.dataFile.name)])

def classify():
	# need to fix the condition if file is too short
	features = DataFeature.objects.filter(classificationResult=None, featureType='audio-mfcc-diff')
	files = map(lambda x: x.featureFile, features)
	print files
	res = classifier.classifyAudio(files)
	print res
	for i in range(len(files)):
		perFileRes = {}
		for c in res:
			perFileRes[c] = res[c][i]
		if None in perFileRes.values():
			sample = DataSample.objects.get(datafeature=features[i])
			sample.delete()
			features[i].delete()
		else:	
			features[i].classificationResult = json.dumps(perFileRes)
			features[i].save()
	print res

def updateConfidence():
	locations = Location.objects.all()
	for loc in locations:
		features = DataFeature.objects.filter(dataSample__location=loc).exclude(classificationResult = None)
		if len(features) > 0:
			scores = map(lambda x: json.loads(x.classificationResult),features)
			res = classifier.getConfs(scores)
			loc.labelConfidenceVals = res
			loc.save()
			print res




