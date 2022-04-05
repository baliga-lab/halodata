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

def find_bucket(bucket_map, left, right):
    for key, bucket in bucket_map.items():
        l, r = key.split('-')
        l = int(l)
        r = int(r)
        if left >= l and left <= r:
            return bucket
    raise Exception('not found')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description=DESCRIPTION)
    parser.add_argument('infile', help="input file")
    parser.add_argument('-sl', '--seqlen', type=int, help='sequence length', default=2571034)
    parser.add_argument('-nc', '--numchunks', type=int, help='number of chunks', default=20)
    args = parser.parse_args()

    intervals = steps(0, args.seqlen - 1, args.numchunks)
    buckets = []
    bucket_map = {}
    for i in range(len(intervals) - 1):
        left = intervals[i]
        if i > 0:
            left += 1
        right = intervals[i + 1]
        buckets.append((left, right))
        key = "%d-%d" % (left, right)
        bucket_map[key] = []
    print(bucket_map)

    with gzip.open(args.infile) as infile:
        for line in infile:
            line = line.decode('utf-8').strip()
            refseq, start, stop, value = line.split('\t')
            start = int(start)
            stop = int(stop)
            bucket = find_bucket(bucket_map, start, stop)
            bucket.append((refseq, start, stop, value))

    filename_stem = os.path.basename(args.infile).replace('.bedgraph.gz', '')
    for key, bucket in bucket_map.items():
        try:
            start, stop = key.split('-')
        except:
            print(key)
        final_filename = '%s_%s-%s.bedgraph.gz'
        with gzip.open(final_filename % (filename_stem, start, stop), 'wb') as outfile:
            for reqseq, start, stop, value in bucket:
                outline = '%s\t%d\t%d\t%s\n' % (refseq, start, stop, value)
                outfile.write(outline.encode('utf-8'))
