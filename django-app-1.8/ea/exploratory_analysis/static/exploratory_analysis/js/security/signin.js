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
	
	$('#register_toggle').click(function(){

		console.log('in register toggle');
		
	});

	$('#signin').click(function(){

		var username = $('#username').val();
        var password = $('#password').val();
		var peernode = 'esg.ccs.ornl.gov';
		
		
		var input_data = {
				'csrfmiddlewaretoken': csrftoken,
				'username':username,
				'password':password,
				'peernode':peernode
		};
		
		for(var key in input_data) {
			console.log('key: ' + key);
		}
		
		var url = 'http://' + EA.host + ':' + EA.port + '/exploratory_analysis/auth_noesgf/';
		
		$.ajax({
			  type: "POST",
			  url: url,
			  data: JSON.stringify(input_data),
			  contentType: 'application/json',
			  success: function(data)
			  { 
				  
				  console.log(data);
				  
				  if(data == 'Authenticated') {
					  console.log('Authenticated - go to the main page with the username');
					  //window.location = 'http://localhost:8081/exploratory_analysis/main/' + username;
					  window.location = 'http://' + EA.host + ':' + EA.port + '/exploratory_analysis/main/' + username;
				  } else {
					  console.log('Not authenticated - stay on page');
					  $('#auth_notice').show();
				  }
				  
			  },
			  error: function(xhr, status, error) {
				  console.log('error' + xhr); 
			    if(xhr.status==404)
			    { 
			    	
			    }
			    
			  }
			  
		});
		
		
		
		
		
		
	});
	
});