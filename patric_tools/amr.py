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
import ftplib
import numpy as np
import os
import pandas as pd

from datetime import datetime
from tempfile import tempdir

from .config import PATRIC_FTP_AMR_METADATA_URL, PATRIC_FTP_BASE_URL
from .utils import download_file_from_url, url_extract_file_name


def get_amr_data_by_species_and_antibiotic(antibiotic, species=None, drop_intermediate=True, amr_metadata_file=None):
    """
    Returns the PATRIC identifiers of the genomes for which there is AMR metadata for some antibiotic

    Parameters:
    -----------
    antibiotic: str
        The name of the antibiotic
    species: list, optional, default=None
        If not specified, all species are considered. Otherwise, only the specified species are considered.
    drop_intermediate: bool, optional, default=True
        Whether or not to consider the genomes with the "Intermediate" phenotype
    amr_metadata_file: str, optional
        The path to the AMR metadata file. If not specified, the latest metadata will be downloaded to a temporary file.

    Returns:
    --------
    patric_ids: array_like, dtpye=str
        The PATRIC identifiers of the genomes
    phenotypes: array_like, dtype=uint8
        The phenotype of each genome (0 = sensitive, 1 = resistant, 2 = intermediate)
    species: array_like, dtype=str
        The species of each genome

    Notes:
    ------
    The phenotypes "Not defined", "Non-susceptible" and "Nonsusceptible" are dropped to avoid adding noise to the data.
    However, this phenotypes are not commonly encountered in the data.

    """
    if amr_metadata_file is None:
        amr_metadata_file = get_latest_metadata(tempdir)

    antibiotic = antibiotic.lower()

    amr = pd.read_table(amr_metadata_file, usecols=["genome_id", "genome_name", "antibiotic", "resistant_phenotype"],
                        converters={'genome_id': str, 'genome_name': lambda x: " ".join(x.lower().split()[:2])})
    amr = amr.dropna()
    amr = amr.loc[amr.antibiotic == antibiotic]
    amr = _remove_duplicates(amr)

    # Drop strange phenotype names that were encountered
    amr = amr.loc[amr.resistant_phenotype != "Not defined"]
    amr = amr.loc[amr.resistant_phenotype != "Non-susceptible"]
    amr = amr.loc[amr.resistant_phenotype != "Nonsusceptible"]

    # XXX: Runtime test to see if the data structure has changed
    assert len(np.unique(amr.resistant_phenotype)) <= 3

    # Drop intermediate if needed
    if drop_intermediate:
        amr = amr.loc[amr.resistant_phenotype != "Intermediate"]

    # Keep only specified species
    if species is not None:
        species = [s.lower() for s in species]
        amr = amr.loc[[n.lower() in species for n in amr.genome_name]]

    numeric_phenotypes = np.zeros(amr.shape[0], dtype=np.uint8)
    numeric_phenotypes[amr.resistant_phenotype.values == "Resistant"] = 1
    numeric_phenotypes[amr.resistant_phenotype.values == "Intermediate"] = 2

    return amr["genome_name"].values, amr["genome_id"].values, numeric_phenotypes


def get_last_metadata_update_date():
    """
    Get the date and time at which the antimicrobial metadata was last modified

    Returns:
    --------
    datetime: DateTime
        The date and time at which the metadata was last modified

    """
    ftps = ftplib.FTP(PATRIC_FTP_BASE_URL.replace("ftp://", ""))
    ftps.login()
    mod_time = ftps.sendcmd("MDTM {0!s}".format(PATRIC_FTP_AMR_METADATA_URL.replace(PATRIC_FTP_BASE_URL, "").replace("ftp://", "")[1:])).split()[1]
    return datetime.strptime(mod_time, '%Y%m%d%H%M%S')


def get_latest_metadata(outdir):
    """
    Downloads the latest antimicrobial resistance metadata

    Parameters:
    -----------
    outdir: str
        The path to the output directory

    """
    exception = download_file_from_url(PATRIC_FTP_AMR_METADATA_URL, outdir)
    if exception != '':
        raise RuntimeError("Failed to download the latest AMR metadata: {0!s}".format(exception))
    return os.path.join(outdir, url_extract_file_name(PATRIC_FTP_AMR_METADATA_URL))


def _remove_duplicates(data):
    # Keep only one measurement for the same genome, antibiotic and phenotype
    data = data.drop_duplicates(subset=['genome_id', 'antibiotic', 'resistant_phenotype'], keep='first')
    # Drop all genomes/antibiotic combinations for which we have contradictory measurements
    data = data.drop_duplicates(subset=['genome_id', 'antibiotic'], keep=False)
    return data


def list_amr_datasets(amr_metadata_file=None, min_resistant=0, max_resistant=np.infty, min_susceptible=0,
                      max_susceptible=np.infty, single_species=True):
    """
    Extracts all antimicrobial resistance datasets from the database metadata

    Parameters:
    -----------
    amr_metadata_file: str, optional
        The path to the AMR metadata file. If not specified, the latest metadata will be downloaded to a temporary file.
    min_resistant: int, optional, default=0
        The minimum number of resistant isolates in the dataset.
    max_resistant: int, optional, default=inf
        The maximum number of resistant isolates in the dataset.
    min_susceptible: int, optional, default=0
        The minimum number of susceptible isolates in the dataset.
    max_susceptible: int, optional, default=inf
        The maximum number of susceptible isolates in the dataset.

    """
    if amr_metadata_file is None:
        amr_metadata_file = get_latest_metadata(tempdir)

    amr = pd.read_table(amr_metadata_file, usecols=["genome_id", "genome_name", "antibiotic", "resistant_phenotype"],
                        converters={'genome_id': str, 'genome_name': lambda x: " ".join(x.lower().split()[:2])})
    amr = amr.dropna()

    dataset_species = []
    dataset_antibiotics = []

    if single_species:
        amr = amr.groupby(['genome_name', 'antibiotic'])
    else:
        amr = amr.groupby('antibiotic')

    for name, data in amr:
        data = _remove_duplicates(data)

        n_res = (data["resistant_phenotype"] == "Resistant").sum()
        n_sus = (data["resistant_phenotype"] == "Susceptible").sum()

        if min_resistant <= n_res <= max_resistant and min_susceptible <= n_sus <= max_susceptible:
            if single_species:
                dataset_antibiotics.append(name[1])
                dataset_species.append([name[0]])
            else:
                dataset_antibiotics.append(name)
                dataset_species.append(data["genome_name"].unique())

    return zip(dataset_species, dataset_antibiotics)