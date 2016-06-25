import json


def timesHelper1(request):
    
    times = ["JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC","DJF","MAM","JJA","SON","ANN"]

    #times = ['jan','feb','mar','apr']
    
    data =  { 'times' : times }
    
    data_string = json.dumps(data,sort_keys=True,indent=2)
    
    return data_string



def timesHelper(request,variable_id):
    #print '\n\n\ntimes for variable ', variable_id
  
    #dataset_id = 'dataset1'
    if(variable_id == None):
        variable_id = 'AR' 
  
    if(variable_id == 'AR'):
        times = ['jan','feb','mar']
    else:
        times = ['april','may','june']
    
    data =  { 'variable_id' : variable_id, 'times' : times }
    print 'DATA:',repr(data)
    data_string = json.dumps(data,sort_keys=True,indent=2)
    jsonStr = json.loads(data_string)
    
    return data_string
    #return HttpResponse(data_string)