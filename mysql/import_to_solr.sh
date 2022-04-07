#!/bin/bash

curl 'http://localhost:8983/solr/halodata/update?commit=true&header=true&overwrite=true' --data-binary @halodata_solr_v2.csv -H 'Content-type:application/csv'
