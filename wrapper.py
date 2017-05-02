#!/usr/env python3.5
# -*- coding: utf-8 -*-

import subprocess as sp
import numpy as np


__author__ = "Tobias Tilly"
__name__ = "Wrapper"

'''
 This module uses the vcftools and bcftools for generating statistics of the
 given vcf-File. Mainly the SNV-, INDEL-counts, the Ts/Tv-ratio and the allele
 frequencies (split into 20 bins).
 Besides that, the given gnomad and 1k genome vcf will be compared regarding
 the EUR and nonFIN-EUR individuals.

 ToDo:
    create docstrings for methods and module variables
    extend bcftools calls with the threads option (number of threads as config?)
 '''

# tools
PATH_BCFTOOLS = "bcftools"
PATH_VCFTOOLS = "vcftools"
PATH_SUBSET = "vcf-subset"

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


"""
    Args:
        individuals(iterable): List of individuals, one per line
        keyword(string): the word you are looking for
        reverse(boolean): if True, all lines not containing the keyword are returned
    Return:
        filtered list of individuals, containing all columns

"""
def filter_list_for_population(individuals, keyword, reverse=False):
    # ToDo: filter a given file with vcf-subset for a list of individuals
    saved = []
    for line in individuals:
        if reverse and keyword not in line:
            saved.append(line)
        elif not reverse and keyword in readline:
            saved.append(line)
    return saved


def vcf_subset(vcf_file, list):
    cmd = [PATH_SUBSET,"-c", "(" + ",".join(list) +")", vcf_file, "|", "fill-an-ac", "|", "bgzip -c", ">", "subset_output.vcf.gz"]
    process = sp.Popen(
        cmd,
        stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
    output, err = process.communicate(
        b"input data that is passed to subprocess' stdin")
    rc = process.returncode
    if rc != 0:
        output = err
    return rc, output.decode("utf-8")




def get_intersection(files, output_dir):
    """ 
        Example: get_intersection(['data/test_src/0000.vcf.gz', 'data/test_src/0002.vcf.gz'], 'data/test')
    """
    index_cmd = ['index']
    intersection_cmd = ['isec', '-n='+str(len(files))]
    # The -p option defines a prefix as well as an output directory
    output_cmd = ['-p', output_dir]
    # Index the files; bcftools needs this for a fast intersection
    for f in files:
        rc, output = execute_bcftools(index_cmd, [f])
        if rc is not 0:
            # ToDo: Errorhandling
            print(output)
    # create intersection
    rc, output = execute_bcftools(intersection_cmd, files, output_cmd)
    if rc is not 0:
            # ToDo: Errorhandling
            print(output)


""" Testing the execute_tool methods; the following part will be extended """

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
    """ 
        Example: get_stats_with_bins(0.0,1.0,0.05,'data/test/0000.vcf')
    """
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

