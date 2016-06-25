#flag for toggling connection to the diags backend
isConnected = True


# Create your views here.
from django.http import HttpResponse
from django.template import RequestContext, loader
#from exploratory_analysis.models import Diags
import json
import sys, os

sys.path.append(str(os.getcwd() + '/exploratory_analysis'))


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
    #sys.path.append(syspath_append_uvcmetrics)
    #sys.path.append(syspath_append_cdscan)
   
    
    from metrics.frontend.options import Options
    from metrics.computation.reductions import *
    from metrics.fileio.filetable import *
    from metrics.fileio.findfiles import *

    from metrics.exploratory.treeview import TreeView 

cache_dir = paths_cache_dir
#front_end_cache_dir = paths_front_end_cache_dir#'../../../static/cache/'




#use these objects temporarily
figures_store = {}


def bookmarkHandler(request,user_id):

  print '\nin bookmarkHandler'
  #print '\nrequest user authenticate: ' + str(request.user.is_authenticated()) + '\n'
    
    
  # get the user name  
  loggedIn = paths.noAuthReq
   
    
  if (str(request.user) == str(user_id)):
    loggedIn = True
    
  username = 'jfharney'
    
  #grab the username
  if user_id != None:
    username = user_id
    
  loggedIn = True  
    
  #get the predefined tree bookmarks of the user
  from exploratory_analysis.models import Tree_Bookmarks
  bookmark_list_obj = Tree_Bookmarks.objects.filter(tree_bookmark_username=username)
  
  bookmark_list = [] 
  for obj in bookmark_list_obj:
    bookmark_list.append(obj.tree_bookmark_name)
 
  
 

  #get the figure bookmarks of the user
  from exploratory_analysis.models import Figure_Bookmarks
  figure_bookmark_list_obj = Figure_Bookmarks.objects.filter(figure_bookmark_username=username)
 
  figure_bookmark_list = [] 
  for obj in figure_bookmark_list_obj:
    figure_bookmark_list.append(obj.figure_bookmark_name)
 
 
 
  
  #defaults = parameter_defaults.get_parameter_defaults()
  defaults = get_parameter_defaults()
  package_list = defaults['package_list']
  dataset_list = defaults['dataset_list']
  variable_list = defaults['variable_list']
  season_list = defaults['season_list']
  set_list = defaults['set_list']
    
 

  
  #not sure why this is here - closer look when refining      
  treeloaded = 'true'
  
  
  #grab the bookmark name
  bookmark = request.GET.get('bookmark')
  bookmark_name = bookmark
    
  #convert the bookmark name to the bookmark file name
  fileName = bookmark + ".json"
    
  #cached_file_name = front_end_cache_dir + fileName
  #'../../../static/exploratory_analysis/cache/tree/uu1/json/tropics_warming_th_q_co2/'
  
  dataset = ''
  path = ''
  
  #the root directory of the tree files
  tree_cache_root_dir = '../../../static/exploratory_analysis/cache/tree/' + username
  
  #convert to the physical location
  tree_cache_root_dir = convertRelToAbsPath(tree_cache_root_dir)
  
  #find the location of the tree file 
  f = findTreeFile(fileName, tree_cache_root_dir)
  
  #if the file was found then the bookmark exists and set it equal to the dataset
  if f:
      print 'the bookmark was found!'
      #print str(f)
      dataset = findTreeDataset(str(f))
      #print '\tdataset returned...\n' + dataset
  #something is really wrong if is false
  else:
      print 'the bookmark wasnt found???'
  
          
      
  cached_file_name = '../../../static/exploratory_analysis/cache/tree/' + username + '/json/' + dataset + '/' + fileName  
  #print 'before---> ' + cached_file_name
  check_file_name = convertRelToAbsPath(cached_file_name)
  #print 'after---> ' + check_file_name
  
  
  treeFile = None
       
  import os
        
    
  treeFile = str(check_file_name)
  '''
        #if exists then return the tree state of that bookmark
  if os.path.exists(check_file_name):
    #print 'Bookmark is there - proceed'   
    treeFile = diagsHelper(user_id,bookmark_name,check_file_name)
  else:
    #print 'Bookmark is not there - do not proceed'
    treeloaded = 'false'
  '''
          
        
  #print 'treeFile---->: ' + str(treeFile)
        
  template = loader.get_template('exploratory_analysis/treeex.html')
   
   
  loggedIn = paths.noAuthReq 
    
  context = RequestContext(request, {
            'loggedIn' : str(loggedIn),
            'username' : username,
            'treeloaded' : treeloaded,
            'cachedfile' : cached_file_name,
            'package_list' : package_list,
            'dataset_list' : dataset_list,
            'variable_list' : variable_list,
            'season_list' : season_list,
            'set_list' : set_list,
            'bookmark_list' : bookmark_list,
            'figure_bookmark_list' : figure_bookmark_list,
            'treefile': treeFile,
            'current_bookmark': bookmark,
            'posttype':'save'
            #'treeFile' : treeFile,
  })
        

  return HttpResponse(template.render(context))


def noBookmarkHandler(request,user_id):

  print '\nrequest user authenticate: ' + str(request.user.is_authenticated()) + '\n'
    
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
  
  #get the predefined tree bookmarks of the user
  from exploratory_analysis.models import Tree_Bookmarks
  bookmark_list_obj = Tree_Bookmarks.objects.filter(tree_bookmark_username=username)
  
  bookmark_list = [] 
  for obj in bookmark_list_obj:
    bookmark_list.append(obj.tree_bookmark_name)
 
 

  #get the figure bookmarks of the user
  from exploratory_analysis.models import Figure_Bookmarks
  figure_bookmark_list_obj = Figure_Bookmarks.objects.filter(figure_bookmark_username=username)
 
  figure_bookmark_list = [] 
  for obj in figure_bookmark_list_obj:
    figure_bookmark_list.append(obj.figure_bookmark_name)
 
 
  #print 'bookmark list: ' + str(bookmark_list)
  #print 'figure bookmark list ' + str(figure_bookmark_list)
 
 
  #defaults = parameter_defaults.get_parameter_defaults()
  defaults = get_parameter_defaults()
  package_list = defaults['package_list']
  dataset_list = defaults['dataset_list']
  variable_list = defaults['variable_list']
  season_list = defaults['season_list']
  set_list = defaults['set_list']
    
 
    
  #first we check if the request is in the cache or if it is the initial call
  #if it is in the cache, no need to do any back end generation
  bookmark = str(request.GET.get('bookmark'))
    
  #print '\nbookmark: ' + str(bookmark)  
      

  #print '\nin noBookmarkHandler'


  #if something has been posted, then a tree could be built       
  if request.POST:
            
      posttype = str(request.POST['posttype'])
            
      tree_bookmark_datasetname = str(request.POST['dataset'])
            
      #print 'tree_bookmark_datasetname----->' + tree_bookmark_datasetname + '\n\n\n\n'
            
      #print 'in a post request with parameters'
            
            
      treename = str(request.POST['treename'])
            
      #if there is no tree name give the tree a default name based on the timestamp
      if treename == None or treename == '':
        import time
        millis = int(round(time.time() * 1000))
        treename = 'tree' + str(millis)
            
            
            
      packages = ''
      #defaults here
      if request.POST['package'] == None:
        packages = ['lmwg']
      else:
        packages = [ str(request.POST['package']) ]
            
            
            
      vars= ''
      variable_arr_str = str(request.POST['variable_arr_str'])
      if variable_arr_str == None:
        #print 'variable_arr_str is None'
        vars = ['TLAI', 'TG','NPP']
      else:
        #print 'variable_arr_str: ' + variable_arr_str
        variable_arr = variable_arr_str.split(';')
        vars = variable_arr
                
      times = ''
      season_arr_str = str(request.POST['season_arr_str'])
      if season_arr_str == None:
        #print 'season_arr_str is None'
        times = ['MAR','APR','MAY','JUNE','JULY']
      else:
        season_arr = season_arr_str.split(';')
        times = season_arr
        
      sets_arr = ''
      sets_arr_str = str(request.POST['sets_arr_str'])
      if sets_arr_str == None:
        print 'sets_arr_str is None'
      else:
        sets_arr = sets_arr_str.split(';')
        print 's: ' + sets_arr[0] 
            
        
      dataset = ''
      path = ''
      if str(request.POST['dataset']) == None:
        dataset = 'tropics_warming_th_q_co2'
        path = [default_tree_sample_data_dir + 'tropics_warming_th_q_co2']
      else:
        dataset = str(request.POST['dataset'])
        path = path = [default_tree_sample_data_dir + str(request.POST['dataset'])]
            
            
      #print '\n\n\t\t\tDATASET: ' + dataset 
      #print 'DATASET LIST: ' + dataset_list[0] + '\n\n\n'    
            
      #    username
                
      #static/exploratory_analysis/cache/tree/' username + '/json/' + dataset_name
      #build tree here 
      #if the post type is "submit" then grab "temp.json", otherwise it is a saved bookmark
            
      #old
      #if posttype == 'submit':
      #    treeFile = cache_dir + 'temp' + '.json'
      #else:
      #    treeFile = cache_dir + treename + '.json'
            
      if posttype == 'submit':
        treeFile = cache_dir + username + '/json/' + 'temp' + '.json'
      else:
        treeFile = cache_dir + username + '/json/' + dataset + '/' + treename + '.json'
            
      import os
      import os.path
      #print 'created tree bookmark file: ' + (cache_dir + username + '/json/' + dataset)
      #print 'treeFile exists? ' + str(os.path.isdir(cache_dir + username + '/json/' + dataset))
      if not os.path.isdir(cache_dir + username + '/json/' + dataset):
        #print 'create dir'
        os.makedirs(cache_dir + username + '/json/' + dataset)
            
      #### Start diagnostics generation here...
      #username = user_id
        
      o = Options()
       
            
      #print 'varsssss---->' + str(vars)
       
      #print 'str(path)--->' + str(path) 
       
      ##### SET THESE BASED ON USER INPUT FROM THE GUI
      o._opts['packages'] = packages
      o._opts['vars'] = vars
      o._opts['path'] = path
      o._opts['times'] = times
        
            
            
      ### NOTE: 'ANN' won't work for times this way, but that shouldn't be a problem
      datafiles = []
      filetables = []
      vars = o._opts['vars']
      #   print vars
    
      #print 'packages--->' + str(packages)
      #print 'vars--->' + str(vars)
      #print 'times--->' + str(times)
      #print 'dataset_list[0]--->' + dataset_list[0]
    
      for p in range(len(o._opts['path'])):
        #print '\ndirtree\n',dirtree_datafiles(o,pathid=p)
        datafiles.append(dirtree_datafiles(o,pathid=p))
        filetables.append(basic_filetable(datafiles[p],o))
            
      #print 'Creating diags tree view JSON file...'
        
      #print 'ftnames->' + dataset_list[0]
      #print 'filetables->' + str(filetables)
        
      #print '\n\n\n\nFILENAME!!!! ' + treeFile
        
      tv = TreeView()
      #dtree = tv.makeTree(o, filetables,None,user=username,ftnames=[dataset_list[0]])
      
      print 'DATA set ----> ' + dataset
      
      dtree = tv.makeTree(o, filetables,ftnames=[dataset],user=username)
      tv.dump(filename=treeFile)
            
            
            
      response_data = {}
      response_data['treename'] = treename
      response_data['username'] = username
      return HttpResponse(json.dumps(response_data), content_type="application/json")
            
  #end if request.POST  
  
  loggedIn = paths.noAuthReq   
            
  if(loggedIn == True):
    template = loader.get_template('exploratory_analysis/treeex.html')
  else:
    #print 'username: ' + username
        #print 'func: ' + str(func)
            
    #func = treeviewer_treeex.func()
    template = loader.get_template('exploratory_analysis/not_logged_in.html')
    
        
        
  treeloaded = 'false'
        
        
    
        
  #print 'figure bookmark list -> ' + str(figure_bookmark_list)
        
  #print '\n\t\t\tloggedIn: ' + str(loggedIn) 
        
  context = RequestContext(request, {
            'loggedIn' : str(loggedIn),
            'username' : username,
            'treeloaded' : treeloaded,
            'package_list' : package_list,
            'dataset_list' : dataset_list,
            'variable_list' : variable_list,
            'season_list' : season_list,
            'set_list' : set_list,
            'bookmark_list' : bookmark_list,
            'figure_bookmark_list' : figure_bookmark_list,
            'posttype':'save'
                                          
  })
        

  return HttpResponse(template.render(context))


def get_parameter_defaults():
    
    defaults = {}
    
    #options for creating a new tree
    package_list = ['lmwg']
        
    #get the dataset_list from ESGF
    dataset_list = ['tropics_warming_th_q_co2']    
    
    
    #get the variable list here using Brian's code 
    #variable_list = ['ACTUAL_IMMOB', 'AGNPP', 'ANN_FAREA_BURNED', 'AR', 'BCDEP', 'BGNPP', 'BIOGENCO', 'BSW', 'BTRAN', 'BUILDHEAT', 'COL_CTRUNC', 'COL_FIRE_CLOSS', 'COL_FIRE_NLOSS', 'COL_NTRUNC', 'CPOOL', 'CWDC', 'CWDC_HR', 'CWDC_LOSS', 'CWDN', 'DEADCROOTC', 'DEADCROOTN', 'DEADSTEMC', 'DEADSTEMN', 'DENIT', 'DISPVEGC', 'DISPVEGN', 'DSTDEP', 'DSTFLXT', 'DWT_CLOSS', 'DWT_CONV_CFLUX', 'DWT_CONV_NFLUX', 'DWT_NLOSS', 'DWT_PROD100C_GAIN', 'DWT_PROD100N_GAIN', 'DWT_PROD10C_GAIN', 'DWT_PROD10N_GAIN', 'DWT_SEEDC_TO_DEADSTEM', 'DWT_SEEDC_TO_LEAF', 'DWT_SEEDN_TO_DEADSTEM', 'DWT_SEEDN_TO_LEAF', 'DZSOI', 'E-T', 'EFLX_DYNBAL', 'EFLX_LH_TOT_R', 'EFLX_LH_TOT_U', 'ELAI', 'ER', 'ERRH2O', 'ERRSEB', 'ERRSOI', 'ERRSOL', 'ESAI', 'EVAPFRAC', 'FCEV', 'FCOV', 'FCTR', 'FGEV', 'FGR', 'FGR12', 'FGR_R', 'FGR_U', 'FIRA', 'FIRA_R', 'FIRA_U', 'FIRE', 'FIRESEASONL', 'FLDS', 'FLUXFM2A', 'FLUXFMLND', 'FPG', 'FPI', 'FPSN', 'FROOTC', 'FROOTC_ALLOC', 'FROOTC_LOSS', 'FROOTN', 'FSA', 'FSAT', 'FSA_R', 'FSA_U', 'FSDS', 'FSDSND', 'FSDSNDLN', 'FSDSNI', 'FSDSVD', 'FSDSVDLN', 'FSDSVI', 'FSH', 'FSH_G', 'FSH_NODYNLNDUSE', 'FSH_R', 'FSH_U', 'FSH_V', 'FSM', 'FSM_R', 'FSM_U', 'FSNO', 'FSR', 'FSRND', 'FSRNDLN', 'FSRNI', 'FSRVD', 'FSRVDLN', 'FSRVI', 'GC_HEAT1', 'GC_ICE1', 'GC_LIQ1', 'GPP', 'GR', 'GROSS_NMIN', 'H2OCAN', 'H2OSNO', 'H2OSNO_TOP', 'H2OSOI', 'HC', 'HCSOI', 'HEAT_FROM_AC', 'HKSAT', 'HR', 'HTOP', 'ISOPRENE', 'LAISHA', 'LAISUN', 'LAND_UPTAKE', 'LAND_USE_FLUX', 'LEAFC', 'LEAFC_ALLOC', 'LEAFC_LOSS', 'LEAFN', 'LHEAT', 'LITFALL', 'LITHR', 'LITR1C', 'LITR1C_TO_SOIL1C', 'LITR1N', 'LITR2C', 'LITR2C_TO_SOIL2C', 'LITR2N', 'LITR3C', 'LITR3C_TO_SOIL3C', 'LITR3N', 'LITTERC', 'LITTERC_HR', 'LITTERC_LOSS', 'LIVECROOTC', 'LIVECROOTN', 'LIVESTEMC', 'LIVESTEMN', 'MEAN_FIRE_PROB', 'MONOTERP', 'MR', 'NBP', 'NDEPLOY', 'NDEP_TO_SMINN', 'NEE', 'NEP', 'NET_NMIN', 'NFIX_TO_SMINN', 'NPP', 'OCDEP', 'ORVOC', 'OVOC', 'PBOT', 'PCO2', 'PFT_CTRUNC', 'PFT_FIRE_CLOSS', 'PFT_FIRE_NLOSS', 'PFT_NTRUNC', 'PLANT_NDEMAND', 'POTENTIAL_IMMOB', 'PREC', 'PROD100C', 'PROD100C_LOSS', 'PROD100N', 'PROD100N_LOSS', 'PROD10C', 'PROD10C_LOSS', 'PROD10N', 'PROD10N_LOSS', 'PRODUCT_CLOSS', 'PRODUCT_NLOSS', 'PSNSHA', 'PSNSHADE_TO_CPOOL', 'PSNSUN', 'PSNSUN_TO_CPOOL', 'Q2M', 'QBOT', 'QCHANR', 'QCHANR_ICE', 'QCHARGE', 'QCHOCNR', 'QCHOCNR_ICE', 'QDRAI', 'QDRIP', 'QFLX_ICE_DYNBAL', 'QFLX_LIQ_DYNBAL', 'QINFL', 'QINTR', 'QMELT', 'QOVER', 'QRGWL', 'QRUNOFF', 'QRUNOFF_NODYNLNDUSE', 'QRUNOFF_R', 'QRUNOFF_U', 'QSNWCPICE', 'QSNWCPICE_NODYNLNDUSE', 'QSOIL', 'QVEGE', 'QVEGT', 'RAIN', 'RAINATM', 'RAINFM2A', 'RETRANSN', 'RETRANSN_TO_NPOOL', 'RH2M', 'RH2M_R', 'RH2M_U', 'RR', 'SABG', 'SABV', 'SEEDC', 'SEEDN', 'SHEAT', 'SMINN', 'SMINN_LEACHED', 'SMINN_TO_NPOOL', 'SMINN_TO_PLANT', 'SNOBCMCL', 'SNOBCMSL', 'SNODSTMCL', 'SNODSTMSL', 'SNOOCMCL', 'SNOOCMSL', 'SNOW', 'SNOWATM', 'SNOWDP', 'SNOWFM2A', 'SNOWICE', 'SNOWLIQ', 'SOIL1C', 'SOIL1N', 'SOIL2C', 'SOIL2N', 'SOIL3C', 'SOIL3N', 'SOIL4C', 'SOIL4N', 'SOILC', 'SOILC_HR', 'SOILC_LOSS', 'SOILICE', 'SOILLIQ', 'SOILPSI', 'SOILWATER_10CM', 'SOMHR', 'SR', 'STORVEGC', 'STORVEGN', 'SUCSAT', 'SUPPLEMENT_TO_SMINN', 'SoilAlpha', 'SoilAlpha_U', 'TAUX', 'TAUY', 'TBOT', 'TBUILD', 'TG', 'TG_R', 'TG_U', 'THBOT', 'TLAI', 'TLAKE', 'TOTCOLC', 'TOTCOLN', 'TOTECOSYSC', 'TOTECOSYSN', 'TOTLITC', 'TOTLITN', 'TOTPFTC', 'TOTPFTN', 'TOTPRODC', 'TOTPRODN', 'TOTSOMC', 'TOTSOMN', 'TOTVEGC', 'TOTVEGN', 'TREFMNAV', 'TREFMNAV_R', 'TREFMNAV_U', 'TREFMXAV', 'TREFMXAV_R', 'TREFMXAV_U', 'TSA', 'TSAI', 'TSA_R', 'TSA_U', 'TSOI', 'TSOI_10CM', 'TV', 'U10', 'URBAN_AC', 'URBAN_HEAT', 'VOCFLXT', 'VOLR', 'WA', 'WASTEHEAT', 'WATSAT', 'WIND', 'WOODC', 'WOODC_ALLOC', 'WOODC_LOSS', 'WOOD_HARVESTC', 'WOOD_HARVESTN', 'WT', 'XSMRPOOL', 'XSMRPOOL_RECOVER', 'ZBOT', 'ZSOI', 'ZWT', 'area', 'areaatm', 'areaupsc', 'date_written', 'edgee', 'edgen', 'edges', 'edgew', 'indxupsc', 'landfrac', 'landmask', 'latixy', 'latixyatm', 'longxy', 'longxyatm', 'mcdate', 'mcsec', 'mdcur', 'mscur', 'nstep', 'pftmask', 'time_bounds', 'time_written', 'topo', 'topodnsc']
    variable_list = ['GPP','NEE','HR','ER','NPP','QVEGT','QVEGE','QSOIL','GROSS_NMIN','TLAI']
    
    #get the season list here using Brian's code
    season_list = ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC','DJF','MAM','JJA','SON','ANN']


    set_list = ['set1','set2','set3','set4','set5','set6','set7','set8','set9']
    
    defaults = {
        'package_list' : package_list,
        'dataset_list' : dataset_list,
        'variable_list' : variable_list,
        'season_list' : season_list,
        'set_list' : set_list
    }
    
    return defaults


'''
def diagsHelper(user_id,bookmark_name,treeFile):
    print 'in diags helper'
    
    
    #check the bookmark name
    
    
    #treeFile = cache_dir + bookmark_name + '.json'
    
    #cache_dir + username + '/json/' + dataset + '/' + treename + '.json
    
    import os
    
    print '\ntreeFile: ' + treeFile + '\n\texists? ' + str(os.path.exists(treeFile)) + '\n'
    
    treeFileExists = os.path.exists(treeFile)
    
    #if the file is not in the cache already, then we have to generate the file
    if not treeFileExists:
        #### Start diagnostics generation here...
        username = user_id
      
        print username
        
        o = Options()
        #   o.processCmdLine()
        #   o.verifyOptions()
       
       ##### SET THESE BASED ON USER INPUT FROM THE GUI
       
        #defaults here
        packages = ['lmwg']
        vars = ['TLAI', 'TG','NPP']
        path = [default_tree_sample_data_dir + 'tropics_warming_th_q_co2']
        times = ['MAR','APR','MAY','JUNE','JULY']
        
        
        o._opts['packages'] = packages
        o._opts['vars'] = vars
        o._opts['path'] = path
        o._opts['times'] = times
        
        
        ### NOTE: 'ANN' won't work for times this way, but that shouldn't be a problem
        datafiles = []
        filetables = []
        vars = o._opts['vars']
        #   print vars
    
        for p in range(len(o._opts['path'])):
            print '\ndirtree\n',dirtree_datafiles(o,pathid=p)
            datafiles.append(dirtree_datafiles(o,pathid=p))
            filetables.append(basic_filetable(datafiles[p],o))
        
        #index = 0
        ##for p in o._opts['path']:
        #  print '\ndirtree\n' , dirtree_datafiles(p)
        #  datafiles.append(dirtree_datafiles(p))
        #  filetables.append(basic_filetable(datafiles[index], o))
        #  index = index+1
        #
        print 'Creating diags tree view JSON file...'
        
        
        tv = TreeView()
        dtree = tv.makeTree(o, filetables,None,user=username,ftnames=['tropics_warming_th_q_co2'])
        tv.dump(filename=treeFile)
        
        
        
    #return the file and the location of the file
    return treeFile
'''


def findTreeFile(name, path):
  #print 'in findTreeFile for name: ' + name + ' and path: ' + path
  import os
  for root, dirs, files in os.walk(path):
    if name in files:
      return os.path.join(root, name)
      #return True
  
  return False
  
  
def findTreeDataset(f):
  f_arr = f.split('/')

  return f_arr[len(f_arr)-2]



def convertRelToAbsPath(name):
  p = re.compile('../../../')
  
  base_dir = '/Users/8xo/software/exploratory_analysis/DiagnosticsViewer/django-app/uvcdat_live/exploratory_analysis/' 
  
  check_file_name = p.sub( base_dir, name)
  
  #print '\t\t\tchck_file_name: ' + check_file_name
  
  return check_file_name
  
        
