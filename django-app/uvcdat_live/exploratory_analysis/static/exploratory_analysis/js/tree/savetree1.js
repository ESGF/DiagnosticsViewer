$(document).ready(function(){

	
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
    

	$body = $("body");
	
	
	
	$('#save_tree').click(function() {
		

		
		
		/*
		console.log('tree: ' + $('#tree_name').val());
		
		
		
		var dataset = '';
		var pckg = '';
		var variable_arr = new Array();
		var season_arr =  new Array();
		var sets_arr = new Array();

		dataset = $("input[type='radio'].dataset_list").val();
		pckg = $("input[type='radio'].package_list").val();
		
		$("input[type='checkbox'].variable_list").each(function(index, element){
			//var a = $("input[type='checkbox'].variable_list");
			
		    if(element.checked) {
		    	
				variable_arr.push(element.id);
		    }
		});
		$("input[type='checkbox'].season_list").each(function(index, element){
			if(element.checked) {
				season_arr.push(element.id);
			}
		    
		});
		
		console.log('season_arr: ' + season_arr);
		
		$("input[type='checkbox'].sets_list").each(function(index, element){
			if(element.checked) {
				sets_arr.push(element.id);
			}
		    
		});
		
		
		var variable_arr_str = '';
		for(var i=0;i<variable_arr.length;i++) {
			if(i < variable_arr.length-1) {
				variable_arr_str += variable_arr[i] + ';';
			} else {
				variable_arr_str += variable_arr[i];
			}
			
		}

		var season_arr_str = '';
		for(var i=0;i<season_arr.length;i++) {
			if(i < season_arr.length-1) {
				season_arr_str += season_arr[i] + ';';
			} else {
				season_arr_str += season_arr[i];
			}
		}

		var sets_arr_str = '';
		for(var i=0;i<sets_arr.length;i++) {
			if(i < sets_arr.length-1) {
				sets_arr_str += sets_arr[i] + ';';
			} else {
				sets_arr_str += sets_arr[i];
			}
		}
		
		var treename = $('#tree_name').val();
		
		
		//sanity checks
		var datasetFlag = true;
		var packageFlag = true;
		var variableFlag = true;
		var seasonFlag = true;
		var nameFlag = true;
		
		//if()
		if(variable_arr_str == '') {
			variableFlag = false;
		}
		if(season_arr_str == '') {
			seasonFlag = false;
		}
		if(treename == '') {
			nameFlag = false;
		}
		
		
		if(variableFlag && seasonFlag && nameFlag) {
			
			if (EA.spinnerFlag) {
				$body.addClass("loading");  
			}
			
			
			var realm = 'land';
			
			
			var username = $('#username_posted').html();
			
			var tree_bookmark_name = treename;
			var tree_bookmark_datasetname = dataset;
			var tree_bookmark_realm = realm;
			var tree_bookmark_username = username;
			var tree_bookmark_variables = variable_arr_str;
			var tree_bookmark_times = season_arr_str;
			var tree_bookmark_sets = sets_arr_str;
			var tree_bookmark_description = '';
			
			
			//var front_end_cache_dir = '../../../static/cache/';
			var tree_cache_url = EA.front_end_tree_cache_dir + tree_bookmark_name + '.json';

			console.log('tree_bookmark_name: ' + tree_bookmark_name);
			console.log('tree_bookmark_datasetname: ' + tree_bookmark_datasetname);
			console.log('tree_bookmark_realm: ' + tree_bookmark_realm);
			console.log('tree_bookmark_username: ' + tree_bookmark_username);
			console.log('tree_bookmark_variables: ' + tree_bookmark_variables);
			console.log('tree_bookmark_times: ' + tree_bookmark_times);
			console.log('tree_bookmark_sets: ' + tree_bookmark_sets);
			console.log('tree_bookmark_description: ' + tree_bookmark_description);
			console.log('tree_cache_url: ' + tree_cache_url);
			
			
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
	    
			
			
			
			
			//This address will save the tree to the database
			var url = 'http://' + EA.host + ':' + EA.port + '/exploratory_analysis/tree_bookmarks/';
			
			
			
			
			$.ajax({
			  type: "POST",
			  url: url,
			  //async: false,
			  data: data,
			  success: function(response_data)
			  { 
					
				  console.log('success');
				  
				  
				  
				  var data = {
							'csrfmiddlewaretoken': csrftoken,
							'treename': treename,
							'dataset': dataset,
							'package': pckg,
							'variable_arr_str': variable_arr_str,
							'season_arr_str':season_arr_str,
							'sets_arr_str':sets_arr_str,
							'posttype':'save'
				  };
				  
				  
				  
				  //var url = 'http://localhost:8081/exploratory_analysis/treeex/jfharney/';
				  var url = 'http://' + EA.host + ':' + EA.port + '/exploratory_analysis/treeex/u1/';
					
				  
				  console.log('save tree url-----> ' + url);
				  
				    
					$.ajax({
						  type: "POST",
						  url: url,
						  //async: false,
						  data: data,
						  dataType: 'json',
						  success: function(data)
						  { 
							  
							  console.log('success');
							  
							  for (var key in data) {
								  console.log('key: ' + key + ' value: ' + data[key])
							  }
							  
							  
							  
							   
							  //hide the options
							  $('#create_tree_options').hide();
							  $('#create_tree').html('Create Tree');
							  
							  //show tree
							  $('#treeviewer').show();
							  
							  $('#current_treename').empty();
							  $('#current_treename').html(data['treename']);
							  
							  
							  var treeFile = $('span#treeFile').html();
							  treeFile = tree_cache_url;
							  
							  treeFile = treeFile.replace(EA.uvcdat_live_root + '/exploratory_analysis','../../..');
							  //treeFile = treeFile.replace('/Users/8xo/software/exploratory_analysis/DiagnosticsViewer/django-app/uvcdat_live/exploratory_analysis','../../..');

							  //console.log('treeFile before: ' + treeFile);
							  //treeFile = '../../../static/cache/temp.json';
							  //console.log('treeFile after: ' + treeFile);
								
							  if(checkFile(treeFile)) {
									
							    //render the tree
										
								d3.json(treeFile, function(error, flare) {
										
									//d3.json(cache_dir + fileName, function(error, flare) {
										
									///Users/8xo/software/exploratory_analysis/DiagnosticsViewer/django-app/uvcdat_live/exploratory_analysis/static/exploratory_analysis/css/tree/flare13.json
									root = flare;
									root.x0 = height / 2;
									root.y0 = 0;
									
									function collapse(d) {
										if (d.children) {
										  d._children = d.children;
										  d._children.forEach(collapse);
										  d.children = null;
										}
									}
									
									root.children.forEach(collapse);
									update(root);
								});
									
								} else {
									console.log('leave blank');
								}
									
							  	if (EA.spinnerFlag) {
							  		$body.removeClass("loading");  
							  	}
							  	
						  },
						  error: function(ts) 
						  { 
							  console.log('response text: ' + ts.responseText);
							  
							  if (EA.spinnerFlag) {
								  $body.removeClass("loading"); 
							  }
						  }
					});
				  
				  	
				  
				  
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
			
			
			
			
			
		} else {
			if(!variableFlag && !seasonFlag && !nameFlag) { 
				alert('Please enter values for variables, seasons, and a valid tree name');
			} else if(!variableFlag && !seasonFlag && nameFlag) { 
				alert('Please enter values for variables and seasons');
			} else if(!variableFlag && seasonFlag && !nameFlag) { 
				alert('Please enter values for variables and a valid tree name');
			} else if(!variableFlag && seasonFlag && nameFlag) { 
				alert('Please enter values for variables');
			} else if(variableFlag && !seasonFlag && !nameFlag) { 
				alert('Please enter values for seasons and a valid tree name');
			} else if(variableFlag && seasonFlag && !nameFlag) { 
				alert('Please enter a valid tree name');
			} else if(variableFlag && !seasonFlag && nameFlag) { 
				alert('Please enter values for seasons');
			}
		}
		
		*/
		
	});
	
	
	
});