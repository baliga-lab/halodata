#!/usr/bin/env python3

import json
import os
import traceback
import pyodbc
from collections import defaultdict

import mysql.connector

from flask import Flask, render_template, jsonify, Response, abort
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)
app.config.from_envvar('APP_SETTINGS')

HALO_ID = 4


def mysql_conn():
    return mysql.connector.connect(host=app.config['MYSQL_HOST'],
                                   user=app.config['MYSQL_USER'],
                                   password=app.config['MYSQL_PASS'],
                                   database=app.config['MYSQL_DB'])

def dbconn(dbname):
    driver = 'FreeTDS'
    """
    return  pymssql.connect(server=app.config['DBSERVER'], port=1433,
                            user=app.config['DBUSER'], password=app.config['DBPASS'],
                            database=dbname)"""
    conn_str = 'DRIVER=%s;SERVER=%s;PORT=1433;DATABASE=%s;UID=%s;PWD=%s' % (driver,
                                                                           app.config['DBSERVER'], dbname,
                                                                           app.config['DBUSER'],
                                                                           app.config['DBPASS'])
    print(conn_str)
    return pyodbc.connect(conn_str)

@app.route('/')
def index():
    return "<p>Hello !</p>"


@app.route('/gene_info/<gene>')
def gene_info(gene):
    conn = mysql_conn()
    result = []
    with conn.cursor() as cur:
        if gene.startswith('VNG_'):
            # search by gene name
            q = """select id from genes where name=%s"""
        else:
            # search by locus tag
            q = """select distinct g.id
                   from genes g
                     join gene_locus_tags glt on g.id=glt.gene_id
                     join locus_tags lt on lt.id=glt.locus_tag_id
                   where lt.name=%s"""
        cur.execute(q, [gene])
        gene_id = None
        for row in cur.fetchall():
            gene_id = row[0]
            break

        range_buckets = make_range_buckets()
        query = """select
                     g.name,g.gene_symbol,g.is_extra,g.product,g.chrom,g.start_pos,g.end_pos,
                     c.name as cog_id,cc.name as cog_category,cp.name as cog_pathway,
                     ins.name as ins_name,ins.family as ins_family,ins.subgroup as ins_subgroup
                   from genes g
                     left outer join cog c on g.cog_id=c.id
                     left outer join cog_categories cc on c.cog_category_id=cc.id
                     left outer join cog_pathways cp on c.cog_pathway_id=cp.id
                     left outer join insertion_sequences ins on g.is_id=ins.id
                   where g.id=%s"""
        cur.execute(query, [gene_id])
        for gene,gene_symbol,is_extra,product,chrom,start_pos,end_pos,cog_id,ccat,cpathway,ins_name,ins_family,ins_subgroup in cur.fetchall():
            igv_loc = make_igv_loc(chrom, start_pos, end_pos)
            track_range = make_track_range(range_buckets, chrom, start_pos, end_pos)
            entry = {'is_extra': is_extra, 'gene': gene, 'gene_symbol': gene_symbol,
                     'cog_id': cog_id, 'cog_category': ccat, 'chrom': chrom,
                     'start_pos': start_pos, 'end_pos': end_pos, 'product': product,
                     'igv_loc': igv_loc, 'track_range': track_range}

            # attach additional information
            print(entry)
            if cpathway is not None:
                entry['cog_pathway'] = cpathway
            if ins_name is not None:
                entry['ins_name'] = ins_name
                entry['ins_family'] = ins_family
                entry['ins_subgroup'] = ins_subgroup
            result.append(entry)
        q = """select lt.name from locus_tags lt join gene_locus_tags glt on lt.id=glt.locus_tag_id join genes g on g.id=glt.gene_id
               where g.id=%s"""
        cur.execute(q, [gene_id])
        for row in cur.fetchall():
            if row[0].startswith('VNG') and not row[0].startswith('VNG_'):
                entry['locus_tag'] = row[0]
    print(result)
    if len(result) == 0:
        abort(404)
    return jsonify(results=result)


TRACK_RANGES = [
  'NC_002607.1:0-223804',
  'NC_002607.1:223805-447608',
  'NC_002607.1:447609-671413',
  'NC_002607.1:671414-895217',
  'NC_002607.1:895218-1119021',
  'NC_002607.1:1119022-1342825',
  'NC_002607.1:1342826-1566630',
  'NC_002607.1:1566631-1790434',
  'NC_002607.1:1790435-2014238',
  'NC_001869.1:0-21261',
  'NC_001869.1:21262-42521',
  'NC_001869.1:42522-63782',
  'NC_001869.1:63783-85042',
  'NC_001869.1:85043-106303',
  'NC_001869.1:106304-127563',
  'NC_001869.1:127564-148824',
  'NC_001869.1:148825-170084',
  'NC_001869.1:170085-191345',
  'NC_002608.1:0-40603',
  'NC_002608.1:40604-81205',
  'NC_002608.1:81206-121808',
  'NC_002608.1:121809-162411',
  'NC_002608.1:162412-203013',
  'NC_002608.1:203014-243616',
  'NC_002608.1:243617-284219',
  'NC_002608.1:284220-324821',
  'NC_002608.1:324822-365424',
]

RANGE_BUCKETS = [
    (0, 107126),
    (107127, 214253),
    (214254, 321379),
    (321380, 428506),
    (428507, 535632),
    (535633, 642758),
    (642759, 749885),
    (749886, 857011),
    (857012, 964137),
    (964138, 1071264),
    (1071265, 1178390),
    (1178391, 1285516),
    (1285517, 1392643),
    (1392644, 1499769),
    (1499770, 1606896),
    (1606897, 1714022),
    (1714023, 1821148),
    (1821149, 1928275),
    (1928276, 2035401),
    (2035402, 2142528),
    (2142529, 2249654),
    (2249655, 2356780),
    (2356781, 2463907),
    (2463908, 2571033)
]

@app.route('/annotations/<gene>')
def annotations(gene):
    conn = dbconn('ProteinStructure2')
    cursor = conn.cursor()
    cursor.execute('select biosequence_desc,gene_symbol,full_gene_name,aliases,functional_description from biosequence_annotation ba join biosequence bs on ba.biosequence_id=bs.biosequence_id where full_gene_name=?', gene)
    result = []
    for bs_desc,gene_symbol,full_gene_name,aliases,functional_description in cursor.fetchall():
        desc_comps = bs_desc.split('" ')
        print(bs_desc)
        for comp in desc_comps:
            if comp.startswith('location'):
                coords = comp.split('=')[1].strip('"')
        result.append({'location': coords, 'gene_symbol': gene_symbol, 'full_gene_name': full_gene_name,
                       'aliases': aliases, 'functional_description': functional_description})

    return jsonify(annotations=result, num_annotations=len(result))


@app.route('/microarray_data/<gene>')
def microarray_data(gene):
    conn = dbconn('microarray3')
    cursor = conn.cursor()
    cursor.execute('select cc.condition_name,ge.common_name,ge.canonical_name,log10_ratio,lambda from gene_expression ge join comparison_condition cc on ge.condition_id=cc.condition_id where canonical_name=?', gene)
    result = []
    for cond_name,common_name,canonical_name,log10,lambdaval in cursor.fetchall():
        result.append({'condition': cond_name,
                       'common_name': common_name,
                       'canonical_name': canonical_name,
                       'log10_ratio': log10,
                       'lambda': lambdaval})

    return jsonify(expressions=result, num_expressions=len(result))


@app.route('/download_microarray_data/<gene>')
def download_microarray_data(gene):
    conn = dbconn('microarray3')
    cursor = conn.cursor()
    cursor.execute('select cc.condition_name,ge.common_name,ge.canonical_name,log10_ratio,lambda from gene_expression ge join comparison_condition cc on ge.condition_id=cc.condition_id where canonical_name=?', gene)
    result = "Condition,Log10 Ratio,Lambda\n"
    for cond_name,common_name,canonical_name,log10,lambdaval in cursor.fetchall():
        result += "%s,%s,%s\n" % (cond_name, str(log10), str(lambdaval))
    return Response(result,
                    mimetype="text/plain",
                    headers={'Content-Disposition': "attachment;filename=%s_microarray.csv" % gene})

"""
Check if the transcript link exists
http://networks.systemsbiology.net/projects/halo/transcript_structure/VNG0002G.pdf
"""

# Size of the IGV display window is +/- IGV_MARGIN
IGV_MARGIN = 5000

def make_range_buckets():
    result = defaultdict(list)
    for entry in TRACK_RANGES:
        chrom, interval = entry.split(':')
        start, stop = interval.split('-')
        start = int(start)
        stop = int(stop)
        result[chrom].append((start, stop))
    return result

@app.route('/proteinstructure/<gene>')
def protein_structure(gene):
    """
    Note: COG Retrieve the protein id from
    https://www.ncbi.nlm.nih.gov/research/cog/api/cog/?cog=COG1136&organism=Halobacterium_salinarum_NRC-1_ATCC_700922&format=json
    can map to multiple: !!!
    prot_id = res['results'][x]['protein']['name']

    We could add footnote links with documentation where they lead to
    Example link:
    https://www.ncbi.nlm.nih.gov/protein/WP_010902558.1


    Genbank

    http://www.ncbi.nlm.nih.gov/sutils/blink.cgi?pid=15789342
    """
    # Set id 2 = Amino acid, 5 = DNA
    range_buckets = make_range_buckets()
    conn = dbconn('ProteinStructure2')
    cursor = conn.cursor()
    cursor.execute('select biosequence_id,biosequence_set_id,biosequence_gene_name,biosequence_desc,biosequence_seq from biosequence where biosequence_name=?', gene)
    result = []
    pstruct = {}
    chr_map = {'Chromosome': 'NC_002607.1',
               'pNRC100': 'NC_001869.1', 'pNRC200': 'NC_002608.1' }
    for bs_id,set_id,common_name,desc,seq in cursor.fetchall():
        n = 60
        seq_chunks = [seq[i:i+n] for i in range(0, len(seq), n)]
        seq = '\n'.join(seq_chunks)
        if set_id == 5:
            pstruct['dna'] = seq
        else:
            pstruct['peptide'] = seq
        pstruct['common_name'] = common_name
        #pstruct['desc'] = desc
        # split up the description
        desc_comps = desc.split('" ')
        for comp in desc_comps:
            key, value = comp.split('=')
            value = value.replace('"', '')
            pstruct[key] = value
            if key == 'location':
                loc_comps = value.split(' ')
                chr_id = chr_map[loc_comps[0]]
                left = int(loc_comps[1])
                right = int(loc_comps[2])
                igv_loc = make_igv_loc(chr_id, left, right)
                pstruct['igv_loc'] = igv_loc
                pstruct['track_range'] = make_track_range(range_buckets, chr_id, left, right)

    return jsonify(result=pstruct)


def make_igv_loc(chrom, left, right):
    left = left - IGV_MARGIN
    left = max(1, left)
    right = right + IGV_MARGIN
    return '%s:%d-%d' % (chrom, left, right)


def make_track_range(range_buckets, chrom, left, right):
    for r in range_buckets[chrom]:
        if left >= r[0] and left <= r[1]:
            return '%s-%d-%d' % (chrom, r[0], r[1])
    return ''


@app.route('/genes')
def genes():
    conn = dbconn('microarray3')
    cursor = conn.cursor()
    cursor.execute('select distinct biosequence_name from biosequence where organism_id=?', HALO_ID)
    result = []
    for row in cursor.fetchall():
        result.append(row[0])

    return jsonify(genes=result, num_genes=len(result))


def _old_name_from_locus_tags(locus_tags):
    locus_tag_list = locus_tags.split(',')
    for lt in locus_tag_list:
        if lt.startswith('VNG') and not lt.startswith('VNG_'):
            return lt
    return ''


@app.route('/locus_tag_entries')
def locus_tag_entries():
    conn = mysql_conn()
    cursor = conn.cursor()
    #cursor.execute('select name,product,old_name from genes order by name')
    cursor.execute('select g.name,g.product,group_concat(lt.name) from genes g join gene_locus_tags glt on g.id=glt.gene_id join locus_tags lt on glt.locus_tag_id=lt.id group by g.name order by g.name')

    result = []
    for name, product, locus_tags in cursor.fetchall():
        old_name = _old_name_from_locus_tags(locus_tags)
        locus_tags = locus_tags.split(',')
        result.append({'representative': name, 'old_name': old_name, 'product': product,
                       'locus_tag': locus_tags})

    return jsonify(entries=result, num_entries=len(result))


@app.route('/cog_info_entries')
def cog_info_entries():
    conn = mysql_conn()
    cursor = conn.cursor()
    cursor.execute('select g.name,c.name,c.cog_name,cc.name,cp.name,group_concat(lt.name) from genes g join cog c on g.cog_id=c.id join cog_categories cc on c.cog_category_id=cc.id join cog_pathways cp on c.cog_pathway_id=cp.id join gene_locus_tags glt on glt.gene_id=g.id join locus_tags lt on lt.id=glt.locus_tag_id group by g.name order by g.name')
    result = []
    for gene, cog_id, cog_name, category_name, pathway_name, locus_tags in cursor.fetchall():
        cog_ids = cog_id.split('|')
        result.append({'representative': gene, 'cog_id': cog_id, 'cog_name': cog_name,
                       'cog_category': category_name, 'cog_pathway': pathway_name,
                       'old_name': _old_name_from_locus_tags(locus_tags),
                       'cog_ids': cog_ids})

    return jsonify(entries=result, num_entries=len(result))


@app.route('/is_info_entries')
def is_info_entries():
    conn = mysql_conn()
    cursor = conn.cursor()
    cursor.execute('select g.name,ins.name,ins.family,ins.subgroup,group_concat(lt.name) from genes g join insertion_sequences ins on g.is_id=ins.id join gene_locus_tags glt on glt.gene_id=g.id join locus_tags lt on lt.id=glt.locus_tag_id group by g.name order by g.name')
    result = []
    for gene, ins_name, ins_family, ins_subgroup, locus_tags in cursor.fetchall():
        result.append({'representative': gene, 'is_name': ins_name, 'is_family': ins_family,
                       'is_subgroup': ins_subgroup, 'old_name': _old_name_from_locus_tags(locus_tags)})

    return jsonify(entries=result, num_entries=len(result))


@app.route('/search2/<search_term>')
def solr_search(search_term):
    solr_url = app.config['SOLR_QUERY_URL']
    solr_url += '?q=all:' + search_term
    print("QUERY: " + solr_url)
    r = requests.get(solr_url)
    solr_result = r.json()
    total = solr_result['response']['numFound']
    start = solr_result['response']['start']
    solr_docs = solr_result['response']['docs']
    print(solr_docs)
    result = []
    for doc in solr_docs:

        ## ADD MISSING FIELDS TODO
        try:
            func_desc = doc['functional_description']
        except:
            func_desc = ''
        try:
            aliases = doc['aliases']
        except:
            aliases = ''
        try:
            gene_symbol = doc['gene_symbol']
        except:
            gene_symbol = ''
        try:
            product = doc['product']
        except:
            product = ''
        result.append({'location': '',
                       'gene_symbol': gene_symbol,
                       'new_name': doc['id'],
                       'full_gene_name': doc['locus_tag'],
                       'product': product,
                       'aliases': aliases, 'functional_description': func_desc})

    return jsonify(results=result, num_results=len(result), total=total, start=start)


@app.route('/autocomplete/<search_term>')
def autocomplete(search_term):
    """
    http://localhost:8983/solr/halodata/suggest?suggest=true&suggest.build=true&suggest.dictionary=mySuggester&wt=json&suggest.q=VNG000    """
    solr_url = app.config['SOLR_SUGGEST_URL']
    solr_url += 'suggest.q=' + search_term
    print(solr_url)
    r = requests.get(solr_url)
    solr_result = r.json()
    suggest_result = solr_result['suggest']['mySuggester'][search_term]
    #count = suggest_result['num_found']
    entries = []
    terms_set = set()
    for s in suggest_result['suggestions']:
        term = s['term']
        terms = term.split(',')
        for t in terms:
            terms_set.add(t)
    entries = [{'Description': t} for t in sorted(terms_set)]
    count = len(entries)
    return jsonify(count=count, entries=entries)

@app.route('/search/<search_term>')
def search(search_term):
    """We need a more secure way to build the IN clause"""
    search_terms = search_term.split()
    print(search_terms)
    plain_search_terms = [term for term in search_terms if not '*' in term]
    wildcard_search_terms = [term for term in search_terms if '*' in term]
    newname_search_terms = [term for term in search_terms if term.startswith('VNG_')]
    newname_search_terms = ["'%s'" % term for term in newname_search_terms]  # quote them
    newname_search_term_list = ('(' + ','.join(newname_search_terms) + ')')

    mysqlconn = mysql_conn()
    if len(newname_search_terms) > 0:
        with mysqlconn.cursor() as cur:
            query = 'select old_name from genes where name in ' + newname_search_term_list
            print(query)
            cur.execute(query)
            for row in cur.fetchall():
                plain_search_terms.append(row[0])

    plain_search_terms = ["'%s'" % term for term in plain_search_terms]
    plain_search_term_list = ('(' + ','.join(plain_search_terms) + ')')

    conn = dbconn('ProteinStructure2')
    cursor = conn.cursor()
    #cursor.execute('select biosequence_desc,gene_symbol,full_gene_name,aliases,functional_description from biosequence_annotation ba join biosequence bs on ba.biosequence_id=bs.biosequence_id where full_gene_name=?', search_term)
    query = 'select biosequence_desc,gene_symbol,full_gene_name,aliases,functional_description from biosequence_annotation ba join biosequence bs on ba.biosequence_id=bs.biosequence_id where'
    print("len plain: %d" % len(plain_search_term_list))
    first_cond = True
    if len(plain_search_terms) > 0:
        query += (' full_gene_name in ' + plain_search_term_list +
        ' or gene_symbol in ' + plain_search_term_list)
        first_cond = False

    for term in wildcard_search_terms:
        term = term.replace('*', '%')
        if not first_cond:
            query += ' or'
        query += " full_gene_name like '%s' or gene_symbol like '%s'" % (term, term)
        first_cond = False
    print(query)
    cursor.execute(query)

    result = []
    gene_added = set()
    with mysqlconn.cursor() as cur:
        for bs_desc,gene_symbol,full_gene_name,aliases,functional_description in cursor.fetchall():
            if not full_gene_name in gene_added:
                gene_added.add(full_gene_name)
                # retrieve new name
                cur.execute('select name from genes where old_name=%s', [full_gene_name])
                row = cur.fetchone()
                if row is not None:
                    new_name = row[0]
                else:
                    new_name = ''
                desc_comps = bs_desc.split('" ')
                for comp in desc_comps:
                    if comp.startswith('location'):
                        coords = comp.split('=')[1].strip('"')
                        result.append({'location': coords,
                                       'gene_symbol': gene_symbol,
                                       'new_name': new_name,
                                       'full_gene_name': full_gene_name,
                                       'aliases': aliases, 'functional_description': functional_description})

    return jsonify(results=result, num_results=len(result))


if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'rtrit#!@#pw34344ct'
    app.run(host='0.0.0.0', debug=True)
