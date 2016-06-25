
'''
def treedataBrian(request,user_id):
    
    username = user_id
  
    o = Options()
    #   o.processCmdLine()
    #   o.verifyOptions()
   
   ##### SET THESE BASED ON USER INPUT FROM THE GUI
    o._opts['packages'] = ['lmwg'] 
    o._opts['vars'] = ['TG']
    o._opts['path'] = [default_sample_data_dir + 'tropics_warming_th_q_co2']
    o._opts['times'] = ['JAN']
    ### NOTE: 'ANN' won't work for times this way, but that shouldn't be a problem
    datafiles = []
    filetables = []
    vars = o._opts['vars']
    #   print vars

    index = 0
    for p in o._opts['path']:
      datafiles.append(dirtree_datafiles(p))
      filetables.append(basic_filetable(datafiles[index], o))
      index = index+1

    print 'Creating diags tree view JSON file...'
    tv = TreeView()
    dtree = tv.makeTree(o, filetables)
    tv.dump(filename='flare11.json')
    
    


    file = '/Users/8xo/software/exploratory_analysis/DiagnosticsViewer/django-app/uvcdat_live/exploratory_analysis/static/exploratory_analysis/css/tree/flare4.json';

    from pprint import pprint

    data = ''
    with open(file) as data_file:    
        data = json.load(data_file)
        pprint(data)
    
    url = 'http://cds.ccs.ornl.gov/y9s/singlef/i1850cn_cruncep_CNDA_Cli_b_2000-2009-i1850cn_cruncep_ctl_2000-2009/setsIndex.html'
    
    children_arr = [ { "name": "Set 1" } ]
    
    #data = { 'name' : 'LND_DIAG', 'url' : url, 'children' : children_arr }
    data_string = json.dumps(data,sort_keys=True,indent=2)
    print 'JSON:',data_string
            
            
            
    
    return HttpResponse(data_string)
'''  
 










'''
http://
'''
'''
def visualizationsBrian(request):
    
   print 'in visualizations Brian'
   
   o = Options()
#   o.processCmdLine()
#   o.verifyOptions()

   ##### SET THESE BASED ON USER INPUT FROM THE GUI
   o._opts['vars'] = ['PBOT'] 
  # o._opts['path'] = ['/path/to/a/dataset'] 
   o._opts['path'] = [default_sample_data_dir + 'tropics_warming_th_q_co2'] 
   o._opts['times'] = ['DJF']
   ### NOTE: 'ANN' won't work for times this way, but that shouldn't be a problem
   #####

   #### This will generate {var}-{times}-climatology.json

   # At this point, we have our options specified. Need to generate some climatologies and such
   datafiles = []
   filetables = []
   vars = o._opts['vars']
#   print vars

   index = 0
   for p in o._opts['path']:
      datafiles.append(dirtree_datafiles(p))
      filetables.append(basic_filetable(datafiles[index], o))
      index = index+1

   for var in o._opts['vars']:
      if var in filetables[0]._varindex.keys():
         for seas in o._opts['times']:
            vid = str(var)+'_'+str(seas)
            season = cdutil.times.Seasons([seas])
            rvar = reduced_variable(variableid = var,
               filetable = filetables[0],
               reduction_function=(lambda x, vid=vid: reduce_time_seasonal(x, season, vid=vid)))

            print 'Reducing ', var, ' for climatology ', seas
            data = {}
            red = rvar.reduce(o)
            filename = var+"-"+seas+"-climatology.json"
            print 'Writing to ', filename
            g = open(filename, 'w')
            data['geo_average_min'] = red.min()
            data['geo_average_max'] = red.max()
            mv = red.missing_value
            data['missing_value'] = mv
            data['geo_average_data'] = red.data.tolist()
            g_avg = cdutil.averager(red, axis='xy')
            data['geo_average_global'] = g_avg.data.tolist()
            json.dump(data, g, separators=(',',':'))
            g.close()
            print 'Done writing ', filename

  
  
  
   print request.GET.get('variable')
  
   variable = ''
   if(request.GET.get('variable') == None):
        variable = 'AR'
   else:
        variable = request.GET.get('variable')
  
   #file = '/Users/csg/Desktop/uvcdat-web/DiagnosticsViewer/django-app/uvcdat_live/exploratory_analysis/static/exploratory_analysis/cache/' + variable + '.json' 
   file = '/Users/8xo/software/exploratory_analysis/DiagnosticsViewer/django-app/uvcdat_live/exploratory_analysis/static/exploratory_analysis/cache/' + variable + '.json' 
 
   with open(file , 'r') as myfile:
      data = myfile.read().replace('\n','')
      
   jsonData = json.dumps(data)

   #jsonData = json.dumps("{ 'variable' : '" + variable  +  "'} ")
   #print jsonData
  
  
  
  
   return HttpResponse(jsonData)

'''




'''
'username' : username,
'cachedfile' : cached_file_name,
'variable_list' : variable_list,
'season_list' : season_list,
'bookmark_list' : bookmark_list,
'figure_bookmark_list' : figure_bookmark_list,
'treefile': treeFile,
'current_bookmark': bookmark
#'treeFile' : treeFile,
'''
    
'''
package_list = ['lmwg']
    
#get the dataset_list from ESGF
dataset_list = ['tropics_warming_th_q_co2']    

#get the variable list here using Brian's code 
#variable_list = ['ACTUAL_IMMOB', 'AGNPP', 'ANN_FAREA_BURNED', 'AR', 'BCDEP', 'BGNPP', 'BIOGENCO', 'BSW', 'BTRAN', 'BUILDHEAT', 'COL_CTRUNC', 'COL_FIRE_CLOSS', 'COL_FIRE_NLOSS', 'COL_NTRUNC', 'CPOOL', 'CWDC', 'CWDC_HR', 'CWDC_LOSS', 'CWDN', 'DEADCROOTC', 'DEADCROOTN', 'DEADSTEMC', 'DEADSTEMN', 'DENIT', 'DISPVEGC', 'DISPVEGN', 'DSTDEP', 'DSTFLXT', 'DWT_CLOSS', 'DWT_CONV_CFLUX', 'DWT_CONV_NFLUX', 'DWT_NLOSS', 'DWT_PROD100C_GAIN', 'DWT_PROD100N_GAIN', 'DWT_PROD10C_GAIN', 'DWT_PROD10N_GAIN', 'DWT_SEEDC_TO_DEADSTEM', 'DWT_SEEDC_TO_LEAF', 'DWT_SEEDN_TO_DEADSTEM', 'DWT_SEEDN_TO_LEAF', 'DZSOI', 'E-T', 'EFLX_DYNBAL', 'EFLX_LH_TOT_R', 'EFLX_LH_TOT_U', 'ELAI', 'ER', 'ERRH2O', 'ERRSEB', 'ERRSOI', 'ERRSOL', 'ESAI', 'EVAPFRAC', 'FCEV', 'FCOV', 'FCTR', 'FGEV', 'FGR', 'FGR12', 'FGR_R', 'FGR_U', 'FIRA', 'FIRA_R', 'FIRA_U', 'FIRE', 'FIRESEASONL', 'FLDS', 'FLUXFM2A', 'FLUXFMLND', 'FPG', 'FPI', 'FPSN', 'FROOTC', 'FROOTC_ALLOC', 'FROOTC_LOSS', 'FROOTN', 'FSA', 'FSAT', 'FSA_R', 'FSA_U', 'FSDS', 'FSDSND', 'FSDSNDLN', 'FSDSNI', 'FSDSVD', 'FSDSVDLN', 'FSDSVI', 'FSH', 'FSH_G', 'FSH_NODYNLNDUSE', 'FSH_R', 'FSH_U', 'FSH_V', 'FSM', 'FSM_R', 'FSM_U', 'FSNO', 'FSR', 'FSRND', 'FSRNDLN', 'FSRNI', 'FSRVD', 'FSRVDLN', 'FSRVI', 'GC_HEAT1', 'GC_ICE1', 'GC_LIQ1', 'GPP', 'GR', 'GROSS_NMIN', 'H2OCAN', 'H2OSNO', 'H2OSNO_TOP', 'H2OSOI', 'HC', 'HCSOI', 'HEAT_FROM_AC', 'HKSAT', 'HR', 'HTOP', 'ISOPRENE', 'LAISHA', 'LAISUN', 'LAND_UPTAKE', 'LAND_USE_FLUX', 'LEAFC', 'LEAFC_ALLOC', 'LEAFC_LOSS', 'LEAFN', 'LHEAT', 'LITFALL', 'LITHR', 'LITR1C', 'LITR1C_TO_SOIL1C', 'LITR1N', 'LITR2C', 'LITR2C_TO_SOIL2C', 'LITR2N', 'LITR3C', 'LITR3C_TO_SOIL3C', 'LITR3N', 'LITTERC', 'LITTERC_HR', 'LITTERC_LOSS', 'LIVECROOTC', 'LIVECROOTN', 'LIVESTEMC', 'LIVESTEMN', 'MEAN_FIRE_PROB', 'MONOTERP', 'MR', 'NBP', 'NDEPLOY', 'NDEP_TO_SMINN', 'NEE', 'NEP', 'NET_NMIN', 'NFIX_TO_SMINN', 'NPP', 'OCDEP', 'ORVOC', 'OVOC', 'PBOT', 'PCO2', 'PFT_CTRUNC', 'PFT_FIRE_CLOSS', 'PFT_FIRE_NLOSS', 'PFT_NTRUNC', 'PLANT_NDEMAND', 'POTENTIAL_IMMOB', 'PREC', 'PROD100C', 'PROD100C_LOSS', 'PROD100N', 'PROD100N_LOSS', 'PROD10C', 'PROD10C_LOSS', 'PROD10N', 'PROD10N_LOSS', 'PRODUCT_CLOSS', 'PRODUCT_NLOSS', 'PSNSHA', 'PSNSHADE_TO_CPOOL', 'PSNSUN', 'PSNSUN_TO_CPOOL', 'Q2M', 'QBOT', 'QCHANR', 'QCHANR_ICE', 'QCHARGE', 'QCHOCNR', 'QCHOCNR_ICE', 'QDRAI', 'QDRIP', 'QFLX_ICE_DYNBAL', 'QFLX_LIQ_DYNBAL', 'QINFL', 'QINTR', 'QMELT', 'QOVER', 'QRGWL', 'QRUNOFF', 'QRUNOFF_NODYNLNDUSE', 'QRUNOFF_R', 'QRUNOFF_U', 'QSNWCPICE', 'QSNWCPICE_NODYNLNDUSE', 'QSOIL', 'QVEGE', 'QVEGT', 'RAIN', 'RAINATM', 'RAINFM2A', 'RETRANSN', 'RETRANSN_TO_NPOOL', 'RH2M', 'RH2M_R', 'RH2M_U', 'RR', 'SABG', 'SABV', 'SEEDC', 'SEEDN', 'SHEAT', 'SMINN', 'SMINN_LEACHED', 'SMINN_TO_NPOOL', 'SMINN_TO_PLANT', 'SNOBCMCL', 'SNOBCMSL', 'SNODSTMCL', 'SNODSTMSL', 'SNOOCMCL', 'SNOOCMSL', 'SNOW', 'SNOWATM', 'SNOWDP', 'SNOWFM2A', 'SNOWICE', 'SNOWLIQ', 'SOIL1C', 'SOIL1N', 'SOIL2C', 'SOIL2N', 'SOIL3C', 'SOIL3N', 'SOIL4C', 'SOIL4N', 'SOILC', 'SOILC_HR', 'SOILC_LOSS', 'SOILICE', 'SOILLIQ', 'SOILPSI', 'SOILWATER_10CM', 'SOMHR', 'SR', 'STORVEGC', 'STORVEGN', 'SUCSAT', 'SUPPLEMENT_TO_SMINN', 'SoilAlpha', 'SoilAlpha_U', 'TAUX', 'TAUY', 'TBOT', 'TBUILD', 'TG', 'TG_R', 'TG_U', 'THBOT', 'TLAI', 'TLAKE', 'TOTCOLC', 'TOTCOLN', 'TOTECOSYSC', 'TOTECOSYSN', 'TOTLITC', 'TOTLITN', 'TOTPFTC', 'TOTPFTN', 'TOTPRODC', 'TOTPRODN', 'TOTSOMC', 'TOTSOMN', 'TOTVEGC', 'TOTVEGN', 'TREFMNAV', 'TREFMNAV_R', 'TREFMNAV_U', 'TREFMXAV', 'TREFMXAV_R', 'TREFMXAV_U', 'TSA', 'TSAI', 'TSA_R', 'TSA_U', 'TSOI', 'TSOI_10CM', 'TV', 'U10', 'URBAN_AC', 'URBAN_HEAT', 'VOCFLXT', 'VOLR', 'WA', 'WASTEHEAT', 'WATSAT', 'WIND', 'WOODC', 'WOODC_ALLOC', 'WOODC_LOSS', 'WOOD_HARVESTC', 'WOOD_HARVESTN', 'WT', 'XSMRPOOL', 'XSMRPOOL_RECOVER', 'ZBOT', 'ZSOI', 'ZWT', 'area', 'areaatm', 'areaupsc', 'date_written', 'edgee', 'edgen', 'edges', 'edgew', 'indxupsc', 'landfrac', 'landmask', 'latixy', 'latixyatm', 'longxy', 'longxyatm', 'mcdate', 'mcsec', 'mdcur', 'mscur', 'nstep', 'pftmask', 'time_bounds', 'time_written', 'topo', 'topodnsc']
variable_list = ['GPP','NEE','HR','ER','NPP','QVEGT','QVEGE','QSOIL','GROSS_NMIN']


#get the season list here using Brian's code
season_list = ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC','DJF','MAM','JJA','SON','ANN']


set_list = ['set1','set2','set3','set4','set5','set6','set7','set8','set9']

#if this is a submission for a new tree
#request.GET.get('variable')
'''




'''
#options for creating a new tree
package_list = ['lmwg']
    
#get the dataset_list from ESGF
dataset_list = ['tropics_warming_th_q_co2']    


#get the variable list here using Brian's code 
#variable_list = ['ACTUAL_IMMOB', 'AGNPP', 'ANN_FAREA_BURNED', 'AR', 'BCDEP', 'BGNPP', 'BIOGENCO', 'BSW', 'BTRAN', 'BUILDHEAT', 'COL_CTRUNC', 'COL_FIRE_CLOSS', 'COL_FIRE_NLOSS', 'COL_NTRUNC', 'CPOOL', 'CWDC', 'CWDC_HR', 'CWDC_LOSS', 'CWDN', 'DEADCROOTC', 'DEADCROOTN', 'DEADSTEMC', 'DEADSTEMN', 'DENIT', 'DISPVEGC', 'DISPVEGN', 'DSTDEP', 'DSTFLXT', 'DWT_CLOSS', 'DWT_CONV_CFLUX', 'DWT_CONV_NFLUX', 'DWT_NLOSS', 'DWT_PROD100C_GAIN', 'DWT_PROD100N_GAIN', 'DWT_PROD10C_GAIN', 'DWT_PROD10N_GAIN', 'DWT_SEEDC_TO_DEADSTEM', 'DWT_SEEDC_TO_LEAF', 'DWT_SEEDN_TO_DEADSTEM', 'DWT_SEEDN_TO_LEAF', 'DZSOI', 'E-T', 'EFLX_DYNBAL', 'EFLX_LH_TOT_R', 'EFLX_LH_TOT_U', 'ELAI', 'ER', 'ERRH2O', 'ERRSEB', 'ERRSOI', 'ERRSOL', 'ESAI', 'EVAPFRAC', 'FCEV', 'FCOV', 'FCTR', 'FGEV', 'FGR', 'FGR12', 'FGR_R', 'FGR_U', 'FIRA', 'FIRA_R', 'FIRA_U', 'FIRE', 'FIRESEASONL', 'FLDS', 'FLUXFM2A', 'FLUXFMLND', 'FPG', 'FPI', 'FPSN', 'FROOTC', 'FROOTC_ALLOC', 'FROOTC_LOSS', 'FROOTN', 'FSA', 'FSAT', 'FSA_R', 'FSA_U', 'FSDS', 'FSDSND', 'FSDSNDLN', 'FSDSNI', 'FSDSVD', 'FSDSVDLN', 'FSDSVI', 'FSH', 'FSH_G', 'FSH_NODYNLNDUSE', 'FSH_R', 'FSH_U', 'FSH_V', 'FSM', 'FSM_R', 'FSM_U', 'FSNO', 'FSR', 'FSRND', 'FSRNDLN', 'FSRNI', 'FSRVD', 'FSRVDLN', 'FSRVI', 'GC_HEAT1', 'GC_ICE1', 'GC_LIQ1', 'GPP', 'GR', 'GROSS_NMIN', 'H2OCAN', 'H2OSNO', 'H2OSNO_TOP', 'H2OSOI', 'HC', 'HCSOI', 'HEAT_FROM_AC', 'HKSAT', 'HR', 'HTOP', 'ISOPRENE', 'LAISHA', 'LAISUN', 'LAND_UPTAKE', 'LAND_USE_FLUX', 'LEAFC', 'LEAFC_ALLOC', 'LEAFC_LOSS', 'LEAFN', 'LHEAT', 'LITFALL', 'LITHR', 'LITR1C', 'LITR1C_TO_SOIL1C', 'LITR1N', 'LITR2C', 'LITR2C_TO_SOIL2C', 'LITR2N', 'LITR3C', 'LITR3C_TO_SOIL3C', 'LITR3N', 'LITTERC', 'LITTERC_HR', 'LITTERC_LOSS', 'LIVECROOTC', 'LIVECROOTN', 'LIVESTEMC', 'LIVESTEMN', 'MEAN_FIRE_PROB', 'MONOTERP', 'MR', 'NBP', 'NDEPLOY', 'NDEP_TO_SMINN', 'NEE', 'NEP', 'NET_NMIN', 'NFIX_TO_SMINN', 'NPP', 'OCDEP', 'ORVOC', 'OVOC', 'PBOT', 'PCO2', 'PFT_CTRUNC', 'PFT_FIRE_CLOSS', 'PFT_FIRE_NLOSS', 'PFT_NTRUNC', 'PLANT_NDEMAND', 'POTENTIAL_IMMOB', 'PREC', 'PROD100C', 'PROD100C_LOSS', 'PROD100N', 'PROD100N_LOSS', 'PROD10C', 'PROD10C_LOSS', 'PROD10N', 'PROD10N_LOSS', 'PRODUCT_CLOSS', 'PRODUCT_NLOSS', 'PSNSHA', 'PSNSHADE_TO_CPOOL', 'PSNSUN', 'PSNSUN_TO_CPOOL', 'Q2M', 'QBOT', 'QCHANR', 'QCHANR_ICE', 'QCHARGE', 'QCHOCNR', 'QCHOCNR_ICE', 'QDRAI', 'QDRIP', 'QFLX_ICE_DYNBAL', 'QFLX_LIQ_DYNBAL', 'QINFL', 'QINTR', 'QMELT', 'QOVER', 'QRGWL', 'QRUNOFF', 'QRUNOFF_NODYNLNDUSE', 'QRUNOFF_R', 'QRUNOFF_U', 'QSNWCPICE', 'QSNWCPICE_NODYNLNDUSE', 'QSOIL', 'QVEGE', 'QVEGT', 'RAIN', 'RAINATM', 'RAINFM2A', 'RETRANSN', 'RETRANSN_TO_NPOOL', 'RH2M', 'RH2M_R', 'RH2M_U', 'RR', 'SABG', 'SABV', 'SEEDC', 'SEEDN', 'SHEAT', 'SMINN', 'SMINN_LEACHED', 'SMINN_TO_NPOOL', 'SMINN_TO_PLANT', 'SNOBCMCL', 'SNOBCMSL', 'SNODSTMCL', 'SNODSTMSL', 'SNOOCMCL', 'SNOOCMSL', 'SNOW', 'SNOWATM', 'SNOWDP', 'SNOWFM2A', 'SNOWICE', 'SNOWLIQ', 'SOIL1C', 'SOIL1N', 'SOIL2C', 'SOIL2N', 'SOIL3C', 'SOIL3N', 'SOIL4C', 'SOIL4N', 'SOILC', 'SOILC_HR', 'SOILC_LOSS', 'SOILICE', 'SOILLIQ', 'SOILPSI', 'SOILWATER_10CM', 'SOMHR', 'SR', 'STORVEGC', 'STORVEGN', 'SUCSAT', 'SUPPLEMENT_TO_SMINN', 'SoilAlpha', 'SoilAlpha_U', 'TAUX', 'TAUY', 'TBOT', 'TBUILD', 'TG', 'TG_R', 'TG_U', 'THBOT', 'TLAI', 'TLAKE', 'TOTCOLC', 'TOTCOLN', 'TOTECOSYSC', 'TOTECOSYSN', 'TOTLITC', 'TOTLITN', 'TOTPFTC', 'TOTPFTN', 'TOTPRODC', 'TOTPRODN', 'TOTSOMC', 'TOTSOMN', 'TOTVEGC', 'TOTVEGN', 'TREFMNAV', 'TREFMNAV_R', 'TREFMNAV_U', 'TREFMXAV', 'TREFMXAV_R', 'TREFMXAV_U', 'TSA', 'TSAI', 'TSA_R', 'TSA_U', 'TSOI', 'TSOI_10CM', 'TV', 'U10', 'URBAN_AC', 'URBAN_HEAT', 'VOCFLXT', 'VOLR', 'WA', 'WASTEHEAT', 'WATSAT', 'WIND', 'WOODC', 'WOODC_ALLOC', 'WOODC_LOSS', 'WOOD_HARVESTC', 'WOOD_HARVESTN', 'WT', 'XSMRPOOL', 'XSMRPOOL_RECOVER', 'ZBOT', 'ZSOI', 'ZWT', 'area', 'areaatm', 'areaupsc', 'date_written', 'edgee', 'edgen', 'edges', 'edgew', 'indxupsc', 'landfrac', 'landmask', 'latixy', 'latixyatm', 'longxy', 'longxyatm', 'mcdate', 'mcsec', 'mdcur', 'mscur', 'nstep', 'pftmask', 'time_bounds', 'time_written', 'topo', 'topodnsc']
variable_list = ['GPP','NEE','HR','ER','NPP','QVEGT','QVEGE','QSOIL','GROSS_NMIN']

#get the season list here using Brian's code
season_list = ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC','DJF','MAM','JJA','SON','ANN']


set_list = ['set1','set2','set3','set4','set5','set6','set7','set8','set9']
'''




'''
tree_bookmark_datasetname = None

#if information was relayed in the post, that means a tree is being created
if request.POST:
#tree_bookmark_name = request.POST['tree_bookmark_name']
tree_bookmark_datasetname = request.POST['tree_bookmark_datasetname']



#if this is the first time visiting the page (or no params given)
if tree_bookmark_datasetname == None:
print 'no dataset name given, display empty tree/only the options'




else:
print 'there is a dataset name given, display the new tree'
treeloaded = 'true'
'''   
        
        
        
#grabs the map
#
'''
Visualizations
#URL String:
  http://<host>/exploratory_analysis/datasetsList/<user_id>
  http://<host>/exploratory_analysis/visualizations

lists all the datasets given a user
output is:
{
  user : '',
  datasets : [],
  paths: [],
  year_range: [[]]
  
}

def visualizations(request):
    
    
    print 'in visualizations'
    print request.GET.get('variable')
  
  
    variable = ''
    if(request.GET.get('variable') == None):
        variable = 'AR'
    else:
        variable = request.GET.get('variable')
  
  
  
    #statically load the json file from the cache - each file is labelled by variable <variable_name>.json
    
    #file = '/Users/i7j/DiagnosticsViewer/django-app/uvcdat_live/exploratory_analysis/static/exploratory_analysis/cache/' + variable + '.json' 
  
  
    file = '/Users/8xo/software/exploratory_analysis/DiagnosticsViewer/django-app/uvcdat_live/exploratory_analysis/static/exploratory_analysis/cache/' + variable + '.json' 
    
    
    with open(file , 'r') as myfile:
       data = myfile.read().replace('\n','')
      
    jsonData = json.dumps(data)

    return HttpResponse(jsonData)

'''


'''  
  #grabs the tree data
  #http://<host>/treedata/<user_id>
def treedata(request,user_id):
  
  username = user_id

  file = '/Users/i7j/DiagnosticsViewer/django-app/uvcdat_live/exploratory_analysis/static/exploratory_analysis/css/tree/flare3.json';
  #file = '/Users/8xo/software/exploratory_analysis/DiagnosticsViewer/django-app/uvcdat_live/exploratory_analysis/static/exploratory_analysis/css/tree/flare2.json';
  

  from pprint import pprint

  data = ''
  with open(file) as data_file:    
      data = json.load(data_file)
      pprint(data)
  
  url = 'http://cds.ccs.ornl.gov/y9s/singlef/i1850cn_cruncep_CNDA_Cli_b_2000-2009-i1850cn_cruncep_ctl_2000-2009/setsIndex.html'
  
  children_arr = [ { "name": "Set 1" } ]
  
  #data = { 'name' : 'LND_DIAG', 'url' : url, 'children' : children_arr }
  data_string = json.dumps(data,sort_keys=True,indent=2)
  print 'JSON:',data_string
          
          
          
  
  return HttpResponse(data_string)
'''
  
  
''' from diagsHelper
    import os
    import shutil
    
    #srcfile = treeFile
    dstroot = cache_dir


    assert not os.path.isabs(treeFile)
    dstdir =  os.path.join(dstroot, os.path.dirname(treeFile))

    

    #file = '/Users/8xo/software/exploratory_analysis/DiagnosticsViewer/django-app/uvcdat_live/exploratory_analysis/static/exploratory_analysis/css/tree/flare4.json';
    file = cache_dir + treeFile

    from pprint import pprint
    
    data = ''
    with open(file) as data_file:    
        data = json.load(data_file)
        pprint(data)
    
    url = 'http://cds.ccs.ornl.gov/y9s/singlef/i1850cn_cruncep_CNDA_Cli_b_2000-2009-i1850cn_cruncep_ctl_2000-2009/setsIndex.html'
    
    children_arr = [ { "name": "Set 1" } ]
    
    #data = { 'name' : 'LND_DIAG', 'url' : url, 'children' : children_arr }
    data_string = json.dumps(data,sort_keys=True,indent=2)
    print 'JSON:',data_string
'''
  
  

