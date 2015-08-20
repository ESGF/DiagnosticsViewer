from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from django.template import RequestContext, loader
from django.contrib.auth import authenticate, login

from metrics.frontend import lmwgmaster
#from metrics.frontend.lmwgmaster import *

import amwg
import lmwg

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import ensure_csrf_cookie

import json
import logging
import traceback
import os

from utils import generate_token_url

logger = logging.getLogger('exploratory_analysis')
logger.setLevel(logging.DEBUG)



fh = logging.FileHandler('exploratory_analysis.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)

# add handler to logger object
logger.addHandler(fh)

import ConfigParser

print 'This one is looking for ./exploratory_analysis/eaconfig.cfg'
config = ConfigParser.ConfigParser()
config.read('./exploratory_analysis/eaconfig.cfg')



#various variables that need to go into a config file
#esgfAuth - flag for turning on (True) or turning off (False) esgf authentication
#esgfAuth = False
esgfAuth = config.get("options", "esgfAuth")

#the directory for the certs to be fetched
#proxy_cert_dir = '/tmp'
proxy_cert_dir = config.get("certificate", "proxy_cert_dir")


#naAuthReq - authentication via the cookie on (True) or off (False)
#authReq = True
authReq = config.get("options", "authReq")



#certNameSuffix - the suffix of the certificate file
#certNameSuffix = 'x509acme'
certNameSuffix = config.get("certificate","certNameSuffix")

#ea_root = '/Users/8xo/software/exploratory_analysis/DiagnosticsViewer'
ea_root = config.get('paths','ea_root')

#uvcdat_live_root = ea_root+ '/django-app-1.8/uvcdat_live/' 
uvcdat_live_root = config.get('paths','uvcdat_live_root')

#img_cache_path = uvcdat_live_root + '/exploratory_analysis/static/exploratory_analysis/cache/'
img_cache_path = config.get('paths','img_cache_path')

#staticfiles_dirs = uvcdat_live_root + "/exploratory_analysis/static/exploratory_analysis"
staticfiles_dirs = config.get('paths','staticfiles_dirs')


#javascript_namespace = 'EA_CLASSIC_VIEWER.functions.'
javascript_namespace = config.get('namespaces','javascript_namespace')


# Main page.
def index(request):
    
    template = loader.get_template('exploratory_analysis/index.html')

    context = RequestContext(request, {
        'username' : '',
    })

    return HttpResponse(template.render(context))


#http://<host>/exploratory_analysis/login
def login_page(request):
    
    template = loader.get_template('exploratory_analysis/login.html')

    context = RequestContext(request, {
        
    })

    return HttpResponse(template.render(context))

def logout_page(request):
    
    
    print 'going to logout.html...'
    
    from django.contrib.auth import logout
    logout(request)
    
    template = loader.get_template('exploratory_analysis/logout.html')

    loggedIn = False
    
    context = RequestContext(request, {
        'loggedIn' : str(loggedIn)
    })

    return HttpResponse(template.render(context))






#Example: curl -i -H "Accept: application/json" -X POST -d '{ "username" :  "u1" }'  http://localhost:8081/exploratory_analysis/auth/
#@ensure_csrf_cookie
def auth(request):
    
    
    if request.method == "POST":
        
        json_data = json.loads(request.body)
        
        username = json_data['username']
        password = json_data['password']
        
        #return a None message if the username is blank
        if username == '':
            return HttpResponse("Not Authenticated")
        elif username == None:
            return HttpResponse("Not Authenticated")
        
        #insert code for authentication here
        #create a valid user object
        
        from fcntl import flock, LOCK_EX, LOCK_UN
        print '*****Begin ESGF Login*****'
        import traceback
        cert_name = certNameSuffix
        outdir = os.path.join(proxy_cert_dir, username)
        
        
        try:
                
                if not os.path.exists(outdir):
                    os.makedirs(outdir)
                else:
                    print 'Did not make directory - path already exists'
                
                outfile = os.path.join(outdir, cert_name)
                outfile = str(outfile)
                
                # outfile = '/tmp/x509up_u%s' % (os.getuid()) 
                #print '----> OUTFILE: ', outfile
                   
                import myproxy_logon
                
                #username = username1
                #password = password1
                peernode = 'esg.ccs.ornl.gov'
           
                myproxy_logon.myproxy_logon(peernode,
                      username,
                      password,
                      outfile,#os.path.join(cert_path,username + '.pem').encode("UTF-8"),
                      lifetime=43200,
                      port=7512
                      )
            
            
                user = authenticate(username=username,password=password)
                
                
                if user is not None:
                    login(request,user)
                    return HttpResponse('Authenticated')
                    
                    
                else:
                    
                    from django.contrib.auth.models import User
                
                    user = User.objects.create_user(username, str(username + '@acme.com'), password)
                    user = authenticate(username=username,password=password)
                    
                    #login to the app and return the string "Authenticated"
                    login(request,user)
                
                    return HttpResponse('Authenticated')
                
                print '*****End ESGF login*****'
                
        except:
                tb = traceback.format_exc()
                logger.debug('tb: ' + tb)
                return HttpResponse("Not Authenticated")
        
    else:
        
        return HttpResponse("Not Authenticated")
    
    
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
    #print 'user: ' + str(request.user)
    
    loggedIn = False
    
    if (str(request.user) == str(user_id)):
        loggedIn = True
        
    return loggedIn



def classic(request,user_id):

    loggedIn = isLoggedIn(request,user_id)
    
    template = loader.get_template('exploratory_analysis/classic.html')
    
    if(loggedIn == False):
        template = loader.get_template('exploratory_analysis/not_logged_in.html')
    
    
    context = RequestContext(request, {
        'username' : str(user_id),
        'loggedIn' : str(loggedIn)
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
    """
    Generate new clasic view html
    The view shown depends on the package
    """    
    sets = str(request.GET.get('set',''))
    
    #sets = str(set[3:])
    varlist = 'TLAI'
    times = 't1'
    dataset = 'd1'
    options = []
    package = ''
    
    html = ''
    
    try:
        if package == 'lnd':
            html = lmwg.pageGenerator(sets, varlist, times, package, dataset, options)
        else:
            html = amwg.pageGenerator(sets, varlist, times, package, dataset, options)
    
    except:
        tb = traceback.format_exc()
        print 'tb: ' + tb
        return HttpResponse("error")
        
    print 'returning html: ' + str(html)
    
    return HttpResponse(html)














