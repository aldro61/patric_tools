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

from patric_tools.amr import list_amr_datasets, get_amr_data_by_species_and_antibiotic


# List all AMR datasets with at least 25 resistant and 25 sensitive isolates (partitioned by species)
for species, antibiotic in list_amr_datasets(single_species=True, min_resistant=25, min_susceptible=25):
    # Load the dataset's AMR metadata
    g_species, g_ids, g_phenotypes = get_amr_data_by_species_and_antibiotic(antibiotic, species)

    print("Dataset:")
    print("--------")
    print("Species:", species, "  Antibiotic:", antibiotic)
    print("Resistant:", int((g_phenotypes == 1).sum()), "   Sensitive:", int((g_phenotypes == 0).sum()))
    print("\n" * 2)

# List all AMR datasets with at least 25 resistant and 25 sensitive isolates (all species merged)
for species, antibiotic in list_amr_datasets(single_species=False, min_resistant=25, min_susceptible=25):
    # Load the dataset's AMR metadata
    g_species, g_ids, g_phenotypes = get_amr_data_by_species_and_antibiotic(antibiotic, species)

    print("Dataset:")
    print("--------")
    print("Species:", species, "  Antibiotic:", antibiotic)
    print("Resistant:", int((g_phenotypes == 1).sum()), "   Sensitive:", int((g_phenotypes == 0).sum()))
    print("\n" * 2)
