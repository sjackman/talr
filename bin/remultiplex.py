#!/usr/bin/env python3

import sys
import re
from collections import namedtuple

ACGT = re.compile("^[ACGT]+$")

Record = namedtuple("Record", "header read comment quality")


def record_generator(fastq_file):
    while True:
        header = fastq_file.readline().rstrip()
        read = fastq_file.readline().rstrip()
        comment = fastq_file.readline().rstrip()
        quality = fastq_file.readline().rstrip()
        if quality == "":
            break
        yield Record(header=header, read=read, comment=comment, quality=quality)


def print_record(record: Record):
    print(record.header)
    print(record.read)
    print(record.comment)
    print(record.quality)


def remultiplex(read: str, barcode: str, read_length=150):
    nc_to_add = read_length - len(read) - len(barcode)
    remultiplex_read = barcode + "N" * nc_to_add + read
    return remultiplex_read


def get_barcode(header: str):
    barcode_index = header.find("Z:") + 2
    if header.find("Z:") == 1:
        print("No barcode in ", header, file=sys.stderr)
        exit()
    barcode = header[barcode_index : len(header) - 2]
    new_header = header[: barcode_index - 6]
    return barcode, new_header


def extend_quality(quality: str, read_length: int, original_read_length=150):
    extension_length = original_read_length - read_length
    new_quality = "I" * extension_length + quality
    return new_quality


def main():
    reads_fastq_path = sys.argv[1]
    fastq_file = open(reads_fastq_path)
    records = record_generator(fastq_file)
    # TODO: check interleaved logic
    for record in records:
        barcode, header = get_barcode(record.header)
        if header.endswith("/2"):
            remultiplex_record = Record(
                header=header,
                read=record.read,
                comment=record.comment,
                quality=record.quality,
            )
            print_record(remultiplex_record)
            continue
        remultiplex_read = remultiplex(record.read, barcode)
        remultiplex_quality = extend_quality(record.quality, len(record.read))
        assert len(remultiplex_read) == len(remultiplex_quality)
        remultiplex_record = Record(
            header=header,
            read=remultiplex_read,
            comment=record.comment,
            quality=remultiplex_quality,
        )
        print_record(remultiplex_record)


if __name__ == "__main__":
    main()
