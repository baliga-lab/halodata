#!/usr/bin/env python3

import json
import os
import traceback
import pymssql


from flask import Flask, render_template, jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
app.config.from_envvar('APP_SETTINGS')

HALO_ID = 4

def dbconn(dbname):
    return  pymssql.connect(server=app.config['DBSERVER'], port=1433,
                            user=app.config['DBUSER'], password=app.config['DBPASS'],
                            database=dbname)

@app.route('/')
def index():
    return "<p>Hello !</p>"


@app.route('/microarray_data/<gene>')
def microarray_data(gene):
    conn = dbconn('microarray3')
    cursor = conn.cursor()
    cursor.execute('select cc.condition_name,ge.common_name,ge.canonical_name,log10_ratio,lambda from gene_expression ge join comparison_condition cc on ge.condition_id=cc.condition_id where canonical_name=%s', gene)
    result = []
    for cond_name,common_name,canonical_name,log10,lambdaval in cursor.fetchall():
        result.append({'condition': cond_name, 'common_name': common_name,
                       'canonical_name': canonical_name, 'log10_ratio': log10,
                       'lambda': lambdaval})

    return jsonify(expressions=result, num_expressions=len(result))


@app.route('/genes')
def genes():
    conn = dbconn('microarray3')
    cursor = conn.cursor()
    cursor.execute('select distinct biosequence_name from biosequence where organism_id=%d' % HALO_ID)
    result = []
    for row in cursor.fetchall():
        result.append(row[0])

    return jsonify(genes=result, num_genes=len(result))


if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'rtrit#!@#pw34344ct'
    app.run(host='0.0.0.0', debug=True)
