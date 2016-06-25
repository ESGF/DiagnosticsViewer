This simple line chart is constructed from a TSV file storing the closing value of AAPL stock over the last few years. The chart employs [conventional margins](http://bl.ocks.org/3019563) and a number of D3 features:

* [d3.tsv](https://github.com/mbostock/d3/wiki/CSV) - load and parse data
* [d3.time.format](https://github.com/mbostock/d3/wiki/Time-Formatting) - parse dates
* [d3.time.scale](https://github.com/mbostock/d3/wiki/Time-Scales) - *x*-position encoding
* [d3.scale.linear](https://github.com/mbostock/d3/wiki/Quantitative-Scales) - *y*-position encoding
* [d3.extent](https://github.com/mbostock/d3/wiki/Arrays#wiki-d3_extent) - compute domains
* [d3.svg.axis](https://github.com/mbostock/d3/wiki/SVG-Axes) - display axes
* [d3.svg.line](https://github.com/mbostock/d3/wiki/SVG-Shapes#wiki-line) - display line shape