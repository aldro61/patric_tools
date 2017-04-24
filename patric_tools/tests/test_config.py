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