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
import os

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

def create_pop_stats(pop_1k_file, pop_gnomad_file, population):
	bcf_stats_1k_pop = wrapper.get_stats_with_bins(0.0,1.0, 0.05, pop_1k_file)
	with open(OUTPUT_BCFTOOLS+"bcf_stats_1k_{}".format(population), 'w') as f:
		f.write(bcf_stats_1k_pop)
	bcf_stats_gnomad_pop = wrapper.get_stats_with_bins(0.0,1.0, 0.05, pop_gnomad_file)
	with open(OUTPUT_BCFTOOLS+"bcf_stats_gnomad_{}".format(population), 'w') as f:
		f.write(bcf_stats_gnomad_pop)

def plot_af_stats_comparison(population, output_file, maf=False):
	with open(OUTPUT_BCFTOOLS + "bcf_stats_1k_{}".format(population) , 'r') as f:
		bcf_stats = f.read()
		AF_1k = parser.extract_allele_frequencies(bcf_stats)
	with open(OUTPUT_BCFTOOLS + "bcf_stats_gnomad_{}".format(population), 'r') as f:
		bcf_stats = f.read()
		AF_gnomad = parser.extract_allele_frequencies(bcf_stats)
	#output.plot_allele_frequencies(AF_1k_ '1000Genomes')
	print(AF_gnomad, AF_1k)
	output.plot_allele_frequency_comparison(AF_1k, AF_gnomad, ['1000Genomes','GnomAD'], output_file, maf)
		
def subset_filtered_list(file):
	population_list = open('data/1k_phase3.panel', 'r')
	eur_list = wrapper.filter_list(population_list, 'EUR')
	eur_column = [x.split("\t")[0] for x in eur_list ]
	nonFin_list = wrapper.filter_list(eur_list, "FIN", True)
	nonFin_column = [x.split("\t")[0] for x in nonFin_list ]
	wrapper.wrap_vcf_subset(file, eur_column, "data/eur_1k")
	wrapper.wrap_vcf_subset(file, nonFin_column, "data/nonFin_1k")

def hwe_analysis(file_path, out):
	wrapper.get_hwe_count(file_path, '0.05', '0.5', out)
	kept, total = parser.get_hwe_quality(out+'.log')
	output.print_hwe_stat(kept, total)

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

# checking if the data directory exists, which is used in most of the workflows
if not os.path.exists('data'):
	os.makedirs('data')
if not os.path.exists(OUTPUT_BCFTOOLS):
	os.makedirs(OUTPUT_BCFTOOLS)
if not os.path.exists(OUTPUT_VCFTOOLS):
	os.makedirs(OUTPUT_VCFTOOLS)


if args.download:
	initial_download(args.download)

if args.summary:
	if os.path.isfile(args.summary):
		shallow_analysis(args.summary)
	else:
		print("The file {} does not exist.".format(args.summary))
		sys.exit(1)
elif args.files:
	if len(args.files) > 2:
		print("Only 2 files are allowed. You gave: {}".format(len(args.files)))
		sys.exit(1)
	else:
		for file in args.files:
			if os.path.isfile(file):
				shallow_analysis(file)
			else:
				print("The file {} does not exist.".format(file))
				sys.exit(1)
		print("Creating EUR and nonFIN-EUR Subsets...")
		subset_filtered_list(args.files[0])
		print("Subsets created!")
		print("Intersecting filtered 1k_EUR with gnomAD...")
		create_intersection(["data/eur_1k_subset_output.vcf.gz", args.files[1]], "data/isec_eur")
		print("EUR Intersection created!")
		print("Creating EUR stats...")
		create_pop_stats("data/isec_eur/0000.vcf", "data/isec_eur/0001.vcf", 'EUR')
		plot_af_stats_comparison('EUR', 'EUR_af_stats.png')
		print("Intersecting filtered 1k_nonFIN with gnomAD...")
		create_intersection(["data/nonFin_1k_subset_output.vcf.gz", args.files[1]], "data/isec_nonFin")
		print("nonFin Intersection created!")
		print("Creating nonFin stats...")
		create_pop_stats("data/isec_nonFin/0000.vcf", "data/isec_nonFin/0001.vcf", 'nonFin')
		print("Stats created!")
		print("Plotted nonFin stats! Saved as 'nonFin_af_stats.png'")
		hwe_analysis("data/isec_nonFin/0000.vcf", "nonFin_hwe")
		print("Full analysis: DONE!")