"""


"""
import logging
try:
    from urlparse import urljoin
except ImportError: # Python 3
    pass  # TODO: include urljoin

from time import sleep

from .config import PATRIC_FTP_GENOMES_FNA_URL
from .utils import download_file_from_url


def download_genome_contigs(patric_id, outdir=".", throttle=False):
    """
    Downloads the contigs for a given genome

    Parameters:
    -----------
    outdir: str
        The output directory in which to store the contig file
    patric_id: str
        The PATRIC identifier of the genome to download
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
    logging.debug("Downloading contigs for genome %s (%s)" % (patric_id, file_name))
    return download_file_from_url(file_name, outdir=outdir)