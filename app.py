#!/usr/bin/env python3

import json
import os
import traceback
import pyodbc

import mysql.connector

from flask import Flask, render_template, jsonify, Response
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


@app.route('/newinfo_for_old/<gene>')
def newinfo_for_old(gene):
    conn = mysql_conn()
    result = []
    with conn.cursor() as cur:
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
        if gene_id is not None:
            print("Found Gene ID !!!!: ", gene_id)

        query = """select
                     g.name,g.gene_symbol,c.name as cog_id,cc.name as cog_category,cp.name as cog_pathway,
                     ins.name as ins_name,ins.family as ins_family,ins.subgroup as ins_subgroup
                   from genes g
                     left outer join cog c on g.cog_id=c.id
                     left outer join cog_categories cc on c.cog_category_id=cc.id
                     left outer join cog_pathways cp on c.cog_pathway_id=cp.id
                     left outer join insertion_sequences ins on g.is_id=ins.id
                   where g.id=%s"""
        cur.execute(query, [gene_id])
        for gene,gene_symbol,cog_id,ccat,cpathway,ins_name,ins_family,ins_subgroup in cur.fetchall():
            entry = {'gene': gene, 'gene_symbol': gene_symbol, 'cog_id': cog_id, 'cog_category': ccat}
            print(entry)
            if cpathway is not None:
                entry['cog_pathway'] = cpathway
            if ins_name is not None:
                entry['ins_name'] = ins_name
                entry['ins_family'] = ins_family
                entry['ins_subgroup'] = ins_subgroup
            result.append(entry)
    return jsonify(results=result)


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
                left = int(loc_comps[1]) - IGV_MARGIN
                left = max(1, left)
                right = int(loc_comps[2]) + IGV_MARGIN
                pstruct['igv_loc'] = '%s:%d-%d' % (chr_id, left, right)

    return jsonify(result=pstruct)


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
        result.append({'representative': gene, 'cog_id': cog_id, 'cog_name': cog_name,
                       'cog_category': category_name, 'cog_pathway': pathway_name,
                       'old_name': _old_name_from_locus_tags(locus_tags)})

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
    solr_url = "http://localhost:8983/solr/halodata/query"
    solr_url += '?q=all:' + search_term
    print(solr_url)
    r = requests.get(solr_url)
    solr_result = r.json()
    solr_result = solr_result['response']['docs']
    print(solr_result)
    result = []
    for doc in solr_result:

        ## ADD MISSING FIELDS TODO
        try:
            func_desc = doc['functional_description']
        except:
            func_desc = ''
        result.append({'location': '',
                       'gene_symbol': doc['gene_symbol'],
                       'new_name': doc['id'],
                       'full_gene_name': doc['locus_tag'],
                       'aliases': doc['aliases'], 'functional_description': func_desc})

    return jsonify(results=result, num_results=len(result))


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
