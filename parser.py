#!/usr/env python3.5
# -*- coding: utf-8 -*-

__author__ = "Tobias Tilly"
__name__ = "Analyzer"


'''
After the parser module is finished with its work, the analyzer will follow.
The analyzer reads the statistics and transforms them into
usable structures and extract hopefully further statistics and correlations.
Afterwards the output module plots the data and creates a human readable
output.
'''


""" Parses the bcftools stats output for a statistic summary. Iterates over each
	 	line and breaks the iteration if a specific line is reached (at the moment: 
	 	"# QUAL")
		Args: 
			bcf_stats_output (iterable, e.g.: string or file): 
                the output of the bcftools stats command
		returns:
			dictionary of statistics, holding the filename, sample_count, 
				record_count, snp_count and indel_count. 
        ToDo:
            get the filename from the stats_output
            the bcftools stats are multiple csvs in one file, would be nice 
            to parse them accordingly
            maybe split into multiple methods
""" 
def analyze_bcf_stats(bcf_stats_output):
    stat_dict = {"filename":"HereShouldBeTheFilename"}
    for line in bcf_stats_output.split('\n'):
        if "SN" in line[0:4]:    
            if "number of samples" in line:
                stat_dict['sample_count'] = line.split("\t")[-1]
            elif "number of records" in line:
                stat_dict['record_count'] = line.split("\t")[-1]
            elif "number of SNPs" in line:
                stat_dict['snp_count'] = line.split("\t")[-1]
            elif "number of indels" in line:
                stat_dict['indel_count'] = line.split("\t")[-1]
        elif "TSTV" in line[0:4]:
            split_line = line.split("\t")
            stat_dict['tstv'] = split_line[4]
            stat_dict['tstv_1st_alt'] = split_line[7]
        elif "AF" in line[0:2]:
            #ToDo: check what to do with the 20 (or more) bins maybe plot them?
            pass   
        elif "# QUAL" in line[0:6]:
            break 

    return stat_dict
