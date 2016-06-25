/*
/bin/bash: indent: command not found || {};


EA.cache_location = '../../../static/exploratory_analysis/img/treeex/';


EA.host = 'acme-dev-2.ornl.gov';

EA.port = document.location.port;


var core_parameters_url = '/exploratory_analysis/core_parameters';
*/

var EA = EA || {};

EA.cache_location = '../../../static/exploratory_analysis/img/treeex/';


EA.host = 'acme-dev-2.ornl.gov';

EA.port = document.location.port;


var core_parameters_url = '/exploratory_analysis/core_parameters';

$.ajax({
	type : "GET",
	url : core_parameters_url,
	async : false,
	success : function(data) {
		
		var obj = JSON.parse(data);
		
		EA.host = obj['host'];
	},
	error: function() {
		
		alert('error in getting core parameters');
		
	}
});


EA.spinnerFlag = true;

//EA.uvcdat_live_root = '/Users/8xo/software/exploratory_analysis/DiagnosticsViewer/django-app/uvcdat_live';
EA.uvcdat_live_root = '/usr/local/uvcdat/DiagnosticsViewer/django-app/uvcdat_live/';


//---------Tree settings----------//
EA.treeDepthFactor = 150;

EA.tree_width = 400;
EA.tree_height = 600;

EA.tree_margin_right = 20;
EA.tree_margin_left = 20;
EA.tree_margin_top = 30;
EA.tree_margin_bottom = 20;


//used in savetree.js
//EA.front_end_tree_cache_dir = '../../../static/cache/';
EA.front_end_tree_cache_dir = '../../../static/exploratory_analysis/cache/tree/';

EA.front_end_figure_cache_dir = '../../../static/exploratory_analysis/img/treeex/';



//--------Default Parameters------------//
EA.packList = ["lmwg"];
EA.timeList = ["JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC","DJF","MAM","JJA","SON","ANN"];
EA.varList = ["GPP","NEE","HR","ER","NPP","QVEGT","QVEGE","QSOIL","GROSSNMIN"];


EA.default_facet_list = [];
project_obj = {'project' : 'ACME'};
data_type_obj = {'data_type' : 'climo,dd,dt,dv,h,h0,h1,h2,h3,h4'};
realm_obj = { 'realm' : 'atm,ice,lnd,ocn,all,ATM' };
regridding_obj = {'regridding' : 'bilinear,downscaled,native,fv257x512,ne30_g16,T341_f02_t12'};
range_obj = {'range' : 'all_dir,all,2-9,10-19,20-29,30-39,30-50,40-49,ALL'};
versionnum_obj = {'versionnum' : 'v0_0,v0_1,v01,HIGHRES,pre-v0'};
experiment_obj = {'experiment' : 'B1850C5_ne30gx1_tuning,341f02.B1850dEdd,B1850C5e1_ne30'};
EA.default_facet_list.push(project_obj);
EA.default_facet_list.push(data_type_obj);
EA.default_facet_list.push(realm_obj);
EA.default_facet_list.push(regridding_obj);
EA.default_facet_list.push(range_obj);
EA.default_facet_list.push(versionnum_obj);
EA.default_facet_list.push(experiment_obj);

EA.useDefaultFacetList = true;

/*
EA.default_facet_list = [];
project_obj = {'project' : 'ACME'};
data_type_obj = {'data_type' : ['climo','dd','dt','dv','h','h0','h1','h2','h3','h4']};
realm_obj = {'realm' : ['atm','ice','lnd','ocn','all','ATM']};
regridding_obj = {'regridding' : ['bilinear','downscaled,native','fv257x512','ne30_g16','T341_f02_t12']};
range_obj = {'range' : ['all_dir','all','2-9','10-19','20-29','30-39','30-50','40-49','ALL']};
versionnum_obj = {'versionnum' : ['v0_0','v0_1','v01','HIGHRES','pre-v0']};
experiment_obj = {'experiment' : ['B1850C5_ne30gx1_tuning','341f02.B1850dEdd','B1850C5e1_ne30']};
EA.default_facet_list.push(project_obj);
EA.default_facet_list.push(data_type_obj);
EA.default_facet_list.push(realm_obj);
EA.default_facet_list.push(regridding_obj);
EA.default_facet_list.push(range_obj);
EA.default_facet_list.push(versionnum_obj);
EA.default_facet_list.push(experiment_obj);
*/

/*
EA.default_facet_list = {};
EA.default_facet_list['project'] = ['ACME'];
EA.default_facet_list['data_type'] = ['climo','dd','dt','dv','h','h0','h1','h2','h3','h4'];
EA.default_facet_list['realm'] = ['atm','ice','lnd','ocn','all','ATM'];
EA.default_facet_list['regridding'] = ['bilinear','downscaled,native','fv257x512','ne30_g16','T341_f02_t12'];
EA.default_facet_list['range'] = ['all_dir','all','2-9','10-19','20-29','30-39','30-50','40-49','ALL'];
EA.default_facet_list['versionnum'] = ['v0_0','v0_1','v01','HIGHRES','pre-v0'];
EA.default_facet_list['experiment'] = ['B1850C5_ne30gx1_tuning','341f02.B1850dEdd','B1850C5e1_ne30'];
*/

EA.tree_state = '';
