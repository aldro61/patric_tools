"""


"""
import logging
try:
    from urlparse import urljoin
except ImportError: # Python 3
    pass  # TODO: include urljoin

from .config import PATRIC_FTP_GENOMES_FNA_URL
from .utils import download_file_from_url


def download_genome_contigs(patric_id, outdir="."):
    """
    Downloads the contigs for a given genome

    Parameters:
    -----------
    patric_id: str
        The PATRIC identifier of the genome to download
    outdir: str
        The output directory in which to store the contig file

    Returns:
    --------
    exception: str
        Empty string if no exception occurred, exception info otherwise

    """
    file_name = urljoin(PATRIC_FTP_GENOMES_FNA_URL, patric_id + ".fna")
    logging.debug("Downloading contigs for genome %s (%s)" % (patric_id, file_name))
    return download_file_from_url(file_name, outdir=outdir)