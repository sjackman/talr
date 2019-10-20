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
parser.add_argument(
    "-b",
    "--barcode-threshold",
    help="Minimum mapped reads with the same barcode required for a barcode to be included.",
    type=int,
    default=2,
)
parser.add_argument(
    "-m",
    "--mapq-threshold",
    help="Minimum mapping quality to consider a read.",
    type=int,
    default=40,
)
args = parser.parse_args()


def main():
    with open(args.alignment_file, "r") as alignment_file, gzip.open(
        args.reads_file, "r"
    ) as reads_file:

        read2seq = {}
        read2map_quality = {}
        seq_barcodes = {}

        for line in alignment_file:
            if line[0] == "@":
                continue

            tokens = line.split()
            if len(tokens) >= 11:
                read_name = tokens[0]
                seq_name = tokens[2]
                map_quality = int(tokens[4])

                if map_quality < args.mapq_threshold:
                    continue

                if args.seq_names == None or seq_name in args.seq_names:
                    if read_name in read2seq:
                        if map_quality > read2map_quality[read_name]:
                            read2seq[read_name] = seq_name
                            read2map_quality[read_name] = map_quality
                    else:
                        read2seq[read_name] = seq_name
                        read2map_quality[read_name] = map_quality

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
                        if not seq in seq_barcodes:
                            seq_barcodes[seq] = {}

                        if not barcode in seq_barcodes[seq]:
                            seq_barcodes[seq][barcode] = 1
                        else:
                            seq_barcodes[seq][barcode] += 1

            i += 1
            i %= 4

    for seq in seq_barcodes:
        print(seq + "\t", end="")
        barcodes = seq_barcodes[seq]
        i = 0
        for barcode in sorted(barcodes):
            if barcodes[barcode] >= args.barcode_threshold:
                if i > 0:
                    print(",", end="")
                print(barcode, end="")
                i += 1
        print()


if __name__ == "__main__":
    main()
