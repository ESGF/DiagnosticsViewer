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
	
	$('#cancel_register').click(function(){

		  $('#register').html('Register');
		  $('#registration_form').hide();
		
	});

	$('#register').click(function(){

			
			if(this.innerHTML == 'Register') {
				this.innerHTML = 'Save';
				$('#registration_form').show('slow');
				
			} else {
				
				
				
		        var register_username = $('#register_username').val();
		        var register_password = $('#register_password').val();
		        var register_email = $('#register_email').val();
				
				
				var input_data = {
						'csrfmiddlewaretoken': csrftoken,
						'register_username':register_username,
						'register_password':register_password,
						'register_email':register_email
				}
				
				
				//var url = 'http://localhost:8081/exploratory_analysis/register/';
				var url = 'http://' + EA.host + ':' + EA.port + '/exploratory_analysis/register/';
				
				console.log('url--->' + url);
				
				$.ajax({
					  type: "POST",
					  url: url,
					  data: input_data,
					  success: function(data)
					  { 
						  console.log('success ' + data);
						  if(data == "Duplicate") {
							  $('#registration_form').append('<div style="color:red">Username already exists.  Please try another username</div>')
						  } else {
							  this.innerHTML = 'Register';
							  $('#registration_form').hide();
						  }
						  
					  },
					  error: function(xhr, status, error) {
						  console.log('error'); 
					      if(xhr.status==404)
					      { 
					      }
					  }
				});
				
				/**/
				
				
			}
			
			
		});
	
	
});