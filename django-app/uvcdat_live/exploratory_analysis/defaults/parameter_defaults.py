
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