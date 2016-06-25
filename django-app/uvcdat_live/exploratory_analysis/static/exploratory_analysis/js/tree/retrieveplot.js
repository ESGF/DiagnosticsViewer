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

	$('.figure_bookmark').click(function() {

		console.log('EA location: ' + EA.cache_location);
		console.log('EA host: ' + EA.host);
		console.log('EA port: ' + EA.port);

        var figure_bookmark_name = $(this).html();//bookmark_id;
        var figure_bookmark_datasetname = 'tropics_warming_th_q_co2';
        var figure_bookmark_realm = 'land';
        //var figure_bookmark_username = 'jfharney';
        
        var figure_bookmark_username =  $('#username_posted').html();
		
        var data = {
				'csrfmiddlewaretoken': csrftoken,
				'figure_bookmark_name' : figure_bookmark_name,
				'figure_bookmark_username' : figure_bookmark_username,
				'figure_bookmark_datasetname' : figure_bookmark_datasetname,
				'figure_bookmark_realm' : figure_bookmark_realm
		}
		
		//var url = 'http://localhost:8081/exploratory_analysis/figure_bookmarks/';
		var url = 'http://' + EA.host + ':' + EA.port + '/exploratory_analysis/figure_bookmarks/';
		
		
		
		$.ajax({
			  type: "GET",
			  url: url,
			  async: false,
			  data: data,
			  dataType: 'json',
			  success: function(data)
			  { 
				  
				  var bookmark_id = figure_bookmark_name + '.png';
				  var staticImg = data['figure_cache_url'] + '.png';
				  
				  figTitle = bookmark_id;
				  
				  
				  
				  staticImg = staticImg.replace('/Users/8xo/software/exploratory_analysis/DiagnosticsViewer/django-app/uvcdat_live/exploratory_analysis','../../..');
					
				  
				  $('#modal-title').empty();
				  $('.modal-body').empty();
				  $('#modal-title').append('<div id="' + "figtitle" + '"> ' + figTitle + '</div>');
				  
				  $('.modal-body').append('<div>' + '<img src="' + staticImg + '" style="max-width:600px;max-height:500px;display: block;display: block;margin-left: auto;margin-right: auto" />' + '</div>')
				  
				 				
				  
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
	