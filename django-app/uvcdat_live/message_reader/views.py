
from django.http import HttpResponse
from django.template import RequestContext, loader
#from exploratory_analysis.models import Diags
import json
import sys 



#Home page view...nothing fancy here just points to the view located at index.html
#corresponds with url: http://<host>/exploratory_analysis
def index(request):
    
 
    template = loader.get_template('message_reader/index.html')

    context = RequestContext(request, {
        'username' : 'jfharney',
    })

    return HttpResponse(template.render(context))




def messages(request):
    
    
    
    print 'in tree bookmarks...request method: ' + request.method
    
    if request.method == 'POST':
        
        '''
        tree_cache_url = request.POST['tree_cache_url']
        
        tree_bookmark_record = Tree_Bookmarks(
                                              tree_bookmark_name=tree_bookmark_name,
                                              tree_bookmark_datasetname=tree_bookmark_datasetname,
                                              tree_bookmark_realm=tree_bookmark_realm,
                                              tree_bookmark_username=tree_bookmark_username,
                                              tree_bookmark_variables=tree_bookmark_variables,
                                              tree_bookmark_times=tree_bookmark_times,
                                              tree_bookmark_sets=tree_bookmark_sets,
                                              tree_bookmark_description=tree_bookmark_description,
                                              tree_cache_url=tree_cache_url
                                              )
        
        tree_bookmark_record.save()
        '''
        print 'POST'
        
        return HttpResponse()
        
        
    elif request.method == 'GET':
        
        print 'GET'
        
        #tree_bookmark_name = request.GET.get('tree_bookmark_name')
        
        return HttpResponse() 
        
        '''
        try:
            tree_bookmark_record = Tree_Bookmarks.objects.get(tree_bookmark_name=tree_bookmark_name,
                                      tree_bookmark_datasetname=tree_bookmark_datasetname,
                                      tree_bookmark_realm=tree_bookmark_realm,
                                      tree_bookmark_username=tree_bookmark_username)
    
            #print tree_bookmark_record.tree_cache_url
            data =  { 
                     'tree_bookmark_name' : tree_bookmark_record.tree_bookmark_name, 
                     'tree_bookmark_datasetname' : tree_bookmark_record.tree_bookmark_datasetname, 
                     'tree_bookmark_realm' : tree_bookmark_record.tree_bookmark_realm, 
                     'tree_bookmark_username' : tree_bookmark_record.tree_bookmark_username,
                     'tree_bookmark_variables' : tree_bookmark_record.tree_bookmark_variables, 
                     'tree_bookmark_times' : tree_bookmark_record.tree_bookmark_times, 
                     'tree_bookmark_sets' : tree_bookmark_record.tree_bookmark_sets, 
                     'tree_bookmark_description' : tree_bookmark_record.tree_bookmark_description,
                     'tree_cache_url' : tree_bookmark_record.tree_cache_url
                     }
            print 'DATA:',repr(data)
            data_string = json.dumps(data,sort_keys=True,indent=2)
        
            return HttpResponse(data_string)
        
    
        except:
            print "Unexpected error:"
            data =  { }
            data_string = json.dumps(data,sort_keys=True,indent=2)
            return HttpResponse(data_string)
            
        
        
        
        
        
        return HttpResponse(data_string)
        '''
 