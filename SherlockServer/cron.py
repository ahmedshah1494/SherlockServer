from django.core.files.storage import FileSystemStorage

def extractFeatures():
	fs = FileSystemStorage()
	files = fs.listdir()
	wavs = filter(lambda x: x.split('.')[-1] = 'wav', files)
	files = filter(lambda x: x+'.mfcc64ms' not in files and 
							x+'.stft' not in files, wavs)
	print files