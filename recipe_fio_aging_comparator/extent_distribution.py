import numpy as np
import sys, json, os,  fnmatch, subprocess
from random import randint

class Extent_distribution:
  def __init__(self, _file):
    ffh = map(lambda x: int(x),filter(lambda x: x!= '', _file.split('\n')))
    #self.bins = bins
    #self.extents = extents
    #self.blocks = blocks
    self.ID = 'ext_dist_'+str(randint(0,10000)) #hash

    self.bins = list(set(ffh))
    if len(self.bins)>1:
  	self.bins.sort()
    self.bins = map(lambda x: str(x), self.bins)
    self.extents = []
    for item in self.bins:
	self.extents.append(str(ffh.count(int(item))))

  
  def generate_histogram_script(self):
    js = 'var '
    js += self.ID+'''_histogram;\n$(document).ready(function () {'''+self.ID+'''_histogram= new Highcharts.Chart({
      chart: {zoomType: 'xy',
      width: 900,
      height: 600,
      backgroundColor: '#F2F2F2',\n renderTo: \''''+self.ID+'''_histogram\'},\ntitle: {text: \'Histogram of extent distribution\'},'''
    js += '''xAxis: [{categories: ['''
    for _bin in self.bins:
      js += '''\''''+_bin+'''\', '''
    js += '''],'''
    js += '''title: {text: 'Throughput [MB/s]'}}],
    plotOptions: {
        column: {
            groupPadding: 0,
            pointPadding: 0,
            borderWidth: 0,
            grouping: false,
            shadow: false
        }
    },
      yAxis: [{labels: { formatter: function () {return this.value;}},
      title: {text: 'Frequency'}}],
      tooltip: {shared: true},
      series: [
      {
      name: \''''      
    js += 'extents of file' + '''\',\ncolor: 'rgba(0, 0, 255, 0.50)',\n	type: 'column',\n	data: [\n'''
    for value in self.extents:
      js += str(value)+',\n'
    js += '''],visible: true,\n	tooltip: {headerFormat: '<em>Extent size {point.key}</em><br/>'}\n},\n ]});})\n'''
    return js[:-3]+self.button_histogram()

  def button_histogram(self):
    button = '''var chart = $('#container').highcharts(),
        type = 1,
        types = ['linear', 'logarithmic'],
        lineColor = 'red';

    $('#'''+self.ID+'''_histogram_button\').click(function () {'''
    button += self.ID+'''_histogram.yAxis[0].update({\n            type: types[type]\n        });'''
    button +='''\ntype += 1;\n        if (type === types.length) {\n            type = 0;\n        }\n    });\n})'''
    return button

  def make_report(self):
    report = '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">
	<html>
	<head>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/> 
	<title>recipe_fio results</title>
	<script type='text/javascript' src='http://code.jquery.com/jquery-1.9.1.js'></script>
        </head>
        <body>
	<script src="http://code.highcharts.com/highcharts.js"></script>
	<script src="http://code.highcharts.com/highcharts-more.js"></script>
	<script src="http://code.highcharts.com/modules/exporting.js"></script>
	<link rel="stylesheet" type="text/css" href="stylesheet.css">
	<br>
	<font size="3"><style>
	    table {
	    width:20%;
	    }
	    table, th, td{
	    border: 1px solid black;
	    border-collapse: collapse;
	    font-size: 14px;
	    }
	    th, td{
	    padding: 5px;
	    text-align: left;
	    }
	    table#t01 tr:nth-child(even) {
	    background-color: #eee;
	    }
	    table#t01 tr:nth-child(odd) {
	    background-color:#fff;
	    }
	    table#t01 th	{
	    background-color: white;
	    color: black;
	    }
	    </style>
	    </head>
	<DT><CENTER><STRONG>recipe_fio results on ''' + self.dev
    report += '''</CENTER> </STRONG>\n  <br>              \n  <br>'''

    report += '''<script type='text/javascript' src=\''''+self.ID+'''_histogram.js\'></script>\n'''

    report += '''<a name="'''+self.ID+'''"_ /a>\n<h3 id="summary top">Free space fragmentation</h3>\n'''
    report += '''<div class="main">\n<table>\n<tr>\n'''''
    report += '''<td><div id=\"'''+self.ID+'''_histogram\" align="center" margin: 0 auto"></div></td>\n'''
    report += '''<LI>Change between linear and logarithmic Y axis\n<br\n><button id=\"'''+self.ID+'''_histogram_button\" class="autocompare">LinY/LogY</button>\n'''
    report += '''</tr>\n</table>\n'''
    report += '''\n<br>\n<br>\n<a href="#TOC">Go back to TOC</a>\n\n'''
    return report

  def save(self):
      f = open(self.ID+'_histogram.js','w+')
      f.write(self.generate_histogram_script())
      f.close()
      #f = open('index.html','w+')
      #f.write(self.make_report())
      #f.close()


