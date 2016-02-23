
# Create your views here.

from django.http import HttpResponse
from django.template import RequestContext, loader

from exploratory_analysis.models import Diags

import json

def index(request):
  print request.GET.get('q')
  template = loader.get_template('exploratory_analysis/index.html')
  context = RequestContext(request, {
    'a' : 'aaaaa',
  })
#  latest_poll_list = Poll.objects.order_by('-pub_date')[:5]
#  template = loader.get_template('polls/index.html')
#  context = RequestContext(request, {
#    'latest_poll_list' : latest_poll_list,
#  })

  return HttpResponse(template.render(context))

def ar(request):
    
  #data = open('/Users/8xo/esgfWorkspace/UVCDAT_live/WebContent/uvcdat_live/exploratory_analysis/static/exploratory_analysis/img/AR1.json')
  #jsonData = json.dumps(data)
    
  print request.GET.get('q')
  
  template = loader.get_template('exploratory_analysis/ar.html')
#  latest_poll_list = Poll.objects.order_by('-pub_date')[:5]
#  template = loader.get_template('polls/index.html')
  context = RequestContext(request, {
    'b' : 'bbbb',
  })

  return HttpResponse(template.render(context))
  #return HttpResponse(jsonData)


def datasets(request):
    
  print request.GET.get('variable')
  
  variable = ''
  if(request.GET.get('variable') == None):
      variable = 'AR'
  else:
      variable = request.GET.get('variable')
  
  file = '/Users/harris112/projects/acme-oui/diagnosticsviewer/django-app/uvcdat_live/exploratory_analysis/static/exploratory_analysis/img/' + variable + '.json' 
  #file = '/Users/csg/Desktop/uvcdat-web/DiagnosticsViewer/django-app/uvcdat_live/exploratory_analysis/static/exploratory_analysis/img/' + variable + '.json' 
  #file = '/Users/8xo/esgfWorkspace/UVCDAT_live/WebContent/uvcdat_live/exploratory_analysis/static/exploratory_analysis/img/' + variable + '.json' 
  
  print file
  
  with open(file , 'r') as myfile:
      data = myfile.read().replace('\n','')
      
  jsonData = json.dumps(data)

  #jsonData = json.dumps("{ 'variable' : '" + variable  +  "'} ")
  #print jsonData
  return HttpResponse(jsonData)




