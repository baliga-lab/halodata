#!/usr/bin/env python3
import mysql.connector
import pyodbc

"""
This script consolidates Halo data contained in MySQL and SBEAMS databases and exports
into a CSV file compatible to the Solr schema
"""

def mysql_conn():
    return mysql.connector.connect(host="127.0.0.1", port=3306, user='root', database='halodata')


DBSERVER = 'mssql.systemsbiology.net'
DBUSER = 'sbeamsro'
DBPASS = 'RDSdump44'
SBEAMS_DB = 'sbeams'

def sqlserver_conn(dbname):
    driver = 'FreeTDS'
    conn_str = 'DRIVER=%s;SERVER=%s;PORT=1433;DATABASE=%s;UID=%s;PWD=%s' % (driver,
                                                                            DBSERVER, dbname, DBUSER,
                                                                            DBPASS)
    return pyodbc.connect(conn_str)

MYSQL_QUERY = """select g.name,g.old_name,g.product,c.name,c.cog_name,cc.name from genes g
left outer join cog c on c.id=g.cog_id
left outer join cog_categories cc on c.cog_category_id=cc.id
"""

FIELD_SEP = ','

if __name__ == '__main__':
    mssql_conn = sqlserver_conn('ProteinStructure2')
    mysql_conn = mysql_conn()

    # step 1: build gene symbol map
    gene_symbol_map = {}
    with mssql_conn.cursor() as mssql_cur:
        mssql_cur.execute('select full_gene_name,gene_symbol from biosequence_annotation ba join biosequence bs on ba.biosequence_id=bs.biosequence_id')
        for gene_name, symbol in mssql_cur.fetchall():
            if gene_name is not None and gene_name.startswith('VNG'):
                gene_symbol_map[gene_name] = symbol

    columns = ['id', 'locus_tag', 'gene_symbol', 'product', 'cog_id', 'cog_name', 'cog_category', 'aliases',
               'functional_description']
    print(FIELD_SEP.join(columns))

    with mysql_conn.cursor() as mysql_cur:
        with mssql_conn.cursor() as mssql_cur:
            mysql_cur.execute(MYSQL_QUERY)
            for gene_id,locus_tag,product,cog_id,cog_name,cog_category in mysql_cur.fetchall():
                try:
                    gene_symbol = gene_symbol_map[locus_tag]
                except:
                    gene_symbol = ''
                mssql_cur.execute('select aliases,functional_description from biosequence_annotation ba join biosequence bs on ba.biosequence_id=bs.biosequence_id where full_gene_name=?', locus_tag)
                aliases, functional_desc = mssql_cur.fetchone()
                if functional_desc is None:
                    functional_desc = ''
                functional_desc = functional_desc.strip().replace('"', "'")
                out_row = [gene_id, locus_tag, gene_symbol, product, cog_id, cog_name, cog_category, aliases, functional_desc]
                out_row2 = []
                for elem in out_row:
                    if elem is None:
                        out_row2.append('')
                    else:
                        out_row2.append('"' + str(elem) + '"')
                print(FIELD_SEP.join(out_row2))
