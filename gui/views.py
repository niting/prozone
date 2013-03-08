from django.http import HttpResponse
from django.template import Context, loader
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from gui.models import EventsPz
from gui.forms import LeftPanel

@login_required(login_url='/')
def index(request):
	""" The only page in the webapp is rendered by this function """
	template = loader.get_template('base.html')
	context = Context()
	if(request.method == 'POST'):
		form = LeftPanel(request.POST)
	else:
		form = LeftPanel()
	return render(request, 'base.html', {'form':form,})
@login_required(login_url='/')
def java_script(request):
    filename = request.path.strip("/")
    data = open(filename, "rb").read()
    return HttpResponse(data, mimetype="application/x-javascript")
