#!/usr/env python3.5
# -*- coding: utf-8 -*-

import subprocess as sp
import numpy as np


__author__ = "Tobias Tilly"
__name__ = "Parser"

'''
 This module uses the vcftools and bcftools for generating statistics of the
 given vcf-File. Mainly the SNV-, INDEL-counts, the Ts/Tv-ratio and the allele
 frequencies (split into 20 bins).
 Besides that, the given gnomad and 1k genome vcf will be compared regarding
 the EUR and nonFIN-EUR individuals.

 ToDo:
    create docstrings for methods and module variables
 '''

# tools
PATH_BCFTOOLS = "bcftools"
PATH_VCFTOOLS = "vcftools"

def execute_vcftools(file_path, filtering=[], output_options=[]):
    cmd = [PATH_VCFTOOLS, '--gzvcf'] + file_path + filtering + output_options
    process = sp.Popen(
        cmd,
        stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
    output, err = process.communicate(
        b"input data that is passed to subprocess' stdin")
    rc = process.returncode
    if rc != 0:
        output = err
    return rc, output.decode("utf-8")


def execute_bcftools(command, file_path, options=[]):
    cmd = [PATH_BCFTOOLS] + command + options + file_path
    process = sp.Popen(
        cmd,
        stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
    output, err = process.communicate(
        b"input data that is passed to subprocess' stdin")
    rc = process.returncode
    if rc != 0:
        output = err
    return rc, output.decode("utf-8")


# Testing the execute_tool methods
# The following part will be extended

def get_bcf_stats(file_path):
    command = ['stats']
    file_path = [file_path]

    rc, output = execute_bcftools(command, file_path)
    if rc is 0:
        return output
    else:
        # ToDo: Errorhandling
        return output


def get_stats_with_bins(start, end, step, file_path):
    bins = np.arange(start, end, step)
    command = ['stats']
    options = ['--af-bins', "(" + ", ".join([str(x) for x in bins]) + ")"]
    file_path = [file_path]

    rc, output = execute_bcftools(command, file_path, options)
    if rc is 0:
        return output
    else:
        # ToDo: Errorhandling
        return output


def get_counts(file_path):
    file_path = [file_path]
    filtering = ["--counts"]
    rc, output = execute_vcftools(file_path, filtering)
    if rc is 0:
        return output
    else:
        # ToDo: Errorhandling
        return output
