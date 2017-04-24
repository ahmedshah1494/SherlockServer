import GMMTest as gmm
import os
from django.conf import settings
from sklearn.externals import joblib
import numpy as np

def classifyAudio(files):
	gmmDir = os.path.join(settings.GMM_ROOT, 'withSannan_64ms/')
	dirs = filter(lambda x: os.path.isdir(os.path.join(gmmDir,x)), os.listdir(gmmDir))
	res = {}
	for d in dirs:
		res[d] = gmm.testFiles(files, 64, os.path.join(gmmDir,d+'/fold_0'))
	return res

def calculateConf(obs, pOgR, pOgnR, alpha):
	score_pOgR = reduce(lambda x,y: x*y, map(np.exp, pOgR.score_samples(obs)))
	score_pOgnR = reduce(lambda x,y: x*y, map(np.exp, pOgnR.score_samples(obs)))
	print score_pOgR, score_pOgnR
	return score_pOgR/((alpha * score_pOgnR) + score_pOgR)

def getConfs(scores):
	scores2 = {}
	# print scores
	for ins in scores:
		for c in ins:
			llr = [float(ins[c][0]) - float(ins[c][1])]
			if scores2.get(c) == None:
				scores2[c] = []
			scores2[c].append(llr)

	confVals = {}
	for c in scores2:
		with open(os.path.join(settings.GMM_ROOT,'forConfidenceCalc/audio/%s/pOgR.pkl'%c), 'rb') as f:
			pOgR = joblib.load(f)

		with open(os.path.join(settings.GMM_ROOT,'forConfidenceCalc/audio/%s/pOgnR.pkl'%c), 'rb') as f:
			pOgnR = joblib.load(f)

		confVals[c] = calculateConf(scores2[c],pOgR,pOgnR,4)
	return confVals
# getConfs([{u'P': [u'-21663.6122799', u'-19747.8544947'], u'SH': [u'-17309.1476082', u'-19152.8812884'], u'BH': [u'-15632.16797', u'-20334.4079489'], u'O': [u'-25966.5485246', u'-18606.1858075'], u'BR': [u'-15117.5250944', u'-20140.8052484']}, {u'P': [u'-21669.6971475', u'-19741.7548633'], u'SH': [u'-17287.8566809', u'-19110.9185025'], u'BH': [u'-15593.0619023', u'-20314.1962622'], u'O': [u'-26014.5373615', u'-18598.9937777'], u'BR': [u'-15024.9321941', u'-20139.5637948']}, {u'P': [u'-21638.2107726', u'-19714.6427696'], u'SH': [u'-17255.0856264', u'-19088.186651'], u'BH': [u'-15564.9728549', u'-20286.3954617'], u'O': [u'-25975.2479731', u'-18567.9857939'], u'BR': [u'-14999.240475', u'-20111.8827824']}, {u'P': [u'-22610.7498101', u'-20546.422479'], u'SH': [u'-17956.0151205', u'-19830.0473961'], u'BH': [u'-16156.7224868', u'-21139.2959782'], u'O': [u'-27246.1251155', u'-19381.0980846'], u'BR': [u'-15552.3092553', u'-20980.2702817']}])
