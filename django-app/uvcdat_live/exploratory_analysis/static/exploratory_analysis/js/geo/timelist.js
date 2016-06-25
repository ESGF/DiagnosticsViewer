/*
  
 $(document).ready(function(){
	
		$('.dropdown-time-menu').on('click','a',function() {

			$('#time_name').empty();
			$('#time_name').append(this.innerHTML);
			
		});
	
		$('.dropdown-variable-menu').on('click','a',function() {
			
			
			var queryString = '';
			
			
			//assemble the query string
			var hostname = location.hostname;
			var port = location.port;
			var url = 'http://' + hostname + ':' + port + '/exploratory_analysis/times/' + this.innerHTML;
			
			
			
			//See menuhelper/times.py for implementation
			$.ajax({
				url: url,
				global: false,
				type: 'GET',
				dataType: 'json',
				data: queryString,
				success: function(data) {
					
					var timeList = data['times'];
					$('.dropdown-time-menu').empty();
					
					console.log(timeList);
					for (var i=0;i<timeList.length;i++) {
						var time = timeList[i];
						console.log('time: ' + time);
						$('.dropdown-time-menu').append('<li class="time_menu" id="' + time + '"><a href="#">' + time + '</a></li>');
					}
					
					$('#dropdown-time-container').show();

					
				},
				error: function( jqXHR, textStatus, errorThrown ) {
					alert('times textStatus: ' + textStatus + ' errorThrown: ' + errorThrown);
					
				}
			});

			$('#variable_name').empty();
			$('#variable_name').append(this.innerHTML);
			
		});
});
*/
		