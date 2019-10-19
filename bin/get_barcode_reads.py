#!/usr/bin/env python3

import sys
import argparse
import subprocess

parser = argparse.ArgumentParser(
    description="""
    Output the reads belonging to the set of given barcodes.
    The barcodes are read from stdin and should be separated by either comma or newline.
"""
)
parser.add_argument('reads_file', help="FASTQ reads file compressed with bgzip.")
parser.add_argument('barcode_index', help="Barcode index file for reads_file.")
args = parser.parse_args()

def main():
    index = {}
    with open(args.barcode_index, 'r') as barcode_index:
        for line in barcode_index:
            tokens = line.split()
            index[tokens[0]] = (tokens[1], tokens[2], tokens[3])

    for line in sys.stdin:
        for barcode in line.strip().split(','):
            byte_start = index[barcode][1]
            byte_size = index[barcode][2]
            out = subprocess.run(["bgzip", "-b", byte_start, "-s", byte_size, args.reads_file], capture_output=True)
            out = out.stdout.decode()
            print(out, end='')

if __name__ == "__main__":
    main()