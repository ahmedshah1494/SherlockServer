from django.core.files.storage import FileSystemStorage
from mfcc import *
import scipy.io.wavfile as wav
import numpy as np
from django.conf import settings
import GMMTest as gmm
from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage
import os

def makeDiffCoefficients(filename):
    fl_arr = np.loadtxt(filename)
    fl_arr = fl_arr.T
    if len(fl_arr.shape) < 2:
		return		
    fl2 = np.append([[0]*fl_arr.shape[1]], fl_arr, axis=0)[:-1]
    diffs = (fl_arr - fl2)
    diffFeats = np.concatenate((fl_arr, diffs), axis=1)
    np.save(filename+'.Dfeat.npy', diffFeats)
    return filename+'.Dfeat.npy'

# Extract MFCCs and STFT from wav file
# output stored in filename.mfcc64ms and filename.stft
# returns output filenames
def extractAudioFeatures(filename):
	fs = FileSystemStorage(location=settings.FEAT_ROOT)
	(rate,sig) = wav.read(filename)
	mfc = MFCC(nfilt=20, ncep=20,
                 lowerf=50, upperf=15000, alpha=0.97,
                 samprate=rate, frate=(1/0.032), wlen=0.064,
                 nfft=512)
	mfccs = mfc.sig2s2mfc(sig).T
	stft = np.exp(mfc.sig2logspec(sig)).T
	mfcc_path = fs.path(filename.split('/')[-1])+'.mfcc64ms'
	stft_path = fs.path(filename.split('/')[-1])+'.stft'
	np.savetxt(mfcc_path, mfccs)
	np.savetxt(stft_path, stft)
	diff_path = makeDiffCoefficients(mfcc_path)
	return [mfcc_path, diff_path, stft_path]

def getConcepts(json):	
	concepts = []
	resp = json['outputs']
	resp = map(lambda x: x['data'], resp)
	resp = map(lambda x: x['concepts'], resp)
	# resp = map(lambda x: map(lambda y: (y['name'],y['value']), x), resp)
	for r in resp:
		d = {}
		# map(lambda y: d[y['name']] = y['value'], r)
		for y in r:
			d[y['name']] = y['value']
		concepts.append(d)
	return concepts

def extractImageFeatures(imgs_files):
	classes = ['BH','BR','O','P','SH']
	fs = FileSystemStorage(location=settings.FEAT_ROOT)
	app = ClarifaiApp('jiBNMPUJ4QR7GT-VRDL6ZdrvfgbYRzK6jX7DQKXp','jlwJ1AKBNSN1B8205X_3oqaZLYrxOa2kL3DUKX77')
	app.auth.get_token()
	batch = 90
	sent_count = 0
	model = app.models.get('general-v1.3')
	concepts = []
	while sent_count < len(imgs_files):
		imgs = map(lambda x: ClImage(file_obj=open(x, 'rb'), image_id=x), 
						imgs_files[sent_count:min(len(imgs_files), sent_count + batch)])
		resp = model.predict(imgs)
		sent_count += min(len(imgs), sent_count + batch)
		filenames = map(lambda x: x['input']['id'], resp['outputs'])
		concepts += getConcepts(resp)

	file_paths = []
	vocabs = os.listdir(settings.VOCAB_ROOT)
	vocabs = map(lambda x: os.path.join(settings.VOCAB_ROOT,x),vocabs)
	for j in range(len(vocabs)):
		vocab = vocabs[j]
		with open(vocab, 'r') as f:
			vocab = f.readlines()

		for i in range(len(concepts)):
			fv = np.array([map(lambda x: concepts[i].get(x[:-1],0.0), vocab)])
			f_path = fs.path(imgs_files[i].split('/')[-1])+"_%s.feat"%classes[j]
			file_paths.append(f_path)
			np.savetxt(f_path, fv, fmt='%s')

	return file_paths



