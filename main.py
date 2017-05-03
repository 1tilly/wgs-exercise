#!/usr/env python3.5
# -*- coding: utf-8 -*-

__author__ = "Tobias Tilly"
__name__ = "main"

'''
The main module holds all other modules and controls the workflow. 

ToDo:
	this could be extended for a nice CLI (with docopt)
'''

import argparse
import sys

import wrapper
import parser
import output
import downloader

# output-directories
OUTPUT_BCFTOOLS = "bcftools-output/"
OUTPUT_VCFTOOLS = "vcftools-output/"

def shallow_analysis(file_path):
    bcf_stats = wrapper.get_bcf_stats(file_path)
    stat_summary = parser.analyze_bcf_stats(bcf_stats, file_path)
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
	#output.plot_allele_frequencies(EUR_1k_af, '1000Genomes')
	output.plot_allele_frequency_comparison(EUR_1k_af, EUR_gnomad_af, ['1000Genomes','GnomAD'])
		
def subset_filtered_list(file):
	population_list = open('data/1k_phase3.panel', 'r')
	eur_list = wrapper.filter_list(population_list, 'EUR')
	eur_column = [x.split("\t")[0] for x in eur_list ]
	nonFin_list = wrapper.filter_list(eur_list, "FIN", True)
	nonFin_column = [x.split("\t")[0] for x in nonFin_list ]
	wrapper.wrap_vcf_subset(file, eur_column, "data/eur_1k")
	wrapper.wrap_vcf_subset(file, nonFin_column, "data/nonFin_1k")

def initial_download(chromosome):
	downloader.download_1k(chromosome)
	downloader.download_1k_panel()
	downloader.download_gnomad(chromosome)



arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('--download', 
	help='starts downloading the 1k and gnomad files for the given chromosome')
arg_parser.add_argument('--files', nargs='+', help='takes 2 files for the full analysis(first 1k, then gnomad)')
arg_parser.add_argument('--summary', help='takes one file for a statistic summary')

args = arg_parser.parse_args()

if args.download:
	initial_download(args.download)

if args.summary:
	shallow_analysis(args.summary)
elif args.files:
	if len(args.files) > 2:
		print("Only 2 files are allowed. You gave: {}".format(len(args.files)))
		sys.exit(1)
	else:
		for file in args.files:
			shallow_analysis(file)
		print("Creating EUR and nonFIN-EUR Subsets...")
		subset_filtered_list(args.files[0])
		print("Subsets created!")
		print("Intersecting filtered 1k_EUR with gnomAD...")
		create_intersection(["data/eur_1k_subset_output.vcf.gz", args.files[1]], "data/isec_eur")
		print("EUR Intersection created!")
		print("Creating EUR stats...")
		create_EUR_stats("data/isec_eur/0002.vcf", "data/isec_eur/0003.vcf")
		plot_af_stats()