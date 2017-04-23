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