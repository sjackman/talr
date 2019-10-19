#!/usr/bin/env python3

import sys
import gzip
import zlib
import argparse
import subprocess

parser = argparse.ArgumentParser(
    description="""
  Index the positions of reads corresponding to each barcode.
  The output .bdx file is tab separated with columns: barcode, number_of_reads,
  first_read_byte_position, reads_size_in_bytes.
"""
)
parser.add_argument(
    "reads_file", help="Path to the file with reads compressed with bgzip."
)
args = parser.parse_args()


def main():
    try:
        # Test whether reads file is valid
        with gzip.open(args.reads_file) as reads_file:
            reads_file.read(1)
    except (OSError, EOFError, zlib.error):
        print(
            "File " + args.reads_file + " does not appear to be bgzipped. Exiting."
        )
        sys.exit(1)
    out = subprocess.run(["bgzip", "-b", "1", "-s", "1", args.reads_file], capture_output=True)
    if out.returncode != 0:
        print(out.stderr.decode())
        sys.exit(1)

    with gzip.open(args.reads_file) as readsfile_file, open(
        args.reads_filepath + ".bdx", "w"
    ) as idx_file:
        i = 0
        current_barcode = "NA"
        current_no_of_reads = 0
        current_byte_start = 0
        current_byte_size = 0
        line_byte_location = 0
        for line in readsfile_file:
            line = line.decode()

            if i == 0:
                comment_tokens = line.split()
                if len(comment_tokens) >= 2 and comment_tokens[1].startswith("BX:Z:"):
                    barcode = comment_tokens[1].split(":")[2]
                else:
                    barcode = "NA"

                if barcode != current_barcode:
                    if current_barcode != "NA":
                        idx_file.write(
                            current_barcode
                            + "\t"
                            + str(current_no_of_reads)
                            + "\t"
                            + str(current_byte_start)
                            + "\t"
                            + str(current_byte_size)
                            + "\n"
                        )

                    current_barcode = barcode
                    current_no_of_reads = 0
                    current_byte_start = line_byte_location
                    current_byte_size = 0

                current_no_of_reads += 1

            i += 1
            i %= 4
            line_byte_location += len(line)
            current_byte_size += len(line)

        if current_barcode != "NA":
            idx_file.write(
                current_barcode
                + "\t"
                + str(current_no_of_reads)
                + "\t"
                + str(current_byte_start)
                + "\t"
                + str(current_byte_size)
                + "\n"
            )


if __name__ == "__main__":
    main()
