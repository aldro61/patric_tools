"""


"""
import numpy as np
import os
import pandas as pd

from .config import PATRIC_FTP_AMR_METADATA_URL
from .utils import download_file_from_url, url_extract_file_name


def get_amr_data_by_species_and_antibiotic(amr_metadata_file, antibiotic, species=None, drop_intermediate=True):
    """
    Returns the PATRIC identifiers of the genomes for which there is AMR metadata for some antibiotic

    Parameters:
    -----------
    amr_metadata_file: str
        The path to the AMR metadata file
    antibiotic: str
        The name of the antibiotic
    drop_intermediate: bool, default=True
        Whether or not to consider the genomes with the "Intermediate" phenotype
    species: list, default=None
        If not specified, all species are considered. Otherwise, only the specified species are considered.

    Returns:
    --------
    patric_ids: array_like, dtpye=str
        The PATRIC identifiers of the genomes
    phenotypes: array_like, dtype=uint8
        The phenotype of each genome (0 = sensitive, 1 = resistant, 2 = intermediate)
    species: array_like, dtype=str
        The species of each genome

    """
    antibiotic = antibiotic.lower()

    amr = pd.read_table(amr_metadata_file, usecols=["genome_id", "genome_name", "antibiotic", "resistant_phenotype"],
                        converters={'genome_id': str, 'genome_name': lambda x: " ".join(x.lower().split()[:2])})
    amr = amr.loc[amr.antibiotic == antibiotic]
    amr = amr.dropna()

    assert len(np.unique(amr.resistant_phenotype)) <= 3  # If this fails, the data structure changed

    # Drop intermediate if needed
    if drop_intermediate:
        amr = amr.loc[amr.resistant_phenotype != "Intermediate"]

    # Keep only specified species
    if species is not None:
        amr = amr.loc[[n in species for n in amr.genome_name]]

    numeric_phenotypes = np.zeros(amr.shape[0], dtype=np.uint8)
    numeric_phenotypes[amr.resistant_phenotype.values == "Resistant"] = 1
    numeric_phenotypes[amr.resistant_phenotype.values == "Intermediate"] = 2

    return amr["genome_name"].values, amr["genome_id"].values, numeric_phenotypes


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
        raise RuntimeError("Failed to download the latest AMR metadata: %s" % exception)
    return os.path.join(outdir, url_extract_file_name(PATRIC_FTP_AMR_METADATA_URL))


def list_amr_datasets(amr_metadata_file, min_resistant=0, max_resistant=None, min_susceptible=0,
                      max_susceptible=None, single_species=True):

    if max_resistant is None:
        max_resistant = np.infty
    if max_susceptible is None:
        max_susceptible = np.infty

    amr = pd.read_table(amr_metadata_file, usecols=["genome_id", "genome_name", "antibiotic", "resistant_phenotype"],
                        converters={'genome_id': str, 'genome_name': lambda x: " ".join(x.lower().split()[:2])})

    dataset_species = []
    dataset_antibiotics = []

    if single_species:
        amr = amr.groupby(['genome_name', 'antibiotic'])
    else:
        amr = amr.groupby('antibiotic')

    for name, data in amr:
        n_res = (data["resistant_phenotype"] == "Resistant").sum()
        n_sus = (data["resistant_phenotype"] == "Susceptible").sum()

        if min_resistant <= n_res <= max_resistant and min_susceptible <= n_sus <= max_susceptible:
            if single_species:
                dataset_antibiotics.append(name[1])
                dataset_species.append([name[0]])
            else:
                dataset_antibiotics.append(name)
                dataset_species.append(None)

    return zip(dataset_species, dataset_antibiotics)