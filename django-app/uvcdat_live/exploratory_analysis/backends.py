'''
class ESGF_Auth_Backend:

    Custom backend to log-in with an ESGF OpenID. Saves a certificate + private
    key as settings.proxy_cert_dir/username/username.pem
    and create .httprc if not already created as settings.proxy_cert_dir/username/.httprc
    (eg: /esgserver/proxycerts/jsmith/jsmith.pem)
'''

import os

import ConfigParser

# some day, we could check for all of the "derived" paths and use them if defined, otherwise derive them.

config = ConfigParser.ConfigParser()
config.read('eaconfig.cfg')


def authenticate1(username=None,password=None,peernode=None):
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
	'''        
	if not os.path.exists(cert_path):
            try:
                os.makedirs(cert_path)
            except:
                pass
        '''
        outfile = '/tmp/x509up_u%s' % (os.getuid()) 
        
        import myproxy_logon
           
        myproxy_logon.myproxy_logon(peernode,
                      username,
                      password,
                      outfile,#os.path.join(cert_path,username + '.pem').encode("UTF-8"),
                      lifetime=43200,
                      port=7512
                      )
            
        print '*****End ESGF login*****'
    except:
        print traceback.print_exc()
        print '*****End ESGF login*****'
        return None
        
    
    
    # if we make it here, the username and password were good
    # output .httprc file if .httprc is not found
    try:
        
         print '+++++.httprc gen+++++'
         '''
         homepath=os.environ['HOME']
         filepath=os.path.join(homepath,".daprc")
         print 'filepathh: ' + filepath
         
         if not os.path.exists(filepath):
             
             print 'filepath does not exist'
             print 'here'
             dodsrc_cache_root=os.path.join(cert_path,".dods_cache")
             dodsrc_curl_ssl_certificate=os.path.join(cert_path,"%s.pem"%username)
             dodsrc_curl_ssl_key=os.path.join(cert_path,"%s.pem"%username)
             dodsrc_curl_ssl_capath=os.path.join(os.environ["HOME"],".esg","certificates")
             
             daprc_text=""
             daprc_text+="USE_CACHE=0\n"
             daprc_text+="MAX_CACHE_SIZE=20\n"
             daprc_text+="MAX_CACHED_OBJ=5\n"
             daprc_text+="IGNORE_EXPIRES=0\n"
             daprc_text+="CACHE_ROOT=%s/\n"%dodsrc_cache_root
             daprc_text+="DEFAULT_EXPIRES=86400\n"
             daprc_text+="ALWAYS_VALIDATE=0\n"
             daprc_text+="DEFLATE=0\n"
             daprc_text+="VALIDATE_SSL=1\n"
             daprc_text+="CURL.COOKIEJAR=.dods_cookies\n"
             daprc_text+="CURL.SSL.VALIDATE=1\n"
             daprc_text+="CURL.SSL.CERTIFICATE=%s\n"%dodsrc_curl_ssl_certificate
             daprc_text+="CURL.SSL.KEY=%s\n"%dodsrc_curl_ssl_key
             daprc_text+="CURL.SSL.CAPATH=%s\n"%dodsrc_curl_ssl_capath
             outfile=open(filepath, 'w')
             flock(outfile, LOCK_EX)
             outfile.write(daprc_text)
             flock(outfile, LOCK_UN)
             outfile.close()
             
             
             print 'dodsrc_cache_root: ' + dodsrc_cache_root
             print 'dodsrc_curl_ssl_certificate: ' + dodsrc_curl_ssl_certificate
             print 'dodsrc_curl_ssl_key: ' + dodsrc_curl_ssl_key
             print 'dodsrc_curl_ssl_capath: ' + dodsrc_curl_ssl_capath
             print 'daprc: ' + dodsrc_curl_ssl_capath
             
             # if we make it here, the username and password were good
             # (myproxy_logon throws GetException if login fails)
         '''    
         
         print '+++++end .httprc gen+++++'
         
         from django.contrib.auth.models import User
         from django.contrib.auth import authenticate
         
         print '------Get/Create the django user object-----'
         
         # try to extract a user from Django's authentication mechanism
         try:
            
            user = User.objects.get(username=username)
         
            print 'user before authenticate: ' + str(user)
            
            
            #user = authenticate(username=username,password='Mattryan12')
            print 'username: ' + username + ' authenticated fine'
            
            print 'user: ' + str(user)
            
            print '------end Get/Create the django user object-----'
            return user
            
         # except if the user has not been added to Django's database
         except User.DoesNotExist:
             
            print 'user does not exist in django - creating user account'
            user = User(username=username,
                         password=password)
            
            #user = authenticate(username=username, password='Mattryan12')
            
            user.is_staff = False
            user.is_superuser = False
            user.save()
         
         
            print '\n\ndir\n\n'
            print dir(user)
            print '------end Get/Create the django user object-----'
            return user
             
             
         
    except Exception as e:
        print e
        print "Unable to locate .daprc\n"
        return None
        


    
        
       
        
        
    '''
    except GetException as e:
        print e
        # myproxy_logon failed, so return None instead of a User
        #
        # TODO: When Django 1.6 comes out, this should be changed to:
        #
        # raise PermissionDenied
        #
        # This will prevent the possibility of someone listing multiple
        # authentication backends in their settings.py, thus allowing an
        # attacker to authenticate as any user simply by using the default
        # password assigned to all users created by this auth backend.
        return None
    '''

'''
def myproxy_logon(hostname,username,passphrase,outfile,lifetime=43200,port=7512):
    print 'in myproxy_logon'
    
    print 'hostname: ' + hostname
    print 'username: ' + username
    print 'passphrase: ' + passphrase
    print 'outfile: ' + outfile
    print 'lifetime: ' + str(lifetime)
    print 'port: ' + str(port)
'''    
    
    
