import sys, os
sys.path.append(str(os.getcwd() + '/exploratory_analysis'))
from paths import paths


from django.http import HttpResponse
from django.http import HttpResponseServerError

from django.http import HttpResponseRedirect

def aaa():
    print 'aaa'
    
    
def esgf_login(request):
    print 'in test1'
    
    username1 = ''
    password1 = ''
    peernode1 = 'esg.ccs.ornl.gov'
    
    curlFlag = False
    
    if curlFlag:
        json_data = json.loads(request.body)
        username1 = json_data['username'] #should be a string
        password1 = json_data['password'] #should be a list
    
    else:
        
        username1 = request.POST['username']
        password1 = request.POST['password']
    
    from OpenSSL import crypto,SSL
    
    # for POST requests, attempt logging-in
    if request.POST:
        print 'it is a post...authenticating'
        
        #from backends import authenticate1
        
        print 'paths.esgfAuth: ' + str(paths.esgfAuth)
        
        #authenticates to ESGF
        if paths.esgfAuth:
            
            print '\n\n\nin esgfAuth'
            
            
            #user = authenticate1(username = username1,
            #                 password = password1,
            #                 peernode = peernode1)
            
            
            #authenticate to esgf here
            print "AUTHENTICATE NOW"

            from fcntl import flock, LOCK_EX, LOCK_UN


            print '*****Begin ESGF Login*****'

            import traceback
        
            try:
            #substitute
            #settings.PROXY_CERT_DIR = /tmp
            #username = 'jfharney'
            #proxy_cert_dir = config.get("options", "proxy_cert_dir")
            #username = 'jfharney'
            #cert_path=os.path.join(proxy_cert_dir,username)
            #print 'cert_path: ' + cert_path
		cert_name = 'x509acme'
		outdir = os.path.join(paths.proxy_cert_dir, username1)
		try:
			os.makedirs(outdir)
		except:
			print 'makedirs \'', outdir, '\' failed. Directory probably already exists'
			pass
		outfile = os.path.join(outdir, cert_name)
		outfile = str(outfile)
                
#                outfile = '/tmp/x509up_u%s' % (os.getuid()) 
		print '----> OUTFILE: ', outfile
        
                import myproxy_logon
           
                username = username1
                password = password1
                peernode = peernode1
           
                myproxy_logon.myproxy_logon(peernode,
                      username,
                      password,
                      outfile,#os.path.join(cert_path,username + '.pem').encode("UTF-8"),
                      lifetime=43200,
                      port=7512
                      )
            
                print '*****End ESGF login*****'
                
            except:
                print 'in the exception'
                print traceback.print_exc()
                print '*****End ESGF login*****'
                
                return HttpResponse('Not Authenticated')
        
            user = authenticate(username=username1,password=password1)
            #return HttpResponse('Authenticated')
            
            
            
            if user is not None:
                
                #authenticate to django
                
                print 'user n: ' + str(user.username)# + ' ' + str(user.password)
            
                #login to the app and return the string "Authenticated"
                login(request,user)
                return HttpResponse('Authenticated')
            else:
                print 'user is None'
                
                from django.contrib.auth.models import User
                
                user = User.objects.create_user(username1, str(username1 + '@acme.com'), password1)
                user = authenticate(username=username1,password=password1)
            
                print str('username1: ' + username1)
#                print str('password1: ' + password1)
                
                #login to the app and return the string "Authenticated"
                login(request,user)
                
                return HttpResponse('Authenticated')
            
            
            
        else:
            
            user = authenticate(username=username1,password=password1)
            if user is not None:
                
                #authenticate to django
                
                print 'user n: ' + str(user.username)# + ' ' + str(user.password)
            
                #login to the app and return the string "Authenticated"
                login(request,user)
                return HttpResponse('Authenticated')
            else:
                print 'user is None'
                
                from django.contrib.auth.models import User
                
                user = User.objects.create_user(username1, str(username1 + '@acme.com'), password1)
                user = authenticate(username=username1,password=password1)
            
                print str('username1: ' + username1)
#                print str('password1: ' + password1)
                
                #login to the app and return the string "Authenticated"
                login(request,user)
                
                return HttpResponse('Authenticated')
        
        return HttpResponse('Authenticated')

    else:
        print 'it is not a post'
        return HttpResponse('Not Authenticated')
        

'''
    from OpenSSL import crypto,SSL
    
    # for POST requests, attempt logging-in
    if request.POST:
        print 'it is a post...authenticating'
        
        from backends import authenticate1
        
        
        
        #authenticates to ESGF
        if paths.esgfAuth:
            
            print '\n\n\nin esgfAuth'
            
            
            #user = authenticate1(username = username1,
            #                 password = password1,
            #                 peernode = peernode1)
            
            
            #authenticate to esgf here
            print "AUTHENTICATE NOW"

            from fcntl import flock, LOCK_EX, LOCK_UN


            print '*****Begin ESGF Login*****'

            import traceback
        
            try:
            #substitute
            #settings.PROXY_CERT_DIR = /tmp
            #username = 'jfharney'
            #proxy_cert_dir = config.get("options", "proxy_cert_dir")
            #username = 'jfharney'
            #cert_path=os.path.join(proxy_cert_dir,username)
            #print 'cert_path: ' + cert_path
                
                outfile = '/tmp/x509up_u%s' % (os.getuid()) 
        
                import myproxy_logon
           
                username = username1
                password = password1
                peernode = peernode1
           
                myproxy_logon.myproxy_logon(peernode,
                      username,
                      password,
                      outfile,#os.path.join(cert_path,username + '.pem').encode("UTF-8"),
                      lifetime=43200,
                      port=7512
                      )
            
                print '*****End ESGF login*****'
                
            except:
                print 'in the exception'
                print traceback.print_exc()
                print '*****End ESGF login*****'
                
                return HttpResponse('Not Authenticated')
        
            user = authenticate(username=username1,password=password1)
            #return HttpResponse('Authenticated')
            
            
            
            if user is not None:
                
                #authenticate to django
                
                print 'user n: ' + str(user.username) #+ ' ' + str(user.password)
            
                #login to the app and return the string "Authenticated"
                login(request,user)
                return HttpResponse('Authenticated')
            else:
                print 'user is None'
                
                from django.contrib.auth.models import User
                
                user = User.objects.create_user(username1, str(username1 + '@acme.com'), password1)
                user = authenticate(username=username1,password=password1)
            
                print str('username1: ' + username1)
                #print str('password1: ' + password1)
                
                #login to the app and return the string "Authenticated"
                login(request,user)
                
                return HttpResponse('Authenticated')
            
            
            
        else:
            
            user = authenticate(username=username1,password=password1)
            if user is not None:
                
                #authenticate to django
                
                print 'user n: ' + str(user.username)# + ' ' + str(user.password)
            
                #login to the app and return the string "Authenticated"
                login(request,user)
                return HttpResponse('Authenticated')
            else:
                print 'user is None'
                
                from django.contrib.auth.models import User
                
                user = User.objects.create_user(username1, str(username1 + '@acme.com'), password1)
                user = authenticate(username=username1,password=password1)
            
                print str('username1: ' + username1)
                #print str('password1: ' + password1)
                
                #login to the app and return the string "Authenticated"
                login(request,user)
                
                return HttpResponse('Authenticated')
        
        return HttpResponse('Authenticated')

    else:
        print 'it is not a post'
'''  
