#!/usr/bin/env python3

import json
import os
import traceback
#import pymssql
import pyodbc


from flask import Flask, render_template, jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
app.config.from_envvar('APP_SETTINGS')

HALO_ID = 4

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


@app.route('/annotations/<gene>')
def annotations(gene):
    conn = dbconn('ProteinStructure2')
    cursor = conn.cursor()
    cursor.execute('select biosequence_desc,gene_symbol,full_gene_name,aliases,functional_description from biosequence_annotation ba join biosequence bs on ba.biosequence_id=bs.biosequence_id where full_gene_name=?', gene)
    result = []
    for bs_desc,gene_symbol,full_gene_name,aliases,functional_description in cursor.fetchall():
        desc_comps = bs_desc.split('" ')
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

"""
Check if the transcript link exists
http://networks.systemsbiology.net/projects/halo/transcript_structure/VNG0002G.pdf
"""

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
                pstruct['igv_loc'] = '%s:%d-%d' % (chr_id,
                                                   int(loc_comps[1]) - 50,
                                                   int(loc_comps[2]) + 50)

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


if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'rtrit#!@#pw34344ct'
    app.run(host='0.0.0.0', debug=True)
