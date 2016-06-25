import ConfigParser

# some day, we could check for all of the "derived" paths and use them if defined, otherwise derive them.

config = ConfigParser.ConfigParser()
config.read('eaconfig.cfg')

ea_hostname = config.get("paths",'ea_hostname')
esgf_hostname = config.get("paths",'esgf_hostname')
esgf_port = config.get("paths",'esgf_port')

try:
   ea_root = config.get("paths", "ea_root")
except:
   print '-------> Couldnt find ea_root in paths section of eaconfig.cfg.'
   print 'Exiting'
   quit()

data_root = config.get("paths", "data_root")
uvcdat_root = config.get("paths", "uvcdat_root")
database_root = config.get("paths", "database_root")
metrics_root = config.get("paths", "metrics_root")

dataset_name = config.get("data", "dataset_names")

noAuthReq = config.get("options", "loggedIn")
if type(noAuthReq) is str and noAuthReq == 'True':
   noAuthReq = True
else:
   noAuthReq = False
   
esgfAccess = config.get("options","esgfAccess")
if type(esgfAccess) is str and esgfAccess == 'True':
   esgfAccess = True
else:
   esgfAccess = False
   
esgfAuth = config.get("options","esgfAuth")
if type(esgfAuth) is str and esgfAuth == 'True':
   esgfAuth = True
else:
   esgfAuth = False
   
secret = config.get("options","secret_key")
protectedPath = config.get("options", "protectedPath")

database_name = database_root +"/mydb.db"

uvcdat_live_root = ea_root+ '/django-app/uvcdat_live/' 
staticfiles_dirs = uvcdat_live_root + "/exploratory_analysis/static/exploratory_analysis"
template_dirs = uvcdat_live_root + "/exploratory_analysis/templates/exploratory_analysis"
cache_dir = uvcdat_live_root + '/exploratory_analysis/static/exploratory_analysis/cache/tree/'
img_cache_path = uvcdat_live_root + '/exploratory_analysis/static/exploratory_analysis/cache/'
timeseries_cache_path = uvcdat_live_root +'/exploratory_analysis/static/exploratory_analysis/cache'
generated_img_path = uvcdat_live_root + '/exploratory_analysis/static/exploratory_analysis/img/tree/'

proxy_cert_dir = config.get("options", "proxy_cert_dir")

syspath_append_uvcmetrics = metrics_root + '/src/python'

syspath_append_cdscan = uvcdat_root+ '/install/Library/Frameworks/Python.framework/Versions/2.7/bin/cdscan'

default_sample_data_dir = data_root

default_tree_sample_data_dir = default_sample_data_dir
default_map_sample_data_dir = default_sample_data_dir + dataset_name

def generate_token_url(filename):
    import os, time, hashlib
    
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
