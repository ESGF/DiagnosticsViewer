var dotcolor = "black";
var zoomedRectOpacity = 0.2;
var gridOpacity = 1;
var gridColor = "#B0B0B0";
var dotOpacity = .6;
var rectColor = "#383838";

var GlobalX = 0;
var GlobalY = 0;
var GlobalScale = 0;
var lastX = 0;
var lasttX = 0;
var lastY = 0;
var lasttY = 0;
var lastScale = 1;
var lasttScale = 1;
var offsetScale = 0;
var offsetX = 0;
var offsetY = 0;
var First = false;
var zoomedFirst = false;

var selectedArrayX = new Array();
var selectedArrayY = new Array();

var data;
var health;
setTimeout(function() {
	/*
	 var opts = {
	 lines : 12, // The number of lines to draw
	 length : 7, // The length of each line
	 width : 4, // The line thickness
	 radius : 10, // The radius of the inner circle
	 color : '#000', // #rgb or #rrggbb
	 speed : 1, // Rounds per second
	 trail : 60, // Afterglow percentage
	 shadow : false // Whether to render a shadow
	 };
	 var target = document.getElementById('spinner');
	 var spinner = new Spinner(opts).spin(target);
	 */

	d3.json("/static/exploratory_analysis/heatmap_data/data.json", function(healthd) {
		d3.text("/static/exploratory_analysis/heatmap_data/coorout.csv", "text/csv", function(csv) {
			data = d3.csv.parseRows(csv);
			health = healthd;
			var crossfields = cross(health.fields);
			var w = size * health.fields.length, h = size * health.fields.length, m = [15, 40, 20, 120];
			// Size parameters.
			var size = 80, padding = 10;
			var mode = "heat";
			// Color scale.
			var color = d3.scale.ordinal().range(["rgb(0%, 0%, 50%)", "rgb(0%, 50%, 0%)"]);
			var heatcolor = d3.scale.quantize().domain([-1, 1]).range(d3.range(17));
			// Position scales.

			var position = {};
			health.fields.forEach(function(field) {
				function value(d) {
					return d[field];
				}

				position[field] = d3.scale.linear().domain([d3.min(health.values, value), d3.max(health.values, value)]).range([(padding / 2) + 1, size - (padding / 2) - 1]);
			});

			var crossValues = cross(health.values);
			// Root panel.
			var svg = d3.select("#chart").append("svg:svg").attr("width", size * health.fields.length).attr("height", size * health.fields.length).attr("class", "BlRd").attr("pointer-events", "all")
			//.attr("transform", "translate(" + padding[3] + "," + padding[0] + ")")
			.call(d3.behavior.zoom().on("zoom", redraw)).append("svg:g");

			// One column per field.
			var column = svg.selectAll("g").data(health.fields).enter().append("svg:a").attr("transform", function(d, i) {
				return "translate(" + i * size + ",0)";
			});

			// One row per field.
			var row = column.selectAll("g").data(crossfields).enter().append("svg:g").style("class", "BlRd").attr("class", quantize).attr("x", padding / 2).attr("y", padding / 2).attr("width", size - padding).attr("graphmode", "heat").attr("height", size - padding).attr("transform", function(d, i) {
				return "translate(0," + i * size + ")";
			});

			// Y-ticks. TODO Cross the field into the tick data?
			// Frame.
			row.append("svg:rect").attr("x", padding / 2).attr("y", padding / 2).attr("width", size - padding).attr("height", size - padding).style("stroke", rectColor).style("stroke-width", 1.5).on("click", function(d, i) {
				//console.log(d.x + " " + d.i);
				gotoselected2(d.x, d.y);

			}).append('svg:title').text(function(d, i) {
				return d.x + " " + d.y
			});

			$('rect').tipsy({
				html : true,
				gravity : 's'
			});

			//.style("class", "Blues")

			//.attr("class", quantize);
			// Dot plot.
			//var dot = row.selectAll("circle")

			var txtrow = svg.selectAll("rowg").data(crossfields).enter().append("svg:g").attr("x", padding / 2).attr("y", padding / 2).attr("width", size - padding).attr("height", size - padding).attr("transform", function(d, i) {
				return "translate(0," + i * size + ")";
			});

			var tex = txtrow.filter(function(d, i) {
				return d.i == 0;
			}).append("svg:g");

			tex.append("svg:rect")

			//.attr("transform", "translate(0," + -5 + ")")
			.attr("height", size - (padding * 2)).attr("width", size - (padding * 2)).style("fill-opacity", 0.8).attr("transform", "translate(0," + 10 + ")").style("fill", "white");

			tex.append("svg:text").style("font", "5px sans-serif").attr("transform", "translate(0," + 12 + ")").each(function(d, i) {
				var splittxt = d.y.split(" ");
				var temp = "";
				var c = 0;
				var t = 0;
				while (t < splittxt.length && c < 7) {
					temp = splittxt[t];

					while ((temp.length < 11) && t < (splittxt.length - 1)) {
						var currentlength = temp.length;
						var nextlength = splittxt[t + 1].length;
						if ((currentlength + nextlength) < 14) {
							t++;
							temp = temp + " " + splittxt[t];
						} else
							break;
					}

					d3.select(this.parentNode).append("svg:text").style("font", "8px sans-serif").text(temp).attr("dy", (c * 8) + 18);

					c++;
					t++;
				}
				d3.select(this.parentNode).select("rect").attr("height", c * 9)
				// d3.select(this).text(splittxt[0]);

			});

			var txtc = svg.selectAll("colg").data(cross(health.fields)).enter().append("svg:g").attr("x", padding / 2).attr("y", padding / 2).attr("width", size - padding).attr("height", size - padding).attr("transform", function(d, i) {
				return "translate(" + i * size + ",0)";
			});

			var ctex = txtc.filter(function(d, i) {
				return d.i == 0;
			}).append("svg:g");

			ctex.append("svg:rect")

			//.attr("transform", "translate(" + -5 + ",0)")
			.attr("height", size - (padding * 2)).attr("width", size - (padding * 2)).attr("transform", "translate(10," + 0 + ")").style("fill-opacity", 0.8).style("fill", "white");

			ctex.append("svg:text").style("font", "5px sans-serif").style("text-anchor", "end").each(function(d, i) {
				var splittxt = d.y.split(" ");
				var temp = "";
				var c = 0;
				var t = 0;
				while (t < splittxt.length && c < 7) {
					temp = splittxt[t];

					while ((temp.length < 11) && t < (splittxt.length - 1)) {
						var currentlength = temp.length;
						var nextlength = splittxt[t + 1].length;
						if ((currentlength + nextlength) < 14) {
							t++;
							temp = temp + " " + splittxt[t];
						} else
							break;
					}

					d3.select(this.parentNode).append("svg:text").text(temp).style("font", "8px sans-serif").attr("dx", 12).attr("dy", (c * 8 + 8));

					c++;
					t++;
				}
				d3.select(this.parentNode).select("rect").attr("height", c * 9)
				// d3.select(this).text(splittxt[0]);

			});

			///////////////////////////////////////////////////////////////////////////////////////////////////
			//
			//   Select boxes
			//
			///////////////////////////////////////////////////////////////////////////////////////////////////

			var
			selectedX;
			var selectedY;
			d3.select("#selectX").selectAll("option").data(health.fields).enter().append("option")
			//.attr("index", function(d,i){return i;})
			.attr("value", String).text(String);

			d3.select("#selectY").selectAll("option").data(health.fields).enter().append("option").attr("value", String).text(String);

			$(function() {
				$("#selectX").multiselect().multiselectfilter();
			});
			$(function() {
				$("#selectY").multiselect().multiselectfilter();
			});

			$("#selectX").multiselect({
				multiple : false,
				header : "Select an option",
				height : "400",
				noneSelectedText : "Select an Option",
				selectedList : 1
			});

			$("#selectY").multiselect({
				multiple : false,
				header : "Select an option",
				height : "400",
				noneSelectedText : "Select an Option",
				selectedList : 1
			});

			$("#selectX").multiselect("refresh");
			$("#selectY").multiselect("refresh");

			d3.select("#selectXX").on("change", function() {
				selectedX = health.fields.indexOf(this.value);
			}).selectAll("option").data(health.fields).enter().append("option").attr("index", function(d, i) {
				return i;
			}).attr("value", String).text(String);

			d3.select("#selectYY").on("change", function() {
				selectedY = health.fields.indexOf(this.value);
			}).selectAll("option").data(health.fields).enter().append("option").attr("value", String).text(String);

			$(function() {
				$("#selectXX").multiselect().multiselectfilter();
			});

			$(function() {
				$("#selectYY").multiselect().multiselectfilter();
			});

			$("#selectXX").multiselect({
				height : "400"
			});

			$("#selectYY").multiselect({
				height : "400"
			});

			$("#selectXX").multiselect("refresh");
			$("#selectYY").multiselect("refresh");

			//spinner.stop();

			window.getfields = function() {
				return health.fields;
			}

			window.options = function() {

				CB_Open("href=htmlcontent,, html=<label for=\"selectX\">Column:</label> <select id=\"selectXX\" multiple =\"true\" size =\"14\"></select> <label for=\"selectYY\">  Row:</label> <select id=\"selectY\" multiple =\"true\" size =\"14\"> </select>  <button onclick=\"gotoselected()\">Go</button> <script type=\"text/javascript\">   d3.select(\"#selectXX\").selectAll(\"option\").data([" + health.fields + "]).enter().append(\"option\").attr(\"index\", function(d,i){return i;}).attr(\"value\", String).text(String); </script>  ");

			}

			window.reset = function() {

				var selectedArrayX = health.fields;
				var selectedArrayY = health.fields;
				svg.selectAll("g").remove();
				d3.behavior.setXyz(0, 0, 1);

				svg.attr("transform", "translate(0,0)" + "scale(1)");

				// One column per field.
				column = svg.selectAll("g").data(selectedArrayX).enter().append("svg:a").attr("transform", function(d, i) {
					return "translate(" + i * size + ",0)";
				});

				// One row per field.
				row = column.selectAll("g").data(cross(selectedArrayY)).enter().append("svg:g").style("class", "Blues").attr("class", quantize).attr("x", padding / 2).attr("y", padding / 2).attr("width", size - padding).attr("graphmode", "heat").attr("height", size - padding).attr("transform", function(d, i) {
					return "translate(0," + i * size + ")";
				});

				// Frame.
				row.append("svg:rect").attr("x", padding / 2).attr("y", padding / 2).attr("width", size - padding).attr("height", size - padding).style("stroke", rectColor).style("stroke-width", 1.5);
				//.style("class", "Blues")

				//.attr("class", quantize);

				// Dot plot.
				//var dot = row.selectAll("circle")

				txtrow = svg.selectAll("rowg").data(cross(selectedArrayY)).enter().append("svg:g").attr("x", padding / 2).attr("y", padding / 2).attr("width", size - padding).attr("height", size - padding).attr("transform", function(d, i) {
					return "translate(0," + i * size + ")";
				});

				tex = txtrow.filter(function(d, i) {
					return d.i == 0;
				}).append("svg:g");

				tex.append("svg:rect")

				//.attr("transform", "translate(0," + -5 + ")")
				.attr("height", size - (padding * 2)).attr("width", size - (padding * 2)).style("fill-opacity", 0.8).attr("transform", "translate(0," + 10 + ")").style("fill", "white");

				tex.append("svg:text").style("font", "5px sans-serif").attr("transform", "translate(0," + 12 + ")").each(function(d, i) {
					var splittxt = d.y.split(" ");
					var temp = "";
					var c = 0;
					var t = 0;
					while (t < splittxt.length && c < 7) {
						temp = splittxt[t];

						while ((temp.length < 11) && t < (splittxt.length - 1)) {
							var currentlength = temp.length;
							var nextlength = splittxt[t + 1].length;
							if ((currentlength + nextlength) < 14) {
								t++;
								temp = temp + " " + splittxt[t];
							} else
								break;
						}

						d3.select(this.parentNode).append("svg:text").style("font", "8px sans-serif").text(temp).attr("dy", (c * 8) + 18);

						c++;
						t++;
					}
					d3.select(this.parentNode).select("rect").attr("height", c * 9)
					// d3.select(this).text(splittxt[0]);

				});

				txtc = svg.selectAll("colg").data(cross(selectedArrayX)).enter().append("svg:g").attr("x", padding / 2).attr("y", padding / 2).attr("width", size - padding).attr("height", size - padding).attr("transform", function(d, i) {
					return "translate(" + i * size + ",0)";
				});

				ctex = txtc.filter(function(d, i) {
					return d.i == 0;
				}).append("svg:g");

				ctex.append("svg:rect")

				//.attr("transform", "translate(" + -5 + ",0)")
				.attr("height", size - (padding * 2)).attr("width", size - (padding * 2)).attr("transform", "translate(10," + 0 + ")").style("fill-opacity", 0.8).style("fill", "white");

				ctex.append("svg:text").style("font", "5px sans-serif").style("text-anchor", "end").each(function(d, i) {
					var splittxt = d.y.split(" ");
					var temp = "";
					var c = 0;
					var t = 0;
					while (t < splittxt.length && c < 7) {
						temp = splittxt[t];

						while ((temp.length < 11) && t < (splittxt.length - 1)) {
							var currentlength = temp.length;
							var nextlength = splittxt[t + 1].length;
							if ((currentlength + nextlength) < 14) {
								t++;
								temp = temp + " " + splittxt[t];
							} else
								break;
						}

						d3.select(this.parentNode).append("svg:text").text(temp).style("font", "8px sans-serif").attr("dx", 12).attr("dy", (c * 8 + 8));

						c++;
						t++;
					}
					d3.select(this.parentNode).select("rect").attr("height", c * 9)
					// d3.select(this).text(splittxt[0]);

				});
			}
			var jsonFile = "data.json";
			var csvFile = "coorout.csv";

			window.setCSV = function(s) {
				csvFile = s;
			}
			window.setJSON = function(s) {
				jsonFile = s;
			}

			window.load = function() {
				d3.json(jsonFile, function(healthd) {
					d3.text(csvFile, "text/csv", function(csv) {

						health = healthd;
						data = d3.csv.parseRows(csv);
						reset();

						d3.select("#selectXX").on("change", function() {
							selectedX = health.fields.indexOf(this.value);
						}).selectAll("option").data(health.fields).enter().append("option").attr("index", function(d, i) {
							return i;
						}).attr("value", String).text(String);

						d3.select("#selectYY").on("change", function() {
							selectedY = health.fields.indexOf(this.value);
						}).selectAll("option").data(health.fields).enter().append("option").attr("value", String).text(String);

						$("#selectXX").multiselect("refresh");
						$("#selectYY").multiselect("refresh");
						$("#selectX").multiselect("refresh");
						$("#selectY").multiselect("refresh");
					});
				});

			}
			window.gotoselected = function() {
				var selectedArrayX = new Array();
				var selectedArrayY = new Array();
				selectedArrayX = $("#selectX").val();
				selectedArrayY = $("#selectY").val();
				gotoselected2(selectedArrayX, selectedArrayY);
			}
			window.gotoselected2 = function(sax, say) {

				//CB_Close();
				var selectedArrayX = new Array();
				var selectedArrayY = new Array();
				selectedArrayX = [sax];
				selectedArrayY = [say];
				var countX = selectedArrayX.length;
				var countY = selectedArrayY.length;

				/*
				 var selX = document.getElementById('selectX');
				 var selY = document.getElementById('selectY');

				 var i;
				 var countX = 0;
				 for (i=0; i<selX.options.length; i++) {
				 if (selX.options[i].selected) {
				 selectedArrayX[countX] = selX.options[i].value;
				 countX++;
				 }
				 }
				 var countY = 0;
				 for (i=0; i<selY.options.length; i++) {
				 if (selY.options[i].selected) {
				 selectedArrayY[countY] = selY.options[i].value;
				 countY++;
				 }
				 }
				 */

				if (countX < 2 && countY < 2) {
					selectedX = health.fields.indexOf(selectedArrayX[0]);
					selectedY = health.fields.indexOf(selectedArrayY[0]);
					var iX = selectedX - 1;
					var iY = selectedY - 1;
					var scale = 3;

					lastX = (((selectedX - 1) * (scale * size)) * -1);
					lastY = (((selectedY - 1) * (size * scale)) * -1);
					lastScale = scale;

					if (!First) {
						if (!zoomedFirst) {
							zoomedFirst = true;
							First = true;
						}
					}
					d3.behavior.setXyz((((selectedX - 1) * (scale * size)) * -1), (((selectedY - 1) * (size * scale)) * -1), scale);

					svg.attr("transform", "translate(" + ((selectedX - 1) * (scale * size)) * -1 + "," + ((selectedY - 1) * (size * scale)) * -1 + ")" + "scale(" + scale + ")");
					ctex.attr("transform", "translate(0," + (((selectedY - 1) * (size)) * 1) + ")");

					tex.attr("transform", "translate(" + (((selectedX - 1) * (size)) * 1) + ",0)");
					if (scale < .5 && hide == false) {
						ctex.attr("display", "none");
						tex.attr("display", "none");
						hide = true;
					}
					if (scale > 1 && hide == true) {
						ctex.attr("display", null);
						tex.attr("display", null);
						hide = false;
					}
					mode = "splom";

					var regionl = row.filter(function(d, i) {
						return (d.i <= iX + 7 && d.i >= iX - 0 && i <= iY + 7 && i >= iY - 0);
					});
					var region = regionl.filter(function(d, i) {
						return d3.select(this).attr("graphmode") == "heat";
					});

					region.attr("graphmode", "splom");

					region.selectAll("rect").style("stroke", function() {
						return $(this).css("fill");
					});
					region.selectAll("rect").style("fill", "white");

					region.selectAll("line.y").data(function(d) {
						return position[d.y].ticks(5).map(position[d.y]);
					}).enter().append("svg:line").attr("class", "y").attr("x1", padding / 2).attr("x2", size - padding / 2).style("stroke", gridColor).style("stroke-width", .2).attr("y1", function(d) {
						return d;
					}).attr("y2", function(d) {
						return d;
					});

					region.selectAll("line.x").data(function(d) {
						return position[d.x].ticks(5).map(position[d.x]);
					}).enter().append("svg:line").attr("class", "x").attr("x1", function(d) {
						return d;
					}).attr("x2", function(d) {
						return d;
					}).attr("y1", padding / 2).style("stroke-width", .2).style("stroke", gridColor).attr("y2", size - padding / 2);

					region.selectAll("circle").data(cross(health.values)).enter().append("svg:circle").attr("cx", function(d) {
						return position[d.x.x](d.y[d.x.x]);
					}).attr("cy", function(d) {
						return size - position[d.x.y](d.y[d.x.y]);
					}).attr("r", .5).attr("location", function(d) {
						return d.y.locations;
					}).style("fill", dotcolor).on("click", function(d) {
						click(d.x.x + ", " + d.x.y + " " + d.y.locations);
					}).on("mouseover", function(d, i) {

						var locale = d3.select(this).attr("location");

						svg.selectAll("circle").filter(function(d) {
							return d3.select(this).attr("location") == locale;
						}).attr("r", "1.5").style("stroke", "yellow");

					}).on("mouseout", function(d, i) {
						var locale = d3.select(this).attr("location");

						svg.selectAll("circle").filter(function(d) {
							return d3.select(this).attr("location") == locale;
						}).attr("r", ".5").style("stroke", null);

					});

					$('circle').tipsy({
						html : true,
						gravity : 's'
					});

					region.selectAll("circle").style("font", "24px sans-serif").append('svg:title').text(function(d, i) {
						return "<font size=2 face=\"Helvetica\" color=white>" + d.y[d.x.y] + "<br> " + d.y[d.x.x] + " " + d.y.locations + "</font>" + "";
					});

				} else {
					function quantize(d, i) {

						return "q" + heatcolor(data[health.fields.indexOf(selectedArrayY[i])][health.fields.indexOf(selectedArrayX[d.i])]) + "-9";

					}


					svg.selectAll("g").remove();
					d3.behavior.setXyz(0, 0, 1);

					svg.attr("transform", "translate(0,0)" + "scale(1)");

					// One column per field.
					column = svg.selectAll("g").data(selectedArrayX).enter().append("svg:a").attr("transform", function(d, i) {
						return "translate(" + i * size + ",0)";
					});

					// One row per field.
					row = column.selectAll("g").data(cross(selectedArrayY)).enter().append("svg:g").style("class", "Blues").attr("class", quantize).attr("x", padding / 2).attr("y", padding / 2).attr("width", size - padding).attr("graphmode", "heat").attr("height", size - padding).attr("transform", function(d, i) {
						return "translate(0," + i * size + ")";
					}).append('svg:title').text(function(d, i) {
						return d.x + " " + d.y
					});

					// Frame.
					row.append("svg:rect").attr("x", padding / 2).attr("y", padding / 2).attr("width", size - padding).attr("height", size - padding).style("stroke", rectColor).style("stroke-width", 1.5);

					$('rect').tipsy({
						html : true,
						gravity : 's'
					});

					//.style("class", "Blues")

					//.attr("class", quantize);

					// Dot plot.
					//var dot = row.selectAll("circle")

					txtrow = svg.selectAll("rowg").data(cross(selectedArrayY)).enter().append("svg:g").attr("x", padding / 2).attr("y", padding / 2).attr("width", size - padding).attr("height", size - padding).attr("transform", function(d, i) {
						return "translate(0," + i * size + ")";
					});

					tex = txtrow.filter(function(d, i) {
						return d.i == 0;
					}).append("svg:g");

					tex.append("svg:rect")

					//.attr("transform", "translate(0," + -5 + ")")
					.attr("height", size - (padding * 2)).attr("width", size - (padding * 2)).style("fill-opacity", 0.8).attr("transform", "translate(0," + 10 + ")").style("fill", "white");

					tex.append("svg:text").style("font", "5px sans-serif").attr("transform", "translate(0," + 12 + ")").each(function(d, i) {
						var splittxt = d.y.split(" ");
						var temp = "";
						var c = 0;
						var t = 0;
						while (t < splittxt.length && c < 7) {
							temp = splittxt[t];

							while ((temp.length < 11) && t < (splittxt.length - 1)) {
								var currentlength = temp.length;
								var nextlength = splittxt[t + 1].length;
								if ((currentlength + nextlength) < 14) {
									t++;
									temp = temp + " " + splittxt[t];
								} else
									break;
							}

							d3.select(this.parentNode).append("svg:text").style("font", "8px sans-serif").text(temp).attr("dy", (c * 8) + 18);

							c++;
							t++;
						}
						d3.select(this.parentNode).select("rect").attr("height", c * 9)
						// d3.select(this).text(splittxt[0]);

					});

					txtc = svg.selectAll("colg").data(cross(selectedArrayX)).enter().append("svg:g").attr("x", padding / 2).attr("y", padding / 2).attr("width", size - padding).attr("height", size - padding).attr("transform", function(d, i) {
						return "translate(" + i * size + ",0)";
					});

					ctex = txtc.filter(function(d, i) {
						return d.i == 0;
					}).append("svg:g");

					ctex.append("svg:rect")

					//.attr("transform", "translate(" + -5 + ",0)")
					.attr("height", size - (padding * 2)).attr("width", size - (padding * 2)).attr("transform", "translate(10," + 0 + ")").style("fill-opacity", 0.8).style("fill", "white");

					ctex.append("svg:text").style("font", "5px sans-serif").style("text-anchor", "end").each(function(d, i) {
						var splittxt = d.y.split(" ");
						var temp = "";
						var c = 0;
						var t = 0;
						while (t < splittxt.length && c < 7) {
							temp = splittxt[t];

							while ((temp.length < 11) && t < (splittxt.length - 1)) {
								var currentlength = temp.length;
								var nextlength = splittxt[t + 1].length;
								if ((currentlength + nextlength) < 14) {
									t++;
									temp = temp + " " + splittxt[t];
								} else
									break;
							}

							d3.select(this.parentNode).append("svg:text").text(temp).style("font", "8px sans-serif").attr("dx", 12).attr("dy", (c * 8 + 8));

							c++;
							t++;
						}
						d3.select(this.parentNode).select("rect").attr("height", c * 9)
						// d3.select(this).text(splittxt[0]);

					});
				}

			};

			window.editview = function() {
				var selX = document.getElementById('selectXX');
				var selY = document.getElementById('selectYY');
				heatZoomTo(selX, selY);
			}

			window.heatZoomTo = function(selx, sely) {

				//CB_Close();

				var selX = selx;
				var selY = sely;
				selectedArrayX = new Array();
				selectedArrayY = new Array();
				var i;
				var countX = 0;
				for ( i = 0; i < selX.options.length; i++) {
					if (selX.options[i].selected) {
						selectedArrayX[countX] = selX.options[i].value;
						countX++;
					}
				}
				var countY = 0;
				for ( i = 0; i < selY.options.length; i++) {
					if (selY.options[i].selected) {
						selectedArrayY[countY] = selY.options[i].value;
						countY++;
					}
				}

				function quantize(d, i) {
					return "q" + heatcolor(data[health.fields.indexOf(selectedArrayY[i])][health.fields.indexOf(selectedArrayX[d.i])]) + "-9";

				}


				svg.selectAll("g").remove();
				d3.behavior.setXyz(0, 0, 1);

				svg.attr("transform", "translate(0,0)" + "scale(1)");

				// One column per field.
				column = svg.selectAll("g").data(selectedArrayX).enter().append("svg:a").attr("transform", function(d, i) {
					return "translate(" + i * size + ",0)";
				});

				// One row per field.
				row = column.selectAll("g").data(cross(selectedArrayY)).enter().append("svg:g").style("class", "Blues").attr("class", quantize).attr("x", padding / 2).attr("y", padding / 2).attr("width", size - padding).attr("graphmode", "heat").attr("height", size - padding).attr("transform", function(d, i) {
					return "translate(0," + i * size + ")";
				});

				// Y-ticks. TODO Cross the field into the tick data?

				// Frame.
				row.append("svg:rect").attr("x", padding / 2).attr("y", padding / 2).attr("width", size - padding).attr("height", size - padding).style("stroke", rectColor).style("stroke-width", 1.5).on("click", function(d, i) {
					//console.log(d.x + " " + d.i);
					gotoselected2(d.x, d.y);

				}).append('svg:title').text(function(d, i) {
					return d.x + " " + d.y
				});

				$('rect').tipsy({
					html : true,
					gravity : 's'
				});
				;
				//.style("class", "Blues")

				//.attr("class", quantize);

				// Dot plot.
				//var dot = row.selectAll("circle")

				txtrow = svg.selectAll("rowg").data(cross(selectedArrayY)).enter().append("svg:g").attr("x", padding / 2).attr("y", padding / 2).attr("width", size - padding).attr("height", size - padding).attr("transform", function(d, i) {
					return "translate(0," + i * size + ")";
				});

				tex = txtrow.filter(function(d, i) {
					return d.i == 0;
				}).append("svg:g");

				tex.append("svg:rect")

				//.attr("transform", "translate(0," + -5 + ")")
				.attr("height", size - (padding * 2)).attr("width", size - (padding * 2)).style("fill-opacity", 0.8).attr("transform", "translate(0," + 10 + ")").style("fill", "white");

				tex.append("svg:text").style("font", "5px sans-serif").attr("transform", "translate(0," + 12 + ")").each(function(d, i) {
					var splittxt = d.y.split(" ");
					var temp = "";
					var c = 0;
					var t = 0;
					while (t < splittxt.length && c < 7) {
						temp = splittxt[t];

						while ((temp.length < 11) && t < (splittxt.length - 1)) {
							var currentlength = temp.length;
							var nextlength = splittxt[t + 1].length;
							if ((currentlength + nextlength) < 14) {
								t++;
								temp = temp + " " + splittxt[t];
							} else
								break;
						}

						d3.select(this.parentNode).append("svg:text").style("font", "8px sans-serif").text(temp).attr("dy", (c * 8) + 18);

						c++;
						t++;
					}
					d3.select(this.parentNode).select("rect").attr("height", c * 9)
					// d3.select(this).text(splittxt[0]);

				});

				txtc = svg.selectAll("colg").data(cross(selectedArrayX)).enter().append("svg:g").attr("x", padding / 2).attr("y", padding / 2).attr("width", size - padding).attr("height", size - padding).attr("transform", function(d, i) {
					return "translate(" + i * size + ",0)";
				});

				ctex = txtc.filter(function(d, i) {
					return d.i == 0;
				}).append("svg:g");

				ctex.append("svg:rect")

				//.attr("transform", "translate(" + -5 + ",0)")
				.attr("height", size - (padding * 2)).attr("width", size - (padding * 2)).attr("transform", "translate(10," + 0 + ")").style("fill-opacity", 0.8).style("fill", "white");

				ctex.append("svg:text").style("font", "5px sans-serif").style("text-anchor", "end").each(function(d, i) {
					var splittxt = d.y.split(" ");
					var temp = "";
					var c = 0;
					var t = 0;
					while (t < splittxt.length && c < 7) {
						temp = splittxt[t];

						while ((temp.length < 11) && t < (splittxt.length - 1)) {
							var currentlength = temp.length;
							var nextlength = splittxt[t + 1].length;
							if ((currentlength + nextlength) < 14) {
								t++;
								temp = temp + " " + splittxt[t];
							} else
								break;
						}

						d3.select(this.parentNode).append("svg:text").text(temp).style("font", "8px sans-serif").attr("dx", 12).attr("dy", (c * 8 + 8));

						c++;
						t++;
					}
					d3.select(this.parentNode).select("rect").attr("height", c * 9)
					// d3.select(this).text(splittxt[0]);

				});

			};
			$("#mies2b").click();
			// + "<form>Comment: <input type=\"comment\" name=\"cmt\" /></form>";

			///////////////////////////////////////////////////////////////////////////////////////////////////
			//
			//    Redraw
			//
			///////////////////////////////////////////////////////////////////////////////////////////////////

			function quantize(d, i) {

				return "q" + heatcolor(data[i][d.i]) + "-9";

			}

			var hide = false;
			function redraw() {

				var translate = d3.event.translate;
				var scale = d3.event.scale;

				if (First) {
					if (zoomedFirst) {
						zoomedFirst = false;
						First = true;
						translate[0] = lastX;
						translate[1] = lastY;
						scale = lastScale;
						d3.behavior.setXyz(lastX, lastY, lastScale);
					}
				}

				var iX = translate[0] / size / scale * -1;
				var iY = translate[1] / size / scale * -1;

				if (scale < .5 && hide == false) {
					ctex.attr("display", "none");
					tex.attr("display", "none");
					hide = true;
				}
				if (scale > 1 && hide == true) {
					ctex.attr("display", null);
					tex.attr("display", null);
					hide = false;
				}

				if (scale < 3 && mode == "heat") {

					svg.attr("transform", "translate(" + translate + ")" + "scale(" + scale + ")");

					GlobalX = translate[1];
					GlobalY = translate[0];
					if (GlobalX < size)
						ctex.attr("transform", "translate(0," + (translate[1] * -1) / scale + ")");
					else
						ctex.attr("transform", "translate(0," + (size * -1) + ")");
					if (GlobalY < size)
						tex.attr("transform", "translate(" + (translate[0] * -1) / scale + ",0)");
					else
						tex.attr("transform", "translate(" + (size * -1) + ",0)");
				} else if (scale < 3 && mode == "splom") {

					var regions = row.filter(function(d, i) {
						return d3.select(this).attr("graphmode") == "splom";
					});

					regions.selectAll("rect").style("fill", function() {
						return $(this).css("stroke");
					});
					regions.selectAll("rect").style("stroke", "black");

					mode = "heat";
					svg.attr("transform", "translate(" + translate + ")" + "scale(" + scale + ")");
					regions.selectAll("circle").remove();
					regions.selectAll("line.y").remove();
					regions.selectAll("line.x").remove();
					regions.attr("graphmode", "heat");
					//row.selectAll("text")
					if (GlobalX < size)
						ctex.attr("transform", "translate(0," + (translate[1] * -1) / scale + ")");
					else
						ctex.attr("transform", "translate(0," + (size * -1) + ")");
					if (GlobalY < size)
						tex.attr("transform", "translate(" + (translate[0] * -1) / scale + ",0)");
					else
						tex.attr("transform", "translate(" + (size * -1) + ",0)");

				} else if (scale >= 3) {
					mode = "splom";
					svg.attr("transform", "translate(" + translate + ")" + "scale(" + scale + ")");

					var regionl = row.filter(function(d, i) {
						return (d.i <= iX + 5 && d.i >= iX - 0 && i <= iY + 5 && i >= iY - 0);
					});
					var region = regionl.filter(function(d, i) {
						return d3.select(this).attr("graphmode") == "heat";
					});

					region.attr("graphmode", "splom");

					region.selectAll("line.y").data(function(d) {
						return position[d.y].ticks(5).map(position[d.y]);
					}).enter().append("svg:line").attr("class", "y").attr("x1", padding / 2).attr("x2", size - padding / 2).style("stroke", gridColor).style("stroke-width", .2).style("fill-opacity", gridOpacity).attr("y1", function(d) {
						return d;
					}).attr("y2", function(d) {
						return d;
					});

					region.selectAll("rect").style("stroke", function() {
						return $(this).css("fill");
					});
					region.selectAll("rect").style("fill", "white");
					//region.selectAll("rect").style("fill-opacity", zoomedRectOpacity);

					// X-ticks. TODO Cross the field into the tick data?
					region.selectAll("line.x").data(function(d) {
						return position[d.x].ticks(5).map(position[d.x]);
					}).enter().append("svg:line").attr("class", "x").attr("x1", function(d) {
						return d;
					}).attr("x2", function(d) {
						return d;
					}).attr("y1", padding / 2).style("stroke-width", .2).style("stroke", gridColor).attr("y2", size - padding / 2);

					region.selectAll("circle").data(crossValues).enter().append("svg:circle").attr("cx", function(d) {
						return position[d.x.x](d.y[d.x.x]);
					}).attr("cy", function(d) {
						return size - position[d.x.y](d.y[d.x.y]);
					}).attr("r", .5).on("click", function(d) {
						click(d.x.x + ", " + d.x.y + " " + d.y.locations, this);
					}).attr("location", function(d) {
						return d.y.locations;
					}).style("fill", dotcolor)
					//.attr("class", quantize)

					.on("mouseover", function(d, i) {

						var locale = d3.select(this).attr("location");

						svg.selectAll("circle").filter(function(d) {
							return d3.select(this).attr("location") == locale;
						}).attr("r", "1.5").style("stroke", "yellow");

					}).on("mouseout", function(d, i) {
						var locale = d3.select(this).attr("location");

						svg.selectAll("circle").filter(function(d) {
							return d3.select(this).attr("location") == locale;
						}).attr("r", ".5").style("stroke", null);

					});

					var timer;

					$('circle').tipsy({
						html : true,
						gravity : 's',
					});

					region.selectAll("circle").style("font", "24px sans-serif").append('svg:title').text(function(d, i) {

						return "<font size=2 face=\"Helvetica\" color=white>" + d.x.y + " : " + d.y[d.x.y] + "<br> " + d.x.x + " : " + d.y[d.x.x] + "</font>";
						//+ "</font><br><b>Comments:</b><br/><TEXTAREA  name=\'filedata\' id=\'txtbox\'  ROWS=2 COLS=8 WRAP></TEXTAREA><br><button onclick=\"save()\">Submit</button>";

					});
					window.save = function(d) {
						var txt = document.getElementById('txtbox');

						alert(txt.value + " " + d);
					}
					if (GlobalX < size)
						ctex.attr("transform", "translate(0," + (translate[1] * -1) / scale + ")");
					else
						ctex.attr("transform", "translate(0," + (size * -1) + ")");
					if (GlobalY < size)
						tex.attr("transform", "translate(" + (translate[0] * -1) / scale + ",0)");
					else
						tex.attr("transform", "translate(" + (size * -1) + ",0)");

				}//end else
				else {
					if (scale < .5 && hide == false)
						ctex.style("display", "none");
					if (scale > .5 && hide == true)
						ctex.styel("display", null);

					if (GlobalX < size)
						ctex.attr("transform", "translate(0," + (translate[1] * -1) / scale + ")");
					else
						ctex.attr("transform", "translate(0," + (size * -1) + ")");
					if (GlobalY < size)
						tex.attr("transform", "translate(" + (translate[0] * -1) / scale + ",0)");
					else
						tex.attr("transform", "translate(" + (size * -1) + ",0)");

				}

				function quantize(d, i) {
					return "q" + heatcolor(data[i][d.i]) + "-9";

				}

				function toTop() {
					alert("here");
					svg.attr("transform", "scale(0.125)");
				}

				function overRect() {
				}

				function outRect() {
				}

			}// end redraw()

			function click(d, dot) {
				/*
				 d3.select(dot).style("fill", "yellow");
				 fcload(d);
				 $("#mies4b").click();
				 */
			}


			window.commentframe = function(d) {
				alert(d);
			}
			function clickb(d) {
				/*
				 CB_Open("href=htmlcontent,, html=<!-- Google Conversation Element Code --><iframe frameborder=\"0\" marginwidth=\"0\" marginheight=\"0\" border=\"0\" style=\"border:0;margin:0;width:250px;height:440px;\" src=\"http://www.google.com/friendconnect/discuss?scope=site&topic=" + d + "\" scrolling=\"no\" allowtransparency=\"true\"></iframe>");
				 this.attr("fill", "red");
				 */
			}

			function quantize(d, i) {
				return "q" + heatcolor(data[i][d.i]) + "-9";

			}

		});
	});
	function startUpload() {
		document.getElementById('f1_upload_process').style.visibility = 'visible';
		return true;
	}

	function stopUpload(success) {
		var result = '';
		if (success == 1) {
			document.getElementById('result').innerHTML = '<span class="msg">The file was uploaded successfully!<\/span><br/><br/>';
		} else {
			document.getElementById('result').innerHTML = '<span class="emsg">There was an error during file upload!<\/span><br/><br/>';
		}
		document.getElementById('f1_upload_process').style.visibility = 'hidden';
		return true;
	}

}, 0);
