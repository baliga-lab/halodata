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

MYSQL_QUERY = """select g.name,g.product,c.name,c.cog_name,cc.name from genes g
left outer join cog c on c.id=g.cog_id
left outer join cog_categories cc on c.cog_category_id=cc.id
"""

FIELD_SEP = '|'

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
            for gene_id,product,cog_id,cog_name,cog_category in mysql_cur.fetchall():
                cur2 = mysql_conn.cursor()
                # first query
                cur2.execute('select lt.name from locus_tags lt join gene_locus_tags glt on lt.id=glt.locus_tag_id join genes g on g.id=glt.gene_id and g.name=%s', [gene_id])
                mysql_aliases = [row[0] for row in cur2.fetchall()]

                # 2nd query to determine if this is a gene that is also in SBEAMS
                cur2.execute('select lt.name from locus_tags lt join gene_locus_tags glt on lt.id=glt.locus_tag_id join genes g on g.id=glt.gene_id and g.name=%s', [gene_id])
                for row in cur2.fetchall():
                    locus_tag = row[0]
                    if locus_tag.startswith('VNG') and not locus_tag.startswith('VNG_'):
                        break
                if not locus_tag.startswith('VNG') or locus_tag.startswith('VNG_'):
                    search_sbeams = False
                    # WARNING: can't get locus tag for this
                    aliases = ''
                    funcional_desc = ''
                    locus_tag = gene_id  # map to itself if not in SBEAMS
                else:
                    search_sbeams = True

                try:
                    gene_symbol = gene_symbol_map[locus_tag]
                except:
                    gene_symbol = ''

                if search_sbeams:
                    mssql_cur.execute('select aliases,functional_description from biosequence_annotation ba join biosequence bs on ba.biosequence_id=bs.biosequence_id where full_gene_name=?', locus_tag)
                    aliases, functional_desc = mssql_cur.fetchone()

                    if functional_desc is None:
                        functional_desc = ''
                    functional_desc = functional_desc.strip().replace('"', "'")

                # add the aliases from MySQL
                aliases = set(aliases.split(',') + mysql_aliases)
                aliases = ','.join(aliases)

                # output 1
                out_row = [gene_id, locus_tag, gene_symbol, product, cog_id, cog_name, cog_category, aliases, functional_desc]
                out_row2 = []
                for elem in out_row:
                    if elem is None:
                        out_row2.append('')
                    else:
                        out_row2.append('"' + str(elem) + '"')
                print(FIELD_SEP.join(out_row2))
