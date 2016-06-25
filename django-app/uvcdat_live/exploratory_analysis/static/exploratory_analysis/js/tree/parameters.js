	
function getDatasets(username) {
	var url = 'http://' + EA.host + ':' + EA.port + '/exploratory_analysis/datasets1/' + username;
	
	
	$.ajax({
	  type: "GET",
	  url: url,
	  dataType: 'json',
	  //async: false,
	  //data: data,
	  success: function(response_data)
	  { 
			
		  console.log('success in getting datasets');
		  
		  var dataList = response_data['datasets'];
		  
		  
		  //var dataList = ["tropics_warming_th_q_co2"];
			
		  $("#selectD").multiselect().multiselectfilter();
			
		  $("#selectD").multiselect({
				multiple : false,
				header : "Select a dataset",
				//noneSelectedText : "tropics_warming_th_q_co2",
				selectedList : 1
		  });

		  d3.select("#selectD").selectAll("option").data(dataList).enter().append("option").attr("value", String).text(String);

		  $("#selectD").multiselect("refresh");
		  
		  
	  },
	  error: function(xhr, status, error) {
		  console.log('error'); 
		  if (EA.spinnerFlag) {
			  $body.removeClass("loading"); 
		  } 
	    if(xhr.status==404)
	    { 
	    	
	    }
	  }
	});
	
}

function getPackages(current_username) {
	
	var packList = EA.packList; //["lmwg"];
	

	url = 'http://' + EA.host + ':' + EA.port + '/exploratory_analysis/packages1';
	
	$.ajax({
		  type: "GET",
		  url: url,
		  dataType: 'json',
		  //async: false,
		  //data: data,
		  success: function(response_data)
		  { 
				
			  console.log('success in getting datasets');
			  
			  packList = response_data['packages'];
			  
			  
			  $("#selectP").multiselect().multiselectfilter();
				
				$("#selectP").multiselect({
					multiple : false,
					header : "Select a package",
					//noneSelectedText : "tropics_warming_th_q_co2",
					selectedList : 1
				});

				d3.select("#selectP").selectAll("option").data(packList).enter().append("option").attr("value", String).text(String);

				$("#selectP").multiselect("refresh");
				
			  
		  },
		  error: function(xhr, status, error) {
			  console.log('error'); 
			  if (EA.spinnerFlag) {
				  $body.removeClass("loading"); 
			  } 
		    if(xhr.status==404)
		    { 
		    	
		    }
		  }
		});

	
	
	
}

function getVariables(current_username) {
	url = 'http://' + EA.host + ':' + EA.port + '/exploratory_analysis/variables1';
	
	
	var varList = EA.varList;//["GPP","NEE","HR","ER","NPP","QVEGT","QVEGE","QSOIL","GROSSNMIN"];
	
	$.ajax({
		  type: "GET",
		  url: url,
		  dataType: 'json',
		  //async: false,
		  //data: data,
		  success: function(response_data)
		  { 
				
			  console.log('success in getting variables');
			  
			  varList = response_data['variables'];
			  
			  /*
			  for(var i=0;i<varList.length;i++) {
				  console.log('times: ' + varList[i]);
			  }
			  */
			  
			  //var dataList = ["tropics_warming_th_q_co2"];
				
			  $("#selectV").multiselect().multiselectfilter();
				
				$("#selectV").multiselect({
					multiple : true,
					header : "Select variables",
					noneSelectedText : "Select variables",
					selectedList : 1
				});

				d3.select("#selectV").selectAll("option").data(varList).enter().append("option").attr("value", String).text(String);


				$("#selectV").multiselect("refresh");
				
			  
			  
		  },
		  error: function(xhr, status, error) {
			  console.log('error'); 
			  if (EA.spinnerFlag) {
				  $body.removeClass("loading"); 
			  } 
		    if(xhr.status==404)
		    { 
		    	
		    }
		  }
		});
	
}

function getTimes(current_username) {
	
	url = 'http://' + EA.host + ':' + EA.port + '/exploratory_analysis/times1';
	
	var timeList = EA.timeList;//["JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC","DJF","MAM","JJA","SON","ANN"]

	
	$.ajax({
		  type: "GET",
		  url: url,
		  dataType: 'json',
		  //async: false,
		  //data: data,
		  success: function(response_data)
		  { 
				
			  var timeList = response_data['times'];
			  
			  /*
			  for(var i=0;i<timeList.length;i++) {
				  console.log('times: ' + timeList[i]);
			  }
			  */
			  
			  //var dataList = ["tropics_warming_th_q_co2"];
				
			  $("#selectT").multiselect().multiselectfilter();
				
			  $("#selectT").multiselect({
					multiple : true,
					header : "Select a dataset",
					//noneSelectedText : "tropics_warming_th_q_co2",
					selectedList : 1
			  });

			  d3.select("#selectT").selectAll("option").data(timeList).enter().append("option").attr("value", String).text(String);

			  $("#selectT").multiselect("refresh");
			  
			  
		  },
		  error: function(xhr, status, error) {
			  console.log('error'); 
			  if (EA.spinnerFlag) {
				  $body.removeClass("loading"); 
			  } 
		    if(xhr.status==404)
		    { 
		    	
		    }
		  }
		});
	
	
	
}
