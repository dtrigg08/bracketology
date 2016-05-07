# Bracketology

This project uses d3.js and python to create a bracket.  The motivation was March Madness, but it can be used elsewhere.

## Installation

###Ipython Notebook
To run ipython notebook portion of this project go to [http://nbviewer.jupyter.org/github/dtrigg08/bracketology/blob/master/bracketworks.ipynb]. 
OR
download the ipython notebook file.  Open a console/terminal from the location of the file.  Type ipython notebook. It should open up a browser with the code in it.

###Python Code
The python code takes a series of brackets and outputs an HTML file with D3.js to make a bracket visual.  Just open the HTML file to view the results.  You can use the bracket class by importing brackethelper and calling bracketmaker(anarray) where anarray is an array of numpy arrays such that [ nparray([team1, team2, team3, team4...]), nparray([winnerof1&2, winnerof3&4..]), ... , nparray([winner])].





