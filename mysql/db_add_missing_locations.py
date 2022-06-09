#!/usr/bin/env python3

"""
This script goes through the gene track file and fixes every missing position it can't find
"""
import mysql.connector
from collections import defaultdict
import traceback as tb

def fix_missing_positions(conn):
    curr_line = 0
    with open('Hsalinarum-gene-annotation-pfeiffer2019-adjusted-names.gff3') as infile:
        header = infile.readline()  # ignore header
        with conn.cursor() as cur:
            for line in infile:
                curr_line += 1
                chrom, l1, typ, start, stop, l2, strand, l3, desc = line.strip().split('\t')
                comps = desc.split(';')
                candidate_gene_names = []
                for comp in comps:
                    if (comp.startswith('Name=') or comp.startswith('locus_tag=')) and not comp.startswith('Name=ID'):
                        try:
                            label, candidate_name = comp.split('=')
                            candidate_gene_names.append(candidate_name)
                        except ValueError:
                            print(comp)
                            raise
                try:
                    final_gene_name = candidate_gene_names[0]
                    #print(final_gene_name)
                except IndexError:
                    continue
                cur.execute('select chrom from genes where name=%s', [final_gene_name])
                for row in cur.fetchall():
                    old_chrom = row[0]
                    if old_chrom is None or old_chrom == '':
                        print("%s -> %s %s-%s" % (final_gene_name, chrom, start, stop))
                        cur.execute('update genes set chrom=%s, start_pos=%s, end_pos=%s where name=%s',
                                    [chrom, start, stop, final_gene_name])
                conn.commit()

if __name__ == '__main__':
    conn = mysql.connector.connect(host="127.0.0.1", port=3306, user='root',
                                   database='halodata')
    fix_missing_positions(conn)
    conn.close()
