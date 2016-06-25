from paths import paths
from lmwgmaster import *
import os

def pageGenerator(set, varlist, times, package, dataset, options):
    
        
       #To be added region = json_data['region'] #should be a list
        html=""
        #regions = ['Global Land','Northern Hemisphere Land', 'Southern Hemisphere Land', 'Alaskan Arctic', 'Central U.S.', 'Mediterranean and Western Asia']  
        regions = ['Global','Alaska','Alaskan_Arctic','Amazonia','Antarctica','Arabian_Peninsula','Asia','Australia','Alaskan_Arctic', 'Central_US', 'Mediterranean'] 
        set3varlist = ['hydro', 'landf', 'moistEnergyFlx', 'radf', 'reg', 'snow', 'turbf']
        set6varlist = ['cnFlx', 'frFlx', 'hydro', 'landf', 'radf', 'reg', 'snowliqIce', 'soilice', 'soilliq', 'soilliiqIce', 'tsoi', 'turbf']
        set3Headers = ['reg', 'landf','randf','turbf','cnFlx','frFlx','moistEnergyFlx','snow','albedo','hydro']
        
        
        if set == '1': 

            url_prefix = paths.staticfiles_dirs + "/img/classic/" + dataset + "/" + package + "/"
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
            
            
            for key in vardict:
                if 1 in vardict[key]['sets'] and key in varlist:
                    html+="<TR>\n"
                    html+='<TH ALIGN=LEFT>'
                    html+=vardict[key]['desc']
                    html+='('
                    html+=key
                    html+=')'
                    html+='<TH ALIGN=LEFT>'
                    html+='<a href="#" onclick="displayImageClick('
                    #file.write(url_prefixIMAGE)#Here we write gif name
                    html+='\''
                    html+= 'http://' + paths.ea_hostname + paths.generate_token_url(url_prefixIMAGE + key + '.gif')
                    html+='\''
                    html+=');" onmouseover="displayImageHover(\''
                    #file.write(url_prefixIMAGE)#Here we write gif name again
                    html+='http://' + paths.ea_hostname + paths.generate_token_url(url_prefixIMAGE + key + '.gif')
                    html+='\''
                    html+=');" onmouseout="nodisplayImage();">plot</A>\n'
                    html+="</TR>\n"
            

            #end for loop and end table generation-------------------------
            
            html+="</TABLE> \n"
            html+="</p>\n"
    

        elif set == '2':
            #########################################
            #change this to the specified directory structure

            url_prefix = paths.staticfiles_dirs + "/img/classic/" + package + "/" + set + "/"
            #url_prefixIMAGE = "\'/static/exploratory_analysis/img/classic/" + package + "/" + dataset + "/set2_"
            url_prefixIMAGE = "/" + dataset + "/" + package + "/set2_"

            
            #assemble the url to be returned
            url = url_prefix + set + ".html"
            #END JOHN's code
        
            #Construct table with description (variable) and link to plot
            #Input from json object from user selection
            #user_selected_varlist = {'TSA', 'PREC'}
            
            #Start writing file (SPECIFY LOCATION TO WRITE FILE TO HERE)     Example: land/tropics_warming_th_q/img/
            html=""
                    
            #Header
            html+="<p>\n"
            html+="<b><font color=maroon size=+2>Set 2 Description: <b></font>Horizontal contour plots of DJF, MAM, JJA, SON, and ANN means </b><br>\n"
            html+="<br clear=left>"
            html+="</p>\n"
            html+="<p>\n"

            html+="<A HREF=\"/static/exploratory_analysis/img/classic/lmwg/set2/variableList_2.html\" target=\"set2_Variables\">\n"
            html+="<font color=maroon size=+1 text-align: right><b>Lookup Table: Set 2 Variable Definition</b></font></a>\n"

            html+="</br>\n"
            html+="</p>\n"
                   
                        
            #Start table
            html+="<p>\n"
            html+="<hr noshade size=2 size=\"100%\">\n</hr>"
            html+="<TABLE> \n"
            html+="<TR>\n"
            html+="<td ALIGN=LEFT><font color=maroon>Description (variable)</font>\n</td>"
            for time in times:  
               html+="<td ALIGN=LEFT><font color=maroon>"+time+"</font>\n</td>"
            html+="</TR>\n"
          
            
            #python for loop----------
            #Descriptions are (predefinedBrianSmithDictionary[key]) 
            
            
            
            for key in vardict:
                if 2 in vardict[key]['sets'] and key in varlist:
                    html+="<TR>\n"
                    html+='<Td ALIGN=LEFT>'
                    html+=vardict[key]['desc']
                    html+='('
                    html+=key
                    html+=')</td>'
                    
                    
                    for time in times:                
                        html+='<td ALIGN=LEFT>'
                        html+='<a href="#" onclick="displayImageClick('
                        html+='\'http://' + paths.ea_hostname + paths.generate_token_url(url_prefixIMAGE + time +'_' + key + '.gif')
                        html+='\');" onmouseover="displayImageHover('
                        html+='\'http://' + paths.ea_hostname + paths.generate_token_url(url_prefixIMAGE + time +'_' + key + '.gif')
                        #html+='\''
                        html+='\');" onmouseout="nodisplayImage();">plot</A>\n'
                        html+='</td>'
                    html+="</TR>\n"
                    
                    
            #end for loop and end table generation-------------------------
            
       
            html+="</TABLE> \n"
            html+="</p>\n"
            
            
        elif set == '3':
             #########################################
            #change this to the specified directory structure
            url_prefix = paths.staticfiles_dirs + "/img/classic/" + package + "/" + set + "/"
            url_prefixIMAGE = "/" + dataset + "/" + package +  "/set3_"
            
            #assemble the url to be returned
            url = url_prefix + set + ".html"
            #END JOHN's code
        
            #Construct table with description (variable) and link to plot
            #Input from json object from user selection
            #user_selected_varlist = {'TSA', 'PREC'}
            
            #Start writing file (SPECIFY LOCATION TO WRITE FILE TO HERE)     Example: land/tropics_warming_th_q/img/
            html=""
            
            #Header
            html+="<p>\n"
            html+="<b><font color=maroon size=+2>Set 3 Description: <b></font>Line plots of monthly climatology: regional air temperature, precipitation, runoff, snow depth, radiative fluxes, and turbulent fluxes</b><br>\n"
            html+="<br clear=left>"
            html+="</p>\n"
            html+="<p>\n"
            html+="<A HREF=\"/static/exploratory_analysis/img/classic/lmwg/set3/variableList_3.html\" target=\"set3_Variables\">\n"
            html+="<font color=maroon size=+1 text-align: right><b>Lookup Table: Set 3 Variable Definition</b></font></a>\n"
            html+="</br>\n"
            html+="</p>\n"
                   
                        
            #Start table
            html+="<p>\n"
            html+="<hr noshade size=2 size=\"100%\">\n</hr>"
            html+="<TABLE> \n"
            html+="<TR>\n"
            html+="<td ALIGN=LEFT><B>All Model Data Regions</font>\n</td>"
            html+='<td>'
            html+='<a href="#" onclick="displayImageClick(\'' + 'http://' + paths.ea_hostname + paths.generate_token_url(url_prefixIMAGE + 'reg_all.gif') + '\''
            html+=');" onmouseover="displayImageHover(\'' + 'http://' + paths.ea_hostname + paths.generate_token_url(url_prefixIMAGE + 'reg_all.gif') + '\''
            html+=');" onmouseout="nodisplayImage();">Map</A>\n'
            html+='</td>'
            html+="</TR>\n"
            html+="<TR>\n"
            html+="<td>Region(s)"
            html+="</td>"
            html+="<td ALIGN=LEFT>Map</font>\n</td>"
            for var in set3varlist:  
               html+="<td ALIGN=LEFT>"+var+"</font>\n</td>"
            html+="</tr>\n"
          
            
            #python for loop----------
            #Descriptions are (predefinedBrianSmithDictionary[key]) 
            
            def containedInDictionary( set ):
                "This prints a passed string into this function"
                for key in vardict:
                    if set in vardict[key]['sets']:  
                        return True
                    else:
                        return False
                    
            
            for region in regions:
                if containedInDictionary( 3 ):  
                    html+="<TR>\n"           
                    html+='<Td ALIGN=LEFT>'
                    html+=region
                    html+='</td>\n'
                    html+='\n'
                    html+='<td>'
                    html+='<a href="#" onclick="displayImageClick(\'' + 'http://' + paths.ea_hostname + paths.generate_token_url(url_prefixIMAGE + 'reg_' + region + '.gif') + '\''
                    html+=');" onmouseover="displayImageHover(\'' + 'http://' + paths.ea_hostname + paths.generate_token_url(url_prefixIMAGE + 'reg_' + region + '.gif') + '\''
                    html+=');" onmouseout="nodisplayImage();">Map</A>'
                    html+='</td>\n'
                    for var in set3varlist:              
                        html+='<td ALIGN=center>'
                        html+='<a href="#" onclick="displayImageClick(\''
                        html+='http://' + paths.ea_hostname + paths.generate_token_url(url_prefixIMAGE + var+'_'+region+'.gif') +'\''
                        html+=');" onmouseover="displayImageHover(\''
                        html+='http://' + paths.ea_hostname + paths.generate_token_url(url_prefixIMAGE + var+'_'+region+'.gif') +'\''
                        html+=');" onmouseout="nodisplayImage();">Plot</A>'
                        html+='</td>\n'
                    html+="</TR>\n"
                    
                    
            #end for loop and end table generation-------------------------
            
       
            html+="</TABLE> \n"
            html+="</p>\n"

            
            
        elif set == '5':
            #########################################
            #change this to the specified directory structure
            url_prefix = paths.staticfiles_dirs + "/img/classic/" + package + "/" + set + "/"
            url_prefixIMAGE = "/" + dataset + "/" + package +  "/set5_"
            
            #assemble the url to be returned
            url = url_prefix + set + ".html"
            #END JOHN's code
        
            #Construct table with description (variable) and link to plot
            #Input from json object from user selection
            #user_selected_varlist = {'TSA', 'PREC'}
            
            #Start writing file (SPECIFY LOCATION TO WRITE FILE TO HERE)     Example: land/tropics_warming_th_q/img/
            html=""
                    
                    #Header
            html+="<p>\n"
            html+="<b><font color=maroon size=+2>Set 5 Description: <b></font>Tables of annual means </b><br>\n"
            html+="<br clear=left>"
            html+="</p>\n"
            html+="<p>\n"
            html+="<A HREF=\"/static/exploratory_analysis/img/classic/lmwg/set5/variableList_5.html\" target=\"set5_Variables\">\n"
            html+="<font color=maroon size=+1 text-align: right><b>Lookup Table: Set 5 Variable Definition</b></font></a>\n"
            html+="</br>\n"
            html+="</p>\n"
                   
                        
            #Start table
            html+="<p>\n"
            html+="<hr noshade size=2 size=\"100%\">\n</hr>"
            html+="<TABLE> \n"
            html+="<TR>\n"
            html+="<td ALIGN=LEFT><font color=maroon>TABLE</font>\n</td>"
            html+="</TR>\n"
          
            html+="<tr>"
            html+='<TH ALIGN=LEFT>Regional Hydrologic Cycle'
            html+='<TH ALIGN=LEFT><font color=black><A HREF= "#" onclick="displayTable(\''
            html+='http://' + paths.ea_hostname + paths.generate_token_url(url_prefixIMAGE + 'hydReg.txt') +'\''
            html+=')\";>Table</a></font>'
            html+='</tr>'
                        
            html+="<tr>"
            html+='<TH ALIGN=LEFT>Global Biogeophysics'
            html+='<TH ALIGN=LEFT><font color=black><A HREF= "#" onclick="displayTable(\''
            html+=u'http://' + paths.ea_hostname + paths.generate_token_url(url_prefixIMAGE + 'clm.txt')
            html+='\')\";>Table</a></font>'
            html+='</tr>'
            
            html+='<tr>'
            html+='<TH ALIGN=LEFT>Global Carbon/Nitrogen'     
            html+='<TH ALIGN=LEFT><font color=black><A HREF= "#" onclick="displayTable(\''
            html+='http://' + paths.ea_hostname + paths.generate_token_url(url_prefixIMAGE + 'cn.txt')
            html+='\')\";>Table</a></font>'
            html+='</tr>'
                 
                 
            #end for loop and end table generation-------------------------
            html+="</TABLE> \n"
            html+="</p>\n"
            
            
            
        elif set == '6':
             #########################################
            #change this to the specified directory structure
            url_prefix = paths.staticfiles_dirs + "/img/classic/" + package + "/" + set + "/"
            url_prefixIMAGE = "/" + dataset + "/" + package +  "/set6_"
            
            #assemble the url to be returned
            url = url_prefix + set + ".html"
            #END JOHN's code
        
            #Construct table with description (variable) and link to plot
            #Input from json object from user selection
            #user_selected_varlist = {'TSA', 'PREC'}
            
            def containedInDictionary( set ):
                "This prints a passed string into this function"
                for key in vardict:
                    if set in vardict[key]['sets']:  
                        return True
                    else:
                        return False
            
            #Start writing file (SPECIFY LOCATION TO WRITE FILE TO HERE)     Example: land/tropics_warming_th_q/img/
            html=""
            
            #Header
            html+="<p>\n"
            html+="<b><font color=maroon size=+2>Set 6 Description: <b></font>Line plots of annual trends in regional soil water/ice and temperature, runoff, snow water/ice, photosynthesis</b><br>\n"
            html+="<br clear=left>"
            html+="</p>\n"
            html+="<p>\n"
            html+="<A HREF=\"/static/exploratory_analysis/img/classic/lmwg/set6/variableList_6.html\" target=\"set6_Variables\">\n"
            html+="<font color=maroon size=+1 text-align: right><b>Lookup Table: Set 6 Variable Definition</b></font></a>\n"
            html+="</br>\n"
            html+="</p>\n"
                   
                        
            #Start table
            html+="<p>\n"
            html+="<hr noshade size=2 size=\"100%\">\n</hr>"
            html+="<TABLE> \n"
            html+="<TR>\n"
            html+="<td ALIGN=LEFT><B>All Model Data Regions</font>\n</td>"
            html+='<td>'
            html+='<a href="#" onclick="displayImageClick(\'' + 'http://' + paths.ea_hostname + paths.generate_token_url(url_prefixIMAGE + 'reg_all.gif') + '\''
            html+=');" onmouseover="displayImageHover(\'' + 'http://' + paths.ea_hostname + paths.generate_token_url(url_prefixIMAGE + 'reg_all.gif') + '\''
            html+=');" onmouseout="nodisplayImage();">Map</A>\n'
            html+='</td>'
            html+="</TR>\n"
            html+="<TR>\n"
            html+="<td>Region(s)"
            html+="</td>"
            html+="<td ALIGN=LEFT>Map</font>\n</td>"
            for var in set6varlist:  
               html+="<td ALIGN=LEFT>"+var+"</font>\n</td>"
            html+="</tr>\n"
          
            
            #python for loop----------
            #Descriptions are (predefinedBrianSmithDictionary[key]) 
            
            
                    
            
            for region in regions:
                if containedInDictionary( 6 ):  
                    html+="<TR>\n"            
                    html+='<Td ALIGN=LEFT>'
                    html+=region
                    html+='</td>\n'
                    html+='\n'
                    html+='<td>'
                    html+='<a href="#" onclick="displayImageClick(\'http://' + paths.ea_hostname + paths.generate_token_url(url_prefixIMAGE + 'reg_'+region+'.gif') + '\''
                    html+=');" onmouseover="displayImageHover(\'http://' + paths.ea_hostname + paths.generate_token_url(url_prefixIMAGE + 'reg_'+region+'.gif') + '\''
                    html+=');" onmouseout="nodisplayImage();">Map</A>'
                    html+='</td>\n'
                    for var in set6varlist:              
                        html+='<td ALIGN=center>'
                        html+='<a href="#" onclick="displayImageClick(\''
                        html+='http://' + paths.ea_hostname + paths.generate_token_url(url_prefixIMAGE + var+'_'+region+'.gif') +'\''
                        html+=');" onmouseover="displayImageHover(\''
                        html+='http://' + paths.ea_hostname + paths.generate_token_url(url_prefixIMAGE + var+'_'+region+'.gif') +'\''
                        html+=');" onmouseout="nodisplayImage();">Plot</A>'
                        html+='</td>\n'
                    html+="</TR>\n"
                    
                    
            #end for loop and end table generation-------------------------
            
       
            html+="</TABLE> \n"
            html+="</p>\n"
            
        elif set == '7':
            #########################################
            #change this to the specified directory structure
            #url_prefix = "/home/user/Desktop/AptanaWorkspace/climate/DiagnosticsViewer/django-app/uvcdat_live/exploratory_analysis/static/exploratory_analysis/img/classic/" + package + "/" + set + "/"
            url_prefixIMAGE = "/" + dataset + "/" + package +  "/set7_"
            url_prefix = paths.staticfiles_dirs + "/img/classic/" + package + "/" + set + "/"
            
            #assemble the url to be returned
            url = url_prefix + set + ".html"
            #END JOHN's code
        
            #Construct table with description (variable) and link to plot
            #Input from json object from user selection
            #user_selected_varlist = {'TSA', 'PREC'}
            
            #Start writing file (SPECIFY LOCATION TO WRITE FILE TO HERE)     Example: land/tropics_warming_th_q/img/
            html=""
            
            html+="<p>\n"
            html+="<b><font color=maroon size=+2>Set 7 Description: <b></font>Line plots, tables, and maps of RTM river flow and discharge to oceans </b><br>\n"
            html+="<br clear=left>\n"
            html+="<p>\n"
            html+="<hr noshade size=2 size=\"100%\">\n"
            html+="<TABLE>\n"
            html+="<TR>\n"
            html+="<TH ALIGN=LEFT><font color=red>TABLE</font>\n"
            html+="<TR>\n"
            html+="<TH ALIGN=LEFT>RTM flow at station for world's 50 largest rivers\\n"
            html+="<TH ALIGN=LEFT><a href=\"#\" onclick=\"displayTable(\'http://"+ paths.ea_hostname +paths.generate_token_url(url_prefixIMAGE+"table_RIVER_STN_VOL.txt") + "\');\">Table</A> \n"
            html+="<TR>\n"
            html+="<TH ALIGN=LEFT><font color=red>SCATTER PLOTS</font>\n"
            html+="<TR>\n"
            html+="<TH ALIGN=LEFT>RTM flow at station versus obs for world's 10 largest rivers (QCHANR) \n"
            html+="<TH ALIGN=LEFT><a href=\"#\" onclick=\"displayImageClick(\'http://"+ paths.ea_hostname +paths.generate_token_url(url_prefixIMAGE+"scatter_50riv.gif") + "\');\" onmouseover=\"displayImageHover(\'http://"+ paths.ea_hostname +paths.generate_token_url(url_prefixIMAGE+"scatter_50riv.gif")+ "');\" onmouseout=\"nodisplayImage();\">plot</A> \n"
            html+="<TR>\n"
            html+="<TH ALIGN=LEFT><font color=red>LINE PLOTS</font>\n"
            html+="<TR>\n"
            html+="<TH ALIGN=LEFT>Mean annual cycle of river flow at station for world's 10 largest rivers (QCHANR) \n"
            html+="<TH ALIGN=LEFT><a href=\"#\" onclick=\"displayImageClick(\'http://"+ paths.ea_hostname +paths.generate_token_url(url_prefixIMAGE+"mon_stndisch_10riv.gif") + "\');\" onmouseover=\"displayImageHover(\'http://"+ paths.ea_hostname +paths.generate_token_url(url_prefixIMAGE+"mon_stndisch_10riv.gif")+ "');\" onmouseout=\"nodisplayImage();\">plot</A> \n"            
            #html+="<TH ALIGN=LEFT><a href=\"#\" onclick=\"displayImageClick("+url_prefixIMAGE+"mon_stndisch_10riv.gif');\" onmouseover=\"displayImageHover("+url_prefixIMAGE+"mon_stndisch_10riv.gif');\" onmouseout=\"nodisplayImage();\">plot</A> \n"
            html+="<TR>\n"
            html+="<TH ALIGN=LEFT>Annual discharge into the Global Ocean (QCHOCNR) \n"
            html+="<TH ALIGN=LEFT><a href=\"#\" onclick=\"displayImageClick(\'http://"+ paths.ea_hostname +paths.generate_token_url(url_prefixIMAGE+"ann_disch_globalocean.gif") + "\');\" onmouseover=\"displayImageHover(\'http://"+ paths.ea_hostname +paths.generate_token_url(url_prefixIMAGE+"ann_disch_globalocean.gif")+ "');\" onmouseout=\"nodisplayImage();\">plot</A> \n"
            #html+="<TH ALIGN=LEFT><a href=\"#\" onclick=\"displayImageClick("+url_prefixIMAGE+"ann_disch_globalocean.gif');\" onmouseover=\"displayImageHover("+url_prefixIMAGE+"ann_disch_globalocean.gif');\" onmouseout=\"nodisplayImage();\">plot</A> \n"
            html+="<TR>\n"
            html+="<TH ALIGN=LEFT>Annual discharge into the Atlantic Ocean (QCHOCNR) \n"
            html+="<TH ALIGN=LEFT><a href=\"#\" onclick=\"displayImageClick(\'http://"+ paths.ea_hostname +paths.generate_token_url(url_prefixIMAGE+"ann_disch_atlantic.gif") + "\');\" onmouseover=\"displayImageHover(\'http://"+ paths.ea_hostname +paths.generate_token_url(url_prefixIMAGE+"ann_disch_atlantic.gif")+ "');\" onmouseout=\"nodisplayImage();\">plot</A> \n"            
            #html+="<TH ALIGN=LEFT><a href=\"#\" onclick=\"displayImageClick("+url_prefixIMAGE+"ann_disch_atlantic.gif');\" onmouseover=\"displayImageHover("+url_prefixIMAGE+"ann_disch_atlantic.gif');\" onmouseout=\"nodisplayImage();\">plot</A> \n"
            html+="<TR>\n"
            html+="<TH ALIGN=LEFT>Annual discharge into the Indian Ocean (QCHOCNR) \n"
            html+="<TH ALIGN=LEFT><a href=\"#\" onclick=\"displayImageClick(\'http://"+ paths.ea_hostname +paths.generate_token_url(url_prefixIMAGE+"ann_disch_indian.gif") + "\');\" onmouseover=\"displayImageHover(\'http://"+ paths.ea_hostname +paths.generate_token_url(url_prefixIMAGE+"ann_disch_indian.gif")+ "');\" onmouseout=\"nodisplayImage();\">plot</A> \n"            
            #html+="<TH ALIGN=LEFT><a href=\"#\" onclick=\"displayImageClick("+url_prefixIMAGE+"ann_disch_indian.gif');\" onmouseover=\"displayImageHover("+url_prefixIMAGE+"ann_disch_indian.gif');\" onmouseout=\"nodisplayImage();\">plot</A> \n"
            html+="<TR>\n"
            html+="<TH ALIGN=LEFT>Annual discharge into the Pacific Ocean (QCHOCNR) \n"
            html+="<TH ALIGN=LEFT><a href=\"#\" onclick=\"displayImageClick(\'http://"+ paths.ea_hostname +paths.generate_token_url(url_prefixIMAGE+"ann_disch_pacific.gif") + "\');\" onmouseover=\"displayImageHover(\'http://"+ paths.ea_hostname +paths.generate_token_url(url_prefixIMAGE+"ann_disch_pacific.gif")+ "');\" onmouseout=\"nodisplayImage();\">plot</A> \n"            
            #html+="<TH ALIGN=LEFT><a href=\"#\" onclick=\"displayImageClick("+url_prefixIMAGE+"ann_disch_pacific.gif');\" onmouseover=\"displayImageHover("+url_prefixIMAGE+"ann_disch_pacific.gif');\" onmouseout=\"nodisplayImage();\">plot</A> \n"
            html+="<TR>\n"
            html+="<TH ALIGN=LEFT>Mean annual cycle of discharge into the oceans (QCHOCNR) \n"
            html+="<TH ALIGN=LEFT><a href=\"#\" onclick=\"displayImageClick(\'http://"+ paths.ea_hostname +paths.generate_token_url(url_prefixIMAGE+"mon_disch.gif") + "\');\" onmouseover=\"displayImageHover(\'http://"+ paths.ea_hostname +paths.generate_token_url(url_prefixIMAGE+"mon_disch.gif")+ "');\" onmouseout=\"nodisplayImage();\">plot</A> \n"            
            #html+="<TH ALIGN=LEFT><a href=\"#\" onclick=\"displayImageClick("+url_prefixIMAGE+"mon_disch.gif');\" onmouseover=\"displayImageHover("+url_prefixIMAGE+"mon_disch.gif');\" onmouseout=\"nodisplayImage();\">plot</A> \n"
            html+="<TR>\n"
            html+="<TH ALIGN=LEFT><font color=red>MAPS</font>\n"
            html+="<TR>\n"
            html+="<TH ALIGN=LEFT>Station locations (50 largest rivers)\n"
            html+="<TH ALIGN=LEFT><a href=\"#\" onclick=\"displayImageClick(\'http://"+ paths.ea_hostname +paths.generate_token_url(url_prefixIMAGE+"stations.gif") + "\');\" onmouseover=\"displayImageHover(\'http://"+ paths.ea_hostname +paths.generate_token_url(url_prefixIMAGE+"stations.gif")+ "');\" onmouseout=\"nodisplayImage();\">Map</A> \n"            
            #html+="<TH ALIGN=LEFT><a href=\"#\" onclick=\"displayImageClick("+url_prefixIMAGE+"stations.gif');\" onmouseover=\"displayImageHover("+url_prefixIMAGE+"stations.gif');\" onmouseout=\"nodisplayImage();\">Map</A> \n"
            html+="<TR>\n"
            html+="<TH ALIGN=LEFT>Ocean Basins\n"
            html+="<TH ALIGN=LEFT><a href=\"#\" onclick=\"displayImageClick(\'http://"+ paths.ea_hostname +paths.generate_token_url(url_prefixIMAGE+"ocean_basin_index.gif") + "\');\" onmouseover=\"displayImageHover(\'http://"+ paths.ea_hostname +paths.generate_token_url(url_prefixIMAGE+"ocean_basin_index.gif")+ "');\" onmouseout=\"nodisplayImage();\">Map</A> \n"            
            #html+="<TH ALIGN=LEFT><a href=\"#\" onclick=\"displayImageClick("+url_prefixIMAGE+"ocean_basin_index.gif');\" onmouseover=\"displayImageHover("+url_prefixIMAGE+"ocean_basin_index.gif');\" onmouseout=\"nodisplayImage();\">Map</A> \n"
            html+="<TR>\n"
            html+="<TH ALIGN=LEFT>River Flow (QCHANR) \n"
            html+="<TH ALIGN=LEFT><a href=\"#\" onclick=\"displayImageClick(\'http://"+ paths.ea_hostname +paths.generate_token_url(url_prefixIMAGE+"ANN_QCHANR_Ac.gif") + "\');\" onmouseover=\"displayImageHover(\'http://"+ paths.ea_hostname +paths.generate_token_url(url_prefixIMAGE+"ANN_QCHANR_Ac.gif")+ "');\" onmouseout=\"nodisplayImage();\">Model1</A> \n"
            
            #html+="<TH ALIGN=LEFT><a href=\"#\" onclick=\"displayImageClick("+url_prefixIMAGE+"ANN_QCHANR_Ac.gif');\" onmouseover=\"displayImageHover("+url_prefixIMAGE+"ANN_QCHANR_Ac.gif');\" onmouseout=\"nodisplayImage();\">Model1</A> \n"
            html+="<TR>\n"
            html+="<TH ALIGN=LEFT><font color=red>VARIABLES</font>\n"
            html+="<TR>\n"
            html+="<TH ALIGN=LEFT>QCHANR \n"
            html+="<TH ALIGN=LEFT>NativeUnits [m^3/s] \n"
            html+="<TR>\n"
            html+="<TH ALIGN=LEFT>QCHOCNR \n"
            html+="<TH ALIGN=LEFT>NativeUnits [m^3/s] \n"
            html+="<TR>\n"
            html+="</table>\n"
            
            html+="</p>\n"
            
        elif set == '9':
            #########################################
            #change this to the specified directory structure
            #url_prefix = "/home/user/Desktop/AptanaWorkspace/climate/DiagnosticsViewer/django-app/uvcdat_live/exploratory_analysis/static/exploratory_analysis/img/classic/" + package + "/" + set + "/"
            url_prefixIMAGE = "/" + dataset + "/" + package +  "/set9_"
            url_prefix = paths.staticfiles_dirs + "/img/classic/" + package + "/" + set + "/"
            
            #assemble the url to be returned
            url = url_prefix + set + ".html"
            #END JOHN's code
        
            #Construct table with description (variable) and link to plot
            #Input from json object from user selection
            #user_selected_varlist = {'TSA', 'PREC'}
            
            #Start writing file (SPECIFY LOCATION TO WRITE FILE TO HERE)     Example: land/tropics_warming_th_q/img/
            html=""
                    
            html+="<p>\n"
            html+="<b><font color=maroon size=+2>Set 9 Description: <b></font>Contour plots and statistics for precipitation and temperature.  Statistics include DJF, JJA, and ANN biases, and RMSE, correlation and standard deviation of the annual cycle relative to observations</b><br>\n"
            html+="<br clear=left>\n"
            html+="<p>\n"
            html+="<hr noshade size=2 size=\"100%\"> \n"
            html+="<TABLE> \n"
            html+="<TR>\n"
            html+="<TH ALIGN=LEFT><font color=navy size=+1> 1. RMSE </font>\n"
            html+="<TH ALIGN=center><a href=\"#\" onclick=\"displayImageClick(\'http://"+paths.ea_hostname + paths.generate_token_url(url_prefixIMAGE+"rmse_TSA.gif")+ "\');\" onmouseover=\"displayImageHover(\'http://"+paths.ea_hostname + paths.generate_token_url(url_prefixIMAGE+"rmse_TSA.gif")+ "\');\" onmouseout=\"nodisplayImage();\">TSA</A>\n"
            html+="<TH ALIGN=center><a href=\"#\" onclick=\"displayImageClick(\'http://"+paths.ea_hostname + paths.generate_token_url(url_prefixIMAGE+"rmse_PREC.gif")+ "\');\" onmouseover=\"displayImageHover(\'http://"+paths.ea_hostname + paths.generate_token_url(url_prefixIMAGE+"rmse_PREC.gif")+ "\');\" onmouseout=\"nodisplayImage();\">PREC</A>\n"
            html+="<TH ALIGN=center><a href=\"#\" onclick=\"displayImageClick(\'http://"+paths.ea_hostname + paths.generate_token_url(url_prefixIMAGE+"rmse_ASA.gif")+ "\');\" onmouseover=\"displayImageHover(\'http://"+paths.ea_hostname + paths.generate_token_url(url_prefixIMAGE+"rmse_ASA.gif")+ "\');\" onmouseout=\"nodisplayImage();\">ASA</A>\n"
            html+="<TR>\n"
            html+="<TH ALIGN=LEFT><font color=navy size=+1> 2. Seasonal bias </font>\n"
            html+="<TR>\n"
            html+="<TH ALIGN=LEFT><font color=navy size=+1>&nbsp&nbsp&nbsp&nbsp TSA </font>\n"
            html+="<TH ALIGN=center><a href=\"#\" onclick=\"displayImageClick(\'http://"+paths.ea_hostname + paths.generate_token_url(url_prefixIMAGE+"bias_TSA_DJF.gif")+ "\');\" onmouseover=\"displayImageHover(\'http://"+paths.ea_hostname + paths.generate_token_url(url_prefixIMAGE+"bias_TSA_DJF.gif")+ "\');\" onmouseout=\"nodisplayImage();\">DJF</A>\n"
            html+="<TH ALIGN=center><a href=\"#\" onclick=\"displayImageClick(\'http://"+paths.ea_hostname + paths.generate_token_url(url_prefixIMAGE+"bias_TSA_MAM.gif")+ "\');\" onmouseover=\"displayImageHover(\'http://"+paths.ea_hostname + paths.generate_token_url(url_prefixIMAGE+"bias_TSA_MAM.gif")+ "\');\" onmouseout=\"nodisplayImage();\">MAM</A>\n"
            html+="<TH ALIGN=center><a href=\"#\" onclick=\"displayImageClick(\'http://"+paths.ea_hostname + paths.generate_token_url(url_prefixIMAGE+"bias_TSA_JJA.gif")+ "\');\" onmouseover=\"displayImageHover(\'http://"+paths.ea_hostname + paths.generate_token_url(url_prefixIMAGE+"bias_TSA_JJA.gif")+ "\');\" onmouseout=\"nodisplayImage();\">JJA</A>\n"
            html+="<TH ALIGN=center><a href=\"#\" onclick=\"displayImageClick(\'http://"+paths.ea_hostname + paths.generate_token_url(url_prefixIMAGE+"bias_TSA_SON.gif")+ "\');\" onmouseover=\"displayImageHover(\'http://"+paths.ea_hostname + paths.generate_token_url(url_prefixIMAGE+"bias_TSA_SON.gif")+ "\');\" onmouseout=\"nodisplayImage();\">SON</A>\n"
            html+="<TH ALIGN=center><a href=\"#\" onclick=\"displayImageClick(\'http://"+paths.ea_hostname + paths.generate_token_url(url_prefixIMAGE+"bias_TSA_ANN.gif")+ "\');\" onmouseover=\"displayImageHover(\'http://"+paths.ea_hostname + paths.generate_token_url(url_prefixIMAGE+"bias_TSA_ANN.gif")+ "\');\" onmouseout=\"nodisplayImage();\">ANN</A>\n"
            html+="<TR>\n"
            html+="<TH ALIGN=LEFT><font color=navy size=+1>&nbsp&nbsp&nbsp&nbsp PREC </font>\n"
            html+="<TH ALIGN=center><a href=\"#\" onclick=\"displayImageClick(\'http://"+paths.ea_hostname + paths.generate_token_url(url_prefixIMAGE+"bias_PREC_DJF.gif")+ "\');\" onmouseover=\"displayImageHover(\'http://"+paths.ea_hostname + paths.generate_token_url(url_prefixIMAGE+"bias_PREC_DJF.gif")+ "\');\" onmouseout=\"nodisplayImage();\">DJF</A>\n"
            html+="<TH ALIGN=center><a href=\"#\" onclick=\"displayImageClick(\'http://"+paths.ea_hostname + paths.generate_token_url(url_prefixIMAGE+"bias_PREC_MAM.gif")+ "\');\" onmouseover=\"displayImageHover(\'http://"+paths.ea_hostname + paths.generate_token_url(url_prefixIMAGE+"bias_PREC_MAM.gif")+ "\');\" onmouseout=\"nodisplayImage();\">MAM</A>\n"
            html+="<TH ALIGN=center><a href=\"#\" onclick=\"displayImageClick(\'http://"+paths.ea_hostname + paths.generate_token_url(url_prefixIMAGE+"bias_PREC_JJA.gif")+ "\');\" onmouseover=\"displayImageHover(\'http://"+paths.ea_hostname + paths.generate_token_url(url_prefixIMAGE+"bias_PREC_JJA.gif")+ "\');\" onmouseout=\"nodisplayImage();\">JJA</A>\n"
            html+="<TH ALIGN=center><a href=\"#\" onclick=\"displayImageClick(\'http://"+paths.ea_hostname + paths.generate_token_url(url_prefixIMAGE+"bias_PREC_SON.gif")+ "\');\" onmouseover=\"displayImageHover(\'http://"+paths.ea_hostname + paths.generate_token_url(url_prefixIMAGE+"bias_PREC_SON.gif")+ "\');\" onmouseout=\"nodisplayImage();\">SON</A>\n"
            html+="<TH ALIGN=center><a href=\"#\" onclick=\"displayImageClick(\'http://"+paths.ea_hostname + paths.generate_token_url(url_prefixIMAGE+"bias_PREC_ANN.gif")+ "\');\" onmouseover=\"displayImageHover(\'http://"+paths.ea_hostname + paths.generate_token_url(url_prefixIMAGE+"bias_PREC_ANN.gif")+ "\');\" onmouseout=\"nodisplayImage();\">ANN</A>\n"
            html+="<TR>\n"
            html+="<TH ALIGN=LEFT><font color=navy size=+1>&nbsp&nbsp&nbsp&nbsp ASA </font>\n"
            html+="<TH ALIGN=center><a href=\"#\" onclick=\"displayImageClick(\'http://"+paths.ea_hostname + paths.generate_token_url(url_prefixIMAGE+"bias_ASA_DJF.gif")+ "\');\" onmouseover=\"displayImageHover(\'http://"+paths.ea_hostname + paths.generate_token_url(url_prefixIMAGE+"bias_ASA_DJF.gif")+ "\');\" onmouseout=\"nodisplayImage();\">DJF</A>\n"
            html+="<TH ALIGN=center><a href=\"#\" onclick=\"displayImageClick(\'http://"+paths.ea_hostname + paths.generate_token_url(url_prefixIMAGE+"bias_ASA_MAM.gif")+ "\');\" onmouseover=\"displayImageHover(\'http://"+paths.ea_hostname + paths.generate_token_url(url_prefixIMAGE+"bias_ASA_MAM.gif")+ "\');\" onmouseout=\"nodisplayImage();\">MAM</A>\n"
            html+="<TH ALIGN=center><a href=\"#\" onclick=\"displayImageClick(\'http://"+paths.ea_hostname + paths.generate_token_url(url_prefixIMAGE+"bias_ASA_JJA.gif")+ "\');\" onmouseover=\"displayImageHover(\'http://"+paths.ea_hostname + paths.generate_token_url(url_prefixIMAGE+"bias_ASA_JJA.gif")+ "\');\" onmouseout=\"nodisplayImage();\">JJA</A>\n"
            html+="<TH ALIGN=center><a href=\"#\" onclick=\"displayImageClick(\'http://"+paths.ea_hostname + paths.generate_token_url(url_prefixIMAGE+"bias_ASA_SON.gif")+ "\');\" onmouseover=\"displayImageHover(\'http://"+paths.ea_hostname + paths.generate_token_url(url_prefixIMAGE+"bias_ASA_SON.gif")+ "\');\" onmouseout=\"nodisplayImage();\">SON</A>\n"
            html+="<TH ALIGN=center><a href=\"#\" onclick=\"displayImageClick(\'http://"+paths.ea_hostname + paths.generate_token_url(url_prefixIMAGE+"bias_ASA_ANN.gif")+ "\');\" onmouseover=\"displayImageHover(\'http://"+paths.ea_hostname + paths.generate_token_url(url_prefixIMAGE+"bias_ASA_ANN.gif")+ "\');\" onmouseout=\"nodisplayImage();\">ANN</A>\n"
            html+="<TR>\n"
            html+="<TR>\n"
            html+="<TH ALIGN=LEFT><font color=navy size=+1> 3. Correlation </font>\n"
            html+="<TH ALIGN=center><a href=\"#\" onclick=\"displayImageClick(\'http://"+paths.ea_hostname + paths.generate_token_url(url_prefixIMAGE+"corr_TSA.gif")+ "\');\" onmouseover=\"displayImageHover(\'http://"+paths.ea_hostname + paths.generate_token_url(url_prefixIMAGE+"corr_TSA.gif")+ "\');\" onmouseout=\"nodisplayImage();\">TSA</A>\n"
            html+="<TH ALIGN=center><a href=\"#\" onclick=\"displayImageClick(\'http://"+paths.ea_hostname + paths.generate_token_url(url_prefixIMAGE+"corr_PREC.gif")+ "\');\" onmouseover=\"displayImageHover(\'http://"+paths.ea_hostname + paths.generate_token_url(url_prefixIMAGE+"corr_PREC.gif")+ "\');\" onmouseout=\"nodisplayImage();\">PREC</A>\n"
            html+="<TH ALIGN=center><a href=\"#\" onclick=\"displayImageClick(\'http://"+paths.ea_hostname + paths.generate_token_url(url_prefixIMAGE+"corr_ASA.gif")+ "\');\" onmouseover=\"displayImageHover(\'http://"+paths.ea_hostname + paths.generate_token_url(url_prefixIMAGE+"corr_ASA.gif")+ "\');\" onmouseout=\"nodisplayImage();\">ASA</A>\n"
            html+="<TR>\n"
            html+="<TH ALIGN=LEFT><font color=navy size=+1> 4. Standard Deviation </font>\n"
            html+="<TH ALIGN=center><a href=\"#\" onclick=\"displayImageClick(\'http://"+paths.ea_hostname + paths.generate_token_url(url_prefixIMAGE+"stdev_TSA.gif")+ "\');\" onmouseover=\"displayImageHover(\'http://"+paths.ea_hostname + paths.generate_token_url(url_prefixIMAGE+"stdev_TSA.gif")+ "\');\" onmouseout=\"nodisplayImage();\">TSA</A>\n"
            html+="<TH ALIGN=center><a href=\"#\" onclick=\"displayImageClick(\'http://"+paths.ea_hostname + paths.generate_token_url(url_prefixIMAGE+"stdev_PREC.gif")+ "\');\" onmouseover=\"displayImageHover(\'http://"+paths.ea_hostname + paths.generate_token_url(url_prefixIMAGE+"stdev_PREC.gif")+ "\');\" onmouseout=\"nodisplayImage();\">PREC</A>\n"
            html+="<TH ALIGN=center><a href=\"#\" onclick=\"displayImageClick(\'http://"+paths.ea_hostname + paths.generate_token_url(url_prefixIMAGE+"stdev_ASA.gif")+ "\');\" onmouseover=\"displayImageHover(\'http://"+paths.ea_hostname + paths.generate_token_url(url_prefixIMAGE+"stdev_ASA.gif")+ "\');\" onmouseout=\"nodisplayImage();\">ASA</A>\n"
            html+="<TR>\n"
            html+="<TH ALIGN=LEFT><font color=navy size=+1> 5. Tables</font>\n"
            html+="<TH ALIGN=center><a href=\"#\" onclick=\"displayTable(\'http://"+paths.ea_hostname + paths.generate_token_url(url_prefixIMAGE+"statTable.html") + "\');\">All Variables</A>\n"
            html+="<TR>\n"
            html+="<TR>\n"
            html+="<TR>\n"
            html+="</TABLE>\n"
            html+="</p>\n"
            
        return html