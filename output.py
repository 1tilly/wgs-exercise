#!/usr/env python3.5
# -*- coding: utf-8 -*-

__author__ = "Tobias Tilly"
__name__ = "Output"

'''
The output module works with the structures created by the analyzer. It will
plot the statistics and write human readable output files, if necessary.
If the time allows it, error handling will happen here as well.
'''


""" Takes the statistic summary parsed by the parser module and print it to the
	command line.
		Args: 
			stat_dict (dictionary): 
                the parsed output of the bcftools stats command
		returns:
			n/a
        ToDo:
            How to represent the allele frequencies with 20 or more bins
""" 
def print_statistic_summary(stat_dict):
	v = stat_dict.pop('filename')
	output = "Statistic summary for {}: \n".format(v)
	for k in stat_dict:
		output += "{}\t{}\n".format(k, stat_dict[k].rstrip())
	print(output)