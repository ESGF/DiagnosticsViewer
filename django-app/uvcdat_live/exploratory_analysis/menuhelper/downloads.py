import json



import sys, os

sys.path.append(str(os.getcwd() + '/exploratory_analysis'))


from paths import paths

from defaults import parameter_defaults


syspath_append_uvcmetrics = paths.syspath_append_uvcmetrics
syspath_append_cdscan = paths.syspath_append_cdscan

paths_cache_dir = paths.cache_dir
#paths_front_end_cache_dir = paths.front_end_cache_dir

default_sample_data_dir = paths.default_sample_data_dir



def getFileList(dataset_id):
    
    import glob
    import json
    from django.contrib.auth.models import User
    
    downloads = []
    
    for f in glob.glob(default_sample_data_dir + '/' + dataset_id + '/climos/*'):
      f_arr = f.split('/')
      print f
      downloads.append(f_arr[len(f_arr)-1])
    
    print 'file_list: ' + str(downloads)
    
    return downloads

