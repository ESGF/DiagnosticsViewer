from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from django.template import RequestContext, loader
from django.contrib.auth import authenticate, login
from django.conf import settings
from metrics.frontend import lmwgmaster
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django.templatetags.static import static
#from metrics.frontend.lmwgmaster import *
from django.contrib.staticfiles.storage import staticfiles_storage

import amwg
import lmwg

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import Dataset

import json
import logging
import traceback
import os
import shutil
from output_viewer.page import Page

from utils import isLoggedIn, generate_token_url

logger = logging.getLogger('exploratory_analysis')
logger.setLevel(logging.DEBUG)



fh = logging.FileHandler('exploratory_analysis.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)

# add handler to logger object
logger.addHandler(fh)

config = settings.CONFIG


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
root_dir = config.get('paths', 'root')
ea_root = os.path.join(root_dir, config.get('paths', 'ea_dir'))

img_cache_path = os.path.join(root_dir, config.get('paths', 'img_cache_path'))

staticfiles_dirs = os.path.join(root_dir, config.get('paths', 'staticfiles_dirs'))

javascript_namespace = config.get('namespaces','javascript_namespace')

data_path = config.get("paths", "dataPath")


EA_hostname = config.get("options", "hostname")
EA_port = config.get("options", "port")


def index(request):

    template = loader.get_template('exploratory_analysis/index.html')

    context = RequestContext(request, {
        'username' : '',
    })

    return HttpResponse(template.render(context))


def login_page(request):

    template = loader.get_template('exploratory_analysis/login.html')

    context = RequestContext(request, {

    })

    return HttpResponse(template.render(context))


def logout_page(request):
    from django.contrib.auth import logout
    logout(request)

    template = loader.get_template('exploratory_analysis/logout.html')

    loggedIn = False

    context = RequestContext(request, {
        'loggedIn' : str(loggedIn)
    })

    return HttpResponse(template.render(context))

#authentication based on the django user model
#VERY SIMPLISTIC - user will have to user either the ACME username or register with a simple new account
def auth_noesgf(request):

    json_data = json.loads(request.body)

    username = json_data['username']
    password = json_data['password']

    user = authenticate(username=username,password=password)

    print 'in auth_noesgf: ' + str(user)
    if user is not None:
        login(request,user)
        return HttpResponse('Authenticated')
    else:
        return HttpResponse('Not Authenticated')


def config(request):

    sets = str(request.GET.get('set',None))
    dataset_name = str(request.GET.get('dataset_name',None))

    config_params = dict( {'EA_hostname' : str(EA_hostname)} )
    config_params['EA_port'] = str(EA_port)

    data = config_params#{'config_params' : config_params}
    data_string = json.dumps(data,sort_keys=False,indent=2)#,indent=2)

    #print 'packages data_string: ' + str(data_string)
    return HttpResponse(data_string + '\n')


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


@login_required
def output(request, dataset, package):
    try:
        dataset = Dataset.objects.get(name=dataset, owner=request.user)
        package_index = os.path.join(dataset.path, "%s-index.json" % package)
        if os.path.exists(package_index):
            # Should now rebuild the pages in case of updates
            with open(package_index) as ind:
                index = json.load(ind)
            for spec in index["specification"]:
                if "short_name" not in spec:
                    spec["short_name"] = spec["title"].split()[0].lower()
                # Hack the filename to have the package prefix
                for group in spec["rows"]:
                    for row in group:
                        for col in row["columns"]:
                            if isinstance(col, dict):
                                if "path" in col:
                                    p = col["path"]
                                    fname, ext = os.path.splitext(p)
                                    fname = os.path.join(package, fname)
                                    fname = "--".join(fname.split(os.sep))
                                    fpath = slugify(fname) + ext
                                    col["path"] = fpath

                p = Page(spec, root_path=dataset.path)
                p.build(os.path.join(dataset.path, "%s-%s" % (package, spec["short_name"])))
            template = loader.get_template("exploratory_analysis/output_index.html")
            return HttpResponse(template.render({"spec": index, "package": package}))
        else:
            return HttpResponse("No package matching %s found." % package, status="404")
    except Dataset.DoesNotExist:
        return HttpResponse("No dataset matching %s found for user." % dataset, status="404")


@login_required
def output_file(request, dataset, package, path):
    try:
        dataset = Dataset.objects.get(name=dataset, owner=request.user)
    except Dataset.DoesNotExist:
        # Need to check if user is in group with access to dataset
        return HttpResponse("No dataset matching %s found for user." % dataset, status="404")

    package_index = os.path.join(dataset.path, "%s-index.json" % package)
    if not os.path.exists(package_index):
        return HttpResponse("No package %s found." % package, status="404")

    if path.startswith("viewer"):
        # Map to our scripts/css files
        _, filename = os.path.split(path)
        if filename.endswith("css"):
            mime = "text/css"
            if filename.startswith("bootstrap"):
                f = open(staticfiles_storage.path("exploratory_analysis/css/bootstrap/bootstrap.css"))
            elif filename.startswith("viewer"):
                f = open(staticfiles_storage.path("exploratory_analysis/css/viewer.css"))
        elif filename.endswith('js'):
            mime = "text/javascript"
            if filename.lower().startswith("jquery"):
                f = open(staticfiles_storage.path('exploratory_analysis/js/jquery/jquery-1.10.2.min.js'))
            elif filename.lower().startswith("viewer"):
                f = open(staticfiles_storage.path('exploratory_analysis/js/viewer.js'))
            elif filename.lower().startswith("bootstrap"):
                f = open(staticfiles_storage.path('exploratory_analysis/js/bootstrap/bootstrap.min.js'))
        return HttpResponse(f, content_type=mime)

    if path.startswith("%s-" % package):
        file_path = os.path.join(dataset.path, path)
    else:
        file_path = os.path.join(dataset.path, "%s-%s" % (package, path))

    if not os.path.exists(file_path):
        return HttpResponse("No file %s found in package." % file_path, status="404")

    return HttpResponse(open(file_path))


@login_required
def browse_datasets(request):
    datasets = request.user.dataset_set.all()
    template = loader.get_template("exploratory_analysis/browse.html")
    return HttpResponse(template.render({"datasets": datasets}))

#classic view
#url(r'^classic/(?P<user_id>\w+)/$',views.classic,name='classic'),
def classic(request,user_id):

    loggedIn = isLoggedIn(request,user_id)

    template = loader.get_template('exploratory_analysis/classic.html')

    if not loggedIn:
        template = loader.get_template('exploratory_analysis/not_logged_in.html')


    context = RequestContext(request, {
        'username' : str(user_id),
        'loggedIn' : str(loggedIn)
    })

    return HttpResponse(template.render(context))


def classic_set_list_html(request):

    #print 'in classic_set_list_html'

    package = request.GET.get('package','')
    #print 'package: ' + package

    '''
    json_data = json.loads(request.body)
    project = json_data['project']
    dataset = json_data['dataset']
    pckg = json_data['pckg']
    variables = json_data['variables']
    times = json_data['times']
    '''

    if (package == 'atm' or package == 'amwg'):
        #print 'getting atm home'
        template = loader.get_template('exploratory_analysis/atm_home.html')
        context = RequestContext(request, {

        })
        return HttpResponse(template.render(context))
    else:
        #print 'getting lnd home'
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
    sets = str(request.GET.get('set',None))
    dataset = str(request.GET.get('dataset_name',None))
    package = str(request.GET.get('package', None))
    if dataset == None or sets == None or package == None:
      print 'Sets or dataset not passed properly. We should never get here.'
      quit()

    print 'Got %s - %s - %s' % (package, dataset, sets)

    varlist = 'TLAI'
    times = 't1'
    options = []

    #print 'IN CLASSIC_VIEWS_HTML - SET: ', sets
    html = ''

    try:
        if package == 'lnd':
            html = lmwg.pageGenerator(sets, varlist, times, package, dataset, options)
        else:
            html = amwg.pageGenerator(sets, varlist, times, package, dataset, options)

    except:
        tb = traceback.format_exc()
        #print 'tb: ' + tb
        return HttpResponse("error")

#    print 'returning html: ' + str(html)

    return HttpResponse(html)



def provenance(request):

    filename = request.GET.get('filename', '')
    dataset_name = request.GET.get('dataset_name','')
    package = request.GET.get('package','')
    path = config.get('paths', 'dataPath')

    import vcs
    fname = os.path.join(path, dataset_name, package, filename)
#    print 'Looking for metadata in ', fname

    md = vcs.png_read_metadata(fname)
#    print 'Found: (%s)' % md

    if md == None or type(md) is not dict or md == {}:
      html = '<p>No provenance data found for ' + filename + '</p>'
    else:
      html = '<table border=1>'
      for k in md.keys():
         html += '<tr><td>%s</td><td>%s</td></tr>' % ( k, md[k])
      html += '</table>'

#    print 'html: ', html

    return HttpResponse(html)



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

        print '*****Begin ESGF Login*****'
        import traceback
        cert_name = certNameSuffix
        outdir = os.path.join(proxy_cert_dir, username)
        print 'Authreq: (%s)' % authReq
        print type(authReq)

        if authReq == 'False':
            print 'Returning "authenticated"'
            return HttpResponse('Authenticated')

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
                                        outfile,
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
                user = authenticate(username=username, password=password)

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
