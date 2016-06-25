from django.views.decorators.csrf import ensure_csrf_cookie
#flag for toggling connection to the diags backend
isConnected = True

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.http import HttpResponseServerError
from django.template import RequestContext, loader
#from exploratory_analysis.models import Diags
import json
import sys 

from paths import paths

from defaults import parameter_defaults

from treeviewer import treeviewer_treeex


syspath_append_uvcmetrics = paths.syspath_append_uvcmetrics
syspath_append_cdscan = paths.syspath_append_cdscan

paths_cache_dir = paths.cache_dir
#paths_front_end_cache_dir = paths.front_end_cache_dir

default_sample_data_dir = paths.default_sample_data_dir
default_tree_sample_data_dir = paths.default_tree_sample_data_dir
default_map_sample_data_dir = paths.default_map_sample_data_dir

img_cache_path = paths.img_cache_path

timeseries_cache_path = paths.timeseries_cache_path

generated_img_path = paths.generated_img_path

# import the diags code
if isConnected:
    sys.path.append(syspath_append_uvcmetrics)
    sys.path.append(syspath_append_cdscan)
   
    print 'sys.path: ' + str(sys.path)
    
    from metrics.frontend.options import Options
    from metrics.computation.reductions import *
    from metrics.fileio.filetable import *
    from metrics.fileio.findfiles import *
    from metrics.packages.diagnostic_groups import *

    from metrics.exploratory.treeview import TreeView 
    from metrics import *

    from metrics.packages.diagnostic_groups import *
    from metrics.frontend.options import *
    import metrics.frontend.defines as defines

cache_dir = paths_cache_dir
#front_end_cache_dir = paths_front_end_cache_dir#'../../../static/cache/'


#use these objects temporarily
print '\nsetting up figures store\n'
figures_store = {}

    
from django.http import HttpResponseRedirect


def celery_test(request,user_id):
    
    import sys
#    sys.path.append('/Users/8xo/software/exploratory_analysis/DiagnosticsViewer/django-app/uvcdat_live/exploratory_analysis')
#    print 'sys.path: ' + str(sys.path)
    
    #from proj import tasks
    #import tasks
    
    from tasks import add
    
    print 'in celery_test new\n'
    
    add.delay(str(request.body),user_id)
    
    return HttpResponse('celery_test_new\n')

def base_facets(request,user_id):
    
    
    import urllib2
    import urllib
    esgf_hostname = paths.esgf_hostname
    esgf_port = paths.esgf_port
    
    url = "http://" + esgf_hostname + ":" + esgf_port + "/acme_services/publishing/base_facets/" + user_id
    
    #curl -X GET http://localhost:8082/groups/base_facets/jfharney
    
    print 'calling base facets url = ' + url
      
    data = urllib2.urlopen(url).read()

    data_json = json.loads(data)
    
    for key in data_json:
        print 'key: ' + str(key)
    
    
    data_string = json.dumps(data_json,sort_keys=False,indent=2)
    
    return HttpResponse(data_string)


def has_publish_role(request,user_id):
    
    ###Insert logic for inspecting the certificate here
    
    data_string = "true"
    
    return HttpResponse(data_string)


def publish(request,user_id):
    
    print 'ABOUT TO PUBLISH'
    
    
    import sys
#    sys.path.append('/Users/8xo/software/exploratory_analysis/DiagnosticsViewer/django-app/uvcdat_live/exploratory_analysis')
#    print 'sys.path: ' + str(sys.path)
    
    #from proj import tasks
    #import tasks
    
    from tasks import add
    
    print 'in celery_test\n'
    
    add.delay(str(request.body),user_id)
    
    return HttpResponse('celery_test -- new\n')

    
    '''
    
    print 'request.body: ' + str(request.body)
    
    json_data = json.loads(request.body)
    
    for key in json_data:
        print 'key: ' + key + ' value: ' + json_data[key]
    
    import urllib2
    import urllib
    
    esgf_hostname = paths.esgf_hostname
    esgf_port = paths.esgf_port

    print 'esgf_hostname: ' + esgf_hostname
    print 'esgf_port: ' + esgf_port
    
    payload = {'project': 'ACME', 
               'data_type': 'climo',
               'regridding' : 'bilinear',
               'realm' : 'atm',
               'experiment' : 'B1850C5e1_ne30',
               'range' : 'all',
               'versionnum' : 'v0_1' }
    
    username = user_id
    
    
#<<<<<<< HEAD
#    url = 'http://esg.ccs.ornl.gov:7070/acme_services/publishing/publish_data/jfharney/'
#=======
    url = 'http://' + esgf_hostname + ':' + esgf_port + '/acme_services/publishing/publish_data/' + username
#>>>>>>> e1c67acadc611939499b3f9587750edfa20acd62
    
    print 'sending to url: ' + str(url) 
    
    
    # This urlencodes your data (that's why we need to import urllib at the top)
    data = urllib.urlencode(payload)

    # Send HTTP POST request
    request = urllib2.Request(url, data)

    response = urllib2.urlopen(request)
 
    html = response.read()
    
    '''
    
    
    
    
    
    
    '''
    r = requests.post(url, data=payload)
    
    print(r.status_code, r.reason)
    
    
    
    
    #url = "http://" + 'localhost' + ":" + '8082' + "/groups/publish/" + user_id
    
    # Prepare the data
    query_args = { 'q':'query string', 'foo':'bar' }

    # This urlencodes your data (that's why we need to import urllib at the top)
    data = urllib.urlencode(query_args)

    # Send HTTP POST request
    request = urllib2.Request(url, data)

    response = urllib2.urlopen(request)
 
    html = response.read()
    '''
    
    
    
    return HttpResponse('success')



def core_parameters(request):
    
    data = {}
    
    data['host'] = paths.ea_hostname
    
    data_string = json.dumps(data,sort_keys=False,indent=2)
    
    return HttpResponse(data_string)

#Service API for the Dataset_Access table
#GET
#http://<host>:<port>/exploratory_analysis/group_dataset/<group>
#POST
#echo '{ "dataset" :  <dataset_name> }' | curl -d @- 'http://<host>:<port>/exploratory_analysis/group_dataset/<group>/' -H "Accept:application/json" -H "Context-Type:application/json"
#DELETE
#http://<host>:<port>/exploratory_analysis/group_dataset/<group>/
def dataset_packages(request,dataset_name):
    
    from exploratory_analysis.models import Packages
        
    if request.method == 'POST':
        
        print '\nIn POST\n'  
        
        #load the json object
        json_data = json.loads(request.body)
            
        #grab the dataset added
        packages = json_data['packages'] #should be a string
        
        #grab the record with the given dataset_name
        da = Packages.objects.filter(dataset_name=dataset_name)
        
        new_dataset_list = ''
        if da:
            #delete the record and rewrite the record with the new dataset list
            da.delete()
        
        
        all = Packages.objects.all()
        
        dataset_packages_record = Packages(
                                                  dataset_name=dataset_name,
                                                  packages=packages
                                                  )
            
        #save to the database
        dataset_packages_record.save()
        
        all = Packages.objects.all()
        
        
        return HttpResponse("POST Done\n")

    elif request.method == 'GET':
        
        print '\nIn GET\n'  
        
        #grab the record with the given dataset_name
        da = Packages.objects.filter(dataset_name=dataset_name)
        
        if not da:
            data = {'packages' : ''}
            data_string = json.dumps(data,sort_keys=False,indent=2)
            return HttpResponse(data_string + "\n")
       
        #otherwise grab the contents and return as a list
        #note: da[0] is the only record in the filtering of the Dataset_Access objects
        dataset_list = []
        
        for dataset in da[0].packages.split(','):
            dataset_list.append(dataset)
            
        data = {'packages' : dataset_list}
        data_string = json.dumps(data,sort_keys=False)#,indent=2)

        print("GET Done\n")
        return HttpResponse(data_string)# + "\n")
        
    
    elif request.method == 'DELETE':
        
        print '\nIn DELETE\n'    
        
        #not sure if this is the right behavior but this will delete the ENTIRE record given the group
        #grab the group record
        da = Packages.objects.filter(dataset_name=dataset_name)
        
        if da:
            da.delete()
        
        all = Packages.objects.all()
        
        return HttpResponse("DELETE Done\n")

    else:
        return HttpResponse("Error\n")

#Service API for the Dataset_Access table
#GET
#http://<host>:<port>/exploratory_analysis/group_dataset/<group>
#POST
#echo '{ "dataset" :  <dataset_name> }' | curl -d @- 'http://<host>:<port>/exploratory_analysis/group_dataset/<group>/' -H "Accept:application/json" -H "Context-Type:application/json"
#DELETE
#http://<host>:<port>/exploratory_analysis/group_dataset/<group>/
#Schema for "Published":
#dataset_name | published_state ( ) 
def dataset_published(request,dataset_name):
    
    from exploratory_analysis.models import Published
        
    if request.method == 'POST':
        
        print '\nIn POST - dsname: ', dataset_name
        
        #load the json object
        json_data = json.loads(request.body)
            
        #grab the dataset added
        published = json_data['published'] #should be a string
        
        print 'published state: ' + published
        
        #grab the record with the given dataset_name
        da = Published.objects.filter(dataset_name=dataset_name)
        
        new_dataset_list = ''
        if da:
            #delete the record and rewrite the record with the new dataset list
            da.delete()
        
        
        all = Published.objects.all()
        
        dataset_published_record = Published(
                                                  dataset_name=dataset_name,
                                                  published=published
                                                  )
            
        #save to the database
        dataset_published_record.save()
        
        all = Published.objects.all()
        
        
        return HttpResponse("POST Done\n")

    elif request.method == 'GET':
        
        print '\nIn GET\n'  
        
        #grab the record with the given dataset_name
        da = Published.objects.filter(dataset_name=dataset_name)
        
        if not da:
            data = {'published' : ''}
            data_string = json.dumps(data,sort_keys=False,indent=2)
            return HttpResponse(data_string + "\n")
       
        #otherwise grab the contents and return as a list
        #note: da[0] is the only record in the filtering of the Dataset_Access objects
        dataset_list = []
        
        for dataset in da[0].published.split(','):
            dataset_list.append(dataset)
            
        data = {'published' : dataset_list}
        data_string = json.dumps(data,sort_keys=False)#,indent=2)

        print("GET Done\n")
        return HttpResponse(data_string)# + "\n")
        
    
    elif request.method == 'DELETE':
        
        print '\nIn DELETE\n'    
        
        #not sure if this is the right behavior but this will delete the ENTIRE record given the group
        #grab the group record
        da = Published.objects.filter(dataset_name=dataset_name)
        
        if da:
            da.delete()
        
        all = Published.objects.all()
        
        return HttpResponse("DELETE Done\n")

    else:
        return HttpResponse("Error\n")

#Service API for the Dataset_Access table
#GET
#http://<host>:<port>/exploratory_analysis/group_dataset/<group>
#POST
#echo '{ "dataset" :  <dataset_name> }' | curl -d @- 'http://<host>:<port>/exploratory_analysis/group_dataset/<group>/' -H "Accept:application/json" -H "Context-Type:application/json"
#DELETE
#http://<host>:<port>/exploratory_analysis/group_dataset/<group>/
def dataset_variables(request,dataset_name):
    
    from exploratory_analysis.models import Variables
        
    if request.method == 'POST':
        
        print '\nIn POST\n'  
        
        #load the json object
        json_data = json.loads(request.body)
            
        #grab the dataset added
        variables = json_data['variables'] #should be a string
        
        #grab the record with the given dataset_name
        da = Variables.objects.filter(dataset_name=dataset_name)
        
        new_dataset_list = ''
        if da:
            #delete the record and rewrite the record with the new dataset list
            da.delete()
        
        
        all = Variables.objects.all()
        
        dataset_variables_record = Variables(
                                                  dataset_name=dataset_name,
                                                  variables=variables
                                                  )
            
        #save to the database
        dataset_variables_record.save()
        
        all = Variables.objects.all()
        
        
        return HttpResponse("POST Done\n")

    elif request.method == 'GET':
        
        print '\nIn GET\n'  
        
        #grab the record with the given dataset_name
        da = Variables.objects.filter(dataset_name=dataset_name)
        
        if not da:
            data = {'variables' : ''}
            data_string = json.dumps(data,sort_keys=False,indent=2)
            return HttpResponse(data_string + "\n")
       
        #otherwise grab the contents and return as a list
        #note: da[0] is the only record in the filtering of the Dataset_Access objects
        dataset_list = []
        
        for dataset in da[0].variables.split(','):
            dataset_list.append(dataset)
            
        data = {'variables' : dataset_list}
        data_string = json.dumps(data,sort_keys=False)#,indent=2)

        print("GET Done\n")
        return HttpResponse(data_string)# + "\n")
        
    
    elif request.method == 'DELETE':
        
        print '\nIn DELETE\n'    
        
        #not sure if this is the right behavior but this will delete the ENTIRE record given the group
        #grab the group record
        da = Variables.objects.filter(dataset_name=dataset_name)
        
        if da:
            da.delete()
        
        all = Variables.objects.all()
        
        return HttpResponse("DELETE Done\n")

    else:
        return HttpResponse("Error\n")


#Models table has the form
#group_name  |   dataset_list
#where dataset_list is a comma separated text blob
def group_dataset(request,group_name):
    
    from exploratory_analysis.models import Dataset_Access
        
    if request.method == 'POST':
    
        print '\nPOSTING new Dataset\n'    
    
        #load the json object
        json_data = json.loads(request.body)
            
        #grab the dataset added
        dataset = json_data['dataset'] #should be a string
    
        #grab the group record
        da = Dataset_Access.objects.filter(group_name=group_name)
        
        #append dataset to the end of the dataset list
        
        new_dataset_list = ''
        if da:
            new_dataset_list = da[0].dataset_list
            new_dataset_list = new_dataset_list + ',' + dataset
        else:
            new_dataset_list = dataset
        
        
        #update the record
        #delete the record and rewrite the record with the new dataset list
        da.delete()
        
        
        all = Dataset_Access.objects.all()
        
        
        dataset_access_record = Dataset_Access(
                                                  group_name=group_name,
                                                  dataset_list=new_dataset_list
                                                  )
            
        #save to the database
        dataset_access_record.save()
        
        all = Dataset_Access.objects.all()
        
        print '\nEND POSTING new Dataset\n'    
    
        return HttpResponse("POST Done\n")
    
    elif request.method == 'GET':

        print '\nIn GET\n'    
        
        #grab the group record
        da = Dataset_Access.objects.filter(group_name=group_name)
        
        #if the dataset list is empty then return empty list
        if not da:
            data = {'dataset_list' : ''}
            data_string = json.dumps(data,sort_keys=False,indent=2)
            return HttpResponse(data_string + "\n")
        
        #otherwise grab the contents and return as a list
        #note: da[0] is the only record in the filtering of the Dataset_Access objects
        dataset_list = []
        
        for dataset in da[0].dataset_list.split(','):
            dataset_list.append(dataset)
            
        data = {'dataset_list' : dataset_list}
        data_string = json.dumps(data,sort_keys=False,indent=2)

        return HttpResponse(data_string + "\n")
    
    elif request.method == 'DELETE':

        print '\nIn DELETE\n'    
        
        #not sure if this is the right behavior but this will delete the ENTIRE record given the group
        #grab the group record
        da = Dataset_Access.objects.filter(group_name=group_name)
        
        da.delete()
        
        all = Dataset_Access.objects.all()
        
        return HttpResponse("DELETE Done\n")

    return HttpResponse('DeleteError')    



  ############
  #Page views#
  ############

#Home page view...nothing fancy here just points to the view located at index.html
#corresponds with url: http://<host>/exploratory_analysis
def index(request):
    
    print request.GET.get('q')
    
    template = loader.get_template('exploratory_analysis/index.html')

    context = RequestContext(request, {
        'username' : 'jfharney',
    })

    return HttpResponse(template.render(context))




#Home page view...nothing fancy here just points to the view located at index.html
#corresponds with url: http://<host>/exploratory_analysis
def main(request,user_id):
    
    
  
    
    loggedIn = isLoggedIn(request,user_id)
    
    template = loader.get_template('exploratory_analysis/index.html')
    if(loggedIn == False):
        template = loader.get_template('exploratory_analysis/not_logged_in.html')
    
    
    
    
    context = RequestContext(request, {
        'username' : str(user_id),
        'loggedIn' : str(loggedIn)
    })

    return HttpResponse(template.render(context))


def isLoggedIn(request,user_id):
    print '\n\n\t\tuser_id: ' + str(user_id)
    print 'user: ' + str(request.user)
    
    print 'main: noAuthReq: ', paths.noAuthReq
    loggedIn = paths.noAuthReq
    
    if (str(request.user) == str(user_id)):
        loggedIn = True
        
    return loggedIn


#geo map/time series view
#corresponds with url: http://<host>/exploratory_analysis/maps
def maps(request,user_id):
    print '\n\nrequest user authenticate: ' + str(request.user.is_authenticated()) + '\n\n\n\n'
    
    
    #need a flag to indicated whether a tree 
    print '\n\n\t\tuser_id: ' + str(user_id)
    print 'user: ' + str(request.user)
    
    loggedIn = paths.noAuthReq
    
    if (str(request.user) == str(user_id)):
        loggedIn = True
    
    username = 'jfharney'
    
    #grab the username
    if user_id != None:
        username = user_id
    
    if(loggedIn == True):
        template = loader.get_template('exploratory_analysis/mapview.html')
    else:
        print 'username: ' + username
        template = loader.get_template('exploratory_analysis/not_logged_in.html')
        
    
    
    context = RequestContext(request, {
      'loggedIn' : str(loggedIn),
      'username' : username,
    })
    
    return HttpResponse(template.render(context))


#geo map/time series view
#corresponds with url: http://<host>/exploratory_analysis/maps
def heatmap(request,user_id):
    #print '\n\n\n\n\nrequest user authenticate: ' + str(request.user.is_authenticated()) + '\n\n\n\n'
    
    
    #need a flag to indicated whether a tree 
    #print '\n\n\n\n\n\n\n\t\t\tuser_id: ' + str(user_id)
    #print 'user: ' + str(request.user)
    
    loggedIn = paths.noAuthReq
    
    if (str(request.user) == str(user_id)):
        loggedIn = True
    
    username = 'jfharney'
    
    #grab the username
    if user_id != None:
        username = user_id
    
    print 'LoggedIn: ' + str(loggedIn)
    
    if(loggedIn == True):
        template = loader.get_template('exploratory_analysis/heatmapview.html')
    else:
        print 'username: ' + username
        template = loader.get_template('exploratory_analysis/not_logged_in.html')
        
    context = RequestContext(request, {
      'loggedIn' : str(loggedIn),
      'username' : username,
    })
    
    return HttpResponse(template.render(context))





def figureGenerator(request):
      print 'in figure generator'
    
      print request.POST
      #hard coded\
      
      dataset = str(request.POST['dataset']);
      
      print 'dataset ---> ' + dataset
      variables = request.POST['variables']
      print 'variables passed in: ', variables
      print type(variables)
      if type(variables) is list:
         variables = [str(x) for x in variables]
      else:
         variables = [str(variables)]

      times = request.POST['times']
      if type(times) is list:
         times = [str(x) for x in times]
      else:
         times = [str(times)]

      sets = request.POST['sets']
      if type(sets) is list:
         sets = [str(x) for x in sets]
      else:
         sets = [str(sets)]

      packages = request.POST['packages']
      if type(packages) is list:
         packages = [str(x) for x in packages]
      else:
         packages = [str(packages)]

      realms = request.POST['realms']
      if type(realms) is list:
         realms = [str(x) for x in realms]
      else:
         realms = [str(realms)]
         
      return HttpResponse('../../../static/exploratory_analysis/img/treeex/land_lmwg_set1_ANN_ER.png')
'''
      print 'sets: ', sets
#      sets = ['1']
    
      
      print 'variables: ' + str(variables)
      print 'times: ' + str(times)
      print 'sets: ' + str(sets)
      print 'packages: ' + str(packages)
      print 'realms: ' + str(realms)
      
    
      inCache = False
      

      # First, see if it is in cache_dir (the shared cache; typically pregenerated figures
      filename = str(packages[0] + '_set' + sets[0][0] + '_' + times[0] + '_' + variables[0] + '.png')
      filepath = os.path.join(cache_dir, dataset, filename)
      print 'Looking for cached image in system cache', filepath
#      path = './' +  'exploratory_analysis/static/exploratory_analysis/img/treeex/' + cachedFile
#      print 'absolute path: ' + os.path.abspath(path)
      if os.path.exists(filepath):
         print 'Found in system cache'
         inCache = True

      if not inCache:
      # Now, see if it was previously generated by this user.
         filepath = os.path.join(generated_img_path, dataset, filename)
         print 'Looking for cached image in user cache', filepath
         if os.path.exists(filepath):
            print 'Found in user cache'
            inCache=True
    
      if(not inCache):
          print 'not in cache'
          o= Options()
          
           Old defaults
          o._opts['path']=[default_sample_data_dir]
          o._opts['vars']=['TG']
          o._opts['times']=['MAM']
          #Note: only use 1 or 2 
          o._opts['sets']=['1']
          o._opts['packages']=['lmwg']
          o._opts['realms']=['land']
          
        
          o._opts['path']=[default_tree_sample_data_dir + paths.dataset_name ]
          o._opts['vars']=variables
          o._opts['times']=times
          #Note: only use 1 or 2 
          o._opts['sets']=sets
          o._opts['packages']=packages
          o._opts['realms']=realms
          dm = diagnostics_menu()
        
	  #filepath is currently set to generated_img_path plus the filename

          import metrics.fileio.filetable as ft
          import metrics.fileio.findfiles as fi
          dtree1 = fi.dirtree_datafiles(o, pathid=0)
          filetable1 = ft.basic_filetable(dtree1, o)
          filetable2 = None
          #print 'No second dataset for comparison'
             
          package=o._opts['packages'][0]
          print 'PACKAGE ' , package
          
          pclass = dm[package.upper()]()
    
          # this needs a filetable probably, or we just define the maximum list of variables somewhere
#          im = ".".join(['metrics', 'packages', package[0], package[0]])
#          if package[0] == 'lmwg':
#             pclass = getattr(__import__(im, fromlist=['LMWG']), 'LMWG')()
#          elif package[0]=='amwg':
#             pclass = getattr(__import__(im, fromlist=['AMWG']), 'AMWG')()
    
          setname = o._opts['sets'][0]
          varid = o._opts['vars'][0]
          seasonid = o._opts['times'][0]
          print 'CALLING LIST SETS'
          slist = pclass.list_diagnostic_sets()
          print 'DONE CALLIGN LIST SETS'
          keys = slist.keys()
          keys.sort()
          import vcs
	  print 'generating ', filepath
          v = vcs.init()
#          diag_template = diagnostics_template()
          for k in keys:
             fields = k.split()
             if setname[0] == fields[0]:
                print 'calling init for ', k, 'varid: ', varid, 'seasonid: ', seasonid
                plot = slist[k](filetable1, filetable2, varid, seasonid)
                res = plot.compute()
                print type(res)
                v.clear()
                v.plot(res[0].vars, res[0].presentation, bg=1)
#### BES - Merge issues. Not sure what to do here. Need to think about it.
#                filename = filename+'_'+varid+'.png'
#                fname = os.path.join(filepath, dataset, filename)
##                fname = filepath+filename+'_'+varid+'.png'
#                print 'fname: ', fname
                
#                v.png(fname)
# was this:
                v.png(filepath)
'''
    
    
      #return HttpResponse()
#      return HttpResponse(cachedFile)
#return HttpResponse('../../../static/exploratory_analysis/img/treeex/land_lmwg_set1_MAY_TG.png')


#Test classic view
@ensure_csrf_cookie
def classic(request,user_id):
      #print '\n\n\n\n\nrequest user authenticate: ' + str(request.user.is_authenticated()) + '\n\n\n\n'
    
    
    username = 'jfharney'
    
    #grab the username
    if user_id != None:
        username = user_id
        
    loggedIn = isLoggedIn(request,user_id)
    
    template = loader.get_template('exploratory_analysis/classic.html')
    if(loggedIn == False):
        template = loader.get_template('exploratory_analysis/not_logged_in.html')
    
    
    context = RequestContext(request, {
      'loggedIn' : str(loggedIn),
      'username' : username,
    })
    
    return HttpResponse(template.render(context))



#New tree view
@ensure_csrf_cookie
def treeex(request,user_id):
    
    print '\n\t--->request user authenticate: ' + str(request.user.is_authenticated()) + '\n'
    
    
    #need a flag to indicated whether a tree 
    #print '\n\n\t\tuser_id: ' + str(user_id)
    #print 'user: ' + str(request.user)
    
    loggedIn = paths.noAuthReq
    
    if (str(request.user) == str(user_id)):
        loggedIn = True
    
    username = 'jfharney'
    
    #grab the username
    if user_id != None:
        username = user_id
    
    loggedIn = True
    
    loggedIn = paths.noAuthReq
    
    
    
    #first we check if the request is in the cache or if it is the initial call
    #if it is in the cache, no need to do any back end generation
    bookmark = request.GET.get('bookmark')
    
    #print '\nbookmark: ' + str(bookmark)  
    
    
    from bookmarks import t_bookmarks
    #import bookmarks

    #no bookmark is being loaded
    if bookmark == None:
        #print '\n\n\n\nbookmark is none\n\n\n\n'
        
        response = t_bookmarks.noBookmarkHandler(request,user_id)
        
        return response
        
    
    #otherwise there are bookmarks
    else:
        
        #print '\n\n\n\nbookmark is something\n\n\n\n'
        
        
        response = t_bookmarks.bookmarkHandler(request,user_id)
        
        return response
        
        
  ############
  #End Page views#
  ############





  ############
  #Services#
  ############
  
  #####Used in the geo page#####

  #grabs datasets given a user id (used in an ajax call)
  #http://<host>/exploratory_analysis/datasets/<user_id>/

def datasets(request,user_id):
    
    print '\n\n\nIn datasets'
    
    from menuhelper import datasets
  
    data_string = datasets.datasetListHelper(request,user_id)
    
    return HttpResponse(data_string)


def datasets1(request,user_id):
    
    print request.META['REMOTE_ADDR']
    
    print '\n\nIn datasets for user_id: ' + user_id
    
    from menuhelper import datasets
    
    data_string = datasets.datasetListHelper1(request,user_id)
    
    print '\nEnd in datasets for user_id: ' + user_id
    
    return HttpResponse(data_string)

def cdflink(request, dataset_id, package_id, variable_id, time_id):
    file_path = 'http://' + paths.ea_hostname + paths.generate_token_url('/' + dataset_id + '/' + package_id + '/' + variable_id)
    return HttpResponse(file_path)


def downloadlist(request, dataset_id, package_id, variable_id, time_id):
    from menuhelper import downloads
    
    data_string = downloads.getFileList(dataset_id)
    print data_string
    html = '<h4>Climos Downloads: ' + dataset_id + '</h4>'
    for d in data_string:
        file_path = 'http://' + paths.ea_hostname + paths.generate_token_url('/' + dataset_id + '/climos/' + d)
        html += '<br>'
        html += '<a href="' + file_path + '">' + d + '</a>'
        print html
        
    return HttpResponse(html)

def generate_token_url(filename):
    #!/usr/bin/env python
    import os, time, hashlib
    
    secret = "secret string"                                # Same as AuthTokenSecret
    protectedPath = "/acme-data/"                           # Same as AuthTokenPrefix
    ipLimitation = False                                    # Same as AuthTokenLimitByIp
    hexTime = "{0:x}".format(int(time.time()))              # Time in Hexadecimal      
    fileName = filename                       # The file to access
    
    # Let's generate the token depending if we set AuthTokenLimitByIp
    if ipLimitation:
      token = hashlib.md5(''.join([secret, fileName, hexTime, os.environ["REMOTE_ADDR"]])).hexdigest()
    else:
      token = hashlib.md5(''.join([secret, fileName, hexTime])).hexdigest()
    
    # We build the url
    url = ''.join([protectedPath, token, "/", hexTime, fileName])
    return url   

def token(request,filename):
    #!/usr/bin/env python
    import os, time, hashlib
    
    secret = "secret string"                                # Same as AuthTokenSecret
    protectedPath = "/downloads/"                           # Same as AuthTokenPrefix
    ipLimitation = False                                    # Same as AuthTokenLimitByIp
    hexTime = "{0:x}".format(int(time.time()))              # Time in Hexadecimal      
    fileName = filename                       # The file to access
    
    # Let's generate the token depending if we set AuthTokenLimitByIp
    if ipLimitation:
      token = hashlib.md5(''.join([secret, fileName, hexTime, os.environ["REMOTE_ADDR"]])).hexdigest()
    else:
      token = hashlib.md5(''.join([secret, fileName, hexTime])).hexdigest()
    
    # We build the url
    url = ''.join([protectedPath, token, "/", hexTime, fileName])
    return HttpResponse(url)
          
def variables(request,dataset_id,package_id):
    from exploratory_analysis.models import Variables
    print '\nIn GET\n'  
    
    #grab the record with the given dataset_name
    dataset_name = dataset_id
    da = Variables.objects.filter(dataset_name=dataset_name)
    
    if da:
        print 'da is not None'
    #otherwise grab the contents and return as a list
    #note: da[0] is the only record in the filtering of the Dataset_Access objects
        dataset_list = []
        
        for dataset in da[0].variables.split(','):
            dataset_list.append(dataset)
            
        data = {'dataset_list' : dataset_list}
        data_string = json.dumps(data,sort_keys=False,indent=2)
    
        print("GET Done\n")
        print(data_string)
        variables = {'vars': [], 'seasons': []} 
        variables['seasons'] = ['ANN', 'DJF', 'MAM', 'JJA', 'SON', 'JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
        variables['vars'] = dataset_list;
        
        if data_string != "":
             return HttpResponse(json.dumps(variables))

    print 'da is None'
    opts = Options()
    opts['path'] = ['/data/tropics/' + dataset_id + '/']
    opts['packages'] = [package_id.upper()]
    path1 = opts['path'][0]
    filt1 = None

    # create a filetable for the path
    dtree1 = dirtree_datafiles(opts, pathid=0)
    filetable1 = basic_filetable(dtree1, opts)
    print filetable1.nrows()
    print dir(filetable1)
    # you can get all regions from defines.all_regions at any time.
    # you can get the superset of all seasons from defines.all_regions at any time as well
    
    dm = diagnostics_menu()
    for pname in opts['packages']:
        pclass = dm[pname]()

        slist = pclass.list_diagnostic_sets()
        # slist contains "Set 1 - Blah Blah Blah", "Set 2 - Blah Blah Blah", etc 

        # now to get all variables, we need to extract just the integer from the slist entries.
        snums = [setnum(x) for x in slist.keys()]
        print slist
        print snums
        variables = {'vars': [], 'seasons': []}
        for s in slist.keys():
            sclass = slist[s]
            # This season list is a subset for a given diagnostic set. This is NOT implemented in land diags
            # yet; you'll just get the entire season list back. I should work on that.
            seasons = pclass.list_seasons()
    
            variables['vars'].extend(pclass.list_variables(filetable1, None, s))
            variables['seasons'] = seasons
            print 'seasons:' , seasons
            print 'variables: ', variables
    variables['vars']=list(set(variables['vars']))
  
    return HttpResponse(json.dumps(variables))
 
def setnum( setname ):
    """extracts the plot set number from the full plot set name, and returns the number.
    The plot set name should begin with the set number, e.g.
       setname = ' 2- Line Plots of Annual Implied Northward Transport'"""
    mo = re.search( r'\d', setname )   # matches decimal digits
    if mo is None:
        return None
    index1 = mo.start()                        # index of first match
    mo = re.search( r'\D', setname[index1:] )  # matches anything but decimal digits
    if mo is None:                             # everything past the first digit is another digit
        setnumber = setname[index1:]
    else:
        index2 = mo.start()                    # index of first match
        setnumber = setname[index1:index1+index2]
    return setnumber

def variables1(request):
    
    #print '\n\nIn variables'
    
    from menuhelper import variablelist
    
    data_string = variablelist.variableListHelper1(request)
    
    return HttpResponse(data_string)


#times service
#gets time ranges for a given variable id
#http://<host>/exploratory_analysis/times/variable_id'
def times(request,variable_id):
    from menuhelper import times
    
    data_string = times.timesHelper(request,variable_id)
    
    return HttpResponse(data_string)

  
def times1(request):  

    from menuhelper import times
    
    data_string = times.timesHelper1(request)
    
    return HttpResponse(data_string)



def packages1(request):  

    from menuhelper import packages
    
    data_string = packages.packagesHelper1(request)
    
    return HttpResponse(data_string)



  #####End Used in the geo page#####
  
  
  
  
  #####Used in the tree page#####
  
   
   

  
#  url(r'^diagplot/$', views.diagplot, name='diagplot'),
#http://<host>/diagplot
def diagplot(request):
    if request.POST:
        print 'posting diagplot'
        print 'figureName: ' + request.POST['figureName']
    elif request.DELETE:
        print 'deleting diagplot'
        print 'figureName: ' + request.DELETE['figureName']
    return HttpResponse("Here's the text of the Web page.")





    
#Tree Figures BookmarksAPI
#http://<host>/exploratory_analysis/login
#Need to store Bookmark name, bookmark variables, bookmark time periods, bookmark description
def login(request):
    template = loader.get_template('exploratory_analysis/login.html')

    print 'going to login.html...'
    context = RequestContext(request, {
        
    })

    return HttpResponse(template.render(context))

#Tree Figures BookmarksAPI
#http://<host>/exploratory_analysis/logout
#Need to store Bookmark name, bookmark variables, bookmark time periods, bookmark description
def logout(request):
    
    
    print 'going to logout.html...'
    
    from django.contrib.auth import logout
    logout(request)
    
    template = loader.get_template('exploratory_analysis/logout.html')

    
    context = RequestContext(request, {
        
    })

    return HttpResponse(template.render(context))

#Authentication to ESGF and synching with django User database
#Caled when the user tries to login
def auth(request):
    
    print '\nin auth\n\n'
    
    from security import signin
    
    response = signin.esgf_login(request)
    
    return response


def register(request):
    
    username = ''
    password = ''
    email = ''
    if request.POST['register_username'] == None or request.POST['register_password'] == None:
        return HttpResponse("Error")
    else:
        username = request.POST['register_username']
        password = request.POST['register_password']
    
    if request.POST['register_email'] == None:
        email = 'N/A'
    
    print 'username: ' + username + ' password: ' + password + ' email: ' + email
    
    from django.db import IntegrityError
    
    try:
        from django.contrib.auth.models import User
        user = User.objects.create_user(username,email,password)
        user.save()
        return HttpResponse("Registered")
    except IntegrityError:
        return HttpResponse("Duplicate")
    
    
    






def tree(request):
    template = loader.get_template('exploratory_analysis/treeview.html')
    
    context = RequestContext(request, {
        'username' : 'jfharney',
    })
    
    return HttpResponse(template.render(context))
 
  
  
#Test classic view
from django.views.decorators.csrf import csrf_exempt

def classic_set_list_html(request):
    
    print 'in classic views html'
    
    options = request.GET.get('options')
    
    print 'options: ' + str(options)
    
    html = ""
    
    response = 'error'
    
    if request.method == "POST":
        sets = None
        varlist = None
        times = None
        package = None
        dataset = None
        
        json_data = json.loads(request.body)
        
        varlist = json_data['vars'] #should be a list
        times = json_data['times'] #should be a list
        package = json_data['package'] #should be a string
        dataset = json_data['dataset']
    
        print 'varlist: ' + str(varlist) + ' ' #+ vars.length
        print 'times: ' + str(times) + ' ' #+ times.length
        print 'package: ' + str(package)
        print 'dataset: ' + str(dataset)
                   
    html = '<TABLE width="1150" ><TR><TD><TH ALIGN=left VALIGN=top><font color=blue>Set </font><font color=blue>Description</font><br><font color=red>Top Ten</font><a class="classic_toggle_sets" id="classicatm_topten" href="#">Tier 1A/Top Ten</a> summary for this dataset.<br><font color=red>0</font><A class="classic_toggle_sets" id="classicatm_topten" HREF="#"> Top Ten</A> of ANN, DJF, JJA, global and regional means and RMSE.<br><font color=red>1</font><A class="classic_toggle_sets" id="classicatm_set1" HREF="#"> Tables</A> of ANN, DJF, JJA, global and regional means and RMSE.<br><font color=red>2</font><A class="classic_toggle_sets" id="classicatm_set2" HREF="#"> Line plots</A> of annual implied northward transports.<br><font color=red>3</font><A class="classic_toggle_sets" id="classicatm_set3" HREF="#"> Line plots</A> of DJF, JJA and ANN zonal means<br><font color=red>4</font> Vertical <A class="classic_toggle_sets" id="classicatm_set4" HREF="#">contour plots</A> of DJF, JJA and ANN zonal means<br><font color=red>4a</font> Vertical (XZ) <A class="classic_toggle_sets" id="classicatm_set4a" HREF="#">contour plots</A> of DJF, JJA and ANN meridional means<br><font color=red>5</font> Horizontal <A class="classic_toggle_sets" id="classicatm_set5" HREF="#">contour plots</A> of DJF, JJA and ANN means<br><font color=red>6</font> Horizontal <A class="classic_toggle_sets" id="classicatm_set6" HREF="#">vector plots</A> of DJF, JJA and ANN means<br><font color=red>7</font> Polar <A class="classic_toggle_sets" id="classicatm_set7" HREF="#">contour and vector plots</A> of DJF, JJA and ANN means<br><font color=red>8</font> Annual cycle <A class="classic_toggle_sets" id="classicatm_set8" HREF="#">contour plots</A> of zonal means<br><font color=red>9</font> Horizontal <A class="classic_toggle_sets" id="classicatm_set9" HREF="#">contour plots</A> of DJF-JJA differences<br><font color=red>10</font> Annual cycle line <A class="classic_toggle_sets" id="classicatm_set10" HREF="#">plots</A> of global means<br><font color=red>11</font> Pacific annual cycle, Scatter plot <A class="classic_toggle_sets" id="classicatm_set11" HREF="#">plots</A><br><font color=red>12</font> Vertical profile <A class="classic_toggle_sets" id="classicatm_set12" HREF="#">plots</A> from 17 selected stations<br><font color=red>13</font> ISCCP cloud simulator <A class="classic_toggle_sets" id="classicatm_set13" HREF="#">plots</A><br><font color=red>14</font> Taylor Diagram <A class="classic_toggle_sets" id="classicatm_set14" HREF="#">plots</A><br><font color=red>15</font> Annual Cycle at Select Stations <A class="classic_toggle_sets" id="classicatm_set15" HREF="#">plots</A><br><br></TD></TR></TABLE>'
    response = html
    print html
    
    return HttpResponse(html);
    
@csrf_exempt

def classic_views_html(request):
    
    print 'in classic views html'
    
    options = request.GET.get('options')
    
    print 'options: ' + str(options)
    
    html = ""
    
    response = 'error'
    
    if request.method == "POST":
        sets = None
        varlist = None
        times = None
        package = None
        dataset = None
        
        json_data = json.loads(request.body)
        
        sets = json_data['set'] #should be a string. strip off the 'set' part of it, and drop unicode
        sets = str(sets.replace('set',''))
        varlist = json_data['vars'] #should be a list
        times = json_data['times'] #should be a list
        package = json_data['package'] #should be a string
        dataset = json_data['dataset']
        
        print 'sets: ' + str(sets)
        print 'varlist: ' + str(varlist) + ' ' #+ vars.length
        print 'times: ' + str(times) + ' ' #+ times.length
        print 'package: ' + package
        print 'dataset: ' + dataset
        
        
        if package == 'amwg':
            print 'atmosphere diagnostics'
        
            from classic import amwghtmlgenerator
            
            html = None
            html = amwghtmlgenerator.pageGenerator(sets, varlist, times, package, dataset, options)
            if html == None:
               html = '<div>set'+sets+' currently unimplemented</div>'
               
        if package == 'lmwg':
            print 'land diagnostics'
        
            from classic import lmwghtmlgenerator
            
            html = None
            html = lmwghtmlgenerator.pageGenerator(sets, varlist, times, package, dataset, options)
            if html == None:
               html = '<div>set'+sets+' currently unimplemented</div>'               
    
    response = html
    print html
    
    return HttpResponse(html);
    
@csrf_exempt

  






  ############
  #Treeview bookmarks API#
  ############
  
  
  #http://<host>/exploratory_analysis/tree_bookmarks
#Tree Bookmarks API
#Need to store Bookmark name, bookmark variables, bookmark time periods, bookmark description
def tree_bookmarks(request):
    
    from exploratory_analysis.models import Tree_Bookmarks
    
    tree_bookmark_name = None
    tree_bookmark_datasetname = None
    tree_bookmark_realm = None
    tree_bookmark_username = None
    tree_bookmark_variables = None
    tree_bookmark_times = None
    tree_bookmark_sets = None
    tree_bookmark_description = None
    tree_cache_url = None
    
    print 'in tree bookmarks...request method: ' + request.method
    
    if request.method == 'POST':
        
        
        tree_bookmark_name = request.POST['tree_bookmark_name']
        #print 'tree_bookmark_name: ' + tree_bookmark_name
        
        tree_bookmark_datasetname = request.POST['tree_bookmark_datasetname']
        print 'tree_bookmark_datasetname: ' + tree_bookmark_datasetname
        
        tree_bookmark_realm = request.POST['tree_bookmark_realm']
        #print 'tree_bookmark_realm: ' + tree_bookmark_realm
        
        
        tree_bookmark_username = request.POST['tree_bookmark_username']
        #print 'tree_bookmark_username: ' + tree_bookmark_username
        
        tree_bookmark_variables = request.POST['tree_bookmark_variables']
        #print 'tree_bookmark_variables: ' + tree_bookmark_variables
        
        tree_bookmark_times = request.POST['tree_bookmark_times']
        tree_bookmark_sets = request.POST['tree_bookmark_sets']
        tree_bookmark_description = request.POST['tree_bookmark_description']
        tree_cache_url = request.POST['tree_cache_url']
        
        print 'tree_cache_url: ' + tree_cache_url
        
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
        
        print 'tree_cache_url ' + tree_cache_url
        
        #save to the database
        tree_bookmark_record.save()
        
        #save the json file
        
        
        
        print 'POST'
        
        return HttpResponse()
        
        
    elif request.method == 'GET':
        
        print 'in get'
        
        tree_bookmark_name = request.GET.get('tree_bookmark_name')
        tree_bookmark_datasetname = request.GET.get('tree_bookmark_datasetname')
        tree_bookmark_realm = request.GET.get('tree_bookmark_realm')
        tree_bookmark_username = request.GET.get('tree_bookmark_username')
    
        from exploratory_analysis.models import Tree_Bookmarks
    
        
        
        
        
        
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
    
        print 'GET'
    elif request.method == 'DELETE':
        
        tree_bookmark_name = request.GET.get('tree_bookmark_name')
        tree_bookmark_datasetname = request.GET.get('tree_bookmark_datasetname')
        tree_bookmark_realm = request.GET.get('tree_bookmark_realm')
        tree_bookmark_username = request.GET.get('tree_bookmark_username')
    
        from exploratory_analysis.models import Tree_Bookmarks
    
        Tree_Bookmarks.objects.filter(tree_bookmark_name=tree_bookmark_name,
                                      tree_bookmark_datasetname=tree_bookmark_datasetname,
                                      tree_bookmark_realm=tree_bookmark_realm,
                                      tree_bookmark_username=tree_bookmark_username).delete()
        
        print 'DELETE'
    
    
        return HttpResponse()
    
    else: 
        return HttpResponse()
    '''
#    season_list_str = ', '.join(season_list)
#    #default bookmark: bookmark + currentmillitime
#        if bookmark_name == None:
#            import time
#            print 'tme ' + str(time.time())
#            millis = int(round(time.time()*1000))
#            print 'millis' + str(millis)
#            bookmark_name = 'bookmark' + str(millis)
#            print 'using default bookmark name ' + bookmark_name
               
    
    '''  
  
def figure_bookmarks_get_helper(figure_bookmark_name,
                                figure_bookmark_datasetname,
                                figure_bookmark_realm,
                                figure_bookmark_username,
                                figure_bookmark_description,
                                figure_cache_ur
                                ):
    figure_bookmark_record = Figure_Bookmarks(
                                            figure_bookmark_name = figure_bookmark_name,
                                            figure_bookmark_datasetname = figure_bookmark_datasetname,
                                            figure_bookmark_realm = figure_bookmark_realm,
                                            figure_bookmark_username = figure_bookmark_username,
                                            figure_bookmark_description = figure_bookmark_description,
                                            figure_cache_url = figure_cache_url
                                              )
        
    figure_bookmark_record.save()
  
  
#Tree Figures BookmarksAPI
#http://<host>/exploratory_analysis/figure_bookmarks
#Need to store Bookmark name, bookmark variables, bookmark time periods, bookmark description
def figure_bookmarks(request):
    
    from exploratory_analysis.models import Figure_Bookmarks
    
    figure_bookmark_name = None
    figure_bookmark_realm = None
    figure_bookmark_datasetname = None
    figure_bookmark_username = None
    figure_bookmark_description = None
    figure_cache_url = None
    
    if request.method == 'POST':
        
        print 'In POST figure_bookmarks'
        
        
        figure_bookmark_name = request.POST['figure_bookmark_name']
        figure_bookmark_realm = request.POST['figure_bookmark_realm']
        figure_bookmark_datasetname = request.POST['figure_bookmark_datasetname']
        figure_bookmark_username = request.POST['figure_bookmark_username']
        figure_bookmark_description = request.POST['figure_bookmark_description']
        figure_cache_url = request.POST['figure_cache_url']
        
        
        
        figure_bookmark_record = Figure_Bookmarks(
                                            figure_bookmark_name = figure_bookmark_name,
                                            figure_bookmark_datasetname = figure_bookmark_datasetname,
                                            figure_bookmark_realm = figure_bookmark_realm,
                                            figure_bookmark_username = figure_bookmark_username,
                                            figure_bookmark_description = figure_bookmark_description,
                                            figure_cache_url = figure_cache_url
                                              )
        
        p = Figure_Bookmarks.objects.filter(
                                            figure_bookmark_name = request.POST['figure_bookmark_name'],
                                            figure_bookmark_datasetname = request.POST['figure_bookmark_datasetname']
                                            )
        
        if not p:
            figure_bookmark_record.save()
        
        
        
        return HttpResponse()
        
    
    elif request.method == 'GET':
        
        
        print 'In GET figure_bookmarks'
        
        figure_bookmark_name = request.GET.get('figure_bookmark_name')
        figure_bookmark_datasetname = request.GET.get('figure_bookmark_datasetname')
        figure_bookmark_realm = request.GET.get('figure_bookmark_realm')
        figure_bookmark_username = request.GET.get('figure_bookmark_username')
    
        from exploratory_analysis.models import Figure_Bookmarks
    
        print 'figure_bookmark_name: ' + figure_bookmark_name
        print 'figure_bookmark_datasetname: ' + figure_bookmark_datasetname
        print 'figure_bookmark_realm: ' + figure_bookmark_realm
        print 'figure_bookmark_username: ' + figure_bookmark_username
        
    
        try:
            figure_bookmark_record = Figure_Bookmarks.objects.get(figure_bookmark_name=figure_bookmark_name,
                                      figure_bookmark_datasetname=figure_bookmark_datasetname,
                                      figure_bookmark_realm=figure_bookmark_realm,
                                      figure_bookmark_username=figure_bookmark_username)
    
            #print tree_bookmark_record.tree_cache_url
            data =  { 
                 'figure_bookmark_name' : figure_bookmark_record.figure_bookmark_name, 
                 'figure_bookmark_datasetname' : figure_bookmark_record.figure_bookmark_datasetname, 
                 'figure_bookmark_realm' : figure_bookmark_record.figure_bookmark_realm, 
                 'figure_bookmark_username' : figure_bookmark_record.figure_bookmark_username,
                 'figure_bookmark_description' : figure_bookmark_record.figure_bookmark_description,
                 'figure_cache_url' : figure_bookmark_record.figure_cache_url
                 }
            print 'DATA:',repr(data)
            
            data_string = json.dumps(data,sort_keys=True,indent=2)
            return HttpResponse(data_string)
        
    
        except:
            print "Unexpected error:"
            data =  { }
            data_string = json.dumps(data,sort_keys=True,indent=2)
            return HttpResponse(data_string)
            
    
    elif request.method == 'DELETE':
        
        print 'DELETE'
        
        figure_bookmark_name = request.GET.get('figure_bookmark_name')
        figure_bookmark_datasetname = request.GET.get('figure_bookmark_datasetname')
        figure_bookmark_realm = request.GET.get('figure_bookmark_realm')
        figure_bookmark_username = request.GET.get('figure_bookmark_username')
    
        from exploratory_analysis.models import Figure_Bookmarks
    
        print 'figure_bookmark_name ' + figure_bookmark_name
        print 'figure_bookmark_datasetname ' + figure_bookmark_datasetname
        print 'figure_bookmark_realm ' + figure_bookmark_realm
        print 'figure_bookmark_username ' + figure_bookmark_username
        
        Figure_Bookmarks.objects.filter(figure_bookmark_name=figure_bookmark_name,
                                      figure_bookmark_datasetname=figure_bookmark_datasetname,
                                      figure_bookmark_realm=figure_bookmark_realm,
                                      figure_bookmark_username=figure_bookmark_username).delete()
        
        
        
        
    
        return HttpResponse()
    
    
#variable_namesAPI
#http://<host>/exploratory_analysis/variable_names/<short_name>
def variable_names(request,variable_short_name):
    
    print 'variable_short_name: ' + variable_short_name
    
    if request.method == 'POST':
        print 'POST Variable'
    elif request.method == 'DELETE':
        print 'DELETE Variable'
    elif request.method == 'GET':
        print 'GET Variable'
    else:
        print 'OTHER'
        
    return HttpResponse()



    
    
def timeseries(request, lat, lon, variable):
   import cdms2, json, cdutil.times
   # need lat/lon, dataset name, variable from the request
   #variable = str(request.POST['variable'])
   #lat = float(request.POST['lat'])
   #lon = float(request.POST['lon'])

   lon = int(lon)
   lat = int(lat)

   # To make URL values positive integers, we add +90 to lat and multiply by 60
   # And +180 to lon and multiply by 60. Need to undo that first.
   print 'values passed in: ',lat, lon
   mylat = lat/60
   mylat = mylat - 90
   mylon = lon/60
   mylon = mylon - 180

   # THIS NEEDS GREPPED FROM DATASET BUT FINE FOR NOW
   xf = 2
   yf = 2
   mylat = (mylat+90) * yf

   if(mylon < 0):
      mylon = (mylon+360)*xf
   elif(mylon >= 0):
      mylon = mylon*xf

   print 'my new coordinates: ', mylat, mylon

   #   might need to be changed on other machines. I'm not really sure why there is a problem with this
   #   dataset = os.path.join(default_sample_data_dir+'tropics_warming_th_q_co2', 'test.xml')
   dataset = os.path.join(default_sample_data_dir, 'test.xml')


   print 'dataset: ' + dataset
   # Note: It is assumed that we are given an index into the dataset rather
   # than actual lat/lon coordinates. This is not a problem currently, but
   # if this code gets used more, we should probably fix that.

   data = []
   f = cdms2.open(dataset)
   thevar = f(variable)
#   thevar = thevar(latitude=(-90,90), longitude=(-180, 180, 'cob'))
   
   axisIndex = thevar.getAxisIndex('time')
   timeAxis = thevar.getTime()
   #print timeAxis
   cdutil.times.setAxisTimeBoundsMonthly(timeAxis)
   #axisIndex = 0;
   # This code assumes time is the 0th axis. The slice/subregion methods
   # in CDAT don't appear to work, so I can't slice out a region based on
   # naming an axis. There must be a better way to do this, but I don't 
   # know what it is currently.
   # Also, for some reason data = thevar.data[:][lat][lon] doesn't work.
   # This could also be adapted to take subranges pretty trivially
   if(axisIndex == 0): 
     for i in range(thevar.shape[axisIndex]):
       data.append(float(thevar.data[i][int(mylat)][int(mylon)]))
   else:
      print 'Unsupported timeaxis != 0'
      quit()

   print data
   f.close()
   # Make the json now
   # Note - Most of the land datasets we have make it challenging to trivially get the
   # start/end month/year. They are all encoded as days since 1-1-1, but it is not necessarily
   # obvious that that is the case. There doesn't appear to be a trivial way to fix that. needs
   # more thought
   j = {}
   j['start_year'] = 151   
   j['start_month'] = 1
   j['end_year'] = 165
   j['end_month'] = 12
   j['timeseries_data'] = data


   return HttpResponse(json.dumps(j, separators=(',',':'), indent=2))




def avgmap(request, year, month, variable):
   dataset = os.path.join(default_map_sample_data_dir,"tropics_warming_th_q.clm2.h0.")
   dataset = dataset+year+'-'+month+'.nc'
   f = cdms2.open(dataset)
   thevar = f(variable)

   j = {}
   j['geo_data'] = thevar.data.tolist()
   f.close()
   return HttpResponse(json.dumps(j, separators=(',',':'), indent=2))







####Example...
def postStateExample(request):
    
    print 'in post state example'
    a = {'a' : 'hello'}
    return HttpResponse('hello')


