#!/usr/env python3.5
# -*- coding: utf-8 -*-

__author__ = "Tobias Tilly"
__name__ = "Parser"

'''
 This module uses the vcftools and bcftools for generating statistics of the
 given vcf-File. Mainly the SNV-, INDEL-counts, the Ts/Tv-ratio and the allele
 frequencies (split into 20 bins).
 Besides that, the given gnomad and 1k genome vcf will be compared regarding
 the EUR and FIN individuals.
'''

# tools
BCFTOOLS_PATH = "../bcftools-1.4/"
VCFTOOLS_PATH = "vcftools"

# output-directories
BCFTOOLS_OUTPUT = "bcftools-output/"
VCFTOOLS_OUTPUT = "vcftools-output/"
