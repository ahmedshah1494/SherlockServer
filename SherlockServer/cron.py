from django.core.files.storage import FileSystemStorage
from SherlockServer.models import *
from mfcc import *
import scipy.io.wavfile as wav
import numpy as np
from mimetypes import guess_type
from django.core.files import File
def extractFeatures():
	mfc = MFCC(nfilt=20, ncep=20,
                 lowerf=50, upperf=15000, alpha=0.97,
                 samprate=44100, frate=(1/0.032), wlen=0.064,
                 nfft=512)
	samples = DataSample.objects.filter(dataFeature=None)
	for i in samples:
		(rate,sig) = wav.read(i.name)
		mfccs = mfc.sig2s2mfc(sig)
		stft = np.exp(mfc.sig2logspec(sig))
		np.savetxt(i.name+'.mfcc64ms', mfccs)
		np.savetxt(i.name+'.stft', stft)
		f1 = DataFeature(dataSample = i,
						featureType = guess_type(i.name),
						featureFile = File(open(i.name+'.mfcc64ms')))
		f1.save()
		f2 = DataFeature(dataSample = i,
						featureType = guess_type(i.name),
						featureFile = File(open(i.name+'.stft')))
		f2.save()
