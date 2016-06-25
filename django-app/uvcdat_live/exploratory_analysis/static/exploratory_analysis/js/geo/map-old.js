function create_map_canvas(json_datafile, map_div_id, width, height) {
    //var width = 720,
    //    height = 360;

    var projection = d3.geo.equirectangular().translate([width/2, height/2]);

    mapdata = JSON.parse(json_datafile);

//    var dx = mapdata[0].length,
//            dy = mapdata.length;
    
//    d3.json(json_datafile, function(mapdata) {
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

        //console.log(json_datafile + " min="+min+" max="+max);

        //var x = d3.scale.linear

        var x = d3.scale.linear()
            .domain([0, dx])
            .range([0, width]);
        //    .range([projection([-180,0])[0], projection([180,0])[0]]);

        var y = d3.scale.linear()
            .domain([0, dy])
            .range([height, 0]);

        var color = d3.scale.linear()
            .domain([min, max])
            //.range(["white", "steelblue"]);
            .range(["hsl(62,100%,90%)", "hsl(228,30%,20%)"]);

        //var xAxis = d3.svg.axis()
        //    .scale(x)
        //    .orient("top")
        //    .ticks(18);

        //var yAxis = d3.svg.axis()
        //    .scale(y)
        //    .orient("right");

        d3.select(map_div_id)
            .style("width", width + "px")
            .style("height", height + "px");

        //d3.select("body").append("canvas")
        d3.select(map_div_id).append("canvas")
            .attr("width", dx)
            .attr("height", dy)
            .style("width", width + "px")
            .style("height", height + "px")
            .call(drawImage);

        //var svg = d3.select("body").append("svg")
        var svg = d3.select(map_div_id).append("svg")
            .attr("width", width)
            .attr("height", height);

        //svg.append("g")
        //    .attr("class", "axis")
        //    .attr("transform", "translate(0," + projection([0, -90])[1] + ")")
        //    .call(d3.svg.axis()
                    //.scale(d3.scale.linear().domain([360,0]).range([projection([-180,0])[0], projection([180, 0])[0]]))
        //            .scale(d3.scale.linear().domain([0,720]).range([projection([-180,0])[0], projection([180, 0])[0]]))
        //            .ticks(9)
        //            .orient("bottom"))
        //    .append("text")
        //        .attr("class", "label")
        //        .attr("transform","translate(" + width / 2 + ")")
        //        .attr("y", 30)
        //        .attr("dy", ".71em")
        //        .style("text-anchor", "middle")
        //        .text("Longitude");

        //svg.append("g")
        //    .attr("class", "x axis")
        //    .attr("transform", "translate(0," + height + ")")
        //    .call(xAxis);
            //.call(removeZero);

        //svg.append("g")
        //    .attr("class", "y axis")
        //    .call(yAxis);
            //.call(removeZero);

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
                        var c = d3.rgb(color(mapdata[y][x]));
                        image.data[++p] = c.r;
                        image.data[++p] = c.g;
                        image.data[++p] = c.b;
                        image.data[++p] = 255;
                    }
                }
            }

            context.putImageData(image, 0, 0);
        }

        function removeZero(axis) {
            axis.selectAll("g").filter(function(d) { return !d; }).remove();
        }
    };
        
//}
