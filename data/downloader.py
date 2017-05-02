#!/usr/env python3.5
# -*- coding: utf-8 -*-

__author__ = "Tobias Tilly"
__name__ = "Downloader"

'''
The downloader will automate the download of gnomad and 1k genome files.
'''

import os
from urllib2 import urlopen, URLError, HTTPError


# source: http://stackoverflow.com/questions/4028697/how-do-i-download-a-zip-file-in-python-using-urllib2
def download_file(url):
    # Open the url
    try:
        f = urlopen(url)
        print "downloading " + url

        # Open our local file for writing
        with open("data/"+os.path.basename(url), "wb") as local_file:
            local_file.write(f.read())

    #handle errors
    except HTTPError, e:
        print "HTTP Error:", e.code, url
    except URLError, e:
        print "URL Error:", e.reason, url


def download_1k(chromosome):
    base_url = "ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/"
    file_name = "ALL.chr{}.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz".format(chromosome)
    download_file(base_url+file_name)
    download_file(base_url+file_name+ '.tbi')

def download_1k_panel():
    download_file("ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/integrated_call_samples_v3.20130502.ALL.panel")

def download_gnomad(chromosome):
    url = "https://storage.googleapis.com/gnomad-public/release-170228/vcf/genomes/gnomad.genomes.r2.0.1.sites.{}.vcf.gz".format(chromosome)
    download_file(url)


download_1k(2)