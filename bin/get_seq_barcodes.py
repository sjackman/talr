#!/usr/bin/env python3

import sys
import gzip
import argparse

parser = argparse.ArgumentParser(
    description="""
  Given reads and reads alignment files, for each target sequence output the set of barcodes \
  belonging to the reads that align to it.
"""
)
parser.add_argument(
    "reads_file", help="FASTQ file containing reads and their barcodes."
)
parser.add_argument("alignment_file", help="The reads alignment file. SAM format only.")
parser.add_argument(
    "-s",
    "--seq_names",
    nargs="+",
    help="List of sequence names to get barcodes for. If empty, \
    the script will get barcodes for all sequences.",
)
args = parser.parse_args()


def main():
    with open(args.alignment_file, "r") as alignment_file, gzip.open(
        args.reads_file, "r"
    ) as reads_file:

        read2seq = {}
        seq_barcodes = {}

        for line in alignment_file:
            if line[0] == "@":
                continue

            tokens = line.split()
            if len(tokens) >= 11:
                read_name = tokens[0]
                seq_name = tokens[2]

                if args.seq_names == None or seq_name in args.seq_names:
                    read2seq[read_name] = seq_name

        i = 0
        for line in reads_file:
            line = line.decode()
            if i == 0:
                tokens = line.split()
                if len(tokens) >= 2:
                    read_name = tokens[0][1:-2]
                    barcode = tokens[1].split(":")[2]

                    if read_name in read2seq:
                        seq = read2seq[read_name]
                        if seq in seq_barcodes:
                            if barcode not in seq_barcodes[seq]:
                                seq_barcodes[seq].add(barcode)
                        else:
                            seq_barcodes[seq] = set()
                            seq_barcodes[seq].add(barcode)

            i += 1
            i %= 4

    for seq in seq_barcodes:
        print(seq + "\t", end="")
        barcodes = seq_barcodes[seq]
        for i, barcode in enumerate(sorted(barcodes)):
            print(barcode, end="")
            if i < len(barcodes) - 1:
                print(",", end="")
        print()


if __name__ == "__main__":
    main()
