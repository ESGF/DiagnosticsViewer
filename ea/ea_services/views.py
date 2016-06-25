from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from django.template import RequestContext, loader
from django.contrib.auth import authenticate, login

import json
import logging
import traceback
import os
import urllib

logger = logging.getLogger('exploratory_analysis')
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler('exploratory_analysis.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)

# add handler to logger object
logger.addHandler(fh)

# Create your views here.
def index(request):
    
    return HttpResponse("ea services index")

#GET
#curl -X GET http://localhost:8081/exploratory_analysis/published/<dataset_name>/
#POST
#curl -i -H "Accept: application/json" -X POST -d '{ "published" :  "true" }'  http://localhost:8081/exploratory_analysis/published/<dataset_name>/
#PUT
#curl -i -H "Accept: application/json" -X PUT -d '{ "published" :  "true" }'  http://localhost:8081/exploratory_analysis/published/<dataset_name>/

class PublishedView(View):
    
    def put(self, request, dataset_name):
        
        try:
            #load the json object
            json_data = json.loads(request.body)
                
            #grab the dataset added
            published = json_data['published'] #should be a string
        
            from exploratory_analysis.models import Published
            
            #grab the group record
            da = Published.objects.filter(dataset_name=dataset_name)
            
            #for put, remove ALL datasets from the list and substitute the new one given
            published_values = published
                
            if da:
                da.delete()
            
            published_record = Published(
                                                      dataset_name=dataset_name,
                                                      published=published_values
                                                      )
            
            
            logger.debug('\nPublished record: ' + str(published_record))
            
            #save to the database
            published_record.save()
            
            
        except:
            tb = traceback.format_exc()
            logger.debug('tb: ' + tb)
            return HttpResponse("error")
        
        
        return HttpResponse("Published Put")
    
    def post(self, request, dataset_name):
        
        try:
            #load the json object
            json_data = json.loads(request.body)
                
            #grab the dataset added
            published = json_data['published'] #should be a string
        
            from exploratory_analysis.models import Published
            
            #grab the group record
            da = Published.objects.filter(dataset_name=dataset_name)
            
            #for post, remove ALL datasets from the list and substitute the new one given
            published_values = published
                
            if da:
                da.delete()
            
            published_record = Published(
                                                      dataset_name=dataset_name,
                                                      published=published_values
                                                      )
            
            logger.debug('\nPublished record: ' + str(published_record))
            
            #save to the database
            published_record.save()
            
            
        except:
            tb = traceback.format_exc()
            logger.debug('tb: ' + tb)
            return HttpResponse("error")
        
        return HttpResponse("Published Post")
    
    
    def get(self, request, dataset_name):
        
        
        print '\nIn GET\n'  
        
        logger.debug('\nIn Published GET\n')
        
        from exploratory_analysis.models import Published
    
        try:
            
            logger.debug('dataset_name: ' + dataset_name)
            
            #grab the group record
            da = Published.objects.filter(dataset_name=dataset_name)
            
            #if the dataset list is empty then return empty list
            if not da:
                data = {'published' : ''}
                data_string = json.dumps(data,sort_keys=False,indent=2)
                return HttpResponse(data_string + "\n")
            
            #otherwise grab the contents and return as a list
            #note: da[0] is the only record in the filtering of the Dataset_Access objects
            published = []
            
            for publish in da[0].published.split(','):
                published.append(publish)
            
            
            data = {'published' : published}
            data_string = json.dumps(data,sort_keys=False,indent=2)
            
                
            return HttpResponse(data_string + "\n")
            #return HttpResponse("response")
        
        except:
            tb = traceback.format_exc()
            logger.debug('tb: ' + tb)
            return HttpResponse("error")
        
        return HttpResponse("Variables Get")





#GET
#curl -X GET http://localhost:8081/exploratory_analysis/variables/<dataset_name>/
#POST
#curl -i -H "Accept: application/json" -X POST -d '{ "variables" :  "a,b,c" }'  http://localhost:8081/exploratory_analysis/variables/<dataset_name>/
#PUT
#curl -i -H "Accept: application/json" -X PUT -d '{ "variables" :  "a,b,c" }'  http://localhost:8081/exploratory_analysis/variables/<dataset_name>/
#NOTE: PUT functionality is buggy and shouldn't be used for now
class VariablesView(View):
    
    def put(self, request, dataset_name):
        
        '''
        #print '\nIn GET\n'  
        logger.debug('\nIn Variables PUT\n')
        
        #load the json object
        json_data = json.loads(request.body)
            
        
        #grab the dataset added
        variables = json_data['variables'] #should be a string
    
        from exploratory_analysis.models import Dataset_Access
        
        #grab the group record
        da = Dataset_Access.objects.filter(group_name=group_name)
        
        #for put, APPEND the new dataset given
        #append dataset to the end of the dataset list
        
        new_variables_list = ''
        if da:
            new_variables = da[0].variables
            
            new_variables_list = new_variables.split(',')
            
            isDuplicate = False
            
            #check for duplicates
            for entry in new_variables_list:
                logger.debug('entry: ' + entry + ' dataset: ' + dataset)
                if entry == dataset:
                    logger.debug('match')
                    isDuplicate = True
            if not isDuplicate:
                new_dataset_list = new_dataset_list + ',' + dataset
                logger.debug('\nNew Dataset List: ' + str(new_dataset_list))
                da.delete()
        else:
            new_dataset_list = dataset
        
        
        #logger.debug('new_dataset_list: ' + str(new_dataset_list))
        
        dataset_access_record = Dataset_Access(
                                                  group_name=group_name,
                                                  dataset_list=new_dataset_list
                                                  )
        
          
        #save to the database
        dataset_access_record.save()
        
        all = Dataset_Access.objects.all()
        
        #logger.debug('all: ' + str(all))
        '''
    
        return HttpResponse("PUT Done\n")   
        
        
        
        
        return HttpResponse("Variables Put")
    def post(self, request, dataset_name):
        
        #load the json object
        json_data = json.loads(request.body)
            
        
        #grab the dataset added
        variables = json_data['variables'] #should be a string
    
        #print 'Group_name: ' + group_name
        #print 'dataset: ' + str(dataset)
        
        from exploratory_analysis.models import Variables
        
        #grab the group record
        da = Variables.objects.filter(dataset_name=dataset_name)
        
        
        #for post, remove ALL datasets from the list and substitute the new one given
        new_variables = variables
            
        if da:
            da.delete()
        
        variables_record = Variables(
                                                  dataset_name=dataset_name,
                                                  variables=new_variables
                                                  )
        
        
        
        
        logger.debug('\nVariables record: ' + str(variables_record))
        
        #save to the database
        variables_record.save()
        
        all = Variables.objects.all()
        
        return HttpResponse("POST Done\n")   
    
    
    def get(self, request, dataset_name):
        
        #print '\nIn GET\n'  
        logger.debug('\nIn Variables GET\n')
        
        from exploratory_analysis.models import Variables
    
        
        try:
            
            logger.debug('dataset_name: ' + dataset_name)
            
            #grab the group record
            da = Variables.objects.filter(dataset_name=dataset_name)
            
            #if the dataset list is empty then return empty list
            if not da:
                data = {'variables' : ''}
                data_string = json.dumps(data,sort_keys=False,indent=2)
                return HttpResponse(data_string + "\n")
            
            #otherwise grab the contents and return as a list
            #note: da[0] is the only record in the filtering of the Dataset_Access objects
            variables = []
            
            for variable in da[0].variables.split(','):
                variables.append(variable)
            
            
            data = {'variables' : variables}
            data_string = json.dumps(data,sort_keys=False,indent=2)
            
                
            return HttpResponse(data_string + "\n")
            #return HttpResponse("response")
        
        except:
            tb = traceback.format_exc()
            logger.debug('tb: ' + tb)
            return HttpResponse("error")
        
        return HttpResponse("Variables Get")



#gets packages information
#Service API for the Dataset_Access table
#GET
#http://<host>:<port>/exploratory_analysis/group_dataset/<group_name>
#POST
#echo '{ "dataset" :  <dataset_name> }' | curl -d @- 'http://<host>:<port>/exploratory_analysis/dataset_packages/(?P<dataset_name>\w+)/$' -H "Accept:application/json" -H "Context-Type:application/json"
#DELETE
#http://<host>:<port>/exploratory_analysis/dataset_packages/<dataset_name>/

class Dataset_AccessView(View):
    
    
    def put(self, request, group_name):
    
        from exploratory_analysis.models import Dataset_Access
        
        #print '\nIn GET\n'  
        logger.debug('\nIn Dataset_Access PUT\n')
        
        #load the json object
        json_data = json.loads(request.body)


        print 'json_data: ' + str(json_data)
            
        #grab the dataset added
        dataset = json_data['dataset'] #should be a string
    
        #grab the group record
        da = Dataset_Access.objects.filter(group_name=group_name)
    
    
        #if the input json data is blank AND there is no da object, create the da object and just return blank
        if dataset == '' and not da:
            #print 'if the input json data is blank AND there is no da object, create the da object and just save the blank'
            new_dataset_list = dataset
            dataset_access_record = Dataset_Access(
                                                  group_name=group_name,
                                                  dataset_list=new_dataset_list
                                                  )
            
            
            #save to the database
            dataset_access_record.save()
            
        #if the input json data is blank AND there is a da object, save the da object
        elif dataset == '' and da:
            print 'if the input json data is blank AND there is a da object, save nothing'
            
            
        #if the input json data is not blank AND there is no da object, create the da object and populate with data
        elif dataset != '' and not da:
            #print 'if the input json data is not blank AND there is no da object, create the da object and populate with data'
            
            new_dataset_list = dataset
            dataset_access_record = Dataset_Access(
                                                  group_name=group_name,
                                                  dataset_list=new_dataset_list
                                                  )
            
            
            #save to the database
            dataset_access_record.save()
            
        #if the input json data is not blank AND there is a da object, union the data with old data
        else:
            #print 'if the input json data is not blank AND there is a da object, union the data with old data'
        
            new_dataset_entries = set(dataset.split(','))
            old_dataset_entries = set(da[0].dataset_list.split(','))
            da.delete()
            refined_dataset_list = old_dataset_entries.union(new_dataset_entries)
            refined_str = ','.join(refined_dataset_list)
            new_dataset_list = refined_str
        
            dataset_access_record = Dataset_Access(
                                                  group_name=group_name,
                                                  dataset_list=new_dataset_list
                                                  )
            
            
            #save to the database
            dataset_access_record.save()
        
        
        return HttpResponse("PUT Done\n")   
    
    def post(self, request, group_name):
        
        from exploratory_analysis.models import Dataset_Access
      
        print '\n\n\tPOSTing...'
  
        #load the json object
        json_data = json.loads(request.body)
        #json_data = json.loads(urllib.unquote(request.body))
            
        #grab the dataset added
        dataset = json_data['dataset'] #should be a string
    
   
        da = Dataset_Access.objects.filter(group_name=group_name)

        if da:
          da.delete()
 
        print 'json_data: ' + str(json_data)   
        
        new_dataset_list = dataset
        dataset_access_record = Dataset_Access(
                                              group_name=group_name,
                                              dataset_list=new_dataset_list
                                              )
        
        
        #save to the database
        dataset_access_record.save()
        
        print 'POST DONE'   
        
        return HttpResponse("POST Done\n")   
        
    
    
    def get(self, request, group_name):
        
        
        #print '\nIn GET\n'  
        logger.debug('\nIn Dataset_Access GET\n')
        
        from exploratory_analysis.models import Dataset_Access
    
        
        try:
            
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
    
            print 'access data_string: ' + str(data_string)
    
            return HttpResponse(data_string + "\n")
            
            return HttpResponse("response")
        except:
            tb = traceback.format_exc()
            logger.debug('tb: ' + tb)
            return HttpResponse("error")
        
        
        
        return HttpResponse("respone")


    def delete(self, request, group_name):
        #print '\nIn GET\n'  
        logger.debug('\nIn Dataset_Access GET\n')
        
        from exploratory_analysis.models import Dataset_Access
        #grab the group record
        da = Dataset_Access.objects.filter(group_name=group_name)
        
        if da:
           da.delete() 
            
        return HttpResponse("DELETE Done\n")   


#gets packages information
class PackagesView(View):
    
    
    
    def get(self, request, dataset_name):
        
        from exploratory_analysis.models import Packages
    
        #print '\nIn GET\n'  
        logger.debug('\nIn GET\n')
        
        try:
            #grab the record with the given dataset_name
            da = Packages.objects.filter(dataset_name=dataset_name)
            
            if not da:
                data = {'packages' : ''}
                data_string = json.dumps(data,sort_keys=False,indent=2)
                return HttpResponse(data_string + "\n")
           
            #otherwise grab the contents and return as a list
            #note: da[0] is the only record in the filtering of the Dataset_Access objects
            packages_list = []
            
            for package in da[0].packages.split(','):
                packages_list.append(package)
                
            data = {'packages' : packages_list}
            data_string = json.dumps(data,sort_keys=False,indent=2)#,indent=2)
    
            print 'packages data_string: ' + str(data_string)
            
            return HttpResponse(data_string + '\n')# + "\
        
        except:
            tb = traceback.format_exc()
            logger.debug('tb: ' + tb)
            return HttpResponse("error")
            
    

    
    def post(self, request, dataset_name):
        
        from exploratory_analysis.models import Packages
        
        
        
        logger.debug('\nIn POST\n')
        
        #load the json object
        json_data = json.loads(request.body)
            
        #grab the dataset added
        packages = json_data['packages'] #should be a string
        
        logger.debug('\nrequest.body' + str(request.body) + '\n')
        logger.debug('\ndataset name: ' + str(dataset_name) + '\n')
        
        #grab the record with the given dataset_name
        try:
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
            
            
            logger.debug('\nEnd POST\n')
            return HttpResponse("Success\n")

        except:
            
            tb = traceback.format_exc()
            logger.debug('tb: ' + tb)
            return HttpResponse("error")
     
        
    def delete(self, request, dataset_name):
       
        from exploratory_analysis.models import Packages
        
        logger.debug('\nIn DELETE\n')   
        
        #not sure if this is the right behavior but this will delete the ENTIRE record given the group
        #grab the group record
        da = Packages.objects.filter(dataset_name=dataset_name)
        
        if da:
            da.delete()
        
        all = Packages.objects.all()
        
        logger.debug('\nEnd DELETE\n')   
        return HttpResponse("Success\n")
    
    
'''
        #grab the group record
        da = Dataset_Access.objects.filter(group_name=group_name)
    
    
        #if the input json data is blank AND there is no da object, create the da object and just return blank
        if dataset == '' and not da:
            #print 'if the input json data is blank AND there is no da object, create the da object and just save the blank'
            new_dataset_list = dataset
            dataset_access_record = Dataset_Access(
                                                  group_name=group_name,
                                                  dataset_list=new_dataset_list
                                                  )
            
            
            #save to the database
            dataset_access_record.save()
            
        #if the input json data is blank AND there is a da object, save the da object
        elif dataset == '' and da:
            print 'if the input json data is blank AND there is a da object, save nothing'
            new_dataset_list = dataset
            dataset_access_record = Dataset_Access(
                                                  group_name=group_name,
                                                  dataset_list=new_dataset_list
                                                  )
            
            
            #save to the database
            dataset_access_record.save()
            
        #if the input json data is not blank AND there is no da object, create the da object and populate with data
        elif dataset != '' and not da:
            #print 'if the input json data is not blank AND there is no da object, create the da object and populate with data'
            
            new_dataset_list = dataset
            dataset_access_record = Dataset_Access(
                                                  group_name=group_name,
                                                  dataset_list=new_dataset_list
                                                  )
            
            
            #save to the database
            dataset_access_record.save()
            
        #if the input json data is not blank AND there is a da object, union the data with old data
        else:
            #print 'if the input json data is not blank AND there is a da object, union the data with old data'
        
            new_dataset_list = dataset
            dataset_access_record = Dataset_Access(
                                                  group_name=group_name,
                                                  dataset_list=new_dataset_list
                                                  )
            
            
            #save to the database
            dataset_access_record.save()
'''    
    
''' removed 4-13
        #load the json object
        json_data = json.loads(request.body)
            
        
        #grab the dataset added
        dataset = json_data['dataset'] #should be a string
    
        #print 'Group_name: ' + group_name
        #print 'dataset: ' + str(dataset)
        
        from exploratory_analysis.models import Dataset_Access
        
        #grab the group record
        da = Dataset_Access.objects.filter(group_name=group_name)
        
        
        #for post, remove ALL datasets from the list and substitute the new one given
        new_dataset_list = dataset
            
        if da:
            da.delete()
        
        dataset_access_record = Dataset_Access(
                                                  group_name=group_name,
                                                  dataset_list=new_dataset_list
                                                  )
        
        
        
        
        #save to the database
        dataset_access_record.save()
        
'''
      
