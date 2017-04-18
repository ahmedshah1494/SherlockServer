from django.shortcuts import render
import django.contrib.staticfiles
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from django.core.files import File
from SherlockServer.models import *
import json
from mimetypes import guess_type
# Create your views here.

def home(request):
	return render(request,'home.html')

@csrf_exempt
def receiveSample(request):
	if request.method == 'POST':
		files = request.FILES
		if len(files) > 0:
			desc = json.loads(request.POST['description'])
			fs = FileSystemStorage()
			for fname in files:
				f = files[fname]
				loc = Location.objects.filter(name=desc['location'])
				if len(loc) == 0:
					loc = Location(name=desc['location'])
					loc.save()
				else:
					loc = loc[0]
				dtype = guess_type(f.name)[0].split('/')[0]	
				ds = DataSample(location=loc,
							dataType=dtype,
							dataFile=File(f))
				ds.save()

	return render(request,'home.html')