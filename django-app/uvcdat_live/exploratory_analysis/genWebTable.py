#!/usr/bin/env python
import land_vardict.py

#Construct table with description (variable) and link to plot

#Input from json object from user selection
user_selected_vars = {'TSA', 'PREC'}


#Start writing file (SPECIFY LOCATION TO WRITE FILE TO HERE) 	Example: land/tropics_warming_th_q/img/
file = open("setTest.html", "w")

#Header
file.write("<p>\n") 
file.write("<b><font color=maroon size=+2>Set 1 Description: <b></font>Line plots of annual trends in energy balance, soil water/ice and temperature, runoff, snow water/ice, photosynthesis </b><br>\n")
file.write("<br clear=left>")
file.write("</p>\n")
file.write("<p>\n")
file.write("<A HREF=\"variableList_1.html\" target=\"set1_Variables\">\n")
file.write("<font color=maroon size=+1 text-align: right><b>Lookup Table: Set 1 Variable Definition</b></font></a>\n")
file.write("</br>\n")
file.write("</p>\n") 


#Start table
file.write("<p>\n")
file.write("<hr noshade size=2 size=\"100%\">\n")
file.write("<TABLE> \n")
file.write("<TR>\n")
file.write("<TH><TH ALIGN=LEFT><font color=maroon>Trend</font>\n")
file.write("</TR>\n")


#python for loop----------
#Descriptions are (predefinedBrianSmithDictionary[key]) 

for key in vardict:
	if 1 in vardict[key]['sets'] and key in user_selected_vars:
		file.write("<TR>\n")
		file.write('<TH ALIGN=LEFT>') 
		file.write(vardict[key]['desc'])
		file.write('(')
		file.write(key)
		file.write(')')
		file.write('<TH ALIGN=LEFT>') 
		file.write('<a href="#" onclick="displayImageClick(')
		file.write('set1_')#Here we write gif name
		file.write(key)
		file.write('.gif') 
		file.write(');" onmouseover="displayImageHover(')
		file.write('set1_')#Here we write gif name again
		file.write(key)
		file.write('.gif') 
		file.write(');" onmouseout="nodisplayImage();">plot</A>\n')
		file.write("</TR>\n")

'''
Figure Names
<package>_<set>_<time>_<variable>.png


#No time in this one


Example: 
lmwg_set1_JAN_TLAI.png
'''

#end for loop and end table generation-------------------------

file.write("</TABLE> \n")
file.write("</p>\n")
file.close()








