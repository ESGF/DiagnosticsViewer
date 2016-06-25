import json
import os

def timeSeriesHelper(request,cache_path):
    
    print 'in time series helper'
    
    print 'cache_path: ' + cache_path
  
    variable = request.GET.get('variable')
    
    
    if(variable == None):
         variable = 'AR'
    
    #grab the variable average json file from the cache
    average_file_path = '/Users/8xo/some_variable.json'
    
    #if not in the cache, then generate it and then put it in the cache
    if(not os.path.exists(average_file_path)):
    
        #do generations here
        
        
        #average_file_path = '/Users/8xo/software/exploratory_analysis/DiagnosticsViewer/django-app/uvcdat_live/exploratory_analysis/static/exploratory_analysis/cache/time/TLAI-avg.json'
        average_file_path = cache_path + '/time/' + 'TLAI-avg' + '.json'
        
    
    
    
    
    data = ''
    with open(average_file_path , 'r') as myfile:
        data = myfile.read().replace('\n','')
      
    jsonData = json.dumps(data)

    return jsonData


def timeSeriesHelper1(request,cache_path):
    
    print 'in time series helper'
    
    print 'cache_path: ' + cache_path
  
    variable = request.GET.get('variable')
    
    
    if(variable == None):
         variable = 'AR'
    
    #grab the variable average json file from the cache
    
    #if not in the cache, then generate it and then put it in the cache
    #if(not os.path.exists(average_file_path)):
    
        #do generations here
        
        
    average_file_path = cache_path + '/time/' + 'TLAI-avg' + '.json'
        
    
    
    
    
    data = ''
    with open(average_file_path , 'r') as myfile:
        data = myfile.read().replace('\n','')
      
    jsonData = json.dumps(data)

    return jsonData
