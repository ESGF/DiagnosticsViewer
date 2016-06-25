
import json

def variableListHelper1(request):
    #print 'in variable list helper1'
    
    
    #variables = ['BTRAN','NPP','TLAI']
  
    variables = ["TLAI","GPP","NEE","HR","ER","NPP","QVEGT","QVEGE","QSOIL","GROSSNMIN"]
  
    data =  { 'variables' : variables }
    data_string = json.dumps(data,sort_keys=True,indent=2)

    jsonStr = json.loads(data_string)

    return data_string
    #return HttpResponse(data_string)


def variableListHelper(request,dataset_id):
    #print 'in variable list helper'
    
    #dataset_id = 'dataset1'
    if(dataset_id == None):
        dataset_id = 'dataset1' 
  
    #if(dataset_id == 'dataset3'):
    #    variables = ['AR','BTRAN','CWDC','DEADCROOTC','DEADSTEMC','ER','FROOTC','FSDS','GPP','HR','LIVECROOTC','LIVESTEMC','NEE','NPP','PCO2', 'RAIN', 'TBOT', 'TLAI', 'TOTECOSYSC', 'TOTLITC','TOTSOMC','TOTVEGC', 'WOODC'    ]
    #else:
    #    variables = ['ALL', 'AR','BTRAN','CWDC','DEADCROOTC','DEADSTEMC','ER','FROOTC','FSDS','GPP','HR','LIVECROOTC','LIVESTEMC','NEE','NPP','PCO2', 'RAIN', 'TBOT', 'TLAI', 'TOTECOSYSC', 'TOTLITC','TOTSOMC','TOTVEGC', 'WOODC'    ]
    #Shared variables
    variables = ['BTRAN','NPP','TLAI']
  
    data =  { 'dataset_id' : dataset_id, 'variables' : variables }
    #print 'DATA:',repr(data)
    data_string = json.dumps(data,sort_keys=True,indent=2)
    #print 'JSON:',data_string
    #data_string = json.dumps(data,sort_keys=False,indent=2)
    #print 'JSON:',data_string

    jsonStr = json.loads(data_string)

    return data_string
    #return HttpResponse(data_string)

 