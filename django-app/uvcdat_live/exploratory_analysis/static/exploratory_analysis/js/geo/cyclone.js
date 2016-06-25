function create_cyclone_plot(data, tdata, time_plot_div_id) {
	//d3.selectAll("button").style("display", null);

	var temp = [];
	var offset = 320;
	for (var i = 0; i < data.length; i++) {

		var vtemp = [];
		for (var j = 0; j < data[i].length; j++) {
			var data_temp = data[i][j];
			if (data_temp == "9.999999616903162e+35")
				data_temp = "-1";
			if (j + offset < data[i].length)
				vtemp[j + offset] = data_temp;
			else
				vtemp[(j + offset) - data[i].length] = data_temp;
		}
		temp[i] = vtemp;
	}

	data = temp;

	var variable = $("#selectV").val();
	if (variable == null)
		return;

	var mapdata = data;
	var timedata = tdata;
	var endyear = 0;
	var mapPlotSize = {
		width : 720,
		height : 360
	}, statusBarSize = {
		width : 720,
		height : 20
	}, timePlotSize = {
		width : 720,
		height : 120
	}, sideBarSize = {
		width : 120,
		height : (mapPlotSize.height + timePlotSize.height)
	};

	// layout parameters
	var margin = {
		top : 20,
		right : 80,
		bottom : 30,
		left : 50
	}, timePlotWidth = timePlotSize.width - margin.left - margin.right, timePlotHeight = timePlotSize.height - margin.top - margin.bottom;

	// sidebar stuff /////////////////////////////////
	/*
	var svg2 = d3.select(time_plot_div_id).append("svg")
	.attr("width", sideBarSize.width+mapPlotSize.width)
	//.attr("height", timePlotHeight + margin.top + margin.bottom)
	.attr("height", sideBarSize.height)
	.append("g")
	//.attr("transform", "translate(" + margin.left + "," + margin.top + ")");
	.attr("transform", "translate(" + mapPlotSize.width + "," + (mapPlotSize.height + margin.top) + ")");

	var title = svg2.append("g")
	.style("text-anchor", "start");
	//.attr("transform", "translate(" + 0 + "," + sideBarSize.height / 2 + ")");

	mapValueText = title.append("text")
	.attr("class", "title")
	.text("Test");

	title.append("text")
	.attr("class", "subtitle")
	.attr("dy", "1em")
	.text("Test2");
	*/

	// time plot stuff /////////////////////////////////////
	var bisectDate = d3.bisector(function(d) {
		return d.date;
	}).left;
	var dateOutput = d3.time.format("%b %Y");
	var dateOutput2 = d3.time.format("%b/%Y");
	var timePlotX = d3.time.scale().range([0, timePlotWidth]);

	var timePlotY = d3.scale.linear().range([timePlotHeight, 0]);

	var timePlotColor = d3.scale.category20();

	var xAxis = d3.svg.axis().scale(timePlotX).orient("bottom");

	var yAxis = d3.svg.axis().scale(timePlotY).ticks(6).orient("left");

	var line = d3.svg.line().interpolate("basis").x(function(d) {
		return timePlotX(d.date);
	}).y(function(d) {
		return timePlotY(d.temperature);
	});
	var svg = d3.select(time_plot_div_id).append("svg").attr("width", timePlotWidth + margin.left + margin.right + sideBarSize.width)
	//.attr("height", timePlotHeight + margin.top + margin.bottom)
	.attr("height", timePlotHeight + margin.top + margin.bottom + mapPlotSize.height + statusBarSize.height).append("g")
	//.attr("transform", "translate(" + margin.left + "," + margin.top + ")");
	.attr("transform", "translate(" + margin.left + "," + (mapPlotSize.height + margin.top + statusBarSize.height) + ")");

	timePlotColor.domain(d3.keys(timedata[0]).filter(function(key) {
		return key !== "date";
	}));
	var profiles = timePlotColor.domain().map(function(name) {
		return {
			name : name,
			values : timedata.map(function(d) {
				return {
					date : d.date,
					temperature : +d[name]
				};
			})
		};
	});

	timePlotX.domain(d3.extent(timedata, function(d) {
		return d.date;
	}));

	timePlotY.domain([d3.min(profiles, function(c) {
		return d3.min(c.values, function(v) {
			return v.temperature;
		});
	}), d3.max(profiles, function(c) {
		return d3.max(c.values, function(v) {
			return v.temperature;
		});
	})]);

	svg.append("g").attr("class", "x axis").attr("transform", "translate(0," + timePlotHeight + ")").call(xAxis);

	svg.append("g").attr("class", "y axis").call(yAxis);
	//.append("text")
	//.attr("transform", "rotate(-90)")
	//.attr("y", 6)
	//.attr("dy", ".71em")
	//.style("text-anchor", "end")
	//.text("Temperature (ºF)");

	var profile = svg.selectAll(".profile").data(profiles).enter().append("g").attr("class", "profile");

	profile.append("path").attr("class", "line").attr("d", function(d) {
		return line(d.values);
	}).style("stroke", function(d) {
		return timePlotColor(d.name);
	});

	profile.append("text").datum(function(d) {
		return {
			name : d.name,
			value : d.values[d.values.length - 1]
		};
	}).attr("transform", function(d) {
		return "translate(" + timePlotX(d.value.date) + "," + timePlotY(d.value.temperature) + ")";
	}).attr("x", 3).attr("dy", ".35em").text(function(d) {
		return d.name;
	});
	var focus1 = svg.append("g").attr("class", "focus").style("display", "none");
	focus1.append("circle").attr("r", 4.5);
	focus1.append("text").attr("x", 9).attr("dy", ".35em");

	//var focus2 = svg.append("g").attr("class", "focus").style("display", "none");
	//focus2.append("circle").attr("r", 4.5);
	//focus2.append("text").attr("x", 9).attr("dy", ".35em");

	//var focus3 = svg.append("g").attr("class", "focus").style("display", "none");
	//focus3.append("circle").attr("r", 4.5);
	//focus3.append("text").attr("x", 9).attr("dy", ".35em");

	var focusLine = svg.append("g").attr("class", "focus").style("display", "none");
	focusLine.append("line").attr("x1", 0).attr("y1", 0).attr("x2", 0).attr("y2", timePlotHeight + (margin.bottom / 2));
	focusLine.append("text").attr("x", 9).attr("y", timePlotHeight - 8).attr("dy", ".35em");

	var playLine = svg.append("g").style("display", "none").attr("stroke", "purple");
	playLine.append("line").attr("x1", 0).attr("y1", 0).attr("x2", 0).attr("y2", timePlotHeight + (margin.bottom / 2));
	playLine.append("text").attr("x", 9).attr("y", timePlotHeight - 8).attr("dy", ".35em");

	svg.append("rect").attr("class", "overlay").attr("width", timePlotWidth).attr("height", timePlotHeight).on("mouseover", function() {
		focus1.style("display", null);
		//focus2.style("display", null);
		//focus3.style("display", null);
		focusLine.style("display", null);
	}).on("mouseout", function() {
		focus1.style("display", "none");
		//focus2.style("display", "none");
		//focus3.style("display", "none");
		focusLine.style("display", "none");
	}).on("mousemove", mousemove).on("click", onclick);

	function mousemove() {
		var x0 = timePlotX.invert(d3.mouse(this)[0]), i = bisectDate(timedata, x0, 1), d0 = timedata[i - 1], d1 = timedata[i], d = x0 - d0.date > d1.date - x0 ? d1 : d0;

		focus1.attr("transform", "translate(" + timePlotX(d.date) + "," + timePlotY(d.value) + ")");
		focus1.select("text").text(d.value);
		//focus2.attr("transform", "translate(" + timePlotX(d.date) + "," + timePlotY(d.co2) + ")");
		//focus2.select("text").text(d.co2);
		//focus3.attr("transform", "translate(" + timePlotX(d.date) + "," + timePlotY(d.no_co2) + ")");
		//focus3.select("text").text(d.no_co2);
		focusLine.attr("transform", "translate(" + timePlotX(d.date) + "," + 0 + ")");
		focusLine.select("text").text(dateOutput(d.date));

	}

	function onclick() {
		var x0 = timePlotX.invert(d3.mouse(this)[0]), i = bisectDate(timedata, x0, 1), d0 = timedata[i - 1], d1 = timedata[i], d = x0 - d0.date > d1.date - x0 ? d1 : d0;
		var dformat = d3.time.format("%Y/%m");
		console.log(dformat(d.date));
		dateText.text("Feb 0151 - Apr 0151")//dateOutput(d.date));
		var filename = "http://" + EA.host + ":" + EA.port + "/exploratory_analysis/avgmap/" + dformat(d.date) + "/" + variable;
		d3.json(filename, function(error, new_mapdata) {
			mapdata = new_mapdata.geo_data;
			var mtemp = [];
			mapdata = mapdata[0];
			for (var i = 0; i < mapdata.length; i++) {

				var mvtemp = [];
				for (var j = 0; j < mapdata[i].length; j++) {
					var data_temp = mapdata[i][j];
					if (data_temp == "9.999999616903162e+35")
						data_temp = "-1";
					if (j + offset < mapdata[i].length)
						mvtemp[j + offset] = data_temp;
					else
						mvtemp[(j + offset) - mapdata[i].length] = data_temp;
				}
				mtemp[i] = mvtemp;
			}

			mapdata = mtemp;
			//d3.select("canvas").remove();
			//call(drawImage);
			d3.select(time_plot_div_id).append("canvas").attr("width", dx).attr("height", dy)

			//.style("width", mapPlotSize.width + "px")
			//.style("height", mapPlotSize.height + "px")
			.call(drawImage).on("mouseover", function() {
				tooltip.style("visibility", "visible");
			}).on("mousemove", timeplot_mousemove).on("click", timeplot_onclick).on("mouseout", function() {
				return tooltip.style("visibility", "hidden");
			});

			var color = d3.scale.linear().domain([min, max])
			//.range(["white", "steelblue"]);
			.range(["hsl(62,100%,90%)", "hsl(228,30%,20%)"]);
			var legend_offset_x = 25;
			var legend_offset_y = 15;
			var numTicks = 6;
			var legend_block_size = 10;
			var legend_top = (dy - legend_offset_y) - ((numTicks + 1) * legend_block_size);
			var legendsvg = d3.select(time_plot_div_id).append("svg").attr("width", dx).attr("height", dy).style("pointer-events", "none");

			var legend = legendsvg.selectAll(".legend").data(color.ticks(numTicks).slice(1).reverse()).enter().append("g").attr("class", "legend").attr("z", 500).attr("transform", function(d, i) {
				return "translate(10," + (legend_top + i * legend_block_size) + ")";
			});

			legend.append("rect").attr("width", legend_block_size).attr("height", legend_block_size).style("fill", color);

			legend.append("text").attr("x", (legend_block_size + 4)).attr("y", legend_block_size / 2).attr("dy", ".35em").text(String);
		});
		//d3.select("canvas").append("g").append("text").text(dateOutput(d.date));

	}


	window.play_button = function() {
		var cmonth = 1;
		var cyear = 151;
		var stop = 0;
		var step = 2;
		playLine.style("display", null);
		var interval = function(current_month, current_year) {

			//var x0 = timePlotX.invert(d3.mouse(this)[0]), i = bisectDate(timedata, x0, 1), d0 = timedata[i - 1], d1 = timedata[i], d = x0 - d0.date > d1.date - x0 ? d1 : d0;
			var dformat = d3.time.format("%Y/%m");
			var nextdate = new Date(current_year, (current_month - 1), 1, 0, 0, 0, 0);
			console.log(dformat(nextdate));
			dateText.text(dateOutput(nextdate));

			playLine.attr("transform", "translate(" + timePlotX(nextdate) + "," + 0 + ")");
			playLine.select("text").text(dateOutput(nextdate));
			var filename = "http://" + EA.host + ":" + EA.port + "/exploratory_analysis/avgmap/" + dformat(nextdate) + "/" + variable;
			//var filename = "/static/exploratory_analysis//json_grid_data/TLAI-geogrid-" + dformat(nextdate) + ".json";
			d3.json(filename, function(error, new_mapdata) {
				mapdata = new_mapdata.geo_data;
				var mtemp = [];
				mapdata = mapdata[0];
				for (var i = 0; i < mapdata.length; i++) {

					var mvtemp = [];
					for (var j = 0; j < mapdata[i].length; j++) {
						var data_temp = mapdata[i][j];
						if (data_temp == "9.999999616903162e+35")
							data_temp = "-1";
						if (j + offset < mapdata[i].length)
							mvtemp[j + offset] = data_temp;
						else
							mvtemp[(j + offset) - mapdata[i].length] = data_temp;
					}
					mtemp[i] = mvtemp;
				}

				mapdata = mtemp;
				d3.select("canvas").remove();
				//call(drawImage);
				d3.select(time_plot_div_id).append("canvas").attr("width", dx).attr("height", dy)
				//.style("width", mapPlotSize.width + "px")
				//.style("height", mapPlotSize.height + "px")
				.call(drawImage).on("mouseover", function() {
					tooltip.style("visibility", "visible");
				}).on("mousemove", timeplot_mousemove).on("click", timeplot_onclick).on("mouseout", function() {
					return tooltip.style("visibility", "hidden");
				});

				var color = d3.scale.linear().domain([min, max])
				//.range(["white", "steelblue"]);
				.range(["hsl(62,100%,90%)", "hsl(228,30%,20%)"]);
				var legend_offset_x = 25;
				var legend_offset_y = 15;
				var numTicks = 6;
				var legend_block_size = 10;
				var legend_top = (dy - legend_offset_y) - ((numTicks + 1) * legend_block_size);
				var legendsvg = d3.select(time_plot_div_id).append("svg").attr("width", dx).attr("height", dy).style("pointer-events", "none");

				var legend = legendsvg.selectAll(".legend").data(color.ticks(numTicks).slice(1).reverse()).enter().append("g").attr("class", "legend").attr("z", 500).attr("transform", function(d, i) {
					return "translate(10," + (legend_top + i * legend_block_size) + ")";
				});

				legend.append("rect").attr("width", legend_block_size).attr("height", legend_block_size).style("fill", color);

				legend.append("text").attr("x", (legend_block_size + 4)).attr("y", legend_block_size / 2).attr("dy", ".35em").text(String);
				//iterate
				step++;
				if (current_month == 12) {
					current_month = 1;
					current_year++;
				} else {
					current_month++;
				}
				if (current_year == 166 || step > timedata.length) {
					current_year = 151;
					current_month = 1;
					step = 1;
				}
				if (stop != 1)
					setTimeout(interval(current_month, current_year), 10);
			});
		}
		interval(cmonth, cyear);
		window.stop_button = function() {
			//clearInterval(interval);
			stop = 1;
			playLine.style("display", "none");
		}
	}
	// map drawing stuff ////////////////////////////
	// var svg2 = d3.select(time_plot_div_id).append("svg")
	// .attr("width", timePlotWidth + margin.left + margin.right + sideBarSize.width)
	// //.attr("height", timePlotHeight + margin.top + margin.bottom)
	// .attr("height", timePlotHeight + margin.top + margin.bottom + mapPlotSize.height + statusBarSize.height)
	// .append("g")
	// //.attr("transform", "translate(" + margin.left + "," + margin.top + ")");
	// .attr("transform", "translate(" + margin.left + "," + (mapPlotSize.height + margin.top) + ")");

	statusText = d3.select(time_plot_div_id).select("svg").insert("g")
	//.attr("width", statusBarSize.width)
	//.attr("height", statusBarSize.height)
	.attr("transform", "translate(" + statusBarSize.width + "," + (mapPlotSize.height + statusBarSize.height) + ")").style("text-anchor", "end").append("text").attr("class", "title").text("Status Bar Text");
	dateText = d3.select(time_plot_div_id).select("svg").insert("g").attr("transform", "translate(" + 0 + "," + (mapPlotSize.height + statusBarSize.height) + ")").style("text-anchor", "front").append("text").attr("class", "title").text("Jan 0151");

	var dx = mapdata[0].length, dy = mapdata.length;

	var max = d3.max(mapdata, function(arr) {
		return d3.max(arr.filter(function(value) {
			return value >= 0.0;
		}));
	});
	var min = d3.min(mapdata, function(arr) {
		return d3.min(arr.filter(function(value) {
			return value >= 0.0;
		}));
	});
	var mapPlotX = d3.scale.linear().domain([0, dx]).range([0, mapPlotSize.width]);

	var mapPlotY = d3.scale.linear().domain([0, dy]).range([mapPlotSize.height, 0]);

	var mapPlotColor = d3.scale.linear().domain([min, max])
	//.range(["white", "steelblue"]);
	.range(["hsl(62,100%,90%)", "hsl(228,30%,20%)"]);

	var tooltip = d3.select("body").append("div").style("position", "absolute").style("z-index", "10").style("visibility", "hidden").text("tooltip");

	var gridmarker = d3.select("body").append("div").attr("id", "marker").style("top", "0px").style("left", "0px").style("position", "absolute").style("z-index", "10").text("o");
	
    //var gridmarker = d3.select(time_plot_div_id).append("svg").attr("width", 100).attr("height", 100).append("g").append("rect").attr("width", 100).attr("height", 100).style("fill", "black").attr("x", 100).attr("y", 50);

	// d3.select(time_plot_div_id)
	// .style("width", (mapPlotSize.width + timePlotSize.width) + "px")
	// .style("height", mapPlotSize.height + "px");

	var degreesPerCell = 360.0 / dx;

	// legend stuff

	//var svg = d3.select("body").append("svg")

	d3.select(time_plot_div_id).append("canvas").attr("width", dx).attr("height", dy)
	//.style("width", mapPlotSize.width + "px")
	//.style("height", mapPlotSize.height + "px")
	.call(drawImage).on("mouseover", function() {
		tooltip.style("visibility", "visible");
	}).on("mousemove", timeplot_mousemove).on("click", timeplot_onclick).on("mouseout", function() {
		return tooltip.style("visibility", "hidden");
	});

	var color = d3.scale.linear().domain([min, max])
	//.range(["white", "steelblue"]);
	.range(["hsl(62,100%,90%)", "hsl(228,30%,20%)"]);
	var legend_offset_x = 25;
	var legend_offset_y = 15;
	var numTicks = 6;
	var legend_block_size = 10;
	var legend_top = (dy - legend_offset_y) - ((numTicks + 1) * legend_block_size);
	var legendsvg = d3.select(time_plot_div_id).append("svg").attr("width", 450).attr("height", dy).style("pointer-events", "none");

	var legend = legendsvg.selectAll(".legend").data(color.ticks(numTicks).slice(1).reverse()).enter().append("g").attr("class", "legend").attr("z", 500).attr("transform", function(d, i) {
		return "translate(10," + (legend_top + i * legend_block_size) + ")";
	});

	legend.append("rect").attr("width", legend_block_size).attr("height", legend_block_size).style("fill", color);
	
	//legend.append("rect").attr("width", 60).attr("height", 10).style("fill", "black").attr("transform", "translate(160, -101)").style('fill-opacity', 0.35).style("stroke");

	legend.append("text").attr("x", (legend_block_size + 4)).attr("y", legend_block_size / 2).attr("dy", ".35em").text(String);
	// Compute the pixel colors; scaled by CSS.
	function drawImage(canvas) {
		var context = canvas.node().getContext("2d"), image = context.createImageData(dx, dy);
		context.clearRect(0, 0, canvas.width, canvas.height)
		//for (var y = 0, p = -1; y < dy; ++y) {
		for (var y = dy - 1, p = -1; y >= 0; --y) {
			for (var x = 0; x < dx; ++x) {
				if (mapdata[y][x] < 0.) {
					image.data[++p] = 200;
					image.data[++p] = 200;
					image.data[++p] = 210;
					image.data[++p] = 255;
				} else {
					var c = d3.rgb(mapPlotColor(mapdata[y][x]));
					image.data[++p] = c.r;
					image.data[++p] = c.g;
					image.data[++p] = c.b;
					image.data[++p] = 255;
				}
			}
		}

		context.putImageData(image, 0, 0);
	}

	function timeplot_mousemove() {
		var row = parseInt(mapdata.length - d3.mouse(this)[1]);
		var col = parseInt(d3.mouse(this)[0]);
		//console.log("here " + d3.mouse(this) + " " + mapdata[row][d3.mouse(this)[0]]);
		tooltip.style("top", (event.pageY - 10) + "px").style("left", (event.pageX + 10) + "px");
		tooltip.text(mapdata[row][col]);
		var longitude = -180.0 + (degreesPerCell * col);
		var latitude = -90.0 + (degreesPerCell * row);
		statusText.text("[" + latitude + ", " + longitude + "]"); //value: " + mapdata[row][d3.mouse(this)[0]]);
		//console.log("grid coordinates are row = " + row + " col = " + col);

		/*
		 * On click of timeseries
		 *
		 * update line path - old timedata = timeseries_objects from html
		 */
	}

	function timeplot_onclick() {
		var row = parseInt(mapdata.length - d3.mouse(this)[1]);
		var col = parseInt(d3.mouse(this)[0]);
		console.log("grid coordinates are row = " + row + " col = " + col);
		var longitude = (degreesPerCell * col);
		var latitude = (degreesPerCell * row);
		var minute_lon = longitude * 60;
		var minute_lat = latitude * 60;
		//remove previous time series plot
		d3.selectAll(".profile").remove();

		gridmarker.style("top", (event.pageY - 5) + "px").style("left", (event.pageX - 5) + "px");
		//var filename = "/static/exploratory_analysis/json_grid_data/TLAI-timeseries-" + row + "-" + col + ".json";

		var filename = "http://" + EA.host + ":" + EA.port + "/exploratory_analysis/timeseries/" + minute_lat + "/" + minute_lon + "/TLAI";

		d3.json(filename, function(error, new_timedata) {
			var current_year = +new_timedata.start_year;
			var current_month = +new_timedata.start_month;
			var timeseries_objects = [];

			new_timedata.timeseries_data.forEach(function(d) {
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
				//console.log(obj);
			});
			timedata = timeseries_objects;
			var profiles = timePlotColor.domain().map(function(name) {
				return {
					name : name,
					values : timeseries_objects.map(function(d) {
						return {
							date : d.date,
							temperature : +d[name]
						};
					})
				};
			});
			var profile = svg.selectAll(".profile").data(profiles).enter().append("g").attr("class", "profile");
			//var svg3 = d3.select("body").transition();

			//update axis
			timePlotX.domain(d3.extent(timeseries_objects, function(d) {
				return d.date;
			}));

			timePlotY.domain([d3.min(profiles, function(c) {
				return d3.min(c.values, function(v) {
					return v.temperature;
				});
			}) - 0.001, d3.max(profiles, function(c) {
				return d3.max(c.values, function(v) {
					return v.temperature;
				}) + 0.001;
			})]);
			d3.selectAll(".x").attr("transform", "translate(0," + timePlotHeight + ")").call(xAxis);

			d3.selectAll(".y").attr("class", "y axis").call(yAxis);
			//draw new
			d3.selectAll(".profile").append("path").attr("class", "line").attr("d", function(d) {
				return line(d.values);
			}).style("stroke", function(d) {
				return timePlotColor(d.name);
			});

			d3.selectAll(".profile").append("line").attr("class", "line").style("stroke", "black").style("stroke-dasharray", "10,10").attr("x1", timePlotX(timePlotX.domain()[0])).attr("x2", timePlotX(timePlotX.domain()[1])).attr("y1", timePlotY(d3.mean(profiles, function(c) {
				return d3.mean(c.values, function(v) {
					return v.temperature;
				})
			}))).attr("y2", timePlotY(d3.mean(profiles, function(c) {
				return d3.mean(c.values, function(v) {
					return v.temperature;
				})
			})));
			
			//d3.selectAll(".profile").append("rect").style("fill", "black").style("fill-opacity", 0.35).attr("width", 120).attr("height", 100).attr("transform", "translate(50, 0)");
		});
	}

}