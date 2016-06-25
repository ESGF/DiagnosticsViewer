function create_cyclone_plot (mapdata, timedata, time_plot_div_id) {
    var mapPlotSize = {width: 720, height: 360},
        statusBarSize = {width: 720, height: 20},
        timePlotSize = {width: 720, height: 120},
        sideBarSize = {width: 120, height: (mapPlotSize.height + timePlotSize.height)};

    // layout parameters
    var margin = {top: 20, right: 80, bottom: 30, left: 50},
        timePlotWidth = timePlotSize.width - margin.left - margin.right,
        timePlotHeight = timePlotSize.height - margin.top - margin.bottom;

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
    var bisectDate = d3.bisector(function(d){ return d.date; }).left;
    var dateOutput = d3.time.format("%b %Y");

    var timePlotX = d3.time.scale()
        .range([0, timePlotWidth]);
 
    var timePlotY = d3.scale.linear()
        .range([timePlotHeight, 0]);
 
    var timePlotColor = d3.scale.category20();
 
    var xAxis = d3.svg.axis()
        .scale(timePlotX)
        .orient("bottom");
 
    var yAxis = d3.svg.axis()
        .scale(timePlotY)
        .ticks(6)
        .orient("left");

    var line = d3.svg.line()
        .interpolate("basis")
        .x(function(d) { return timePlotX(d.date); })
        .y(function(d) { return timePlotY(d.temperature); });
 
    var svg = d3.select(time_plot_div_id).append("svg")
        .attr("width", timePlotWidth + margin.left + margin.right + sideBarSize.width)
        //.attr("height", timePlotHeight + margin.top + margin.bottom)
        .attr("height", timePlotHeight + margin.top + margin.bottom + mapPlotSize.height + statusBarSize.height)
      .append("g")
        //.attr("transform", "translate(" + margin.left + "," + margin.top + ")");
        .attr("transform", "translate(" + margin.left + "," + (mapPlotSize.height + margin.top + statusBarSize.height) + ")");
 
    timePlotColor.domain(d3.keys(timedata[0]).filter(function(key) { return key !== "date"; }));

    var profiles = timePlotColor.domain().map(function(name) {
        return {
            name: name,
            values: timedata.map(function(d) {
                return {date: d.date, temperature: +d[name]};
            })
        };
    });

    timePlotX.domain(d3.extent(timedata, function(d) { return d.date; }));

    timePlotY.domain([
        d3.min(profiles, function(c) { return d3.min(c.values, function(v) { return v.temperature; }); }),
        d3.max(profiles, function(c) { return d3.max(c.values, function(v) { return v.temperature; }); })
    ]);

    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + timePlotHeight + ")")
        .call(xAxis);

    svg.append("g")
        .attr("class", "y axis")
        .call(yAxis);
      //.append("text")
        //.attr("transform", "rotate(-90)")
        //.attr("y", 6)
        //.attr("dy", ".71em")
        //.style("text-anchor", "end")
        //.text("Temperature (ºF)");

    var profile = svg.selectAll(".profile")
        .data(profiles)
      .enter().append("g")
        .attr("class", "profile");

    profile.append("path")
        .attr("class", "line")
        .attr("d", function(d) { return line(d.values); })
        .style("stroke", function(d) { return timePlotColor(d.name); });

    profile.append("text")
        .datum(function(d) { return {name: d.name, value: d.values[d.values.length - 1]}; })
        .attr("transform", function(d) { return "translate(" + timePlotX(d.value.date) + "," + timePlotY(d.value.temperature) + ")"; })
        .attr("x", 3)
        .attr("dy", ".35em")
        .text(function(d) { return d.name; });

    var focus1 = svg.append("g")
        .attr("class", "focus")
        .style("display", "none");
    focus1.append("circle")
        .attr("r", 4.5);
    focus1.append("text")
        .attr("x", 9)
        .attr("dy", ".35em");

    var focus2 = svg.append("g")
        .attr("class", "focus")
        .style("display", "none");
    focus2.append("circle")
        .attr("r", 4.5);
    focus2.append("text")
        .attr("x", 9)
        .attr("dy", ".35em");

    var focus3 = svg.append("g")
        .attr("class", "focus")
        .style("display", "none");
    focus3.append("circle")
        .attr("r", 4.5);
    focus3.append("text")
        .attr("x", 9)
        .attr("dy", ".35em");

    var focusLine = svg.append("g")
        .attr("class", "focus")
        .style("display", "none");
    focusLine.append("line")
        .attr("x1", 0)
        .attr("y1", 0)
        .attr("x2", 0)
        .attr("y2", timePlotHeight+(margin.bottom/2));
    focusLine.append("text")
        .attr("x", 9)
        .attr("y", timePlotHeight-8)
        .attr("dy", ".35em");

    svg.append("rect")
        .attr("class", "overlay")
        .attr("width", timePlotWidth)
        .attr("height", timePlotHeight)
        .on("mouseover", function() {
            focus1.style("display", null);
            focus2.style("display", null);
            focus3.style("display", null);
            focusLine.style("display", null);
        })
        .on("mouseout", function() {
            focus1.style("display", "none");
            focus2.style("display", "none");
            focus3.style("display", "none");
            focusLine.style("display", "none");
        })
        .on("mousemove", mousemove);

    /*
    var brush = d3.svg.brush()
        .x(timePlotX)
        .on("brush", brushed)

    //    svg.append("rect")
//        .attr("class", "grid-background")
//        .attr("width", timePlotWidth)
//        .attr("height", timePlotHeight);

    var gBrush = svg.append("g")
        .attr("class", "brush")
        .call(brush);

    gBrush.selectAll("rect")
        .attr("height", timePlotHeight);

    function brushed() {
        var extent0 = brush.extent(),
            extent1;

        // if dragging, preserve the width of the extent
        if (d3.event.mode === "move") {
            var d0 = d3.time.day.round(extent0[0]),
                d1 = d3.time.day.offset(d0, Math.round((extent0[1] - extent0[0]) / 864e5));
            extent1 = [d0, d1];
        }
        // otherwise, if resizing, round both dates
        else {
            extent1 = extent0.map(d3.time.day.round);

            // if empty when rounded, use floor & ceil instead
            if (extent1[0] >= extent1[1]) {
                extent1[0] = d3.time.day.floor(extent0[0]);
                extent1[1] = d3.time.day.ceil(extent0[1]);
            }
        }

        d3.select(this).call(brush.extent(extent1));
    }
    */

    function mousemove() {
        var x0 = timePlotX.invert(d3.mouse(this)[0]),
            i = bisectDate(timedata, x0, 1),
            d0 = timedata[i - 1],
            d1 = timedata[i],
            d = x0 - d0.date > d1.date - x0 ? d1 : d0;

        focus1.attr("transform", "translate(" + timePlotX(d.date) + "," + timePlotY(d.spinup) + ")");
        focus1.select("text").text(d.spinup);
        focus2.attr("transform", "translate(" + timePlotX(d.date) + "," + timePlotY(d.co2) + ")");
        focus2.select("text").text(d.co2);
        focus3.attr("transform", "translate(" + timePlotX(d.date) + "," + timePlotY(d.no_co2) + ")");
        focus3.select("text").text(d.no_co2);
        focusLine.attr("transform","translate(" + timePlotX(d.date) + "," + 0 + ")");
        focusLine.select("text").text(dateOutput(d.date));
    }

    

    // map drawing stuff ////////////////////////////
//    var svg2 = d3.select(time_plot_div_id).append("svg")
//        .attr("width", timePlotWidth + margin.left + margin.right + sideBarSize.width)
//        //.attr("height", timePlotHeight + margin.top + margin.bottom)
//        .attr("height", timePlotHeight + margin.top + margin.bottom + mapPlotSize.height + statusBarSize.height)
//      .append("g")
//        //.attr("transform", "translate(" + margin.left + "," + margin.top + ")");
//        .attr("transform", "translate(" + margin.left + "," + (mapPlotSize.height + margin.top) + ")");
 
    statusText = d3.select(time_plot_div_id).select("svg").insert("g")
        //.attr("width", statusBarSize.width)
        //.attr("height", statusBarSize.height)
        .attr("transform", "translate(" + statusBarSize.width + "," + (mapPlotSize.height+statusBarSize.height) + ")")
        .style("text-anchor", "end")
      .append("text")
        .attr("class", "title")
        .text("Status Bar Text");
      

    var dx = mapdata[0].length,
            dy = mapdata.length;

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

    var mapPlotX = d3.scale.linear()
        .domain([0, dx])
        .range([0, mapPlotSize.width]);

    var mapPlotY = d3.scale.linear()
        .domain([0, dy])
        .range([mapPlotSize.height, 0]);

    var mapPlotColor = d3.scale.linear()
        .domain([min, max])
        //.range(["white", "steelblue"]);
        .range(["hsl(62,100%,90%)", "hsl(228,30%,20%)"]);

    var tooltip = d3.select("body")
        .append("div")
        .style("position", "absolute")
        .style("z-index", "10")
        .style("visibility", "hidden")
        .text("tooltip");

 //   d3.select(time_plot_div_id)
 //       .style("width", (mapPlotSize.width + timePlotSize.width) + "px")
 //       .style("height", mapPlotSize.height + "px");

    var degreesPerCell = 360.0 / dx;

    d3.select(time_plot_div_id).append("canvas")
        .attr("width", dx)
        .attr("height", dy)
        //.style("width", mapPlotSize.width + "px")
        //.style("height", mapPlotSize.height + "px")
        .call(drawImage)
        .on("mouseover", function() {
            tooltip.style("visibility", "visible");
        })
        .on("mousemove", 
            function(){
                var row = mapdata.length - d3.mouse(this)[1];
                var col = d3.mouse(this)[0];
                //console.log("here " + d3.mouse(this) + " " +  mapdata[row][d3.mouse(this)[0]]); 
                tooltip.style("top", (event.pageY-10)+"px").style("left",(event.pageX+10)+"px");
                tooltip.text(mapdata[row][col]);
                var longitude = -180.0 + (degreesPerCell * col);
                var latitude = -90.0 + (degreesPerCell * row);
                statusText.text("[" + latitude + ", " + longitude + "] value: " + mapdata[row][d3.mouse(this)[0]]);
                //console.log("grid coordinates are row = " + row + " col = " + col);
        })
        .on("click", function() {
            var row = mapdata.length - d3.mouse(this)[1];
            var col = d3.mouse(this)[0];
            console.log("grid coordinates are row = " + row + " col = " + col);    

            var filename = "./json_grid_data/TLAI-timeseries-" + row + "-" + col + ".json";
            d3.json(filename, function(error, new_timedata) {
                var current_year = +new_timedata.start_year;
                var current_month = +new_timedata.start_month;
                var timeseries_objects = [];
                new_timedata.timeseries_data.forEach(function(d) {
                    //d.date = parseDate(d.date);
                    var obj = {};
                    obj.date = new Date(current_year, (current_month-1), 1, 0, 0, 0, 0);
                    obj.value = d;
                    timeseries_objects.push(obj);
                    console.log(obj);
                    if (current_month == 12) {
                        current_month = 1;
                        current_year++;
                    } else {
                        current_month++;
                    }
                    console.log(obj);
                });

                var profiles = timePlotColor.domain().map(function(name) {
                    return {
                        name: name,
                        values: timedata.map(function(d) {
                            return {date: d.date, temperature: +d[name]};
                        })
                    };
                });

                var svg3 = d3.select("body").transition();
                svg3.select(".line")
                    .duration(750)
                    .attr("d", profiles);
            });
        })
        .on("mouseout", function(){
            return tooltip.style("visibility", "hidden");
        });

    /*
    var svg = d3.select(map_div_id).append("svg")
        .attr("width", width)
        .attr("height", height);

    // legend stuff
    legend_offset_x = 4;
    legend_offset_y = 4;
    numTicks = 6;
    legend_block_size = 10;
    legend_top = (height - legend_offset_y) - ((numTicks + 1) * legend_block_size);
    var legend = svg.selectAll(".legend")
        .data(color.ticks(numTicks).slice(1).reverse())
      .enter().append("g")
        .attr("class", "legend")
        .attr("transform", function(d, i) {return "translate(10," + (legend_top + i * legend_block_size) + ")"; });

    legend.append("rect")
        .attr("width", legend_block_size)
        .attr("height", legend_block_size)
        .style("fill", color);

    legend.append("text")
        .attr("x", (legend_block_size + 4))
        .attr("y", legend_block_size/2)
        .attr("dy", ".35em")
        .text(String);
*/
    // Compute the pixel colors; scaled by CSS.
    function drawImage(canvas) {
        var context = canvas.node().getContext("2d"),
            image = context.createImageData(dx, dy);

        //for (var y = 0, p = -1; y < dy; ++y) {
        for (var y = dy-1, p = -1; y >= 0; --y) {
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
}
