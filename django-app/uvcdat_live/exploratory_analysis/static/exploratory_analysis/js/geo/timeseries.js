var parseDate = d3.time.format("%Y%m").parse;

var timedata;
/*
$(document).ready(function(){
	
	$('#viz_button').click(function() {

			console.log('dataset id: ' + $('span#dataset_name').html());
			console.log('variable id: ' + $('span#variable_name').html());
			console.log('time id: ' + $('span#time_name').html());
			
			
			var variable_id = $('span#variable_name').html();
			
			if(variable_id == '' || variable_id == ' ' || variable_id == 'undefined') {
				variable_id = 'AR';
			}
			
			var queryString = '';
			
			
			//assemble the query string
			var hostname = location.hostname;
			var port = location.port;
			var url = 'http://' + hostname + ':' + port + '/exploratory_analysis/timeseries?variable=' + variable_id;
			
			
			
			$.ajax({
				url: url,
				global: false,
				type: 'GET',
				dataType: 'json',
				data: queryString,
				success: function(data) {
					
					
					var timedata = JSON.parse(data);
					
					timedata.forEach(function(d) {
                        d.date = parseDate(d.date);
                        console.log('d ' + d.date);
                    });
					
					
					create_multiseries_time_plot(timedata, "#map_plot_canvas1", 720, 150);
					
					
				},
				error: function( jqXHR, textStatus, errorThrown ) {
					alert('timeseries textStatus: ' + textStatus + ' errorThrown: ' + errorThrown);
					
				}
			});
			
			
		});

});
*/
