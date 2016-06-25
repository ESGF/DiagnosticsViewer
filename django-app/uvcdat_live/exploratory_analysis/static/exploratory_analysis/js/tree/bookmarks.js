$(document).ready(function(){

//testers for the bookmark API
	
	//for post requests, need to get the csrf token
	function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');
    
	console.log('csrftoken ' + csrftoken);
	
	
	$('#test4').click(function() {
		//alert('test 2 submit');
		
		
		//var fileUrl = 'http://localhost:8081/exploratory_analysis/tree_bookmarks/';
		var fileUrl = 'http://' + EA.host + ':' + EA.port + "/exploratory_analysis/tree_bookmarks/";
		

	    var data = getSampleDataTree(csrftoken);
	    var querystring = getSampleQueryStringTree();
		
		fileUrl = fileUrl + querystring;
		test4(fileUrl,csrftoken,data);
		
		
	});
	
	
	
	
	
	$('#test3').click(function() {
		//alert('test 2 submit');
		
		//var fileUrl = 'http://localhost:8081/exploratory_analysis/tree_bookmarks/';
		var fileUrl = 'http://' + EA.host + ':' + EA.port + "/exploratory_analysis/tree_bookmarks/";
		
	    

	    var data = getSampleDataTree(csrftoken);
	    var querystring = getSampleQueryStringTree();
	    
		fileUrl = fileUrl + querystring;
	    
		test3(fileUrl,csrftoken,data);
		
	});
	
	
	
	
	
	$('#test2').click(function() {
		//alert('test 2 submit');
		
		//var fileUrl = 'http://localhost:8081/exploratory_analysis/tree_bookmarks/';
		var fileUrl = 'http://' + EA.host + ':' + EA.port + "/exploratory_analysis/tree_bookmarks/";
		
		
		
	    var data = getSampleDataTree(csrftoken);
	    var querystring = getSampleQueryStringTree();
	    
	    test2(fileUrl,csrftoken,data);
		
		
	});
	
	
	
	$('#test14').click(function() {
		//alert('test 2 submit');
		
		//var fileUrl = 'http://localhost:8081/exploratory_analysis/figure_bookmarks/';
		var fileUrl = 'http://' + EA.host + ':' + EA.port + "/exploratory_analysis/tree_bookmarks/";
		
		
		
		var data = getSampleDataFigure(csrftoken);
		var querystring = getSampleQueryStringFigure();
		
		
		fileUrl = fileUrl + querystring;
		test14(fileUrl,csrftoken,data);
		
		
	});
	
	
	
	
	
	$('#test13').click(function() {
		//alert('test 2 submit');
		
		//var fileUrl = 'http://localhost:8081/exploratory_analysis/figure_bookmarks/';
		var fileUrl = 'http://' + EA.host + ':' + EA.port + "/exploratory_analysis/tree_bookmarks/";
		
		
		var data = getSampleDataFigure(csrftoken);
		var querystring = getSampleQueryStringFigure();
		
		fileUrl = fileUrl + querystring;
	    
		test13(fileUrl,csrftoken,data);
	    
		
	});
	
	
	
	$('#test12').click(function() {
		//alert('test 2 submit');
		
		//var fileUrl = 'http://localhost:8081/exploratory_analysis/figure_bookmarks/';
		var fileUrl = 'http://' + EA.host + ':' + EA.port + "/exploratory_analysis/tree_bookmarks/";
		
		
	    var data = getSampleDataFigure(csrftoken);
		var querystring = getSampleQueryStringFigure();
		
	    
	    test12(fileUrl,csrftoken,data);
	    
	});
	
	
	
	
	
});



function test2(fileUrl,csrftoken,data) {
	$.ajax({
		  type: "POST",
		  url: fileUrl,
		  async: false,
		  data: data,
		  success: function(response_data)
		  { 
			  
			  
			  console.log('success');
		  },
		  error: function(xhr, status, error) {
			  console.log('error'); 
		    if(xhr.status==404)
		    { 
		    	
		    }
		  }
		});
}

function test3(fileUrl,csrftoken,data) {

	$.ajax({
		  type: "DELETE",
		  url: fileUrl,
		  async: false,
		  beforeSend: function(xhr) {
		        xhr.setRequestHeader("X-CSRFToken", csrftoken);//getCookie("csrftoken"));
		  },
		  //data: data,
		  success: function(response_data)
		  { 
			  
			  
			  console.log('success');
		  },
		  error: function(xhr, status, error) {
			  console.log('error'); 
		    if(xhr.status==404)
		    { 
		    	
		    }
		  }
		});
}

function test4(fileUrl,csrftoken,data) {
	$.ajax({
		  type: "GET",
		  url: fileUrl,
		  dataType: 'json',
		  async: false,
		  beforeSend: function(xhr) {
		        xhr.setRequestHeader("X-CSRFToken", csrftoken);//getCookie("csrftoken"));
		  },
		  //data: data,
		  success: function(response_data)
		  { 
			  console.log(response_data);
			  
			  for (var key in response_data) {
				  console.log('key: ' + key + ' value: ' + response_data[key]);
			  }
			  
			  console.log('success');
		  },
		  error: function(xhr, status, error) {
			  console.log('error'); 
		    if(xhr.status==404)
		    { 
		    	
		    }
		  }
		});
}

function test12(fileUrl,csrftoken,data) {
	$.ajax({
		  type: "POST",
		  url: fileUrl,
		  async: false,
		  data: data,
		  success: function(response_data)
		  { 
			  
			  console.log('success');
		  },
		  error: function(xhr, status, error) {
			  console.log('error'); 
		    if(xhr.status==404)
		    { 
		    	
		    }
		  }
		});
}

function test13(fileUrl,csrftoken,data) {
	$.ajax({
		  type: "DELETE",
		  url: fileUrl,
		  async: false,
		  beforeSend: function(xhr) {
		        xhr.setRequestHeader("X-CSRFToken", csrftoken);//getCookie("csrftoken"));
		  },
		  //data: data,
		  success: function(response_data)
		  { 
			  
			  
			  console.log('delete success');
		  },
		  error: function(xhr, status, error) {
			  console.log('error'); 
		    if(xhr.status==404)
		    { 
		    	
		    }
		  }
		});
}

function test14(fileUrl,csrftoken,data) {
	$.ajax({
		  type: "GET",
		  url: fileUrl,
		  dataType: 'json',
		  async: false,
		  beforeSend: function(xhr) {
		        xhr.setRequestHeader("X-CSRFToken", csrftoken);//getCookie("csrftoken"));
		  },
		  //data: data,
		  success: function(response_data)
		  { 
			  console.log(response_data);
			  
			  for (var key in response_data) {
				  console.log('key: ' + key + ' value: ' + response_data[key]);
			  }
			  
			  console.log('success');
		  },
		  error: function(xhr, status, error) {
			  console.log('error'); 
		    if(xhr.status==404)
		    { 
		    	
		    }
		  }
		});
}


function getSampleDataTree(csrftoken) {
	var tree_bookmark_name = 'tree_bookmark_name1';
    var tree_bookmark_datasetname = 'tree_bookmark_datasetname1';
    var tree_bookmark_realm = 'tree_bookmark_realm1';
    var tree_bookmark_username = 'tree_bookmark_username1';
    var tree_bookmark_variables = 'tree_bookmark_variables1';
    var tree_bookmark_times = 'tree_bookmark_times1';
    var tree_bookmark_sets = 'tree_bookmark_sets1';
    var tree_bookmark_description = 'tree_bookmark_description1';
    var tree_cache_url = 'tree_cache_url1';
    
    var data = {
    			'csrfmiddlewaretoken': csrftoken,
    			'tree_bookmark_name': tree_bookmark_name,
    			'tree_bookmark_datasetname':tree_bookmark_datasetname,
    			'tree_bookmark_realm':tree_bookmark_realm,
    			'tree_bookmark_username':tree_bookmark_username,
    			'tree_bookmark_variables':tree_bookmark_variables,
    			'tree_bookmark_times':tree_bookmark_times,
    			'tree_bookmark_sets':tree_bookmark_sets,
    			'tree_bookmark_description':tree_bookmark_description,
    			'tree_cache_url':tree_cache_url
    };
    
    return data;
}

function getSampleQueryStringTree() {
	var tree_bookmark_name = 'tree_bookmark_name1';
    var tree_bookmark_datasetname = 'tree_bookmark_datasetname1';
    var tree_bookmark_realm = 'tree_bookmark_realm1';
    var tree_bookmark_username = 'tree_bookmark_username1';
    
    var querystring = '?tree_bookmark_name=' + tree_bookmark_name+
	'&tree_bookmark_datasetname=' + tree_bookmark_datasetname+
	'&tree_bookmark_realm=' + tree_bookmark_realm+
	'&tree_bookmark_username=' + tree_bookmark_username;

    
    return querystring;
}



function getSampleDataFigure(csrftoken) {
	
	var figure_bookmark_name = 'figure_bookmark_name1';
    var figure_bookmark_datasetname = 'figure_bookmark_datasetname1';
    var figure_bookmark_realm = 'figure_bookmark_realm1';
    var figure_bookmark_username = 'figure_bookmark_username1';
    var figure_bookmark_description = 'figure_bookmark_description1';
    var figure_cache_url = 'figure_cache_url1';
    
    var data = {
    			'csrfmiddlewaretoken': csrftoken,
    			'figure_bookmark_name': figure_bookmark_name,
    			'figure_bookmark_datasetname':figure_bookmark_datasetname,
    			'figure_bookmark_realm':figure_bookmark_realm,
    			'figure_bookmark_username':figure_bookmark_username,
    			'figure_bookmark_description':figure_bookmark_description,
    			'figure_cache_url':figure_cache_url
    };
	
	return data;
}

function getSampleQueryStringFigure() {
	
	var figure_bookmark_name = 'figure_bookmark_name1';
    var figure_bookmark_datasetname = 'figure_bookmark_datasetname1';
    var figure_bookmark_realm = 'figure_bookmark_realm1';
    var figure_bookmark_username = 'figure_bookmark_username1';
	
	var querystring = '?figure_bookmark_name=' + figure_bookmark_name+
						'&figure_bookmark_datasetname=' + figure_bookmark_datasetname+
						'&figure_bookmark_realm=' + figure_bookmark_realm+
						'&figure_bookmark_username=' + figure_bookmark_username;
	
	
	return querystring;
}





