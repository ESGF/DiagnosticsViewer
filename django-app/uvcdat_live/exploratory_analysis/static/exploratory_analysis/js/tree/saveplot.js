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
	

	$body = $("body");
	
	
	$('#save_plot').click(function() {
		
		

		console.log('title: ' + $('#modal-title').find('#figtitle').html());
		console.log('url: ' + $('#modal-title').find('#figurl').html());
		
		var figureName = $('#modal-title').find('#figtitle').html();
		
		//console.log('need to push a figure url (e.g. ' + figureUrl +') with figure name: ' + figureName);
		
		
		var indexOf = figureName.indexOf('.png');
		
		
		figureName = figureName.substr(0,indexOf).trim();
		
		var fileUrl = $('#modal-body').find('#fig_url').html();


		fileUrl = EA.front_end_figure_cache_dir + figureName;
		
		
		var description = $('textarea#figure_bookmark_description').val();
		
		
		
		var figure_bookmark_username = $('#username_posted').html();//'jfharney';
		var figure_bookmark_name = figureName;
		var figure_bookmark_description = description;

		var figure_bookmark_realm = 'land';
		var figure_bookmark_datasetname = 'tropics_warming_th_q_co2';
		var figure_cache_url = fileUrl;

		
		var data = {
				'csrfmiddlewaretoken': csrftoken,
				'figure_bookmark_name' : figure_bookmark_name,
				'figure_bookmark_realm' : figure_bookmark_realm,
				'figure_bookmark_datasetname' : figure_bookmark_datasetname,
				'figure_bookmark_username' : figure_bookmark_username,
				'figure_bookmark_description' : figure_bookmark_description,
				'figure_cache_url' : figure_cache_url
		};


		//$body.addClass("loading");  
		
		//var url = 'http://localhost:8081/exploratory_analysis/figure_bookmarks/';
		var url = 'http://' + EA.host + ':' + EA.port + "/exploratory_analysis/figure_bookmarks/";
		
		
		$.ajax({
			  type: "POST",
			  url: url,
			  //async: false,
			  data: data,
			  success: function()
			  { 
				  
				  var navigate_url = trimPound(document.URL);
				  
				  location.href=navigate_url;
				  
			  },
			  error: function(xhr, status, error) {
				  console.log('error'); 
			    if(xhr.status==404)
			    { 
			    	
			    }
			  }
			});
		
		
	});
	
	
	
	
});

function trimPound(word) {
	
	
	var indexPound = word.search('#');
	
	console.log('---->' + word.substr(0,indexPound));
	
	var newWord = word.substr(0,indexPound);
	
	return newWord;
	
	
}
	
	