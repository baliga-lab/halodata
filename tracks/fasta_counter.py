#!/usr/bin/env python3

import argparse

DESCRIPTION = """fasta_counter - count bases in the FASTA file"""

if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description=DESCRIPTION)
    parser.add_argument('infile', help="input file")
    args = parser.parse_args()
    cur_chrom_seq = None
    cur_chrom_name = None
    chroms = {}

    with open(args.infile) as infile:
        for line in infile:
            if line.startswith('>'):
                if cur_chrom_name is not None:
                    chroms[cur_chrom_name] = cur_chrom_seq
                cur_chrom_seq = ''
                cur_chrom_name = line.strip()[1:]
            else:
                cur_chrom_seq += line.strip()
        # do the last chromosome at the end
        chroms[cur_chrom_name] = cur_chrom_seq


        for chrom, seq in chroms.items():
            print('%s\t%d' % (chrom, len(seq)))
