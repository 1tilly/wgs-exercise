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
		output += "\t{}:\t{}\n".format(HUMAN_READABLE[k], stat_dict[k].rstrip())
	print(output)


def plot_allele_frequencies(af_stats, legend, output, maf=False):
	af_bins = []
	n_of_snps = []
	n_of_indels = []
	for line in af_stats:
		line = line.split('\t')
		# collect data if maf is True and af is <= 0.5 or maf is False
		if not(maf and line[2] > 0.5):
			af_bins.append(line[2])
			n_of_snps.append(line[3])
			n_of_indels.append(line[6])
		else:
			break

	fig = plt.figure()
	plot1 = fig.add_subplot(211)
	plot1.set_title('SNPs per allele frequency')
	plot1.semilogy(af_bins, n_of_snps, marker='D', label=legend)
	plot1.set_ylabel('Number of SNPs')
	plot1.set_xlabel('Allele frequencies')
	plot1.legend()
	plot2 = fig.add_subplot(212)
	plot2.set_title('INDELs per allele frequency')
	plot2.semilogy(af_bins, n_of_indels, marker='D', label=legend)
	plot2.set_ylabel('Number of INDELs')
	plot2.set_xlabel('Allele frequencies')
	plot2.legend()
	if output is not '':
		plt.savefig(output)
	else:
		plt.show()


def plot_allele_frequency_comparison(stats1, stats2, legend, output, maf=False):
	af_bins1 = []
	n_of_snps1 = []
	n_of_indels1 = []
	af_bins2 = []
	n_of_snps2 = []
	n_of_indels2 = []
	for line in stats1:
		line = line.split('\t')
		# collect data if maf is True and af is <= 0.5 or maf is False
		if not(maf and float(line[2]) > 0.5):
			af_bins1.append(line[2])
			n_of_snps1.append(line[3])
			n_of_indels1.append(line[6])
		else:
			break

	for line in stats2:
		line = line.split('\t')
		# collect data if maf is True and af is <= 0.5 or maf is False
		if not(maf and float(line[2]) > 0.5):
			af_bins2.append(line[2])
			n_of_snps2.append(line[3])
			n_of_indels2.append(line[6])
		else:
			break

	fig = plt.figure()
	plot1 = fig.add_subplot(211)
	plot1.set_title('SNPs per allele frequency')
	plot1.semilogy(af_bins1, n_of_snps1, marker='D', color='red', label=legend[0])
	plot1.semilogy(af_bins2, n_of_snps2, marker='*', color='blue', label=legend[1])
	plot1.set_ylabel('Number of SNPs')
	plot1.set_xlabel('Allele frequencies')
	plot1.legend()
	plot2 = fig.add_subplot(212)
	plot2.set_title('INDELs per allele frequency')
	plot2.semilogy(af_bins1, n_of_indels1, marker='D', color='red', label=legend[0])
	plot2.semilogy(af_bins2, n_of_indels2, marker='*', color='blue', label=legend[1])
	plot2.set_ylabel('Number of INDELs')
	plot2.set_xlabel('Allele frequencies')
	plot2.legend()
	if output is not '':
		plt.savefig(output)
	else:
		plt.show()


def print_hwe_stat(kept, total):
	kept = int(kept)
	total = int(total)
	kept = total-kept
	print("HWE Quality:")
	print("{} out of {} Sites have a HWE below 0.05 and an MAF of 0.5".format(kept, total))
