import os
import numpy as np
from sklearn import mixture
import pickle
import sys

def loadGMM(gmmFile):
	gmm = pickle.load(open(gmmFile,'rb'))
	gmm.covars_ = np.load(gmmFile+'_01.npy')
	gmm.weights_ = np.load(gmmFile+'_02.npy')
	gmm.means_ = np.load(gmmFile+'_03.npy')
	return gmm

def testFiles(files, ncomps ,gmmFileDir):
	gmm_P = loadGMM(gmmFileDir+"/P/"+str(ncomps)+"/sklearnGMM.pkl")
	gmm_N = loadGMM(gmmFileDir+"/N/"+str(ncomps)+"/sklearnGMM.pkl")
	print 'reading filelist:', files

	'compiling data'
	alldata = None
	
	results = []
	for i in range(len(files)):
		#print "reading ", fl
		fl = files[i]
		fl = fl.strip()

		if fl.split('.')[-1] == 'npy':
			data = np.load(fl.strip())
		else:
			data = np.loadtxt(fl.strip())

		data_f = np.array(filter(lambda x: not np.isnan(np.sum(x)), data))

		if data.shape[0] < 80:
		    results.append(None)
		if len(data_f.shape) != 2:
			data_f = np.zeros((80,40))
		ll_P = sum(gmm_P.score(data_f))
		ll_N = sum(gmm_N.score(data_f))
		P_P = ll_P
		P_N = ll_N
		
		label = int(ll_P > ll_N)
		results.append([str(P_P), str(P_N)])
	return results
if __name__ == "__main__":
    if len(sys.argv) < 6:
        sys.exit()
    if len(sys.argv) == 6:
    	print "HELLO"
        testFiles(sys.argv[1],int(sys.argv[2]),sys.argv[3],sys.argv[4],sys.argv[5])
    else:
        print "arg1 - in file list, arg2 - nComp, arg3 - output file, argv4-actaul label, argv5-gmm output Folder"
        sys.exit()

# testFiles('../files/folds/BR/BR_p.fold0', '../GMMs/BR/fold_0/', 1, "test_result.txt")
