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
PATRIC_FTP_GENOMES_METADATA_URL = urljoin(PATRIC_FTP_CURRENT_RELEASE_URL, urljoin("RELEASE_NOTES/", "genome_metadata"))
PATRIC_FTP_GENOMES_TAB_URL = urljoin(PATRIC_FTP_CURRENT_RELEASE_URL, "tab/")