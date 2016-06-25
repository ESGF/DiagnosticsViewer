var myApp;
myApp = myApp || (function () {
    var pleaseWaitDiv = $('<div class="modal hide" id="pleaseWaitDialog" data-backdrop="static" data-keyboard="false"><div class="modal-header"><h1>Processing...</h1></div><div class="modal-body"><div class="progress progress-striped active"><div class="bar" style="width: 100%;"></div></div></div></div>');
    return {
        showPleaseWait: function() {
        	console.log('showing please wait');
            pleaseWaitDiv.modal();
        },
        hidePleaseWait: function () {
            pleaseWaitDiv.modal('hide');
        },

    };
})();
		

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
    
	console.log('csrftoken ' + csrftoken);
	

	//$body = $("body");
	
	
	$('#submit_tree').click(function() {
		
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
		
		//if()
		if(variable_arr_str == '') {
			variableFlag = false;
		}
		if(season_arr_str == '') {
			seasonFlag = false;
		}
		
		
		if(variableFlag && seasonFlag) {
			

			$body.addClass("loading");
			
			var data = {
					'csrfmiddlewaretoken': csrftoken,
					'treename': treename,
					'dataset': dataset,
					'package': pckg,
					'variable_arr_str': variable_arr_str,
					'season_arr_str':season_arr_str,
					'sets_arr_str':sets_arr_str,
					'posttype':'submit'
			};
			
			//var url = 'http://localhost:8081/exploratory_analysis/treeex/jfharney/';
			var url = 'http://' + EA.host + ':' + EA.port + '/exploratory_analysis/treeex/jfharney/';
			
			
			$.ajax({
				  type: "POST",
				  url: url,
				  //async: false,
				  data: data,
				  dataType: 'json',
				  success: function(data)
				  { 
					  

					  $body.removeClass("loading");
					  
					  for (var key in data) {
						  console.log('key: ' + key + ' value: ' + data[key])
					  }
					  
					  
					  
					  //hide the options
					  $('#create_tree_options').hide();
					  $('#create_tree').html('Create Tree');
					  
					  //post usermname
					  //$('#username_posted').append(data['username']);
					  
					  //show tree
					  $('#treeviewer').show();
					  
					  $('#current_treename').empty();
					  $('#current_treename').html(data['treename']);
					  
					  
					  var treeFile = $('span#treeFile').html();
					  //alert('treeFile: ' + treeFile);
					  treeFile = treeFile.replace('/Users/8xo/software/exploratory_analysis/DiagnosticsViewer/django-app/uvcdat_live/exploratory_analysis','../../..');
						
					  treeFile = '../../../static/cache/temp.json';
					  console.log('treeFile: ' + treeFile);
						
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
							
					  
					  
				  },
				  error: function(ts) 
				  { 
					  console.log('response text: ' + ts.responseText);

					  //$body.removeClass("loading");
				  }
			});
			
		} else {
			console.log('Missing fields');
		}
		
		
	});
	
	
});
