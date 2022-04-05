#!/usr/bin/env python3
import argparse
import os
import gzip

FIELD_SEPARATOR = '\t'
LINE_SEPARATOR = '\n'


def process_lines(infile, outfile):
    dformat = '%.' + str(args.places) + 'f'
    for line in infile:
        if line.startswith('#'):
            continue
        comps = line.strip().split(FIELD_SEPARATOR)
        decimal1 = float(comps[args.column])
        decimal2 = dformat % decimal1
        comps[args.column] = decimal2
        outfile.write(FIELD_SEPARATOR.join(comps) + LINE_SEPARATOR)


def compress(args):
    if args.infile.endswith('.gz'):
        if not args.outfile.endswith('.gz'):
            print('ERROR: outfile must end with .gz')
        with gzip.open(args.infile, 'rt') as infile:
            with gzip.open(args.outfile, 'wt') as outfile:
                process_lines(infile, outfile)
    else:
        with open(args.infile) as infile:
            with open(args.outfile, 'w') as outfile:
                process_lines(infile, outfile)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("infile", type=str, help="input file")
    parser.add_argument("outfile", type=str, help="output file")
    parser.add_argument("-c", "--column", type=int, help="column with the decimal to compress", default=5)
    parser.add_argument("-p", "--places", type=int, help="number of result places", default=2)
    args = parser.parse_args()
    compress(args)

