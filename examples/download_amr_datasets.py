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

Example: downloading AMR data sets from the PATRIC database

"""
from joblib import Parallel, delayed
from patric_tools import amr, genomes

# Find all antibiotic resistance data sets that match some criteria
amr_datasets = amr.list_amr_datasets(min_resistant=20,
                                     min_susceptible=20,
                                     single_species=True)
print "Available antibiotic resistance data sets:"
for species, antibiotic in amr_datasets:
    print "... Species:", species[0].title(), "  Antibiotic:", antibiotic
print "\n" * 2

print "Downloading genomes and metadata for one data set:"
species, genome_ids, labels = \
    amr.get_amr_data_by_species_and_antibiotic(species=amr_datasets[0][0],
                                               antibiotic=amr_datasets[0][1])
print "... Genomes: {}".format(len(labels))
print "...... Resistant: {}".format((labels == 1).sum())
print "...... Sensible: {}".format((labels == 0).sum())

print "... Fetching genome sequences:"
def download_genome(g_id):
    print "...... Isolate: {0!s} -> {0!s}.fna".format(g_id)
    genomes.download_genome_contigs(g_id)
# Download 4 genomes in parallel
Parallel(n_jobs=4)(delayed(download_genome)(g_id) for g_id in genome_ids)
print "Done."
