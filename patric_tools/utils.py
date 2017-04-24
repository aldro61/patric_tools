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
import os
import posixpath

try:
    from urlparse import urlsplit, urljoin
    from urllib import unquote, urlretrieve
except ImportError: # Python 3
    from urllib.parse import urlsplit, unquote  #TODO: include urljoin
    from urllib.request import urlretrieve


def download_file_from_url(url, outdir):
    """
    Download a file and save it to some output directory

    Parameters:
    -----------
    url: str
        The URL of the file to download
    outdir: str
        The path to the output directory

    Returns:
    --------
    exception: str
        Empty string if no error, url + exception otherwise

    Notes:
    ------
    * Will automatically skip files that have already been downloaded.

    """
    url = url.strip()
    try:
        from os import system
        system("wget --quiet -o /dev/null -O {0!s} --continue --timeout 20 {1!s}".format(os.path.join(outdir, url_extract_file_name(url)), url))
        return ""
    except Exception as e:
        print e
        return url + str(e)


def url_extract_file_name(url):
    """
    Return basename corresponding to url

    """
    urlpath = urlsplit(url).path
    basename = posixpath.basename(unquote(urlpath))
    if os.path.basename(basename) != basename:
        raise ValueError(url)
    return basename