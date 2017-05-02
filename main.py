#!/usr/env python3.5
# -*- coding: utf-8 -*-

__author__ = "Tobias Tilly"
__name__ = "main"

'''
The main module holds all other modules and controls the workflow. 

ToDo:
	this could be extended for a nice CLI (with docopt)
'''

import parser
import analyzer
import output


# output-directories
OUTPUT_BCFTOOLS = "bcftools-output/"
OUTPUT_VCFTOOLS = "vcftools-output/"

# vcf.gz paths
PATH_1K_VCFGZ = "data/1k_phase3_chr22.vcf.gz"
PATH_GNOMAD_VCFGZ = "data/gnomad_chr22.vcf.gz"
PATH_1K_EUR_VCFGZ = "data/isec_EUR_Gnomad/0002.vcf"
PATH_GNOMAD_EUR_VCFGZ = "data/isec_EUR_Gnomad/0003.vcf"


def shallow_analysis():
	bcf_stats = parser.get_bcf_stats(PATH_1K_VCFGZ)
	stat_summary = analyzer.analyze_bcf_stats(bcf_stats)
	output.print_statistic_summary(stat_summary)


def create_EUR_stats():
	bcf_stats_1k_EUR = parser.get_bcf_stats(PATH_1K_EUR_VCFGZ)
	with open(OUTPUT_BCFTOOLS+"bcf_stats_1k_EUR", 'w') as f:
		f.write(bcf_stats_1k_EUR)
	bcf_stats_gnomad_EUR = parser.get_bcf_stats(PATH_GNOMAD_EUR_VCFGZ)
	with open(OUTPUT_BCFTOOLS+"bcf_stats_gnomad_EUR", 'w') as f:
		f.write(bcf_stats_gnomad_EUR)
		

create_EUR_stats()