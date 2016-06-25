#if __name__ != '__main__':
from paths import paths
   
#from amwgmaster import *
from metrics.frontend.defines import *
from metrics.frontend.amwgmaster import *
import os


def pageGenerator(sets, varlist, times, package, dataset, options):

   if __name__ != '__main__':
      img_prefix = os.path.join(paths.img_cache_path, dataset, package, 'img', '')
   else:
      img_prefix ='path'

   obssort = 1 
   # Header stuff
   html = ''
   html = '<p>'
   html += '<img src="/static/exploratory_analysis/img/classic/amwg/SET'+sets+'.gif" border=1 hspace=10 align=left alt="set '+sets+'">'
   html += '<font color=maroon size=+3><b>'
   html += dataset+'<br>and<br>OBS data'
   html += '</b></font>'
        
   html += '<p>'
   html += '<b>DIAG Set'+sets+' '+diags_collection[sets]['desc']
   html += '<hr noshade size=2 size="100%">'
    
   html += '<b>'+diags_collection[sets].get('preamble', '')

   html += '<TABLE>'

   print 'DEFAULTING TO ALL VARS FOR NOW'
   print 'DEFAULTING TO EXISTING FILENAME CONVENTIONS'
   print 'DEFAULTING TO NO ABSOLUTE PATHS'

   # Determine number of columns
   # The default is just 'ANN', and if that is the only one or nothing is specified, we don't need a column for it.
   # ['NA'] is also something to deal with.
   seasons = diags_collection[sets].get('seasons', ['ANN'])
   # Were some specific seasons passed in? If so, limit our list.
   print 'DEFAULTING TO ALL SEASONS FOR NOW'
   #if seasons != ['NA']:
   #   seasons = list(set(times) & set(def_seasons))

   regions = diags_collection[sets].get('regions', ['Global'])
   # get a list of all obssets used in this collection
   varlist = list(set(diags_collection[sets].keys()) - set(collection_special_vars))
   obslist = []
   for v in varlist:
      obslist.extend(diags_collection[sets][v]['obs'])
   # unique-ify
   obslist = list(set(obslist))

   # does this set need the --combined filename?
   # Eventually this might be per-variable...
   hasCombined = diags_collection[sets].get('combined',False)

   specialCases = ['1', '2', '11', '12', '13', '14']
   
   if sets not in specialCases:
      if obssort == 1:
         for o in obslist:
            html += '<TR>'
            html += '<TH><BR>' # the variable
            obsname = diags_obslist[o]['desc']
            html += '  <TH ALIGN=LEFT><font color="navy" size="+1">'+obsname+'</font>' # the obs/desc
            if len(seasons) != 1:
               for season in seasons: 
                  html += '    <TH>'+season # the plot links
            else:
               html += '<TH>'

            for v in varlist:
               # Is this obsset used by this variable?
               if o in diags_collection[sets][v]['obs']:
                  obsfname = diags_obslist[o]['filekey']
                  html += '<TR>'
                  html += '    <TH ALIGN=LEFT>' + v
                  html += '    <TH ALIGN=LEFT>' + diags_varlist[v]['desc']

		  if regions == ['Global']:
		     regionstr = '_Global'
   
                  for season in seasons:
                     if season == 'NA':
                        seasonstr = ''
                     else:
                        seasonstr = '_'+season
                     if hasCombined == True:
                        postfix = '-combined.png'
                     else:
                        postfix = '-model.png'
                     varopts = diags_collection[sets][v].get('varopts', False)
                     if varopts == False:
                        fname = 'http://' + paths.ea_hostname + paths.generate_token_url('/' + dataset + '/' + package + '/set'+sets+regionstr+seasonstr+'_'+v+'_'+obsfname+postfix)
                     else:
                        for varopt in varopts:
                           fname = 'http://' + paths.ea_hostname + paths.generate_token_url('/' + dataset + '/' + package + '/set'+sets+regionstr+seasonstr+'_'+v+'_'+varopt+'_'+obsfname+postfix)
                           
#                     print 'Looking for: ', fname
#                     if 'TTRP' in v:
#                        fname = 'http://' + paths.ea_hostname + paths.generate_token_url('/' + dataset + '/' + package +'/set'+sets+'_'+regionstr+'_'+season+'_'+v.replace('_TROP','')+'_'+obsfname+'-combined.png')
#                     elif 'TTRP' in v:
#                        fname = 'http://' + paths.ea_hostname + paths.generate_token_url('/' + dataset + '/' + package +'/set'+sets+'_'+season+'_'+v+'_'+obsfname+'_TROP-combined.png')
#                     else:
#                        fname = 'http://' + paths.ea_hostname + paths.generate_token_url('/' + dataset + '/' + package +'/set'+sets+'_'+season+'_'+v+'_'+obsfname+'-combined.png')
                     click = 'onclick="displayImageClick(\''+fname+'\');" '
                     over = 'onmouseover="displayImageHover(\''+fname+'\');" '
                     out = 'onmouseout="nodisplayImage();" '
                     html += '<TH ALIGN=LEFT><A HREF="#" '+click+over+out+'">plot</a>'

         html += '</TABLE>'
         return html
      else:
         print 'NOT IMPLEMENTED SORTING BY VAR'
         return None

   # The special cases.
   if sets == '1':
      regions = diags_collection[sets]['regions']

      html += '<TR>'
      html += '<TH ALIGN=LEFT><font color="navy" size="+1">Domain</font>'
      for season in seasons:
         html += '<TH>'+season
      for r in regions:
         html +='<TR>'
         html+='<TH>'+r+'</TH>'
         for season in seasons:
             #whenever these are paths.generated with diags use this?
             fname = 'http://' + paths.ea_hostname + paths.generate_token_url('/' + dataset + '/' + package + '/set1_'+season+'_'+all_regions[r].filekey+'-table.text')
#             print 'looking for '+fname
             click = 'onclick="displayTable(\''+fname+'\');" '
             over = 'onmouseover="displayTableHover(\''+fname+'\');" '
             out = 'onmouseout="nodisplayImage();" '
             html += ' <TH ALIGN=LEFT><A HREF="#" '+click+over+out+'>table</a>'
      html += '</TABLE>'
      return html

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
         fname = 'http://' + paths.ea_hostname + paths.generate_token_url('/' + dataset + '/' + package +'/set11_SWCF_LWCF_'+obsfname+'.png')
         click = 'onclick="displayImageClick(\''+fname+'\');" '
         over = 'onmouseover="displayImageHover(\''+fname+'\');" '
         out = 'onmouseout="nodisplayImage();" '
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
            fname = 'http://' + paths.ea_hostname + paths.generate_token_url('/' + dataset + '/' + package +'/set11_'+v+'_'+set2list[v]['obslist'][o]+'.png')
            click = 'onclick="displayImageClick(\''+fname+'\');" '
            over = 'onmouseover="displayImageHover(\''+fname+'\');" '
            out = 'onmouseout="nodisplayImage();" '
            html += '<TH ALIGN=LEFT><A HREF="#" '+click+over+out+'">plot</a>'

      return html


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
               fname = 'http://' + paths.ea_hostname + paths.generate_token_url('/' + dataset + '/' + package  + 'set13_' + col + '_' + vlist[var] + '.png')
            else:
               fname = 'http://' + paths.ea_hostname + paths.generate_token_url('/' + dataset + '/' + package  + 'set12_' + vlist[var] + '_' + col + '.png')

            click = 'onclick="displayImageClick(\''+fname+'\');" '
            over = 'onmouseover="displayImageHover(\''+fname+'\');" '
            out = 'onmouseout="nodisplayImage();" '
            html += '<TH ALIGN=LEFT><A HREF="#" '+click+over+out+'">plot</a>'

            
      html += '</TABLE>'
    
      return html


   if sets == '14':
      html += '<TR>'
      html += ' <TH ALIGN=LEFT>Space and Time'
      fname = 'http://' + paths.ea_hostname + paths.generate_token_url('/' + dataset + '/' + package + '/set14_ANN_SPACE_TIME.png')
      click = 'onclick="displayImageClick(\''+fname+'\');" '
      over = 'onmouseover="displayImageHover(\''+fname+'\');" '
      out = 'onmouseout="nodisplayImage();" '
      html += ' <TH ALIGN=LEFT><A HREF="#" '+click+over+out+'">plot</a>'

      html += '<TR>'
      html += ' <TH ALIGN=LEFT>Space only'
      seasons = ['ANN', 'DJF', 'MAM', 'JJA', 'SON']
      for season in seasons:
         fname = 'http://' + paths.ea_hostname + paths.generate_token_url('/' + dataset + '/' + package + '/set14_'+season+'_SPACE.png')
         click = 'onclick="displayImageClick(\''+fname+'\');" '
         over = 'onmouseover="displayImageHover(\''+fname+'\');" '
         out = 'onmouseout="nodisplayImage();" '
         html += ' <TH ALIGN=LEFT><A HREF="#" '+click+over+out+'">'+season+'</a>'

      html += '</TABLE>'

      html += '<TABLE>'
      html += '<TR>'
      html += '<TH ALIGN=LEFT>Bias(%), Variance (ratio), Correlation Coefficient Tables'
      html += '<TR>'
      html += '<TH ALIGN=LEFT>Space and Time'
      varl = {'Correlation':'CC', 'Variance': 'VAR', 'Bias':'BIAS'}
      for v in varl.keys():
         fname = 'http://' + paths.ea_hostname + paths.generate_token_url('/' + dataset + '/' + package + '/set14.METRICS_'+varl[v]+'_SPACE_TIME.png')
         click = 'onclick="displayImageClick(\''+fname+'\');" '
         over = 'onmouseover="displayImageHover(\''+fname+'\');" '
         out = 'onmouseout="nodisplayImage();" '
         html += ' <TH ALIGN=LEFT><A HREF="#" '+click+over+out+'">'+v+'</a>'
      html += '<TR>'
      html += '<TH ALIGN=LEFT>Space only'
      for v in varl.keys():
         fname = 'http://' + paths.ea_hostname + paths.generate_token_url('/' + dataset + '/' + package + '/set14.METRICS_'+varl[v]+'_SPACE.png')
         click = 'onclick="displayImageClick(\''+fname+'\');" '
         over = 'onmouseover="displayImageHover(\''+fname+'\');" '
         out = 'onmouseout="nodisplayImage();" '
         html += ' <TH ALIGN=LEFT><A HREF="#" '+click+over+out+'">'+v+'</a>'
      html += '<TR>'
      html += '<TH ALIGN=LEFT>Time only'
      fname = 'http://' + paths.ea_hostname + paths.generate_token_url('/' + dataset + '/' + package +'/set14.METRICS_CC_TIME.png')
      click = 'onclick="displayImageClick(\''+fname+'\');" '
      over = 'onmouseover="displayImageHover(\''+fname+'\');" '
      out = 'onmouseout="nodisplayImage();" '
      html += ' <TH ALIGN=LEFT><A HREF="#" '+click+over+out+'">Correlation</a>'
      html += '</TABLE>'

      return html
      
   if sets == '2' :
      for v in varlist:
         obsname = diags_collection[sets][v]['obs']

      html += '<TR>'
      html += '<TH ALIGN=LEFT><font color="navy" size="+1">Annual Implied Northward Transports</font><TH>'
      for v in varlist:
         obsname = diags_collection[sets][v]['obs']
         fkey = diags_varlist[v]['filekey']
	 print 'file key:', fkey
         desc = diags_varlist[v]['desc']
         if type(obsname) == list and len(obsname) != 1:
            print 'Set 2 only supports one obs set for a given "variable"'
            quit()
         if type(obsname) == list:
            obsname = obsname[0]
         obskey = diags_obslist[obsname]['filekey']

         html += '<TR>'
         html += ' <TH ALIGN=LEFT>'+desc
         fname ='http://' + paths.ea_hostname + paths.generate_token_url('/' + dataset + '/' + package + '/set2_ANN_'+fkey+'_'+obskey+'_Global-combined.png')
#         print 'set 2 fname: ', fname
         click = 'onclick="displayImageClick(\''+fname+'\');" '
         over = 'onmouseover="displayImageHover(\''+fname+'\');" '
         out = 'onmouseout="nodisplayImage();" '
         html += ' <TH ALIGN=LEFT><A HREF="#" '+click+over+out+'">plot</a>'
      html += '</TABLE>'
      return html

if __name__ == '__main__':
   from dummyfuncs import paths
   sets = ['1', '2', '3', '4', '4a', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', 'topten', 'so']
   times = ['DJF', 'ANN', 'JJA']

   for s in sets:
      html = pageGenerator(s, None, times, 'AMWG', 'datasetname', None)
      fname = 'set'+s+'.html'
      f = open(fname, "w")
      f.write(html)
      f.close()
#      print html
   
   
