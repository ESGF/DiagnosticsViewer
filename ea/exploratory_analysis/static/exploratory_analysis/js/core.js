var EA = EA || {};


//EA.host = 'acme-ea-dev1.ornl.gov';
//EA.host = 'acme-ea.ornl.gov'
EA.host = 'localhost';
EA.port = '8081'; //document.location.port;
//EA.port = '80';

EA.default_groups = ['ACME'];
EA.default_datasets = ['a','b','c'];
EA.default_packages = ['amwg','lmwg'];
EA.default_variables = ['v1','v2','v3'];
EA.default_times = ["JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC","DJF","MAM","JJA","SON","ANN"];

EA.noImageSource = "/static/exploratory_analysis/img/classic/Noimage.png";

EA.config_url = '/exploratory_analysis/config?set=' + 'set' + '&dataset_name=' + 'dataset';// + '&package=' + pckg;   //+ '?_=' + Math.round(Math.random() * 10000);
console.log('url: ', EA.config_url);

/*

$.ajax({
	type : "GET",
	url : EA.config_url,
	dataType: 'json',
	//async: false,
	success : function(data) {
		alert(data);
		for (var key in data) {
			console.log('mykey: ' + key);
		}
		
		EA.host = data['EA_hostname'];
		EA.port = data['EA_port'];
		
		
		
	},
	error : function(xhr, status, error) {
		console.log('error');
	}
});
*/


var EA_CLASSIC_VIEWER = EA_CLASSIC_VIEWER || {};

EA_CLASSIC_VIEWER.namespace = function(ns_string) {
	var parts = ns_string.split('.'),
		parent = EA_CLASSIC_VIEWER,
		i;
	
	//strip redundant leading global
	if (parts[0] === 'EA_CLASSIC_VIEWER') {
		parts = parts.slice(1);
	}
	
	for(i=0;i<parts.length;i++) {
		// create a property if it doesn't exist
		if (typeof parent[parts[i]] === 'undefined') {
			parent[parts[i]] = {};
		}
		parent = parent[parts[i]];
	}
	return parent;
	
};


EA_CLASSIC_VIEWER.namespace('EA_CLASSIC_VIEWER.functions');


