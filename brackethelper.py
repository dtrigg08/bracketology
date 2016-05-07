import re
import numpy as np


htmlcode = '''
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">

    <title>Collapsible Tree Example</title>

    <style>

 .node circle {
   fill: #fff;
   stroke: steelblue;
   stroke-width: 3px;
 }

 .node text { font: 12px sans-serif; }

 .link {
   fill: none;
   stroke: #ccc;
   stroke-width: 2px;
 }
 
    </style>

  </head>

  <body>

<!-- load the d3.js library --> 
<script src="http://d3js.org/d3.v3.min.js"></script>
 
<script>
var treeData = {myData};

// ************** Generate the tree diagram  *****************
var margin = {top: 20, right: 120, bottom: 20, left: 120},
 width = 1960 - margin.right - margin.left,
 height = 1500 - margin.top - margin.bottom;
 
var zoom = d3.behavior.zoom()
    .scaleExtent([1, 10])
    .on("zoom", zoomed);    
    
var i = 0;

var tree = d3.layout.tree()
 .size([height, width]);

var svg = d3.select("body").append("svg")
 .attr("width", width + margin.right + margin.left)
 .attr("height", height + margin.top + margin.bottom)
 .call(d3.behavior.zoom().on("zoom", function () {
    svg.attr("transform", "translate(" + d3.event.translate + ")" + " scale(" + d3.event.scale + ")")
  }))
 .append("g")
 .attr("transform", "translate(" + margin.left + "," + margin.top + ")");


root = treeData[0];
  
update(root);

function zoomed() {
  container.attr("transform", "translate(" + d3.event.translate + ")scale(" + d3.event.scale + ")");
}
   
function update(source) {

  // Compute the new tree layout.
  var nodes = tree.nodes(root).reverse(),
   links = tree.links(nodes);

  // Normalize for fixed-depth.
  nodes.forEach(function(d) { d.y = d.depth * 180; });

  // Declare the nodes
  var node = svg.selectAll("g.node")
   .data(nodes, function(d) { return d.id || (d.id = ++i); });

  // Enter the nodes.
  var nodeEnter = node.enter().append("g")
   .attr("class", "node")
   .attr("transform", function(d) { 
    return "translate(" + d.y + "," + d.x + ")"; });

  nodeEnter.append("circle")
      .attr("r", 4.5)
      .style("fill", function(d) { return d._children ? "lightsteelblue" : "#fff"; });

  nodeEnter.append("text")
   .attr("dy", -15)
   .attr("text-anchor", "middle")
   .text(function(d) { return d.name; })
   .style("fill-opacity", 1);

  // Declare the links
  var link = svg.selectAll("path.link")
   .data(links, function(d) { return d.target.id; });

  // Enter the links.
  link.enter().insert("path", "g")
   .attr("class", "link")
   .attr("d", elbow);

function elbow(d, i) {
  return "M" + d.source.y + "," + d.source.x
	  + "H" + ((d.source.y+d.target.y) / 2)
      + "V" + d.target.x + "H" + d.target.y ;
}   
   
   
}

</script>
 
  </body>
</html>
'''

def replace_all(txt,d):
    rep = dict((re.escape('{'+k+'}'), str(v)) for k, v in d.items())
    pattern = re.compile("|".join(rep.keys()))
    return pattern.sub(lambda m: rep[re.escape(m.group(0))], txt)    
	
	
# Create a tree bracket of arbitrary size, inputs only can be 2^x.
def treeMaker(size): 
    levels = np.log(size)/np.log(2)
    if np.log(size)%np.log(2) > 0:
        size = 2 ** int(levels)
    bracket = []     
    bracket = [{"name": team+1 , "parent" : "" , "children" : ""} for team in np.arange(size)]
    bracket = level(bracket)        
    return bracket

# Take an array of tree data and recursively combine it until all matches have been done
def level(bracket):
    newbracket = []
    for loop in np.arange(0, np.size(bracket),2):
        newbracket.append( {"name": "winner" , "parent" : "" , "children" : [bracket[loop],bracket[loop+1]]})
    if np.size(newbracket)>1:
        newbracket = level(newbracket)
    return newbracket

# take an array of brackets and combine them
def combineData(arr):
    for loop1 in np.arange(1, np.size(arr)):
        for loop2 in np.arange(0, np.size(arr[loop1])):
            arr[loop1][loop2]['children'] = [arr[loop1-1][2*loop2], arr[loop1-1][2*loop2+1]]
            #print(arr[loop1][loop2])
    return arr[-1]
	
# change an array (or array of arrays) to a tree data form
def bracketmaker(bracket, html = htmlcode):
    newbracket = []
    for loop1 in bracket:
        levels = []
        for loop2 in loop1:
            levels.append( {"name": loop2 , "parent" : "" , "children" :""})
        newbracket.append(levels)	
    newbracket = combineData(newbracket) 
    d={'myData' : newbracket}
    html = replace_all(html, d)
    Html_file= open("Brackethtml.html","w")
    Html_file.write(html)
    Html_file.close()

def randwinners(bracket2015):
    #^bracket2015 is expected to be an array of arrays
    bracket = np.array([],dtype = bool)
    an_array = np.random.randint(0,2,np.size(bracket2015[-1])/2)
    for value in an_array:
        if value:
            bracket = np.append(bracket,[True, False])
        else:
            bracket = np.append(bracket,[False, True])
    bracket2015.append(bracket2015[-1][bracket.astype(bool)])
#    print(bracket2015)
    if np.size(bracket2015[-1])==1:
        print bracket2015
        return bracket2015
    else:
        return(randwinners(bracket2015))

##Example below
North = np.array(['Duke',"UNF",'San Diego St.','St. Johns','Utah','SF Austin','Georgetown','E. Wash.','SMU','UCLA',
         'Iowa St.','UAB','Iowa','Davidson','Gonzaga','N. Dak. St.'])

teams = randwinners([North])
		 
comboteams = bracketmaker(teams)
