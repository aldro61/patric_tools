"""


"""
try:
    from urlparse import urlsplit, urljoin
    from urllib import unquote, urlretrieve
except ImportError: # Python 3
    from urllib.parse import urlsplit, unquote  # TODO: include urljoin
    from urllib.request import urlretrieve

PATRIC_FTP_BASE_URL = "ftp://ftp.patricbrc.org"
PATRIC_FTP_CURRENT_RELEASE_URL = urljoin(PATRIC_FTP_BASE_URL, "patric2/current_release/")
PATRIC_FTP_AMR_METADATA_URL = urljoin(PATRIC_FTP_CURRENT_RELEASE_URL, urljoin("RELEASE_NOTES/", "PATRIC_genomes_AMR.txt"))
PATRIC_FTP_GENOMES_FNA_URL = urljoin(PATRIC_FTP_CURRENT_RELEASE_URL, "fna/")
PATRIC_FTP_GENOMES_TAB_URL = urljoin(PATRIC_FTP_CURRENT_RELEASE_URL, "tab/")