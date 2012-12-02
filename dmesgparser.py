#!/usr/bin/env python
# -*- coding:Utf-8 -*-
#
# (c) 2009, Jean-Patrick Gelas <jpgelas@ens-lyon.fr>
#           INRIA Rhône-Alpes, LIP, ENS Lyon / Université de Lyon - UCB Lyon 1
#           20 april 2009
#
# Licensed under the terms of the GNU GPL License version 2
#
# This script parses the log file /var/log/dmesg. It shows duration of each
# entries and builds a bar graph (log scale).  This script assumes that the
# CONFIG_PRINTK_TIME kernel option has been set.

import re 		#compile
import operator 	#itemgetter 
import sys		#exit
from math import log

VERSION   ="0.1a"
LOGFILE	  ="/var/log/dmesg"

TIMESTAMP =0 
DURATION  =1
TEXT 	  =2

lines=[]
lines_reduced=[]

timestamp_parser=re.compile("^\[\s*(\d+\.\d+)\](.*)") # "[  timestamp] text"

def lineparser(line):
	m=timestamp_parser.search(line)
	lines.append( (float(m.group(1)), (m.group(2).strip())) )

def reduce_lines(): 

	"""Populate lines_reduced table.
	NB : All the message with the same timestamp are stored in the same
	tuple. A tuple holds a timestamp, a duration and concatenated messages."""

	# sort first because some messages may be chronologically unordered. 
	lines.sort(key=operator.itemgetter(TIMESTAMP))

	# builds the new list
	last_timestamp = 0.0
	last_text = ""
	SEPARATOR = "$" # used to separate messages sharing the same time stamp
	for item in lines:
		if item[TIMESTAMP] == last_timestamp:
			if last_text:
				last_text += SEPARATOR + item[1]
			else:
				last_text = item[1]
		else:
			duration = item[TIMESTAMP] - last_timestamp 
			lines_reduced.append((last_timestamp, duration, last_text))
			last_timestamp = item[TIMESTAMP]
			last_text = item[1]
		


def pretty_print_lines_reduced_asciibargraph():
	offset = 15
	bar_maxsize = 70
	
	scale = "...-6........-5.......-4.......-3........-2.......-1.......0........+1"
	print '[%s] %s %s | %s' % \
	("timestp ", "<delta> ", scale, "[Times in seconds - Log scale (pwr of 10)]" )

	for index, item in enumerate(lines_reduced):
		cnum = int(((log(item[DURATION])+offset) * \
			bar_maxsize) / (log(10.0)+offset))
		if cnum < bar_maxsize:
			bar = cnum * "*" + (bar_maxsize-cnum) * "-"
		else:
			mesg_outofrange = "--- OUT OF RANGE ---"
			bar = mesg_outofrange + (bar_maxsize - len(mesg_outofrange)) * " "
        	print '[%f] %f %s | %s...' % \
		(item[TIMESTAMP], item[DURATION], bar, item[TEXT][0:50])



def main():
	try:
		logfile_hdl=file(LOGFILE, 'r')
	except:
		print "Problem opening file: %s" % LOGFILE
		sys.exit(1)
	
	# process log file 
	while 1:
		line=logfile_hdl.readline()
		if line == "": 
			break
		lineparser(line) # populate lines table
	logfile_hdl.close()
	
	reduce_lines() 
	pretty_print_lines_reduced_asciibargraph() 
	

main()


