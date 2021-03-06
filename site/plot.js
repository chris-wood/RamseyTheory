var w = 1024,
    h = 1024,
    fill = d3.scale.category20();

var vis = d3.select("#chart")
  .append("svg:svg")
    .attr("width", w)
    .attr("height", h);

var callback = function() {
}

// Load the data...
$(document).ready(function() {

  // Make the call to load the damn data... (avoid cross domain call nonsense)
  $.ajax({
    type: "GET",
    url: 'plot.json',
    dataType: "jsonp",
    jsonp: false,
    jsonpCallback: "callback",
    crossDomain : true,

    // Here is the success handler that will parse and render the graph to be displayed
    success: function (json) {
        console.log(json);
        var force = d3.layout.force()
          .charge(-30)
          .linkDistance(600)
          .nodes(json.nodes)
          .links(json.links)
          .size([w, h])
          .start();

      var link = vis.selectAll("line.link")
          .data(json.links)
          .enter().append("svg:line")
          .attr("class", "link")
          .style("stroke-width", function(d) { return Math.sqrt(d.value); })
          .attr("x1", function(d) { return d.source.x; })
          .attr("y1", function(d) { return d.source.y; })
          .attr("x2", function(d) { return d.target.x; })
          .attr("y2", function(d) { return d.target.y; });

      var node = vis.selectAll("g.node")
          .data(json.nodes)
          .enter().append("svg:g")
          .attr("class", "node")

        node.append("svg:circle")
          .attr("r", 5)
          .style("fill", function(d) { return fill(d.group); })
          .call(force.drag);

      vis.style("opacity", 1e-6)
          .transition()
          .duration(1000)
          .style("opacity", 1);

      force.on("tick", function() {
        link.attr("x1", function(d) { return d.source.x; })
            .attr("y1", function(d) { return d.source.y; })
            .attr("x2", function(d) { return d.target.x; })
            .attr("y2", function(d) { return d.target.y; });
        
        node.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });
      });
    },
    error: function (data) {
      console.log(arguments);
    }
  });
});