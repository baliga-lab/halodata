#!/usr/bin/env python3

import argparse

DESCRIPTION = """fasta_counter - count bases in the FASTA file"""

if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description=DESCRIPTION)
    parser.add_argument('infile', help="input file")
    args = parser.parse_args()

    with open(args.infile) as infile:
        infile.readline()
        seq = ""
        for line in infile:
            seq += line.strip()

        print('genome size: %d' % len(seq))
