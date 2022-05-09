#!/bin/bash

curl 'http://localhost:8983/solr/halodata/update?commit=true&header=true&overwrite=true&separator=|&f.aliases.split=true&f.aliases.separator=%2C&f.aliases.encapsulator="' --data-binary @halodata_solr.csv -H 'Content-type:application/csv'
