$(document).ready(function() {


	$body = $("body");
	
	$('#viz_button').click(function() {
	    $('#marker').remove();
		$('#map-canvas').empty();
		var parseDate = d3.time.format("%Y%m").parse;

		var variable = $("#selectV").val();
		if (variable == null) {
			if (EA.spinnerFlag) {
				$body.removeClass("loading");  
			}
			alert('please select a variable');
			return;
		}

		d3.json("http://" + EA.host + ":" + EA.port + "/exploratory_analysis/avgmap/0151/01/" + variable, function(error, mapdata) {
		//d3.json("/static/exploratory_analysis/json_grid_data/TLAI-geogrid-0151-01.json", function(error, mapdata) {

			d3.json("http://" + EA.host + ":" + EA.port + "/exploratory_analysis/timeseries/0/0/" + variable, function(error, timedata) {
				console.log(timedata);
				var current_year = +timedata.start_year;
				var current_month = +timedata.start_month;
				var timeseries_objects = [];
				timedata.timeseries_data.forEach(function(d) {
					//d.date = parseDate(d.date);
					var obj = {};
					obj.date = new Date(current_year, (current_month - 1), 1, 0, 0, 0, 0);
					obj.value = d;
					timeseries_objects.push(obj);
					//console.log(obj);
					if (current_month == 12) {
						current_month = 1;
						current_year++;
					} else {
						current_month++;
					}
				});
				create_cyclone_plot(mapdata.geo_data[0], timeseries_objects, "#map-canvas");

			});
		});

	});

});

