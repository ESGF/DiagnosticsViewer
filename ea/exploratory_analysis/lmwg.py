'''
Begin page generator for ;nd
'''

from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from django.template import RequestContext, loader
from django.contrib.auth import authenticate, login

import traceback
import os

from metrics.frontend import amwgmaster
from utils import generate_token_url

#various variables that need to go into a config file
#esgfAuth - flag for turning on (True) or turning off (False) esgf authentication
esgfAuth = False

#the directory for the certs to be fetched
proxy_cert_dir = '/tmp'

#naAuthReq - authentication via the cookie on (True) or off (False)
authReq = True

#certNameSuffix - the suffix of the certificate file
certNameSuffix = 'x509acme'


ea_root = '/Users/8xo/software/exploratory_analysis/DiagnosticsViewer'
uvcdat_live_root = ea_root+ '/django-app-1.8/uvcdat_live/' 
img_cache_path = uvcdat_live_root + '/exploratory_analysis/static/exploratory_analysis/cache/'
staticfiles_dirs = uvcdat_live_root + "/exploratory_analysis/static/exploratory_analysis"

javascript_namespace = 'EA_CLASSIC_VIEWER.functions.'


def pageGenerator(set, varlist, times, package, dataset, options):

    html = ''
    
    return html


'''
def landPageGenerator(set, varlist, times, package, dataset, options):
    
    print 'in landPageGenerator'
    
    html = ''
    
    #regions = ['Global Land','Northern Hemisphere Land', 'Southern Hemisphere Land', 'Alaskan Arctic', 'Central U.S.', 'Mediterranean and Western Asia']  
    regions = ['Global','Alaska','Alaskan_Arctic','Amazonia','Antarctica','Arabian_Peninsula','Asia','Australia','Alaskan_Arctic', 'Central_US', 'Mediterranean'] 
    set3varlist = ['hydro', 'landf', 'moistEnergyFlx', 'radf', 'reg', 'snow', 'turbf']
    set6varlist = ['cnFlx', 'frFlx', 'hydro', 'landf', 'radf', 'reg', 'snowliqIce', 'soilice', 'soilliq', 'soilliiqIce', 'tsoi', 'turbf']
    set3Headers = ['reg', 'landf','randf','turbf','cnFlx','frFlx','moistEnergyFlx','snow','albedo','hydro']
       
    if set == '1': 

            url_prefix = staticfiles_dirs + "/img/classic/" + dataset + "/" + package + "/"
            url_prefixIMAGE = "/" + dataset + "/" + package + "/set1_"
            url = url_prefix + set + ".html"

            html=""        
            
            #Header
            html+="<p>\n" 
            html+="<b><font color=maroon size=+2>Set 1 Description: <b></font>Line plots of annual trends in energy balance, soil water/ice and temperature, runoff, snow water/ice, photosynthesis </b><br>\n"
            html+="<br clear=left>"
            html+="</p>\n"
            html+="<p>\n"
            html+="<A HREF=\"/static/exploratory_analysis/img/classic/lmwg/set1/variableList_1.html\" target=\"set1_Variables\">\n"
            html+="<font color=maroon size=+1 text-align: right><b>Lookup Table: Set 1 Variable Definition</b></font></a>\n"
            html+="</br>\n"
            html+="</p>\n"
           
            
            
            #Start table
            html+="<p>\n"
            html+="<hr noshade size=2 size=\"100%\">\n"
            html+="<TABLE> \n"
            html+="<TR>\n"
            html+="<TH><TH ALIGN=LEFT><font color=maroon>Trend</font>\n"
            html+="</TR>\n"
            
            
            #python for loop----------
            #Descriptions are (predefinedBrianSmithDictionary[key]) 
            
            
            for key in lmwgmaster.diags_collection.keys():
                if 1 in lmwgmaster.diags_collection[key]['sets'] and key in varlist:
                    html+="<TR>\n"
                    html+='<TH ALIGN=LEFT>'
                    html+=lmwgmaster.diags_collection[key]['desc']
                    html+='('
                    html+=key
                    html+=')'
                    html+='<TH ALIGN=LEFT>'
                    html+='<a href="#" onclick="' + javascript_namespace + 'displayImageClick('
                    #file.write(url_prefixIMAGE)#Here we write gif name
                    html+='\''
                    html+= 'http://' + ea_hostname + generate_token_url(url_prefixIMAGE + key + '.gif')
                    html+='\''
                    html+=');" onmouseover="' + javascript_namespace + 'displayImageHover(\''
                    #file.write(url_prefixIMAGE)#Here we write gif name again
                    html+='http://' + ea_hostname + generate_token_url(url_prefixIMAGE + key + '.gif')
                    html+='\''
                    html+=');" onmouseout="' + javascript_namespace + 'nodisplayImage();">plot</A>\n'
                    html+="</TR>\n"
            

            #end for loop and end table generation-------------------------
            
            html+="</TABLE> \n"
            html+="</p>\n"
    

    

    
    return html 

'''
