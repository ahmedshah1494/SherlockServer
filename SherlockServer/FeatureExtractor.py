from django.core.files.storage import FileSystemStorage
from SherlockServer.models import *
from mfcc import *
import scipy.io.wavfile as wav
import numpy as np
from django.conf import settings
import GMMTest as gmm
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

def classifyAudio(files):
	gmmDir = os.path.join(settings.PROJECT_ROOT, 'DataModels/GMMs/CMU_NUQ_handsOnly/')
	res = {}
	mfcc_files = filter(lambda x: x.split('.')[-len(mfcc_ext):] == mfcc_ext, files)
	for d in dirs:
		res[d] = gmm.testFiles(mfcc_files, 64, os.path.join(gmmDir,d+'/fold_0'))
	return res