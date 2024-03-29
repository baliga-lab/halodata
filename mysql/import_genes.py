#!/usr/bin/env python3

import mysql.connector
from collections import defaultdict
import traceback as tb

import db_add_missing_locations as fix_loc

HALO_UNIPROT_PATH = "uniprot-compressed_true_download_true_fields_accession_2Cgene_primar-2022.07.21-16.43.57.65.tsv"
#HALO_UNIPROT_PATH = 'Halo_uniprot-taxonomy_64091.csv'

UP_ID_IDX = 0
UP_GENE_SYMBOL_IDX = 1
UP_LOCUS_TAG_IDX = 2
UP_PATHWAY_IDX = 3
UP_GO_BIO_IDX = 4
UP_GO_CELL_IDX = 5
UP_GO_MOL_IDX = 6
UP_STRING_IDX = 7
UP_EGGNOG_IDX = 8
UP_ORTHODB_IDX = 9
UP_UNIPATHWAY_IDX = 10
UP_CDD_IDX = 11
UP_PROSITE_IDX = 12
UP_SMART_IDX = 13
UP_PFAM_IDX = 14
UP_INTERPRO_IDX = 15
UP_GENE_NAMES_IDX = 16


def dbconn():
    return mysql.connector.connect(host="127.0.0.1", port=3306, user='root', database='halodata')

def read_synonyms():
    dict_data = {}  # synonyms
    with open('alan_data/dictionary.tsv') as infile:
        infile.readline()
        for line in infile:
            name, product, locus_tag = line.strip().split('\t')
            locus_tags = locus_tag.split(',')
            dict_data[name] = { 'product': product, 'locus_tags': list(sorted(set(locus_tags))) }
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
    symbol_map = defaultdict(list)
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
            if symbol is not None:
                symbol_map[rep].append(symbol)
    return cog_map, gene2cog, symbol_map


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


def import_genes(conn, gene_info_map):
    synonyms = read_synonyms()
    seqs = read_sequences()
    symbol_map1 = read_symbolmap()
    cog_map, gene2cog, symbol_map2 = read_cog_data()
    final_symbol_map = merge_symbol_maps(symbol_map1, symbol_map2)
    is_map, gene2is = read_is_info()
    locus_tag_map = {}

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
            # this is a hack to append RNAse to a known gene
            if gene == 'VNG_2099C':
                product += ', RNAse'
            elif gene == 'VNG_1496G':
                product += ', SmAP1'
            locus_tags = synonyms[gene]['locus_tags']
            try:
                gene_symbol = final_symbol_map[gene]
                """
                gene_symbols = set(symbol_map[gene])
                if len(gene_symbols) > 1:
                    print('more than one symbol for %s' % gene)
                    print(gene_symbols)
                gene_symbol = list(gene_symbols)[0]"""
            except KeyError:
                gene_symbol = None

            if gene in gene2cog:
                cog_id = gene2cog[gene]['cog_id']
                cog_pk = cog_id_map[cog_id]
            else:
                cog_id = None
            if gene in gene2is:
                is_name = gene2is[gene]
            else:
                is_name = None

            try:
                gene_info = gene_info_map[gene]
            except:
                gene_info = {'gene_symbol': '',
                             'chrom': '', 'start': 0,
                             'stop': 0, 'strand': ''}

            if cog_id is not None and is_name is not None:
                cur.execute('insert into genes (name,gene_symbol,product,cog_id,is_id,sequence,chrom,start_pos,end_pos,strand) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                            [gene, gene_symbol, product, cog_pk, is_id_map[is_name], seq,
                             gene_info['chrom'], gene_info['start'],
                             gene_info['stop'], gene_info['strand']
                             ])
            elif cog_id is not None and is_name is None:
                cur.execute('insert into genes (name,gene_symbol,product,cog_id,sequence,chrom,start_pos,end_pos,strand) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                            [gene, gene_symbol, product, cog_pk, seq,
                             gene_info['chrom'], gene_info['start'],
                             gene_info['stop'], gene_info['strand']
                             ])

            elif cog_id is None and is_name is None:
                cur.execute('insert into genes (name,gene_symbol,product,sequence,chrom,start_pos,end_pos,strand) values (%s,%s,%s,%s,%s,%s,%s,%s)',
                            [gene, gene_symbol, product, seq,
                             gene_info['chrom'], gene_info['start'],
                             gene_info['stop'], gene_info['strand']
                             ])
            elif cog_id is None and is_name is not None:
                cur.execute('insert into genes (name,gene_symbol,product,is_id,sequence,chrom,start_pos,end_pos,strand) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                            [gene, gene_symbol, product, is_id_map[is_name], seq,
                             gene_info['chrom'], gene_info['start'],
                             gene_info['stop'], gene_info['strand']
                             ])

            gene_id = cur.lastrowid
            for locus_tag in locus_tags:
                # add all LOCUS TAGS for that gene (TODO)
                # should not exist
                if locus_tag in locus_tag_map:
                    locus_tag_id = locus_tag_map[locus_tag]
                else:
                    cur.execute('insert into locus_tags (name) values (%s)', [locus_tag])
                    locus_tag_id = cur.lastrowid
                    locus_tag_map[locus_tag] = locus_tag_id
                cur.execute('insert into gene_locus_tags (gene_id,locus_tag_id) values (%s,%s)',
                            [gene_id, locus_tag_id])

        conn.commit()

def read_gene_tracks():
    gene_track_map = {}
    with open('genes.tsv') as infile:
        for line in infile:
            gene_symbol, locus_tag, chrom, start, stop, strand = line.strip().split('\t')
            gene_track_map[locus_tag] = {'gene_symbol': gene_symbol,
                                         'chrom': chrom, 'start': start,
                                         'stop': stop, 'strand': strand}
    return gene_track_map


def mark_extra_genes(conn):
    """Update the genes that have no locus tag as extra gene"""
    with conn.cursor() as cur:
        cur.execute('select id,name from genes')
        for gene_id, gene_name in cur.fetchall():
            cur2 = conn.cursor()
            cur2.execute('select lt.name from locus_tags lt join gene_locus_tags glt on lt.id=glt.locus_tag_id join genes g on g.id=glt.gene_id where g.id=%s', [gene_id])
            num_olds = 0
            for row in cur2.fetchall():
                name = row[0]
                if name.startswith('VNG') and not name.startswith('VNG_'):
                    num_olds += 1
            if num_olds == 0:
                cur2.execute('update genes set is_extra=1 where id=%s', [gene_id])
        conn.commit()


def import_extra_genes(conn, gene_track_map):
    num_extras = 0
    with conn.cursor() as cur:
        for locus_tag, info in gene_track_map.items():
            cur.execute('select count(*) from genes where name=%s', [locus_tag])
            count = cur.fetchone()[0]
            if count == 0:
                print('locus_tag not found: %s' % locus_tag)
                num_extras += 1
                cur.execute('insert into genes (name,gene_symbol,chrom,start_pos,end_pos,strand,is_extra) values (%s,%s,%s,%s,%s,%s,%s)',
                            [locus_tag, info['gene_symbol'], info['chrom'],
                             info['start'], info['stop'], info['strand'], 1])
        conn.commit()
    print('num extras found: %d' % num_extras)


def read_symbolmap():
    symbol_map = defaultdict(list)
    with open(HALO_UNIPROT_PATH) as infile:
        # The gene names fiield has EVERYTHING !!!!
        header = infile.readline()
        for line in infile:
            comps = line.strip().split('\t')
            try:
                gene_names = comps[UP_GENE_NAMES_IDX]
                gcomps = gene_names.strip().split()
                locus_tags = []
                symbols = []
                for comp in gcomps:
                    if comp.startswith('VNG_'):
                        locus_tags.append(comp)
                    elif not comp.startswith('VNG'):
                        symbols.append(comp)
                for locus_tag in locus_tags:
                    for symbol in symbols:
                        symbol_map[locus_tag].append(symbol)
            except IndexError:
                pass
    return symbol_map

def update_crossrefs(conn):
    lt2uniprot = {}
    lt2string = {}
    symbol_map = {}
    with open(HALO_UNIPROT_PATH) as infile:
        headers = infile.readline().strip().split('\t')
        print(list(zip(headers, range(len(headers)))))

        linenum = 0
        # every locus tag has at most one uniprot id
        for line in infile:
            linenum += 1
            comps = line.strip().split('\t')
            uniprot_id = comps[UP_ID_IDX]

            try:
                string_str = comps[UP_STRING_IDX]
                string_comps = [sc for sc in string_str.split(';') if len(sc) > 0]
                #print(string_comps)
            except IndexError:
                continue  # skip this entry

            if len(string_comps) > 1:
                raise Exception('more than 1 STRING !!')

            try:
                locus_tag_str = comps[UP_LOCUS_TAG_IDX]
                if len(locus_tag_str.strip()) > 0:
                    locus_tags = [lt.strip() for lt in locus_tag_str.split(';')]
                    for lt in locus_tags:
                        if not lt in lt2uniprot:
                            lt2uniprot[lt] = uniprot_id
                        else:
                            raise Exception("I'm double UNIPROT !!!")

                        if not lt in lt2string:
                            lt2string[lt] = string_comps[0]
                        else:
                            raise Exception("I'm double STRING")
                    #print(locus_tags)
            except IndexError:
                continue  # skip this entry

    print(lt2string.keys())
    with conn.cursor() as cur:
        for lt, uniprot_id in lt2uniprot.items():
            cur.execute('update genes set uniprot_id=%s where name=%s', [uniprot_id, lt]);

        for lt, string_id in lt2string.items():
            cur.execute('update genes set string_id=%s where name=%s', [string_id, lt]);
        conn.commit()

def process_uniprot_field(conn, uniprot_id, comp, table_name, relation_table, idmap):
    comp = comp.strip('"')
    values = [value.strip() for value in comp.split(';') if len(value) > 0]
    with conn.cursor() as cur:
        for value in values:
            if value in idmap:
                pk = idmap[value]
            else:
                cur.execute('insert into ' + table_name + ' (name) values (%s)', [value])
                pk = cur.lastrowid
                idmap[value] = pk
            cur.execute('select id from genes where uniprot_id=%s', [uniprot_id])
            row = cur.fetchone()
            if row is not None:
                gene_id = row[0]
                cur.execute('insert into ' + relation_table + ' values (%s,%s)', [gene_id, pk])

def process_uniprot_field_single(conn, uniprot_id, compstr, field):
    compstr.strip('"')
    comps = [value.strip() for value in compstr.split(';') if len(value) > 0]
    if len(comps) > 1:
        raise Execption('Too many values (more than one) in field %s' % field)
    if len(comps) > 0:
        with conn.cursor() as cur:
            cur.execute('update genes set ' + field + '=%s where uniprot_id=%s', [comps[0], uniprot_id])

def update_crossrefs2(conn):
    """update based on UniprotID"""
    pathway2id = {}
    gobio2id = {}
    gocell2id = {}
    gomol2id = {}
    unipathway2id = {}
    cdd2id = {}
    prosite2id = {}
    smart2id = {}
    pfam2id = {}
    interpro2id = {}

    with open(HALO_UNIPROT_PATH) as infile:
        infile.readline()  # skip header
        linenum = 0
        # every locus tag has at most one uniprot id
        for line in infile:
            linenum += 1
            comps = line.strip().split('\t')
            uniprot_id = comps[UP_ID_IDX]

            # insert pathways
            try:
                process_uniprot_field(conn, uniprot_id, comps[UP_PATHWAY_IDX], 'pathways', 'gene_pathways', pathway2id)
            except IndexError:
                continue  # skip this entry
            try:
                process_uniprot_field(conn, uniprot_id, comps[UP_GO_BIO_IDX], 'go_bio', 'gene_go_bio', gobio2id)
            except IndexError:
                continue  # skip this entry
            try:
                process_uniprot_field(conn, uniprot_id, comps[UP_GO_CELL_IDX], 'go_cell', 'gene_go_cell', gocell2id)
            except IndexError:
                continue  # skip this entry
            try:
                process_uniprot_field(conn, uniprot_id, comps[UP_GO_MOL_IDX], 'go_mol', 'gene_go_mol', gomol2id)
            except IndexError:
                continue  # skip this entry
            try:
                process_uniprot_field_single(conn, uniprot_id, comps[UP_ORTHODB_IDX], 'orthodb_id')
            except IndexError:
                continue  # skip this entry
            try:
                process_uniprot_field(conn, uniprot_id, comps[UP_UNIPATHWAY_IDX], 'uni_pathways', 'gene_uni_pathways', unipathway2id)
            except IndexError:
                continue  # skip this entry
            try:
                process_uniprot_field(conn, uniprot_id, comps[UP_CDD_IDX], 'cdd_refs', 'gene_cdd_refs', cdd2id)
            except IndexError:
                continue  # skip this entry
            try:
                process_uniprot_field(conn, uniprot_id, comps[UP_PROSITE_IDX], 'prosite_refs', 'gene_prosite_refs', prosite2id)
            except IndexError:
                continue  # skip this entry
            try:
                process_uniprot_field(conn, uniprot_id, comps[UP_SMART_IDX], 'smart_refs', 'gene_smart_refs', smart2id)
            except IndexError:
                continue  # skip this entry
            try:
                process_uniprot_field(conn, uniprot_id, comps[UP_PFAM_IDX], 'pfam_refs', 'gene_pfam_refs', pfam2id)
            except IndexError:
                continue  # skip this entry
            try:
                process_uniprot_field(conn, uniprot_id, comps[UP_INTERPRO_IDX], 'interpro_refs', 'gene_interpro_refs', interpro2id)
            except IndexError:
                continue  # skip this entry

    conn.commit()

def merge_symbol_maps(symbol_map1, symbol_map2):
    """merge symbol mappings from cog and uniprot, always prefer Uniprot mappings
    """
    final_symbol_map = {}
    keys1 = sorted(symbol_map1.keys())
    keys2 = sorted(symbol_map2.keys())
    all_keys = set(keys1 + keys2)
    #print("keys1: %d elems, keys2: %d elems all_keys: %d elems" % (len(keys1), len(keys2), len(all_keys)))
    for key in sorted(all_keys):
        try:
            symbol1 = symbol_map1[key][0]
        except KeyError:
            symbol1 = None
        except IndexError:
            symbol1 = None
        symbols2 = symbol_map2[key]
        if len(symbols2) > 0:
            symbol2 = symbols2[0]
        else:
            symbol2 = None
        """
        if symbol1 != symbol2:
            print("MISMATCH: %s [%s] != [%s]" % (key, symbol1, symbol2))
        else:
            print("MATCH: %s [%s] != [%s]" % (key, symbol1, symbol2))
        """
        # Always favor the uniprot symbols
        if symbol1 is not None:
            final_symbol_map[key] = symbol1
        elif symbol2 is not None:
            final_symbol_map[key] = symbol2

    return final_symbol_map


if __name__ == '__main__':
    """
    symbol_map1 = read_symbolmap()
    cog_map, gene2cog, symbol_map2 = read_cog_data()
    final_symbol_map = merge_symbol_maps(symbol_map1, symbol_map2)
    for key, value in final_symbol_map.items():
        print('%s\t%s' % (key, value))"""

    gene_track_map = read_gene_tracks()
    conn = dbconn()
    import_genes(conn, gene_track_map)
    with conn.cursor() as cur:
        cur.execute('select count(*) from genes')
        num_genes = cur.fetchone()[0]
        print("# genes imported: ", num_genes)
    mark_extra_genes(conn)
    import_extra_genes(conn, gene_track_map)

    update_crossrefs(conn)
    update_crossrefs2(conn)
    fix_loc.fix_missing_positions(conn)
    conn.close()
