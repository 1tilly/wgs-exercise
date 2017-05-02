#!/usr/env python3.5
# -*- coding: utf-8 -*-

__author__ = "Tobias Tilly"
__name__ = "main"

'''
The main module holds all other modules and controls the workflow. 

ToDo:
	this could be extended for a nice CLI (with docopt)
	allow generation of statistic as well as reading it from file
'''

import wrapper
import parser
import output


# output-directories
OUTPUT_BCFTOOLS = "bcftools-output/"
OUTPUT_VCFTOOLS = "vcftools-output/"

# vcf.gz paths
PATH_1K_VCFGZ = "data/1k_phase3_chr22.vcf.gz"
PATH_GNOMAD_VCFGZ = "data/gnomad_chr22.vcf.gz"
PATH_1K_EUR_VCFGZ = "data/isec_EUR_Gnomad/0002.vcf"
PATH_GNOMAD_EUR_VCFGZ = "data/isec_EUR_Gnomad/0003.vcf"


def shallow_analysis(file_path):
    bcf_stats = wrapper.get_bcf_stats(file_path)
    stat_summary = parser.analyze_bcf_stats(bcf_stats)
    output.print_statistic_summary(stat_summary)

def create_intersection(files, output_dir):
	wrapper.get_intersection(files, output_dir)

def create_EUR_stats(eur_1k_file, eur_gnomad_file):
	bcf_stats_1k_EUR = wrapper.get_stats_with_bins(0.0,1.0, 0.05, eur_1k_file)
	with open(OUTPUT_BCFTOOLS+"bcf_stats_1k_EUR", 'w') as f:
		f.write(bcf_stats_1k_EUR)
	bcf_stats_gnomad_EUR = wrapper.get_stats_with_bins(0.0,1.0, 0.05, eur_gnomad_file)
	with open(OUTPUT_BCFTOOLS+"bcf_stats_gnomad_EUR", 'w') as f:
		f.write(bcf_stats_gnomad_EUR)

def plot_af_stats():
	with open(OUTPUT_BCFTOOLS + 'bcf_stats_1k_EUR', 'r') as f:
		bcf_stats = f.read()
		EUR_1k_af = parser.extract_allele_frequencies(bcf_stats)
	with open(OUTPUT_BCFTOOLS + 'bcf_stats_gnomad_EUR', 'r') as f:
		bcf_stats = f.read()
		EUR_gnomad_af = parser.extract_allele_frequencies(bcf_stats)
	output.plot_allele_frequencies(EUR_1k_af, '1000Genomes')
	#output.plot_allele_frequency_comparison(EUR_1k_af, EUR_gnomad_af, ['1000Genomes','GnomAD'])
		
def subset_filtered_list():
	population_list = open("data/1k_all.panel", 'r')
	eur_list = wrapper.filter_list(population_list, "EUR")
	eur_column = [x.split("\t")[0] for x in eur_list ]
	nonFin_list = wrapper.filter_list(eur_list, "FIN", True)
	nonFin_column = [x.split("\t")[0] for x in nonFin_list ]
	wrapper.wrap_vcf_subset("data/1k_phase3_chr22.vcf.gz", eur_column, "eur_1k")
	wrapper.wrap_vcf_subset("data/1k_phase3_chr22.vcf.gz", nonFin_column, "nonFin_1k")



#shallow_analysis()
#plot_af_stats()

