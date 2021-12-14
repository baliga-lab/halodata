<template>
  <v-container>
      <v-row class="text-center">
        <v-col class="mb-4">
  <div id="igv-div"></div>
  </v-col>
      </v-row>
  </v-container>
</template>

<script>
import igv from 'igv';
var BASE_URL = 'http://localhost:5000';
// var BASE_URL = '/api';
export default {
    name: 'IGV',
    props: ['igvLocation'],
    data: () => ({
        //locus: "NC_001869.1:17,638-27,205",
        //locus: "NC_002607.1:1450-2115",
        locus: "NC_002607.1:1400-2165",
        fastaURL: BASE_URL + "/static/Hsalinarum.fa",
        indexURL: BASE_URL + "/static/Hsalinarum.fa.fai",
        igv: null
    }),
    methods: {
    },
    mounted() {
        var igvDiv = document.getElementById("igv-div");
        var self = this;
        var options = {
            locus: this.locus,
            reference: {
                id: "Halobacterium salinarum NRC-1",
                fastaURL: this.fastaURL,
                indexURL: this.indexURL,
                wholeGenomeView: false
            },
            tracks: [
              /*
          {
            url: "https://alanlorenzetti.github.io/miscfiles/igv_tlr/ribosomal_RNA_TP2-fwd.bedgraph.gz",
            type: "wig",
            format: "bedgraph",
            autoscaleGroup: "ribo",
            name: "Ribo-Seq TP2 (+)",
            color: "darkgrey"
          },
          {
            url: "https://alanlorenzetti.github.io/miscfiles/igv_tlr/total-RNA-TP2-rev.bedgraph.gz",
            type: "wig",
            format: "bedgraph",
            autoscaleGroup: "tot",
            name: "RNA-Seq TP2 (+)",
            color: "darkgrey"
          },
          {
            url: "https://alanlorenzetti.github.io/miscfiles/igv_tlr/TPS_gff_fwd.gff3",
            type: "annotation",
            format: "gff3",
            name: "TPS (+)",
            height: 30,
            color: "#59A14F",
            displayMode: "SQUISHED"
          },
          {
            url: "https://alanlorenzetti.github.io/miscfiles/igv_tlr/br1biorep1-interaction-regions-entire-genome-fwd.gff3",
            type: "annotation",
            format: "gff3",
            name: "SmAP1 interaction (+) Rep 1",
            height: 30,
            color: "#E15759",
            displayMode: "SQUISHED"
          },
          {
            url: "https://alanlorenzetti.github.io/miscfiles/igv_tlr/br2biorep2-interaction-regions-entire-genome-fwd.gff3",
            type: "annotation",
            format: "gff3",
            name: "SmAP1 interaction (+) Rep 2",
            height: 30,
            color: "#E15759",
            displayMode: "SQUISHED"
          },
          {
            url: "https://alanlorenzetti.github.io/miscfiles/igv_tlr/Hsalinarum-846asRNAs-deAlmeida2019.gff3",
            type: "annotation",
            format: "gff3",
            name: "Antisense RNAs",
            color: "#B07AA1",
            displayMode: "EXPANDED"
          },
          */
                {
                    url: BASE_URL + "/static/Hsalinarum-gene-annotation-pfeiffer2019-adjusted-names.gff3",
            type: "annotation",
                    searchable: true,
                    format: "gff3",
                    name: "Genes",
                    color: "#4E79A7",
                    displayMode: "COLLAPSED"
                },
              /*
          {
            url: "https://alanlorenzetti.github.io/miscfiles/igv_tlr/Hsalinarum-pfeiffer2019-mobileElements.gff3",
            type: "annotation",
            searchable: true,
            format: "gff3",
            name: "IS annotation",
            color: "#59A14F",
            displayMode: "COLLAPSED"
          },
          {
            url: "https://alanlorenzetti.github.io/miscfiles/igv_tlr/br1biorep1-interaction-regions-entire-genome-rev.gff3",
            type: "annotation",
            format: "gff3",
            name: "SmAP1 interaction (-) Rep 1",
            height: 30,
            color: "#E15759",
            displayMode: "SQUISHED"
          },
          {
            url: "https://alanlorenzetti.github.io/miscfiles/igv_tlr/br2biorep2-interaction-regions-entire-genome-rev.gff3",
            type: "annotation",
            format: "gff3",
            name: "SmAP1 interaction (-) Rep 2",
            height: 30,
            color: "#E15759",
            displayMode: "SQUISHED"
          },
          {
            url: "https://alanlorenzetti.github.io/miscfiles/igv_tlr/TPS_gff_rev.gff3",
            type: "annotation",
            format: "gff3",
            name: "TPS (-)",
            height: 30,
            color: "#59A14F",
            displayMode: "SQUISHED"
          },
          {
            url: "https://alanlorenzetti.github.io/miscfiles/igv_tlr/ribosomal_RNA_TP2-rev.bedgraph.gz",
            type: "wig",
            format: "bedgraph",
            autoscaleGroup: "ribo",
            name: "Ribo-Seq TP2 (-)",
            color: "darkgrey"
          },
          {
            url: "https://alanlorenzetti.github.io/miscfiles/igv_tlr/total-RNA-TP2-fwd.bedgraph.gz",
            type: "wig",
            format: "bedgraph",
            autoscaleGroup: "tot",
            name: "RNA-Seq TP2 (-)",
            color: "darkgrey"
          }*/
            ]
        };

        igv.createBrowser(igvDiv, options)
            .then(function (browser) {
                self.igv = browser;
                console.log(self.igv);
            });
    }
};
</script>
