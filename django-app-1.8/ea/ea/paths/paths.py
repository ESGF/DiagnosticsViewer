import ConfigParser
import os
print os.getcwd()
# some day, we could check for all of the "derived" paths and use them if defined, otherwise derive them.

print 'This one is looking for ../eaconfig.cfg in uvcdat_live/paths/paths.py'
config = ConfigParser.ConfigParser()
config.read('eaconfig.cfg')

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

database_name = database_root +"/mydb.db"

uvcdat_live_root = ea_root+ '/django-app/uvcdat_live/' 
staticfiles_dirs = uvcdat_live_root + "/exploratory_analysis/static/exploratory_analysis"
template_dirs = uvcdat_live_root + "/exploratory_analysis/templates/exploratory_analysis"
cache_dir = uvcdat_live_root + '/exploratory_analysis/static/exploratory_analysis/cache/tree/'
img_cache_path = uvcdat_live_root + '/exploratory_analysis/static/exploratory_analysis/cache/'
timeseries_cache_path = uvcdat_live_root +'/exploratory_analysis/static/exploratory_analysis/cache'
generated_img_path = uvcdat_live_root + '/exploratory_analysis/static/exploratory_analysis/img/treeex/'
message_reader_template_dirs = uvcdat_live_root + '/message_reader/templates/message_reader'

syspath_append_uvcmetrics = metrics_root + '/src/python'

syspath_append_cdscan = uvcdat_root+ '/install/Library/Frameworks/Python.framework/Versions/2.7/bin/cdscan'

default_sample_data_dir = data_root

default_tree_sample_data_dir = default_sample_data_dir
default_map_sample_data_dir = default_sample_data_dir + dataset_name
