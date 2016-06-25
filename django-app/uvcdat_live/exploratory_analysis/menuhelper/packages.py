import json

def packagesHelper1(request):

    #print 'in packageListHelper1'
    packages = ["amwg","lmwg"]
    data =  { 'packages' : packages }
    data_string = json.dumps(data,sort_keys=False,indent=2)
    print 'JSON:',data_string
    
    return data_string
    
    

