$(function(){
	  $("#poolInfo").load("mmm_files/data/poolString.html"); 
	});
	$(function(){
	  $("#minerlist_all").load("mmm_files/data/totals.html"); 
	});
	$(function(){
	  $("#minerlist_short").load("mmm_files/data/totalsShort.html"); 
	});
	$(function(){
	  $("#server_info").load("mmm_files/data/server_info.html"); 
	});
	$(function(){
	  $("#log_start").load("mmm_files/data/logging_start.html"); 
	});
	$(function(){
	  $("#poollist").load("mmm_files/data/pool.html"); 
	});
	$(function(){
	  $("#info_s").load("mmm_files/data/info_s.html"); 
	});
	$(function(){
	  $("#long_heading").load("mmm_files/data/long_heading.html"); 
	});
	$(function(){
	  $("#short_heading").load("mmm_files/data/short_heading.html"); 
	});
	
	//Plotting
	var curvy = false
	function curve() {
	 if (curvy) return d3.curveBasis
	 return d3.curveStepAfter
	}
	
	//Long
	var parseTime = d3.timeParse("%Y-%m-%d %H:%M:%S");
	d3.csv("mmm_files/data/hashAll.csv", type, function(error, data) {
	  if (error) throw error;
	  
	  var svg = d3.select("#long"),
		margin = {top: 20, right: 80, bottom: 30, left: 50},
		width = svg.attr("width") - margin.left - margin.right,
		height = svg.attr("height") - margin.top - margin.bottom,
		g = svg.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");
		
	  var x = d3.scaleTime().range([0, width]),
		  y = d3.scaleLinear().range([height, 0]),
		  z = d3.scaleOrdinal(d3.schemeCategory10);
		  
	  var line = d3.line()
		.curve(curve())
		.x(function(d) { return x(d.time); })
		.y(function(d) { return y(d.shares); });
		
	  var cities = data.columns.slice(1).map(function(id) {
		return {
		  id: id,
		  values: data.map(function(d) {
			return {time: d.time, shares: d[id]};
		  })
		};
	  });

	  x.domain(d3.extent(data, function(d) { return d.time; }));

	  y.domain([
		d3.min(cities, function(c) { return d3.min(c.values, function(d) { return d.shares; }); }),
		d3.max(cities, function(c) { return d3.max(c.values, function(d) { return d.shares; }); })
	  ]);

	  z.domain(cities.map(function(c) { return c.id; }));

	  g.append("g")
		  .attr("class", "axis axis--x")
		  .attr("transform", "translate(0," + height + ")")
		  .call(d3.axisBottom(x));

	  g.append("g")
		  .attr("class", "axis axis--y")
		  .call(d3.axisLeft(y))
		  .append("text")
		  .attr("transform", "rotate(-90)")
		  .attr("y", -45)
		  .attr("dy", "0.71em")
		  .attr("fill", "#000")
		  .text("Shares");

	  var ip = g.selectAll(".ip")
		.data(cities)
		.enter().append("g")
		  .attr("class", "ip");

	  ip.append("path")
		  .attr("class", "line")
		  .attr("d", function(d) { return line(d.values); })
		  .style("stroke", function(d) { return z(d.id); });

	  ip.append("text")
		  .datum(function(d) { return {id: d.id, value: d.values[d.values.length - 1]}; })
		  .attr("transform", function(d) { return "translate(" + x(d.value.time) + "," + y(d.value.shares) + ")"; })
		  .attr("x", 3)
		  .attr("dy", "0.35em")
		  .style("font", "10px sans-serif")
		  .text(function(d) { return d.id; });
	});

	d3.csv("mmm_files/data/hashShort.csv", type, function(error, data) {
	  if (error) throw error;
	  
	  var svg = d3.select("#short"),
		margin = {top: 20, right: 80, bottom: 30, left: 50},
		width = svg.attr("width") - margin.left - margin.right,
		height = svg.attr("height") - margin.top - margin.bottom,
		g = svg.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");
		
	  var x = d3.scaleTime().range([0, width]),
		  y = d3.scaleLinear().range([height, 0]),
		  z = d3.scaleOrdinal(d3.schemeCategory10);
		  
	  var line = d3.line()
		.curve(curve())
		.x(function(d) { return x(d.time); })
		.y(function(d) { return y(d.shares); });
		
	  var cities = data.columns.slice(1).map(function(id) {
		return {
		  id: id,
		  values: data.map(function(d) {
			return {time: d.time, shares: d[id]};
		  })
		};
	  });

	  x.domain(d3.extent(data, function(d) { return d.time; }));

	  y.domain([
		d3.min(cities, function(c) { return d3.min(c.values, function(d) { return d.shares; }); }),
		d3.max(cities, function(c) { return d3.max(c.values, function(d) { return d.shares; }); })
	  ]);

	  z.domain(cities.map(function(c) { return c.id; }));

	  g.append("g")
		  .attr("class", "axis axis--x")
		  .attr("transform", "translate(0," + height + ")")
		  .call(d3.axisBottom(x));

	  g.append("g")
		  .attr("class", "axis axis--y")
		  .call(d3.axisLeft(y))
		  .append("text")
		  .attr("transform", "rotate(-90)")
		  .attr("y", -45)
		  .attr("dy", "0.71em")
		  .attr("fill", "#000")
		  .text("Shares");

	  var ip = g.selectAll(".ip")
		.data(cities)
		.enter().append("g")
		  .attr("class", "ip");

	  ip.append("path")
		  .attr("class", "line")
		  .attr("d", function(d) { return line(d.values); })
		  .style("stroke", function(d) { return z(d.id); });

	  ip.append("text")
		  .datum(function(d) { return {id: d.id, value: d.values[d.values.length - 1]}; })
		  .attr("transform", function(d) { return "translate(" + x(d.value.time) + "," + y(d.value.shares) + ")"; })
		  .attr("x", 3)
		  .attr("dy", "0.35em")
		  .style("font", "10px sans-serif")
		  .text(function(d) { return d.id; });
	});

	function type(d, _, columns) {
		  d.time = parseTime(d.time);
		  for (var i = 1, n = columns.length, c; i < n; ++i) d[c = columns[i]] = +d[c];
		  return d;
	}
	function checklength(i) {
		'use strict';
		if (i < 10) {
			i = "0" + i;
		}
		return i;
	}

	var minutes, seconds, count, counter, timer;
	count = 601; //seconds
	counter = setInterval(timer, 1000);

	function timer() {
		'use strict';
		count = count - 1;
		minutes = checklength(Math.floor(count / 60));
		seconds = checklength(count - minutes * 60);
		if (count < 0) {
			clearInterval(counter);
			return;
		}
		document.getElementById("timer").innerHTML = 'Next refresh in ' + minutes + ':' + seconds + ' ';
		if (count === 0) {
			location.reload();
		}
	}