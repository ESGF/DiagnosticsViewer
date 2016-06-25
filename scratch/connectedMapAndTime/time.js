function create_multiseries_time_plot(data, plot_div_id, plot_width, plot_height) {
    var margin = {top: 20, right: 80, bottom: 30, left: 50},
        width = plot_width - margin.left - margin.right,
        height = plot_height - margin.top - margin.bottom;
 
    var bisectDate = d3.bisector(function(d){ return d.date; }).left;
    var dateOutput = d3.time.format("%b %Y");

    var x = d3.time.scale()
        .range([0, width]);
 
    var y = d3.scale.linear()
        .range([height, 0]);
 
    var color = d3.scale.category20();
 
    var xAxis = d3.svg.axis()
        .scale(x)
        .orient("bottom");
 
    var yAxis = d3.svg.axis()
        .scale(y)
        .ticks(6)
        .orient("left");
 
    var line = d3.svg.line()
        .interpolate("basis")
        .x(function(d) { return x(d.date); })
        .y(function(d) { return y(d.temperature); });
 
    var svg = d3.select(plot_div_id).append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
      .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
 
        color.domain(d3.keys(data[0]).filter(function(key) { return key !== "date"; }));
 
        var profiles = color.domain().map(function(name) {
            return {
                name: name,
                values: data.map(function(d) {
                    return {date: d.date, temperature: +d[name]};
                })
            };
        });
 
        x.domain(d3.extent(data, function(d) { return d.date; }));
 
        y.domain([
            d3.min(profiles, function(c) { return d3.min(c.values, function(v) { return v.temperature; }); }),
            d3.max(profiles, function(c) { return d3.max(c.values, function(v) { return v.temperature; }); })
        ]);
 
        svg.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + height + ")")
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
            .style("stroke", function(d) { return color(d.name); });
 
        profile.append("text")
            .datum(function(d) { return {name: d.name, value: d.values[d.values.length - 1]}; })
            .attr("transform", function(d) { return "translate(" + x(d.value.date) + "," + y(d.value.temperature) + ")"; })
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
            .attr("y2", height+(margin.bottom/2));
        focusLine.append("text")
            .attr("x", 9)
            .attr("y", height-8)
            .attr("dy", ".35em");

        svg.append("rect")
            .attr("class", "overlay")
            .attr("width", width)
            .attr("height", height)
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

        function mousemove() {
            var x0 = x.invert(d3.mouse(this)[0]),
                i = bisectDate(data, x0, 1),
                d0 = data[i - 1],
                d1 = data[i],
                d = x0 - d0.date > d1.date - x0 ? d1 : d0;

            focus1.attr("transform", "translate(" + x(d.date) + "," + y(d.spinup) + ")");
            focus1.select("text").text(d.spinup);
            focus2.attr("transform", "translate(" + x(d.date) + "," + y(d.co2) + ")");
            focus2.select("text").text(d.co2);
            focus3.attr("transform", "translate(" + x(d.date) + "," + y(d.no_co2) + ")");
            focus3.select("text").text(d.no_co2);
            focusLine.attr("transform","translate(" +x(d.date)+","+0+")");
            focusLine.select("text").text(dateOutput(d.date));
        }
}
