from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from django.template import RequestContext, loader
from django.contrib.auth import authenticate, login

from metrics.frontend.amwgmaster import *
    

import json
import logging
import traceback
import os

logger = logging.getLogger('exploratory_analysis')
logger.setLevel(logging.DEBUG)



fh = logging.FileHandler('exploratory_analysis.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)

# add handler to logger object
logger.addHandler(fh)



#various variables that need to go into a config file
#esgfAuth - flag for turning on (True) or turning off (False) esgf authentication
esgfAuth = False

#the directory for the certs to be fetched
proxy_cert_dir = '/tmp'

#naAuthReq - authentication via the cookie on (True) or off (False)
authReq = True

#certNameSuffix - the suffix of the certificate file
certNameSuffix = 'x509acme'

# Main page.
def index(request):
    
    template = loader.get_template('exploratory_analysis/index.html')

    context = RequestContext(request, {
        'username' : '',
    })

    return HttpResponse(template.render(context))


#http://<host>/exploratory_analysis/login
def login(request):
    
    template = loader.get_template('exploratory_analysis/login.html')

    context = RequestContext(request, {
        
    })

    return HttpResponse(template.render(context))




from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import ensure_csrf_cookie

#Example: curl -i -H "Accept: application/json" -X POST -d '{ "username" :  "u1" }'  http://localhost:8081/exploratory_analysis/auth/
@ensure_csrf_cookie
def auth(request):
    
    
    if request.method == "POST":
        json_data = json.loads(request.body)
        
        username = json_data['username'] 
        password = json_data['password'] 
        
        
        #return a None message if the username is blank
        if username == '':
            return HttpResponse("None")
        if username == None:
            return HttpResponse("None")
    
        #insert code for authentication here
        #create a valid user object
        
        
        #authenticates to ESGF
        if esgfAuth:
            print 'esgfAuth is true, so authenticate'
    
            from fcntl import flock, LOCK_EX, LOCK_UN
            
            cert_name = certNameSuffix
            
            outdir = os.path.join(proxy_cert_dir, username)
                
            try:
                
                if not os.path.exists(outdir):
                    os.makedirs(outdir)
                else:
                    print 'path already exists'
                
                outfile = os.path.join(outdir, cert_name)
                outfile = str(outfile)
                
                # outfile = '/tmp/x509up_u%s' % (os.getuid()) 
                print '----> OUTFILE: ', outfile
                
                    
                    
                
            except:
                tb = traceback.format_exc()
                logger.debug('tb: ' + tb)
                print "couldn't make directory " + str(outdir)
                return HttpResponse("Not Authenticated")
            
    
        else:
            print 'esgfAuth is false, so dont authenticate'
            return HttpResponse("Authenticated")
           
    
    return HttpResponse("Hello")



#Main view
def main(request,user_id):
  
    #check to see if the user is logged in
    loggedIn = isLoggedIn(request,user_id)
    
    template = loader.get_template('exploratory_analysis/index.html')
    
    if(loggedIn == False):
        template = loader.get_template('exploratory_analysis/not_logged_in.html')
    
    context = RequestContext(request, {
        'username' : str(user_id),
        'loggedIn' : str(loggedIn)
    })

    return HttpResponse(template.render(context))



#Belongs in a common utils package
def isLoggedIn(request,user_id):
    
    print 'user: ' + str(request.user) + ' user_id: ' + user_id
    
    if authReq:
        
        
        return True
    
    else:
        if (str(request.user) == str(user_id)):
            loggedIn = True
        else: 
            return False



def classic(request,user_id):


    template = loader.get_template('exploratory_analysis/classic.html')
    
    context = RequestContext(request, {
      'username' : user_id,
    })

    return HttpResponse(template.render(context))




def classic_set_list_html(request):

    print 'in classic_set_list_html'

    package = request.GET.get('package','')
    print 'package: ' + package

    '''
    json_data = json.loads(request.body)
    project = json_data['project']
    dataset = json_data['dataset']
    pckg = json_data['pckg']
    variables = json_data['variables']
    times = json_data['times']
    '''
    
    #html = '<TABLE width="1150" ><TR><TD><TH ALIGN=left VALIGN=top><font color=blue>Set </font><font color=blue>Description</font><br><font color=red>Top Ten</font><a class="classic_toggle_sets" id="classicatm_topten" href="#">Tier 1A/Top Ten</a> summary for this dataset.<br><font color=red>0</font><A class="classic_toggle_sets" id="classicatm_topten" HREF="#"> Top Ten</A> of ANN, DJF, JJA, global and regional means and RMSE.<br><font color=red>1</font><A class="classic_toggle_sets" id="classicatm_set1" HREF="#"> Tables</A> of ANN, DJF, JJA, global and regional means and RMSE.<br><font color=red>2</font><A class="classic_toggle_sets" id="classicatm_set2" HREF="#"> Line plots</A> of annual implied northward transports.<br><font color=red>3</font><A class="classic_toggle_sets" id="classicatm_set3" HREF="#"> Line plots</A> of DJF, JJA and ANN zonal means<br><font color=red>4</font> Vertical <A class="classic_toggle_sets" id="classicatm_set4" HREF="#">contour plots</A> of DJF, JJA and ANN zonal means<br><font color=red>4a</font> Vertical (XZ) <A class="classic_toggle_sets" id="classicatm_set4a" HREF="#">contour plots</A> of DJF, JJA and ANN meridional means<br><font color=red>5</font> Horizontal <A class="classic_toggle_sets" id="classicatm_set5" HREF="#">contour plots</A> of DJF, JJA and ANN means<br><font color=red>6</font> Horizontal <A class="classic_toggle_sets" id="classicatm_set6" HREF="#">vector plots</A> of DJF, JJA and ANN means<br><font color=red>7</font> Polar <A class="classic_toggle_sets" id="classicatm_set7" HREF="#">contour and vector plots</A> of DJF, JJA and ANN means<br><font color=red>8</font> Annual cycle <A class="classic_toggle_sets" id="classicatm_set8" HREF="#">contour plots</A> of zonal means<br><font color=red>9</font> Horizontal <A class="classic_toggle_sets" id="classicatm_set9" HREF="#">contour plots</A> of DJF-JJA differences<br><font color=red>10</font> Annual cycle line <A class="classic_toggle_sets" id="classicatm_set10" HREF="#">plots</A> of global means<br><font color=red>11</font> Pacific annual cycle, Scatter plot <A class="classic_toggle_sets" id="classicatm_set11" HREF="#">plots</A><br><font color=red>12</font> Vertical profile <A class="classic_toggle_sets" id="classicatm_set12" HREF="#">plots</A> from 17 selected stations<br><font color=red>13</font> ISCCP cloud simulator <A class="classic_toggle_sets" id="classicatm_set13" HREF="#">plots</A><br><font color=red>14</font> Taylor Diagram <A class="classic_toggle_sets" id="classicatm_set14" HREF="#">plots</A><br><font color=red>15</font> Annual Cycle at Select Stations <A class="classic_toggle_sets" id="classicatm_set15" HREF="#">plots</A><br><br></TD></TR></TABLE>'
         
    if package == 'atm':
        print 'getting atm home'
        template = loader.get_template('exploratory_analysis/atm_home.html')
        context = RequestContext(request, {
            
        })
        return HttpResponse(template.render(context))
    else:
        print 'getting lnd home'
        template = loader.get_template('exploratory_analysis/land_home.html')
        context = RequestContext(request, {
            
        })
        return HttpResponse(template.render(context))
    
    #return HttpResponse(html);


def classic_views_html(request):
    
    sets = str(request.GET.get('set',''))
    
    #sets = str(set[3:])
    varlist = 'TLAI'
    times = 't1'
    package = 'p1'
    dataset = 'd1'
    options = []
    
    html = pageGenerator(sets, varlist, times, package, dataset, options)
    
    print 'returning html: ' + str(html)
    
    return HttpResponse(html)


def pageHeader(dataset,sets):
    # Header stuff
    html = ''
    html = '<p>'
    html += '<img src="/static/exploratory_analysis/img/classic/amwg/SET'+sets+'.gif" border=1 hspace=10 align=left alt="set '+sets+'">'
    html += '<font color=maroon size=+3><b>'
    html += dataset+'<br>and<br>OBS data'
    html += '</b></font>'
            
    html += '<p>'
    html += '<b>DIAG Set'+sets+' '+diags_collection[sets]['desc']
    html += '<hr noshade size=2 size="100%">'
        
    html += '<b>'+diags_collection[sets].get('preamble', '')

    return html
    
    

def pageGenerator(sets, varlist, times, package, dataset, options):
    
    ea_root = '/Users/8xo/software/exploratory_analysis/DiagnosticsViewer'
    uvcdat_live_root = ea_root+ '/django-app-1.8/uvcdat_live/' 
    img_cache_path = uvcdat_live_root + '/exploratory_analysis/static/exploratory_analysis/cache/'
    
    print 'img_cache_path: ' + img_cache_path
    
    print 'sets: ' + sets
    
    html = ''
    try:
        img_prefix = ''
        if __name__ != '__main__':
          img_prefix = os.path.join(img_cache_path, dataset, package, 'img', '')
        else:
          img_prefix ='path'
    
    
        #sets = '3'
        #sets = '4'
        
        html = pageHeader(dataset,sets)
        
        
        obssort = 1 
   
        '''
        html = '<div>' + img_prefix + '</div>'
    
    
        obssort = 1 
        # Header stuff
        html = ''
        html = '<p>'
        html += '<img src="/static/exploratory_analysis/img/classic/amwg/SET'+sets+'.gif" border=1 hspace=10 align=left alt="set '+sets+'">'
        html += '<font color=maroon size=+3><b>'
        html += dataset+'<br>and<br>OBS data'
        html += '</b></font>'
                
        html += '<p>'
        html += '<b>DIAG Set'+sets+' '+diags_collection[sets]['desc']
        html += '<hr noshade size=2 size="100%">'
            
        html += '<b>'+diags_collection[sets].get('preamble', '')
        '''
    
    
        
        html += '<TABLE>'

        print 'DEFAULTING TO ALL VARS FOR NOW'
        print 'DEFAULTING TO EXISTING FILENAME CONVENTIONS'
        print 'DEFAULTING TO NO ABSOLUTE PATHS'
     
        # Determine number of columns
        # The default is just 'ANN', and if that is the only one or nothing is specified, we don't need a column for it.
        # ['NA'] is also something to deal with.
        seasons = diags_collection[sets].get('seasons', ['ANN'])
        # Were some specific seasons passed in? If so, limit our list.
        print 'DEFAULTING TO ALL SEASONS FOR NOW'
        #if seasons != ['NA']:
        #   seasons = list(set(times) & set(def_seasons))
        
        regions = diags_collection[sets].get('regions', ['Global'])
        
        
        # get a list of all obssets used in this collection
        varlist = list(set(diags_collection[sets].keys()) - set(collection_special_vars))
        obslist = []
        for v in varlist:
            obslist.extend(diags_collection[sets][v]['obs'])
            # unique-ify
        obslist = list(set(obslist))

        # does this set need the --combined filename?
        # Eventually this might be per-variable...
        hasCombined = diags_collection[sets].get('combined',False)

        print 'regions: ' + str(regions)
        print 'varlist: ' + str(varlist)
        print 'obslist: ' + str(obslist)
        print 'hasCombined: ' + str(hasCombined)
        
        specialCases = ['1', '2', '11', '12', '13', '14']
   
        ea_hostname = 'localhost'
        
        
        
        
        if sets not in specialCases:
            if obssort == 1:
                print 'obsort = 1'
                for o in obslist:
                    html += '<TR>'
                    html += '<TH><BR>' # the variable
                    obsname = diags_obslist[o]['desc']
                    html += '  <TH ALIGN=LEFT><font color="navy" size="+1">'+obsname+'</font>' # the obs/desc
                    '''
                    print '\thtml: ' + '  <TH ALIGN=LEFT><font color="navy" size="+1">'+obsname+'</font>' # the obs/desc
                    if len(seasons) != 1:
                        for season in seasons: 
                            print '\t    <TH>'+season
                            html += '    <TH>'+season # the plot links
                    else:
                        html += '<TH>'
                    '''
                    
                '''
                for o in obslist:
                    html += '<TR>'
                    html += '<TH><BR>' # the variable
                    obsname = diags_obslist[o]['desc']
                    html += '  <TH ALIGN=LEFT><font color="navy" size="+1">'+obsname+'</font>' # the obs/desc
                    if len(seasons) != 1:
                        for season in seasons: 
                            html += '    <TH>'+season # the plot links
                    else:
                        html += '<TH>'

                    for v in varlist:
                    # Is this obsset used by this variable?
                        print 'v: ' + v
                        if diags_collection[sets][v]['obs'] != None:
                            
                            if o in diags_collection[sets][v]['obs']:
                                obsfname = diags_obslist[o]['filekey']
                                html += '<TR>'
                                html += '    <TH ALIGN=LEFT>' + v
                                html += '    <TH ALIGN=LEFT>' + diags_varlist[v]['desc']
                
                #print '\n\nregions: ' + str(regions) + '\n\n'
                if regions == ['Global']:
                     regionstr = '_Global'
                     for season in seasons:
                         if season == 'NA':
                            seasonstr = ''
                         else:
                            seasonstr = '_'+season
                         if hasCombined == True:
                            postfix = '-combined.png'
                         else:
                            postfix = '-model.png'
                         varopts = diags_collection[sets][v].get('varopts', False)
                         if varopts == False:
                            fname = 'http://' + ea_hostname + generate_token_url('/' + dataset + '/' + package + '/set'+sets+regionstr+seasonstr+'_'+v+'_'+obsfname+postfix)
                         else:
                            for varopt in varopts:
                               fname = 'http://' + ea_hostname + generate_token_url('/' + dataset + '/' + package + '/set'+sets+regionstr+seasonstr+'_'+v+'_'+varopt+'_'+obsfname+postfix)
                                        
#                     print 'Looking for: ', fname
#                     if 'TTRP' in v:
#                        fname = 'http://' + paths.ea_hostname + paths.generate_token_url('/' + dataset + '/' + package +'/set'+sets+'_'+regionstr+'_'+season+'_'+v.replace('_TROP','')+'_'+obsfname+'-combined.png')
#                     elif 'TTRP' in v:
#                        fname = 'http://' + paths.ea_hostname + paths.generate_token_url('/' + dataset + '/' + package +'/set'+sets+'_'+season+'_'+v+'_'+obsfname+'_TROP-combined.png')
#                     else:
#                        fname = 'http://' + paths.ea_hostname + paths.generate_token_url('/' + dataset + '/' + package +'/set'+sets+'_'+season+'_'+v+'_'+obsfname+'-combined.png')
                         click = 'onclick="displayImageClick(\''+fname+'\');" '
                         over = 'onmouseover="displayImageHover(\''+fname+'\');" '
                         out = 'onmouseout="nodisplayImage();" '
                         
                         html += '<TH ALIGN=LEFT><A HREF="#" '+click+over+out+'">plot</a>'
                '''
                            
                            
        html += '</TABLE>'
        
        
        return html
      

    
        
    
    except:
        tb = traceback.format_exc()
        print 'tb: ' + tb
        return HttpResponse("error")
    
    
    

    return html


def generate_token_url(filename):
    import os, time, hashlib
    
    secret = "secret string"#config.get("options","secret_key")
    protectedPath = "/acme-data/"#config.get("options", "protectedPath")
    
    
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
        
        
        #print '\nIn GET\n'  
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
    
        #print '\nIn GET\n'  
        logger.debug('\nIn Dataset_Access PUT\n')
        
        #load the json object
        json_data = json.loads(request.body)
            
        
        #grab the dataset added
        dataset = json_data['dataset'] #should be a string
    
        from exploratory_analysis.models import Dataset_Access
        
        #grab the group record
        da = Dataset_Access.objects.filter(group_name=group_name)
        
        #for put, APPEND the new dataset given
        #append dataset to the end of the dataset list
        
        new_dataset_list = ''
        if da:
            new_dataset_list = da[0].dataset_list
            
            new_dataset_list_list = new_dataset_list.split(',')
            
            isDuplicate = False
            
            #check for duplicates
            for entry in new_dataset_list_list:
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
        
    
        return HttpResponse("PUT Done\n")   
    
    def post(self, request, group_name):
        
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
        
        all = Dataset_Access.objects.all()
        
    
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
    
            return HttpResponse(data_string + "\n")
            
            return HttpResponse("response")
        except:
            tb = traceback.format_exc()
            logger.debug('tb: ' + tb)
            return HttpResponse("error")
        
        return HttpResponse("respone")






#gets packages information
#Service API for the Dataset_Access table
#GET
#http://<host>:<port>/exploratory_analysis/dataset_packages/<dataset_name>
#POST
#echo '{ "dataset" :  <dataset_name> }' | curl -d @- 'http://<host>:<port>/exploratory_analysis/dataset_packages/(?P<dataset_name>\w+)/$' -H "Accept:application/json" -H "Context-Type:application/json"
#DELETE
#http://<host>:<port>/exploratory_analysis/group_dataset/<group_name>
class PackagesView(View):
    
    
    
    def get(self, request, dataset_name):
        
        from exploratory_analysis.models import Packages
    
        #print '\nIn GET\n'  
        logger.debug('\nIn GET\n')
        
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

        
        logger.debug("End GET\n")
        return HttpResponse(data_string)# + "\

    
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
    
