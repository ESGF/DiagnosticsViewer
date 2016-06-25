
'''
Begin page generator for atm
'''

from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from django.template import RequestContext, loader
from django.conf import settings
#from django.contrib.auth import authenticate, login

from metrics.frontend import amwgmaster
from utils import generate_token_url

import traceback
import os

import ConfigParser
config = ConfigParser.ConfigParser()

if __name__ != '__main__':
   fp = open(settings.CFG_PATH)
   print 'Open returned: ', fp
   config.readfp(fp)


   root = config.get('paths', 'root')

   esgfAuth = config.get('options','esgfAuth')
   authReq = config.get('options', 'authReq')

   proxy_cert_dir = config.get('certificate', 'proxy_cert_dir')
   certNameSuffix = config.get('certificate', 'certNameSuffix')

   ea_root = os.path.join(root, config.get('paths', 'ea_dir'))

   img_cache_path = os.path.join(root, config.get('paths', 'img_cache_path'))
   staticfiles_dirs = os.path.join(root, config.get('paths', 'staticfiles_dirs'))

   javascript_namespace = config.get('namespaces', 'javascript_namespace')

   ea_name = str(config.get('options', 'hostname'))
   ea_port = str(config.get('options', 'port'))
   #print type(ea_name)
   #print type(ea_port)
   #print 'EA_host: %s:%s\n' % (ea_name, ea_port)
   fp.close()

else:
   ea_name = "STANDALONE_TEST"
   ea_port = "1234"
   root = "."
   esgfAuth = False
   authReq = False
   proxy_cert_dir = "."
   certNameSuffix = ""
   ea_root = "."
   img_cache_path = "."
   staticfiles_dirs = "."
   javascript_namespace = "foo"


ea_hostname = ':'.join([str(ea_name), str(ea_port)])
ea_hostname = str(ea_name)
#print 'EA_HOSTNAME: %s' % ea_hostname

def pageHeader(dataset,sets):
    '''
    HTML for the header of the AMWG plots
    '''
    html = ''
    html = '<p>'
    html += '<img src="/static/exploratory_analysis/img/classic/amwg/SET'+sets+'.gif" border=1 hspace=10 align=left alt="set '+sets+'">'
    html += '<font color=maroon size=+3><b>'
    html += dataset+'<br>and<br>OBS data'
    html += '</b></font>'
            
    html += '<p>'
    html += '<b>DIAG Set'+sets+' '+amwgmaster.diags_collection[sets]['desc']
    html += '<hr noshade size=2 size="100%">'
        
    html += '<b>'+amwgmaster.diags_collection[sets].get('preamble', '')

    return html
    
    

def pageGenerator(sets, varlist, times, package, dataset, options):
    '''
    HTML for the body of the AMWG plots
    '''
    
    print 'img_cache_path: ' + img_cache_path
    
    
    #print 'sets passed in: ' + sets
    # we get {classicatm}_setX passed in. Need to strip off up to the first underscore.
    if '_' in sets: # and 'tier1b' not in sets: # need to figure out why this code was there before
        ind = sets.find('_')
        setv = sets[ind+1:]
        print 'actual set:', setv
        sets = setv
        if 'set' in sets[0:3]: # now remove set from set[number]
            ind = sets.find('t')
            setv = sets[ind+1:]
            sets = setv
    #print 'key will be: ' + sets
        
       
    
    html = ''
    try:
        img_prefix = ''
        if __name__ != '__main__':
          img_prefix = os.path.join(img_cache_path, dataset, package, 'img', '')
        else:
          img_prefix ='path'
    
    
        #sets = '3'
        #sets = '4'
        
        html = pageHeader(dataset,sets)
        
        obssort = 1 
        
        # Determine number of columns
        # The default is just 'ANN', and if that is the only one or nothing is specified, we don't need a column for it.
        # ['NA'] is also something to deal with.
        seasons = amwgmaster.diags_collection[sets].get('seasons', ['ANN'])
        
	# see if there is a collections-level region. If not, set it to global. Still need checks per-variable though.
        regions = amwgmaster.diags_collection[sets].get('regions', ['Global'])
        
        # get a list of all obssets used in this collection
        varlist = list(set(amwgmaster.diags_collection[sets].keys()) - set(amwgmaster.collection_special_vars))
        obslist = []
        for v in varlist:
            obslist.extend(amwgmaster.diags_collection[sets][v]['obs'])
            # unique-ify
        obslist = list(set(obslist))

        # does this set need the --combined filename?
        # Eventually this might be per-variable...
        hasCombined = amwgmaster.diags_collection[sets].get('combined',False)

      
        specialCases = ['1', '2', '11', '12', '13', '14']
   
        html += '<TABLE>'

        
        if sets not in specialCases:
            if obssort == 1:
                for o in obslist:
                    html += '<TR>'
                    html += '<TH><BR>' # the variable
                    obsname = amwgmaster.diags_obslist[o]['desc']
                    html += '  <TH ALIGN=LEFT><font color="navy" size="+1">'+obsname+'</font>' # the obs/desc
                    
                    #print '\thtml: ' + '  <TH ALIGN=LEFT><font color="navy" size="+1">'+obsname+'</font>' # the obs/desc
                    if len(seasons) != 1:
                        for season in seasons: 
#                            print '\t    <TH>'+season
                            html += '    <TH>'+season # the plot links
                    else:
                        html += '<TH>'
                    
                    for v in varlist:
                    # Is this obsset used by this variable?
#                        print 'v: ' + v
                        if amwgmaster.diags_collection[sets][v]['obs'] != None:
#                            print '\tNot None'
                            if o in amwgmaster.diags_collection[sets][v]['obs']:
#                                print '\t\o: ' + str(o)
                                obsfname = amwgmaster.diags_obslist[o]['filekey']
                                html += '<TR>'
                                html += '    <TH ALIGN=LEFT>' + v
                                html += '    <TH ALIGN=LEFT>' + amwgmaster.diags_varlist[v]['desc']
                
				for season in seasons:
					if season == 'NA':
						season = 'ANN'

                                        if hasCombined == True:
                                        	postfix = 'combined.png'
                                        else:
                                        	postfix = 'model.png'

					var_regions = amwgmaster.diags_collection[sets][v].get('regions', [])
					if var_regions == []:
						var_regions = regions # the collection-level if we don't have a var-level.
					 
					for region in var_regions:
                                        	varopts = amwgmaster.diags_collection[sets][v].get('varopts', False)
                                        	pfixes = amwgmaster.diags_collection[sets][v].get('postfixes', False)
						regionstr = amwgmaster.all_regions[region].filekey

						if varopts == False and pfixes == False:
							fname_str = '/set%s_%s_%s_%s_%s-%s' % (sets, season, v, obsfname, regionstr, postfix)
							fname = 'http://' + ea_hostname + generate_token_url('/' + dataset + '/' + package + fname_str)
#set3_ANN_PRECT_LEGATES_Global-combined.png
                                                        '''
                                                        #print 'find()...' + str(fname_str.find("set3_ANN_PRECT_LEGATES"))
                                                        if fname_str.find("set3_ANN_PRECT_LEGATES") != -1: 
                                                          print 'what should i print here?\n'
                                                          print 'fname_str: ' + fname_str
                                                          print 'fname: ' + str(fname)
                                                        '''
#							print 'FNAME: %s - dataset (%s) package (%s) set (%s)\n' % ( fname, dataset, package, sets)
							click = 'onclick="' + javascript_namespace + 'displayImageClick(\''+fname+'\');" '
							over = 'onmouseover="' + javascript_namespace + 'displayImageHover(\''+fname+'\');" '
							out = 'onmouseout="' + javascript_namespace + 'nodisplayImage();" '
							html_class = 'plot_links'
							html += '<TH ALIGN=LEFT><A HREF="#" class="' + html_class + '" ' +click+over+out+'">plot</a> '               

						else:
							if pfixes == False:
								for varopt in varopts:
									fname_str = '/set%s_%s_%s_%s_%s_%s-%s' % (sets, season, v, varopt, obsfname, regionstr, postfix)
									fname = 'http://' + ea_hostname + generate_token_url('/' + dataset + '/' + package + fname_str)
									click = 'onclick="' + javascript_namespace + 'displayImageClick(\''+fname+'\');" '
									over = 'onmouseover="' + javascript_namespace + 'displayImageHover(\''+fname+'\');" '
									out = 'onmouseout="' + javascript_namespace + 'nodisplayImage();" '
									html_class = 'plot_links'
									html += '<TH ALIGN=LEFT><A HREF="#" class="' + html_class + '" ' +click+over+out+'">plot</a> '               
							else:
								for pfix in pfixes: # these are just used on some loose-coupled diags
									fname_str = '/set%s_%s_%s_%s_%s_%s-%s' % (sets, season, v, pfixes, obsfname, regionstr, postfix)
									fname = 'http://' + ea_hostname + generate_token_url('/' + dataset + '/' + package + fname_str)
									click = 'onclick="' + javascript_namespace + 'displayImageClick(\''+fname+'\');" '
									over = 'onmouseover="' + javascript_namespace + 'displayImageHover(\''+fname+'\');" '
									out = 'onmouseout="' + javascript_namespace + 'nodisplayImage();" '
									html_class = 'plot_links'
									html += '<TH ALIGN=LEFT><A HREF="#" class="' + html_class + '" ' +click+over+out+'">'+pfix+'</a> '

                                         
#            		print '\nadding a link\n'
                
            html += '</TABLE>'
                            
        # The special cases.
        if sets == '1': # The tables.
            regions = amwgmaster.diags_collection[sets]['regions']
        
            html += '<TR>'
            html += '<TH ALIGN=LEFT><font color="navy" size="+1">Domain</font>'
            for season in seasons:
                html += '<TH>'+season
            for r in regions:
                html +='<TR>'
                html+='<TH>'+r+'</TH>'
                for season in seasons:
                     fname = 'http://' + ea_hostname + generate_token_url('/' + dataset + '/' + package + '/set1_'+season+'_'+amwgmaster.all_regions[r].filekey+'-table.text')
                     print 'amwgmaster.all_regions[%s].filekey - %s' % (r, amwgmaster.all_regions[r].filekey)
        #             print 'looking for '+fname
                     click = 'onclick="' + javascript_namespace + 'displayTable(\''+fname+'\');" '
                     over = 'onmouseover="' + javascript_namespace + 'displayTableHover(\''+fname+'\');" '
                     out = 'onmouseout="' + javascript_namespace + 'nodisplayImage();" '
                     html += ' <TH ALIGN=LEFT><A HREF="#" '+click+over+out+'>table</a>'
            html += '</TABLE>'
        
        
        if sets == '11':
            # two subtables.
            # format for both is <var><obs><plot link>
            set1obs = { 'CERES2 March 2000-October 2005':'CERES2','CERES 2000-2003':'CERES', 'ERBE 1985-1989':'ERBE'}
            set2list = {}
            set2list['LHFLX'] = {'desc':'Latent Heat Flux', 'obslist':{'ECMWF 1979-1993':'ECMWF', 'WHOI 1958-2006':'WHOI'}}
            set2list['PRECT'] = {'desc':'Precipitation Rate', 'obslist':{'GPCP 1979-2003':'GPCP'}}
            set2list['SST'] = {'desc':'Sea Surface Temperature', 'obslist':{'HADISST 1982-2001':'HADISST'}}
            set2list['SWCF'] = {'desc':'Shortwave Cloud Forcing', 'obslist':{'ERBE 1985-1989':'ERBE'}}
            set2list['TAUX'] = {'desc':'Surface Zonal Stress', 'obslist':{'ERS 1992-2000':'ERS', 'LARGE-YEAGER 1984-2004':'LARYEA'}}
            set2list['TAUY'] = {'desc':'Surface Meridional Stress', 'obslist':{'ERS 1992-2000':'ERS', 'LARGE-YEAGER 1984-2004':'LARYEA'}}
        
            html += '<TR>'
            html += ' <TH ALIGN=LEFT>Warm Pool Scatter Plot<TH><TH>'
        
            for o in set1obs:
               html += '<TR>'
               html += '  <TH ALIGN=LEFT>SW/LW Cloud Forcing'
               html += '  <TH ALIGN=LEFT><font color="navy">'+o+'</font>'
               obsfname = set1obs[o]
               fname = 'http://' + ea_hostname + generate_token_url('/' + dataset + '/' + package +'/set11_SWCF_LWCF_'+obsfname+'.png')
               click = 'onclick="' + javascript_namespace + 'displayImageClick(\''+fname+'\');" '
               over = 'onmouseover="' + javascript_namespace + 'displayImageHover(\''+fname+'\');" '
               out = 'onmouseout="' + javascript_namespace + 'nodisplayImage();" '
               html += '<TH ALIGN=LEFT><A HREF="#" '+click+over+out+'">plot</a>'
        
            html += '</TABLE>'
            html += '<TABLE>'
        
            html += '<TR>'
            html += '<TH ALIGN=LEFT">Annual Cycle on the Equatorial Pacific<TH><TH>'
            for v in set2list.keys():
                for o in set2list[v]['obslist'].keys():
                    html += '<TR>'
                    html += '  <TH ALIGN=LEFT>'+set2list[v]['desc']
                    html += '  <TH ALIGN=LEFT>'+o
                    fname = 'http://' + ea_hostname + generate_token_url('/' + dataset + '/' + package +'/set11_'+v+'_'+set2list[v]['obslist'][o]+'.png')
                    click = 'onclick="' + javascript_namespace + 'displayImageClick(\''+fname+'\');" '
                    over = 'onmouseover="' + javascript_namespace + 'displayImageHover(\''+fname+'\');" '
                    out = 'onmouseout="' + javascript_namespace + 'nodisplayImage();" '
                    html += '<TH ALIGN=LEFT><A HREF="#" '+click+over+out+'">plot</a>'
        
              
        
      
        
        
        # These two are pretty similar at least.
        if sets == '12' or sets == '13':
        
            if sets == '12':
               cols = ['T', 'Q', 'H']
               vlist = { 'Thule Greenland':'Thule_Greenland', 'Resolute NWT Canada':'Resolute_Canada', 'Ship P Gulf of Alaska':'ShipP_GulfofAlaska', 'Midway Island (N Pacific)':'Midway_Island', 'Northern Great Plains USA':'Great_Plains_USA', 'San Francisco Calif USA':'SanFrancisco_CA', 'Western Europe':'Western_Europe', 'Miami Florida USA':'Miami_FL', 'Panama Central America':'Panama', 'Hawaii (Eq Pacific)':'Hawaii', 'Marshall Islands (Eq Pacific)':'Marshall_Islands', 'Yap Island (Eq Pacific)':'Yap_Island', 'Truk Island (Eq Pacific)':'Truk_Island', 'Diego Garcia (Eq Indian)':'Diego_Garcia', 'Ascension Island (Eq Atlantic)':'Ascension_Island', 'Easter Island (S Pacific)':'Easter_Island', 'McMurdo Antarctica':'McMurdo_Antarctica'}
               header = 'Station Name'
            else:
               cols = ['DJF', 'JJA', 'ANN']
               vlist = {'Global':'global', 'Tropics (15S-15N)':'tropics', 'NH SubTropics (15N-30N)':'nsubtrop', 'SH SubTropics (30S-15S)':'ssubtrop', 'NH Mid-Latitudes (30N-70N)':'nmidlats', 'SH Mid-Latitudes (70S-30S)':'smidlats', 'NH Polar (70N-90N)':'npole', 'SH Polar (90S-70S)':'spole', 'North Pacific Stratus':'npacstrat', 'South Pacific Stratus':'spacstrat', 'North Pacific':'npacific', 'North Atlantic':'natlantic', 'Warm Pool':'warmpool', 'Central Africa':'cafrica', 'USA':'usa'}
               header = 'Region'
        
            html += '<TR>'
            html += '<TH ALIGN=LEFT><font color=blue>'+header+'</font>'
        
            for col in cols:
               html += '<TH>' + col
            
            for var in vlist:
               html += '<TR>'
               html += '<TH ALIGN=LEFT>' + var
               # some day, we could check for all of the "derived" paths and use them if defined, otherwise derive them.
            
               for col in cols:
                  if sets == '13':
                     fname = 'http://' + ea_hostname + generate_token_url('/' + dataset + '/' + package  + '/set13_' + col + '_' + vlist[var] + '.png')
                  else:
                     fname = 'http://' + ea_hostname + generate_token_url('/' + dataset + '/' + package  + '/set12_' + vlist[var] + '_' + col + '.png')
    
                  click = 'onclick="' + javascript_namespace + 'displayImageClick(\''+fname+'\');" '
                  over = 'onmouseover="' + javascript_namespace + 'displayImageHover(\''+fname+'\');" '
                  out = 'onmouseout="' + javascript_namespace + 'nodisplayImage();" '
                  html += '<TH ALIGN=LEFT><A HREF="#" '+click+over+out+'">plot</a>'
    
                
            html += '</TABLE>'
    
    
        if sets == '14':
            html += '<TR>'
            html += ' <TH ALIGN=LEFT>Space and Time'
            fname = 'http://' + ea_hostname + generate_token_url('/' + dataset + '/' + package + '/set14_ANN_SPACE_TIME.png')
            click = 'onclick="' + javascript_namespace + 'displayImageClick(\''+fname+'\');" '
            over = 'onmouseover="' + javascript_namespace + 'displayImageHover(\''+fname+'\');" '
            out = 'onmouseout="' + javascript_namespace + 'nodisplayImage();" '
            html += ' <TH ALIGN=LEFT><A HREF="#" '+click+over+out+'">plot</a>'
    
            html += '<TR>'
            html += ' <TH ALIGN=LEFT>Space only'
            seasons = ['ANN', 'DJF', 'MAM', 'JJA', 'SON']
            for season in seasons:
               fname = 'http://' + ea_hostname + generate_token_url('/' + dataset + '/' + package + '/set14_'+season+'_SPACE.png')
               click = 'onclick="' + javascript_namespace + 'displayImageClick(\''+fname+'\');" '
               over = 'onmouseover="' + javascript_namespace + 'displayImageHover(\''+fname+'\');" '
               out = 'onmouseout="' + javascript_namespace + 'nodisplayImage();" '
               html += ' <TH ALIGN=LEFT><A HREF="#" '+click+over+out+'">'+season+'</a>'
    
            html += '</TABLE>'

            html += '<TABLE>'
            html += '<TR>'
            html += '<TH ALIGN=LEFT>Bias(%), Variance (ratio), Correlation Coefficient Tables'
            html += '<TR>'
            html += '<TH ALIGN=LEFT>Space and Time'
            varl = {'Correlation':'CC', 'Variance': 'VAR', 'Bias':'BIAS'}
            for v in varl.keys():
               fname = 'http://' + ea_hostname + generate_token_url('/' + dataset + '/' + package + '/set14.METRICS_'+varl[v]+'_SPACE_TIME.png')
               click = 'onclick="' + javascript_namespace + 'displayImageClick(\''+fname+'\');" '
               over = 'onmouseover="' + javascript_namespace + 'displayImageHover(\''+fname+'\');" '
               out = 'onmouseout="' + javascript_namespace + 'nodisplayImage();" '
               html += ' <TH ALIGN=LEFT><A HREF="#" '+click+over+out+'">'+v+'</a>'
            html += '<TR>'
            html += '<TH ALIGN=LEFT>Space only'
            for v in varl.keys():
               fname = 'http://' + ea_hostname + generate_token_url('/' + dataset + '/' + package + '/set14.METRICS_'+varl[v]+'_SPACE.png')
               click = 'onclick="' + javascript_namespace + 'displayImageClick(\''+fname+'\');" '
               over = 'onmouseover="' + javascript_namespace + 'displayImageHover(\''+fname+'\');" '
               out = 'onmouseout="' + javascript_namespace + 'nodisplayImage();" '
               html += ' <TH ALIGN=LEFT><A HREF="#" '+click+over+out+'">'+v+'</a>'
            html += '<TR>'
            html += '<TH ALIGN=LEFT>Time only'
            fname = 'http://' + ea_hostname + generate_token_url('/' + dataset + '/' + package +'/set14.METRICS_CC_TIME.png')
            click = 'onclick="' + javascript_namespace + 'displayImageClick(\''+fname+'\');" '
            over = 'onmouseover="' + javascript_namespace + 'displayImageHover(\''+fname+'\');" '
            out = 'onmouseout="' + javascript_namespace + 'nodisplayImage();" '
            html += ' <TH ALIGN=LEFT><A HREF="#" '+click+over+out+'">Correlation</a>'
            html += '</TABLE>'

      
      
        if sets == '2' :
          for v in varlist:
             obsname = amwgmaster.diags_collection[sets][v]['obs']
    
          html += '<TR>'
          html += '<TH ALIGN=LEFT><font color="navy" size="+1">Annual Implied Northward Transports</font><TH>'
          for v in varlist:
             obsname = amwgmaster.diags_collection[sets][v]['obs']
             fkey = amwgmaster.diags_varlist[v]['filekey']
             print 'file key:', fkey
             desc = amwgmaster.diags_varlist[v]['desc']
             if type(obsname) == list and len(obsname) != 1:
                print 'Set 2 only supports one obs set for a given "variable"'
                quit()
             if type(obsname) == list:
                obsname = obsname[0]
             obskey = amwgmaster.diags_obslist[obsname]['filekey']
    
             html += '<TR>'
             html += ' <TH ALIGN=LEFT>'+desc
             fname ='http://' + ea_hostname + generate_token_url('/' + dataset + '/' + package + '/set2_ANN_'+fkey+'_'+obskey+'_Global-combined.png')
    #         print 'set 2 fname: ', fname
             click = 'onclick="' + javascript_namespace + 'displayImageClick(\''+fname+'\');" '
             over = 'onmouseover="' + javascript_namespace + 'displayImageHover(\''+fname+'\');" '
             out = 'onmouseout="' + javascript_namespace + 'nodisplayImage();" '
             html += ' <TH ALIGN=LEFT><A HREF="#" '+click+over+out+'">plot</a>'
          html += '</TABLE>'

        
        return html
    
    except:
        tb = traceback.format_exc()
        #print 'tb: ' + tb
        return HttpResponse("error")
    
    
    

    return html



if __name__ == '__main__':
   for x in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', 'topten', 'tier1b_clouds']: # '41'
      page = pageGenerator(x, 'TLAI', 't1', 'd1', 'test', [])
      fname = 'page-%s.html' % x
      f = open(fname, 'w')
      f.write(page)
      f.close()


'''
End page generator for atm
'''
