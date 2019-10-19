#!/usr/bin/env python3

import sys
import argparse
import subprocess as sp
from collections import OrderedDict

# import os.path as op
# import logging


def main(argv=None):
    """Where the magic happens!"""
    if argv is None:
        argv = sys.argv

    args = get_parse_args()

    # logfmt = '[%(asctime)s - %(levelname)s - line:%(lineno)d] %(message)s'
    # datefmt = '%Y-%m-%d %H:%M:%S'
    # logfile = '{}.log'.format(op.basename(op.splitext(__file__)[0]))
    # sys.stderr.write("Log messages will be written to: {}\n".format(logfile))
    # logging.basicConfig(filename=logfile, format=logfmt, datefmt=datefmt,
    #                     filemode='w', level=logging.INFO)

    bdx = import_bdx(bdx_file=args.bdx)

    fbb = import_path(path_file=args.path, bdx=bdx)
    # print(fbb[0][list(fbb[0].keys())[0]])
    # print(fbb[0])

    # TODO:
    #  1. Scrub bdx to remove or zero-out suspicious GEMs
    #  2. Compute # chunks
    #  3. Compute # reads
    #  4. Compute reads / chunk
    #  5. Iterate over GEMs, extracting reads until the reads / chunk threshold is reached,
    #     then dump them to a file and start a new chunk
    #  6. Repeat Step 5 until GEMs are exhausted
    # subset_reads(fqbgz=args.fqbgz, bdx=bdx, barcode=barcode)


def import_bdx(bdx_file):
    """Import barcode to coordinate mappings

    Args:
        bdx_file: A .bdx index file corresponding to the bgzip'd read files that will be split

    Returns:
        bdx: A dictionary mapping GEM barcodes to lists containing:
                1. # reads in GEM
                2. Starting position of read data in bgzip'd FASTQ file
                3. Length of read data in bgzip'd FASTQ file
    """
    bdx = {}
    with open(bdx_file, 'r') as fin:
        for line in fin:
            temp = line.strip().split()
            if not temp:
                continue
            bdx[temp[0]] = temp[1:4]

    return(bdx)


def scrub_bdx(bdx):
    """Remove or zero out gems with too many or too few reads

    Args:
        bdx: Dictionary output by the import_bdx() function

    Returns:
        None: Scrubs bdx in place
    """
    # TODO:
    #   1. Extract read counts for each GEM
    #   2. Compute distribution across all GEMs
    #   3. Identify a threshold for suspicious GEMs
    #   4. Remove suspicious GEMs or zero out their read counts and size
    pass


def import_path(path_file, bdx):
    """Parse path file into dictionary

    Args:
        path_file: A .backbone.fleshed.path file output by Physlr

        bdx: Dictionary output by the import_bdx() function

    Returns:
        fbb: A complex nested data structure combining the path and bdx information
            Level 1: List corresponding to each sequence in the Physlr path file
            Level 2: Ordered dicts corresponding to barcodes in pre-fleshed backbone ("vertebrae")
            Level 3: List of bgx index stats for each vertebrae, and...
            Level 4: Dictionary barcodes and bgx stats for each GEM overlapping the vertebra
    """
    fbb = []  # Fleshed backbone
    with open(path_file) as fin:
        for line in fin:

            # Fleshed backbone path for a single sequence
            seq_path = line.strip().split()
            if not seq_path:
                continue

            # Strip flesh from backbone
            bb_barcodes = [b for b in seq_path if not b.startswith('(')]

            # Re-fleshify vertebrae
            seq_fbb = OrderedDict([(b, fleshify_vertebra(seq_path=seq_path, bdx=bdx, vertebra=b))
                                   for b in bb_barcodes])

            fbb.append(seq_fbb)

    return(fbb)


def fleshify_vertebra(seq_path, bdx, vertebra):
    """Assign overlapping barcodes to barcodes from the backbone

    Args:
        seq_path: A single line from a Physlr path file, split by whitespace
        bdx: Dictionary output by the import_bdx() function
        vertebra: Barcode of a single GEM from the pre-fleshed backbone

    Returns:
        vertebral_flesh: List with four elements:
            1. Number of reads with barcode of vertebra
            2. Starting position of reads in bgzip'd FASTQ file
            3. Length of read information in bgzip'd FASTQ file
            4. Dictionary with info for each overlapping GEMs, key'd by barcode, and with the same 3 stats as values
    """
    try:
        # Get item (potentially a list of barcodes for overlapping GEMs) immediately after backbone barcode
        olap_bars = seq_path[seq_path.index(vertebra) + 1]

    # Return empty overlap list if we reach the end of the path list for this sequence
    except IndexError:
        return([])

    # Return empty list if next item is another vertebra instead  of a list of overlapping GEM barcodes
    if not olap_bars.startswith('('):
        return([])

    # Gather and format information for vertebra and any overlapping GEMs
    olap_bars = olap_bars.strip('()').split(',')
    olap_dict = {b: bdx[b.split('_')[0]] for b in olap_bars}
    vertebral_flesh = bdx[vertebra.split('_')[0]] + [olap_dict]

    return(vertebral_flesh)


def subset_reads(fqbgz, bdx, barcode):
    """Extract reads corresponding to a barcode

    Args:
        fqbgz: Name of bgzip'd FASTQ file to be subset
        bdx: Dictionary output by the import_bdx() function
        barcode: GEM barcode for which corresponding reads should be subset

    Returns:
        reads: String containing data for reads corresponding to GEM
    """
    offset, size = bdx[barcode.split('_')[0]][1:3]
    out = sp.run(["bgzip", "-b", offset, "-s", size, fqbgz], capture_output=True)
    reads = out.stdout.decode()
    return(reads)


def get_parse_args():
    """Parse commandline arguments and options"""
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="Subset bgzip'd FASTQ file using linked read barcode")

    parser.add_argument('path',
                        type=str,
                        help="A .backbone.fleshed.path file from Physlr")

    parser.add_argument('fqbgz',
                        type=str,
                        help="A bgzip'd (not gzip'd) FASTQ file")

    parser.add_argument('bdx',
                        type=str,
                        help="A .bdx index file for a bgzip'd (not gzip'd) FASTQ file")

    parser.add_argument('-o', '--outfile',
                        type=argparse.FileType('w'),
                        default=sys.stdout,
                        help="Output FASTQ file")

    # TODO: Add parameters for # chunks and overlap fraction

    args = parser.parse_args()
    return args

if __name__ == "__main__":
    sys.exit(main())




# bgzip -r fly/f1chr4.1.fq.gz
# bgzip -b 5497 -s 7443 fly/f1chr4.1.fq.gz
