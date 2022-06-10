#!/bin/bash

OUTDIR=split_tracks2

./tracksplitter.py -nc 8 ribosomal_RNA_TP1-fwd.bedgraph.gz $OUTDIR
./tracksplitter.py -nc 8 ribosomal_RNA_TP1-rev.bedgraph.gz $OUTDIR
./tracksplitter.py -nc 8 ribosomal_RNA_TP2-fwd.bedgraph.gz $OUTDIR
./tracksplitter.py -nc 8 ribosomal_RNA_TP2-rev.bedgraph.gz $OUTDIR
./tracksplitter.py -nc 8 ribosomal_RNA_TP3-fwd.bedgraph.gz $OUTDIR
./tracksplitter.py -nc 8 ribosomal_RNA_TP3-rev.bedgraph.gz $OUTDIR
./tracksplitter.py -nc 8 ribosomal_RNA_TP4-fwd.bedgraph.gz $OUTDIR
./tracksplitter.py -nc 8 ribosomal_RNA_TP4-rev.bedgraph.gz $OUTDIR
./tracksplitter.py -nc 8 total-RNA-TP1-fwd.bedgraph.gz $OUTDIR
./tracksplitter.py -nc 8 total-RNA-TP1-rev.bedgraph.gz $OUTDIR
./tracksplitter.py -nc 8 total-RNA-TP2-fwd.bedgraph.gz $OUTDIR
./tracksplitter.py -nc 8 total-RNA-TP2-rev.bedgraph.gz $OUTDIR
./tracksplitter.py -nc 8 total-RNA-TP3-fwd.bedgraph.gz $OUTDIR
./tracksplitter.py -nc 8 total-RNA-TP3-rev.bedgraph.gz $OUTDIR
./tracksplitter.py -nc 8 total-RNA-TP4-fwd.bedgraph.gz $OUTDIR
./tracksplitter.py -nc 8 total-RNA-TP4-rev.bedgraph.gz $OUTDIR
