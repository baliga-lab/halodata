#!/usr/bin/env python3

import argparse
import gzip
import os
from collections import defaultdict

DESCRIPTION = """tracksplitter - Split bedgraph files

This tool splits bedgraph files into chunks
"""

def steps(start,end,n):
    if n<2:
        raise Exception("behaviour not defined for n<2")
    step = (end-start)/float(n-1)
    return [int(round(start+x*step)) for x in range(n)]

def find_bucket(bucket_map, refseq, left, right):
    for key, bucket in bucket_map.items():
        chrom, interval = key.split(':')
        #print('scan chrom: %s with %s' % (chrom, refseq))
        if chrom == refseq:
            l, r = interval.split('-')
            l = int(l)
            r = int(r)
            if left >= l and left <= r:
                return key, bucket
    raise Exception("not found: '%s'" % refseq)


SEQLENS = {
    'NC_002607.1': 2014239,
    'NC_001869.1': 191346,
    'NC_002608.1': 365425
}
NUM_CHUNKS = 10


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description=DESCRIPTION)
    parser.add_argument('infile', help="input file")
    parser.add_argument('outdir', help='output directory')
    parser.add_argument('-nc', '--numchunks', type=int, help='number of chunks', default=NUM_CHUNKS)
    args = parser.parse_args()

    if not os.path.exists(args.outdir):
        os.makedirs(args.outdir)

    chrom_intervals = {}
    for chrom, seqlen in SEQLENS.items():
        intervals = steps(0, seqlen - 1, args.numchunks)
        chrom_intervals[chrom] = intervals

    # arrange every element in a bucket
    bucket_map = {}  # all possible bucket keys
    for chrom, intervals in chrom_intervals.items():
        for i in range(len(intervals) - 1):
            left = intervals[i]
            if i > 0:
                left += 1
            right = intervals[i + 1]
            key = "%s:%d-%d" % (chrom, left, right)
            bucket_map[key] = []

    with gzip.open(args.infile) as infile:
        for line in infile:
            line = line.decode('utf-8').strip()
            refseq, start, stop, value = line.split('\t')
            start = int(start)
            stop = int(stop)
            bucket_key, bucket = find_bucket(bucket_map, refseq, start, stop)
            if not bucket_key.startswith(refseq):
                raise Exception('%s is not %s' % (bucket_key, refseq))
            bucket.append((refseq, start, stop, value))

    filename_stem = os.path.basename(args.infile).replace('.bedgraph.gz', '')
    for key, bucket in bucket_map.items():
        print('process bucket "%s"' % key)
        try:
            chrom, interval = key.split(':')
            start, stop = interval.split('-')
        except:
            print(key)
        final_filename = os.path.join(args.outdir, '%s_%s-%s-%s.bedgraph.gz')
        final_filename2 = final_filename % (filename_stem, chrom, start, stop)
        print("writing file: '%s'" % final_filename2)
        with gzip.open(final_filename2, 'wb') as outfile:
            for refseq, start, stop, value in bucket:
                outline = '%s\t%d\t%d\t%s\n' % (refseq, start, stop, value)
                outfile.write(outline.encode('utf-8'))

    with open(os.path.join(args.outdir, 'track_ranges.py'), 'w') as outfile:
        outfile.write('TRACK_RANGES = [\n')
        for key in bucket_map.keys():
            outfile.write("  '%s',\n" % key)
        outfile.write(']\n')
