"""


"""
import numpy as np
import pandas as pd

from patric_tools.config import PATRIC_FTP_AMR_METADATA_URL
from patric_tools.utils import download_file_from_url


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


def genome_ids_by_antibiotic_and_species(amr_metadata_file, antibiotic, species=None, drop_intermediate=True):
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