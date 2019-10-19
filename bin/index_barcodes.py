#!/usr/bin/env python3

import sys
import gzip
import zlib
import argparse

parser = argparse.ArgumentParser(description="""
  Index the positions of reads corresponding to each barcode.
  The output .bdx file is tab separated with columns: barcode, number_of_reads,
  first_read_byte_position, reads_size_in_bytes.
""")
parser.add_argument('reads_filepath', help="Path to the file with reads compressed with bgzip.")
args = parser.parse_args()

def main():
  reads_filepath = args.reads_filepath

  try:
    # Test whether reads file is valid
    with gzip.open(reads_filepath) as reads_file:
      reads_file.read()
  except (OSError, EOFError, zlib.error):
      print("File " + reads_filepath + " does not appear to be bgzipped. Exiting.")
      sys.exit(1)

  with gzip.open(reads_filepath) as readsfile_file, open(reads_filepath + '.bdx', 'w') as idx_file:
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
        if len(comment_tokens) >= 2 and comment_tokens[1].startswith('BX:Z:'):
          barcode = comment_tokens[1].split(':')[2]
        else:
          barcode = 'NA'

        if barcode != current_barcode:
          if current_barcode != 'NA':
            idx_file.write(current_barcode + '\t' +
                          str(current_no_of_reads) + '\t' +
                          str(current_byte_size) + '\t' +
                          str(current_byte_start) + '\n')
          
          current_barcode = barcode
          current_no_of_reads = 0
          current_byte_start = line_byte_location
          current_byte_size = 0

        current_no_of_reads += 1

      i += 1
      i %= 4
      line_byte_location += len(line)
      current_byte_size += len(line)
    
    if current_barcode != 'NA':
      idx_file.write(current_barcode + '\t' +
                      str(current_no_of_reads) + '\t' +
                      str(current_byte_size) + '\t' +
                      str(current_byte_start) + '\n')

if __name__ == "__main__":
  main()