#!/usr/bin/env python3

import mysql.connector

def dbconn():
    return mysql.connector.connect(host="127.0.0.1", port=3306, user='root', database='halodata')

def read_synonyms():
    dict_data = {}  # synonyms
    with open('alan_data/dictionary.tsv') as infile:
        infile.readline()
        for line in infile:
            name, product, locus_tag = line.strip().split('\t')
            locus_tags = locus_tag.split(',')
            dict_data[name] = { 'product': product, 'locus_tags': locus_tags }
    return dict_data

def read_sequences():
    # read sequences from fasta
    gene_seqs = {}
    with open('alan_data/Hsalinarum_nrtx.fa') as infile:
        gene_name = None
        seq = None
        for line in infile:
            line = line.strip()
            if line.startswith('>'):
                if gene_name is not None:
                    gene_seqs[gene_name] = seq

                gene_name = line[1:]
                seq = ''
            else:
                seq += line
    return gene_seqs

def read_cog_data():
    cog_map = {}
    gene2cog = {}
    with open('alan_data/cog.tsv') as infile:
        infile.readline()
        for line in infile:
            rep, symbol, cog_id, cog_name, cog_cat, pathway = line.strip().split('\t')
            if symbol == 'Undefined':
                symbol = None
            gene2cog[rep] = {'cog_id': cog_id, 'symbol': symbol}

            if pathway == 'Undefined':
                pathway = None
            cog_map[cog_id] = {'name': cog_name, 'category': cog_cat, 'pathway': pathway}
    return cog_map, gene2cog


def read_is_info():
    with open('alan_data/is_info.tsv') as infile:
        infile.readline()
        is_map = {}
        gene2is = {}
        for line in infile:
            rep, name, family, subgroup = line.strip().split()
            is_map[name] = {'family': family, 'subgroup': subgroup}
            gene2is[rep] = name
    return is_map, gene2is


def import_insertion_sequences(conn, is_map):
    is_id_map = {}
    with conn.cursor() as cur:
        for is_name, is_value in is_map.items():
            family = is_value['family']
            subgroup = is_value['subgroup']
            if subgroup != 'NA':
                cur.execute('insert into insertion_sequences (name, family, subgroup) values (%s,%s,%s)',
                            [is_name, family, subgroup])
            else:
                cur.execute('insert into insertion_sequences (name,family) values (%s,%s)',
                            [is_name, family])
            pk = cur.lastrowid
            is_id_map[is_name] = pk
        conn.commit()
    return is_id_map

def import_cog_data(conn, cog_map):
    cog_id_map = {}
    cog_categories = set()
    cog_pathways = set()
    category_ids = {}
    pathway_ids = {}
    for cog_id, cog_values in cog_map.items():
        cog_categories.add(cog_values['category'])
        if cog_values['pathway'] is not None:
            cog_pathways.add(cog_values['pathway'])

    with conn.cursor() as cur:
        for cat in cog_categories:
            cur.execute('insert into cog_categories (name) values (%s)', [cat])
            category_ids[cat] = cur.lastrowid
        for pathway in cog_pathways:
            cur.execute('insert into cog_pathways (name) values (%s)', [pathway])
            pathway_ids[pathway] = cur.lastrowid

        for cog_id, cog_values in cog_map.items():
            pathway = cog_values['pathway']
            category = cog_values['category']
            if pathway is None:
                cur.execute('insert into cog (name,cog_name,cog_category_id) values (%s,%s,%s)',
                            [cog_id, cog_values['name'], category_ids[category]])
            else:
                cur.execute('insert into cog (name,cog_name,cog_category_id,cog_pathway_id) values (%s,%s,%s,%s)',
                            [cog_id, cog_values['name'], category_ids[category], pathway_ids[pathway]])
            cog_id_map[cog_id] = cur.lastrowid
        conn.commit()

    return cog_id_map


def import_genes(conn):
    synonyms = read_synonyms()
    seqs = read_sequences()
    cog_map, gene2cog = read_cog_data()
    is_map, gene2is = read_is_info()

    # integrity check
    num_genes = len(seqs)
    missing_cog = 0
    missing_is = 0
    for name in seqs:
        if name not in synonyms:
            print("no synomym for '%s'" % name)
        if name not in gene2cog:
            missing_cog += 1
        if name not in gene2is:
            missing_is += 1
    print("no cog for %d out of %d" % (missing_cog, num_genes))
    print("no is for %d out of %d" % (missing_is, num_genes))

    is_id_map = import_insertion_sequences(conn, is_map)
    cog_id_map = import_cog_data(conn, cog_map)
    print(cog_id_map)
    with conn.cursor() as cur:
        for gene, seq in seqs.items():
            # isolate the vng name
            product = synonyms[gene]['product']
            locus_tags = synonyms[gene]['locus_tags']
            for locus_tag in locus_tags:
                if locus_tag.startswith('VNG') and not locus_tag.startswith('VNG_'):
                    vng_name = locus_tag

            if gene in gene2cog:
                cog_id = gene2cog[gene]['cog_id']
                cog_pk = cog_id_map[cog_id]
            else:
                cog_id = None
            if gene in gene2is:
                is_name = gene2is[gene]
            else:
                is_name = None

            if cog_id is not None and is_name is not None:
                cur.execute('insert into genes (name,old_name,product,cog_id,is_id,sequence) values (%s,%s,%s,%s,%s,%s)',
                            [gene, vng_name, product, cog_pk, is_id_map[is_name], seq])
            elif cog_id is not None and is_name is None:
                cur.execute('insert into genes (name,old_name,product,cog_id,sequence) values (%s,%s,%s,%s,%s)',
                            [gene, vng_name, product, cog_pk, seq])

            elif cog_id is None and is_name is None:
                cur.execute('insert into genes (name,old_name,product,sequence) values (%s,%s,%s,%s)',
                            [gene, vng_name, product, seq])
        conn.commit()

if __name__ == '__main__':
    conn = dbconn()
    import_genes(conn)
    with conn.cursor() as cur:
        cur.execute('select count(*) from genes')
        num_genes = cur.fetchone()[0]
        print("Hello: ", num_genes)
    conn.close()
