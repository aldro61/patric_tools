"""
    patric_tools: A Python package to download data from the PATRIC database
    Copyright (C) 2017 Alexandre Drouin
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
import logging
import os
try:
    from urlparse import urljoin
except ImportError: # Python 3
    pass  # TODO: include urljoin

from time import sleep

from .config import PATRIC_FTP_GENOMES_FNA_URL, PATRIC_FTP_GENOMES_METADATA_URL, PATRIC_FTP_GENOMES_TAB_URL
from .utils import download_file_from_url, url_extract_file_name


def download_genome_contigs(patric_id, outdir=".", throttle=False):
    """
    Downloads the contigs for a given genome

    Parameters:
    -----------
    patric_id: str
        The PATRIC identifier of the genome
    outdir: str
        The output directory in which to store the contig file
    throttle: bool
        Whether or not to throttle the download by sleeping for a short period of time

    Returns:
    --------
    exception: str
        Empty string if no exception occurred, exception info otherwise

    """
    if throttle:
        sleep(2)  # Give that server a break!
    file_name = urljoin(PATRIC_FTP_GENOMES_FNA_URL, patric_id + ".fna")
    logging.debug("Downloading contigs for genome {0!s} ({1!s})".format(patric_id, file_name))
    return download_file_from_url(file_name, outdir=outdir)


def download_genome_features(patric_id, outdir=".", throttle=False):
    """
    Downloads the PATRIC feature annotations for a given genome

    Parameters:
    -----------
    patric_id: str
            The PATRIC identifier of the genome
    outdir: str
        The output directory in which to store the annotation file
    throttle: bool
        Whether or not to throttle the download by sleeping for a short period of time

    Returns:
    --------
    exception: str
        Empty string if no exception occurred, exception info otherwise

    """
    if throttle:
        sleep(2)  # Give that server a break!
    file_name = urljoin(PATRIC_FTP_GENOMES_TAB_URL, patric_id + ".PATRIC.features.tab")
    logging.debug("Downloading PATRIC feature annotations for genome {0!s} ({1!s})".format(patric_id, file_name))
    return download_file_from_url(file_name, outdir=outdir)


def download_genome_pattyfam_annotations(patric_id, outdir=".", throttle=False):
    """
    Downloads the PATRIC PATtyFams annotations for a given genome

    Reference:
    -----------
    Davis et al. PATtyFams: Protein Families for the Microbial Genomes in the PATRIC Database.
    Frontiers in Microbiology. 2016;7:118. doi:10.3389/fmicb.2016.00118.

    Parameters:
    -----------
    patric_id: str
            The PATRIC identifier of the genome
    outdir: str
        The output directory in which to store the annotation file
    throttle: bool
        Whether or not to throttle the download by sleeping for a short period of time

    Returns:
    --------
    exception: str
        Empty string if no exception occurred, exception info otherwise

    """
    if throttle:
        sleep(2)  # Give that server a break!
    file_name = urljoin(PATRIC_FTP_GENOMES_TAB_URL, patric_id + ".PATRIC.cds.tab")
    logging.debug("Downloading PATRIC PATtyFams for genome {0!s} ({1!s})".format(patric_id, file_name))
    return download_file_from_url(file_name, outdir=outdir)


def get_latest_metadata(outdir):
    """
    Downloads the latest genome metadata (not to be confused with AMR metadata)

    Parameters:
    -----------
    outdir: str
        The path to the output directory

    """
    exception = download_file_from_url(PATRIC_FTP_GENOMES_METADATA_URL, outdir)
    if exception != '':
        raise RuntimeError("Failed to download the latest AMR metadata: {0!s}".format(exception))
    return os.path.join(outdir, url_extract_file_name(PATRIC_FTP_GENOMES_METADATA_URL))
