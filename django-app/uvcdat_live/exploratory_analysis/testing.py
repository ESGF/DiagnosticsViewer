#!/usr/bin/env python

vardict={}
vardict['PFT_FIRE_CLOSS']={'RepUnits': 'PgC/y', 'sets': [1, 2, 3, 5, 6], 'NatUnits': 'gC/m^2/s', 'desc': 'total pft-level fire C loss'}
vardict['SNOWDP']={'RepUnits': 'NA', 'sets': [2, 3, 5, 6], 'NatUnits': 'm', 'desc': 'snow height'}
vardict['LITHR']={'RepUnits': 'PgC/y', 'sets': [1, 2, 5], 'NatUnits': 'gC/m^2/s', 'desc': 'litter hetereotrophic respiration'}
vardict['QSOIL']={'RepUnits': 'mm/d', 'sets': [1, 2, 5], 'NatUnits': 'mm/s', 'desc': 'ground evaporation'}
vardict['WA']={'RepUnits': 'mm', 'sets': [1, 2, 3, 5, 6], 'NatUnits': 'mm', 'desc': 'water in the unconfined aquifer'}

#Input from json object from user selection
user_selected_vars = {'LITHR', 'QSOIL'}


#FOR plot 1
for key in vardict:
	if 1 in vardict[key]['sets'] and key in user_selected_vars:
		print vardict[key]['desc']
		print key  	






'''
#FOR plot 2
for key in vardict:
	if 2 in vardict[key]['sets']:
		print vardict[key]['desc'] 


#FOR plot 3
for key in vardict:
	if 3 in vardict[key]['sets']:
		print vardict[key]['desc']
'''
