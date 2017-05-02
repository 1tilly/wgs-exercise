#!/usr/env python3.5
# -*- coding: utf-8 -*-

__author__ = "Tobias Tilly"
__name__ = "Output"

'''
The output module works with the structures created by the analyzer. It will
plot the statistics and write human readable output files, if necessary.
If the time allows it, error handling will happen here as well.
'''

import matplotlib.pyplot as plt

HUMAN_READABLE = {
	'sample_count': 'Number of samples',
	'record_count': 'Number of records',
	'snp_count': 'Number of SNPs',
	'indel_count': 'Number of INDELs',
	'tstv': 'Ts/Tv ratio',
	'tstv_1st_alt': 'Ts/TV ratio of the 1st ALT',
}


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
		output += "{}:\t{}\n".format(HUMAN_READABLE[k], stat_dict[k].rstrip())
	print(output)


def plot_variant_frequencies(stats):
	datapoints = []
	for line in stats:
		line = line.split('\t')
		# ToDo: check if number of SNPs is optimal variable for plotting
		datapoints.append((line[2], line[3]))
	# ToDo: change axis-label, color etc
	plt.plot(datapoints)
	plt.show()


def plot_minor_allele_frequencies(stats):
	pass
