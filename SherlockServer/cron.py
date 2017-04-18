from django.core.files.storage import FileSystemStorage
from SherlockServer.models import *
from mfcc import *
import scipy.io.wavfile as wav
import numpy as np
from django.core.files import File
import FeatureExtractor as fe
import json
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

def classify():
	features = DataFeature.objects.filter(classificationResult=None, featureType='audio_mfcc_diff')
	files = map(lambda x: x.featureFile, features)
	res = fe.classifyAudio(files)
	for i in range(len(files)):
		perFileRes = {}
		for c in res:
			perFileRes[c] = res[c][i]
		features[i].classificationResult = json.dumps(perFileRes)
		features[i].save()
	print res
