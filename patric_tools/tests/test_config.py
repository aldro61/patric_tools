from __future__ import print_function, division, absolute_import, unicode_literals

from unittest import TestCase

from ..config import PATRIC_FTP_BASE_URL, PATRIC_FTP_CURRENT_RELEASE_URL, PATRIC_FTP_AMR_METADATA_URL, \
    PATRIC_FTP_GENOMES_FNA_URL, PATRIC_FTP_GENOMES_METADATA_URL, PATRIC_FTP_GENOMES_TAB_URL

class UtilityTests(TestCase):
    def setUp(self):
        """
        Called before each test

        """
        pass

    def _test_url(self, url):
        import urllib2
        try:
            urllib2.urlopen(url, timeout=10)
        except:
            self.fail("Could not reach {0!s}".format(url))

    def test_ftp_base_url(self):
        """
        FTP base URL is reachable
        """
        self._test_url(PATRIC_FTP_BASE_URL)

    def test_ftp_current_release_url(self):
        """
        FTP current release URL is reachable
        """
        self._test_url(PATRIC_FTP_CURRENT_RELEASE_URL)

    def test_ftp_amr_metadata_url(self):
        """
        FTP antimicrobial resistance metadata is reachable
        """
        self._test_url(PATRIC_FTP_AMR_METADATA_URL)

    def test_ftp_genomes_fasta_url(self):
        """
        FTP genome FASTA file storage is reachable
        """
        self._test_url(PATRIC_FTP_GENOMES_FNA_URL)

    def test_ftp_genomes_metadata_url(self):
        """
        FTP genome metadata is reachable
        """
        self._test_url(PATRIC_FTP_GENOMES_METADATA_URL)

    def test_ftp_genomes_features_url(self):
        """
        FTP genome TAB file storage is reachable
        """
        self._test_url(PATRIC_FTP_GENOMES_TAB_URL)