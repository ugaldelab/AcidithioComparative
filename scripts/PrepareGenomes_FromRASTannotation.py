#!/Users/juan/anaconda/bin/python
#Updated 9/13/14

#This script will analyze a set of genomes annotated with RAST.
#The genome folder contains the information for each genome obtained
#from RAST. This includes:
#Tabular format with the annotation

__author__ = "Juan A. Ugalde"

import os
import argparse

program_description = "This script that will process a list of genomes annotated with RAST, and " \
                      "prepare that information for ortholog and other analysis"

parser = argparse.ArgumentParser(description=program_description)

parser.add_argument("-l", "--genome_list", type=str, help="Table with the genome list. First column"
                                                          "has the RAST ID, second the genome prefix", required=True)

parser.add_argument("-f", "--genome_folder", type=str, help="Folder that has all the genome information", required=True)

parser.add_argument("-o", "--output_directory", type=str, help="Output folder", required=True)

args = parser.parse_args()

#Make output directory
if not os.path.exists(args.output_directory):
    os.makedirs(args.output_directory)
    os.makedirs(args.output_directory + "/nucleotide")
    os.makedirs(args.output_directory + "/protein")


#Read the genome list
for line in open(args.genome_list, 'r'):
    if line.strip():
        line = line.rstrip()

        rast_id, genome_prefix = line.split("\t")

        out_nuc_file = open(args.output_directory + "/nucleotide/" + genome_prefix + ".fna", 'w')
        out_prot_file = open(args.output_directory + "/protein/" + genome_prefix + ".faa", 'w')

        annotation_file = args.genome_folder + "/" + rast_id + ".txt"

        for entry in open(annotation_file, 'r'):

            if entry.startswith("contig_id"):
                continue

            entry = entry.rstrip()

            type = entry.split("\t")[2]
            feature_id = entry.split("\t")[1].split("|")[1]

            if type == "peg":

                nucleotide_sequence = entry.split("\t")[11]
                aminoacid_sequence = entry.split("\t")[12]
                fasta_header = ">" + genome_prefix + "|" + feature_id

                out_nuc_file.write(fasta_header + "\n")
                out_nuc_file.write(nucleotide_sequence + "\n")

                out_prot_file.write(fasta_header + "\n")
                out_prot_file.write(aminoacid_sequence + "\n")

        out_nuc_file.close()
        out_prot_file.close()





















