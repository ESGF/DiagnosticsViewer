$(document).ready(function(){

		//grab the username from the model pushed to the view
		var mapview_username = $('#mapview_username').html();
		
		//initially no query string params
		var queryStringParams = '';
		
		//assemble the query string
		var hostname = location.hostname;
		var port = location.port;
		var url = 'http://' + hostname + ':' + port + '/exploratory_analysis/datasets/' + mapview_username;
		
		

		$.ajax({
			url: url,
			global: false,
			type: 'GET',
			dataType: 'json',
			data: queryStringParams,
			success: function(data) {
				
				/*
				var datasetList = data['datasets'];
				$('#dataset_name').empty();
				for (var i=0;i<datasetList.length;i++) {
					var dataset = datasetList[i];
					$('.dropdown-dataset-menu').append('<li class="dataset_menu" id="' + dataset + '"><a href="#">' + dataset + '</a></li>');
				}
				*/
			},
			error: function( jqXHR, textStatus, errorThrown ) {
				alert('datasetList textStatus: ' + textStatus + ' errorThrown: ' + errorThrown);

				
			}
		});
		
		

	});