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


def dbconn(dbname):
    return  pymssql.connect(server=app.config('DBSERVER'), port=1433,
                            user=app.config('DBUSER'), password=app.config('DBPASS'),
                            database=dbname)

@app.route('/')
def index():
    return "<p>Hello !</p>"


if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'rtrit#!@#pw34344ct'
    app.run(host='0.0.0.0', debug=True)
