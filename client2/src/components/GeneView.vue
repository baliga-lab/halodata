<template>
  <v-container>
    <!-- IGV Browser -->
    <v-row>
      <div id="igv-div"></div>
    </v-row>

    <!-- Proceinstructure data -->
    <div style="text-align: left" v-if="proteinStructureData">
      <v-row>
        <h3>Annotation</h3>
      </v-row>
      <v-row class="text-center">
        <v-col class="mb-4">
          <v-simple-table>
            <template v-slot:default>
              <thead>
                <tr>
                  <th class="text-left">COG ID</th>
                  <th class="text-left">Genbank ID</th>
                  <th class="text-left">Gene Symbol</th>
                  <th class="text-left">Location</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td class="text-left">{{proteinStructureData.COG_ID}}</td>
                  <td class="text-left">{{proteinStructureData.Genbank_ID}}</td>
                  <td class="text-left">{{proteinStructureData.common_name}}</td>
                  <td class="text-left">{{proteinStructureData.location}}</td>
                </tr>
              </tbody>
            </template>
          </v-simple-table>
        </v-col>
      </v-row>

      <v-list-item>
        <v-list-item-content>
          <v-list-item-title>Function</v-list-item-title>
          <v-list-item-subtitle>{{proteinStructureData.function}}</v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>
      <v-spacer style="height: 12pt"></v-spacer>
      <v-list-item>
        <v-list-item-content>
          <v-list-item-title>Transcript Structure</v-list-item-title>
          <v-list-item-subtitle><a :href="transcriptPDFLink" target="_blank">PDF</a></v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>
      <v-spacer style="height: 12pt"></v-spacer>

      <v-expansion-panels>
        <v-expansion-panel>
          <v-expansion-panel-header>DNA</v-expansion-panel-header>
          <v-expansion-panel-content style="font-family: Courier; font-size: 8pt; text-align: left">
            {{proteinStructureData.dna}}
          </v-expansion-panel-content>
        </v-expansion-panel>
        <v-expansion-panel>
          <v-expansion-panel-header>Peptide</v-expansion-panel-header>
          <v-expansion-panel-content style="font-family: Courier; font-size: 8pt; text-align: left">
          {{proteinStructureData.peptide}}
          </v-expansion-panel-content>
        </v-expansion-panel>
      </v-expansion-panels>
    </div>

    <v-spacer style="height: 20pt"></v-spacer>

    <!-- Microarray data -->
    <v-row v-if="microarrayData.length" class="text-center">
      <h4>Microarray Data</h4> (<a :href="downloadMicroarrayURL">Download</a>)
    </v-row>
    <v-row v-if="microarrayData.length" class="text-center">
      <v-col class="mb-4">
        <v-data-table
          :headers="maHeaders"
          :items="microarrayData"
          item-key="condition">
          <template v-slot:item="{item}">
            <tr>
            <td style="text-align: left">{{item.condition}}</td>
            <td >{{item.log10_ratio}}</td>
            <td>{{item.lambda}}</td>
            </tr>
          </template>
        </v-data-table>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import igv from 'igv';
var BASE_URL = process.env.VUE_APP_API_BASE_URL;
var STATIC_URL = process.env.VUE_APP_STATIC_URL;

export default {
    name: 'GeneView',

    data: () => ({
        transcriptPDFLink: '',
        microarrayData: [],
        //downloadMicroarrayURL: BASE_URL + '/download_microarray_data' + this.$route.params.gene,
        downloadMicroarrayURL: BASE_URL + '/download_microarray_data',
        proteinStructureData: null,
        maHeaders: [
          {text: 'Condition', value: 'condition'},
          {text: 'Log10 Ratio', value: 'log10_ratio'},
          {text: 'Lambda', value: 'lambda'}
        ],

        // IGV Browser stuff
        locus: "NC_002607.1:1400-2165",
        fastaURL: STATIC_URL + "Hsalinarum.fa",
        indexURL: STATIC_URL + "Hsalinarum.fa.fai",
        igv: null

    }),
    methods: {
        loadIGVBrowser: function(igvLoc) {
            console.log(STATIC_URL);
            igv.removeAllBrowsers();
            var igvDiv = document.getElementById("igv-div");
            var self = this;
            var options = {
                locus: igvLoc,
                reference: {
                    id: "Halobacterium salinarum NRC-1",
                    fastaURL: this.fastaURL,
                    indexURL: this.indexURL,
                    wholeGenomeView: false
                },
                tracks: [
                    {
                        url: STATIC_URL + "ribosomal_RNA_TP2-fwd.bedgraph.gz",
                        type: "wig",
                        format: "bedgraph",
                        autoscaleGroup: "ribo",
                        name: "Ribo-Seq TP2 (+)",
                        color: "darkgrey"
                    },
                    {
                        url: STATIC_URL + "total-RNA-TP2-rev.bedgraph.gz",
                        type: "wig",
                        format: "bedgraph",
                        autoscaleGroup: "tot",
                        name: "RNA-Seq TP2 (+)",
                        color: "darkgrey"
                    },
                    {
                        url: STATIC_URL + "TPS_gff_fwd.gff3",
                        type: "annotation",
                        format: "gff3",
                        name: "TPS (+)",
                        height: 30,
                        color: "#59A14F",
                        displayMode: "SQUISHED"
                    },
                    {
                        url: STATIC_URL + "br1biorep1-interaction-regions-entire-genome-fwd.gff3",
                        type: "annotation",
                        format: "gff3",
                        name: "SmAP1 interaction (+) Rep 1",
                        height: 30,
                        color: "#E15759",
                        displayMode: "SQUISHED"
                    },
                    {
                        url: STATIC_URL + "br2biorep2-interaction-regions-entire-genome-fwd.gff3",
                        type: "annotation",
                        format: "gff3",
                        name: "SmAP1 interaction (+) Rep 2",
                        height: 30,
                        color: "#E15759",
                        displayMode: "SQUISHED"
                    },
                    {
                        url: STATIC_URL + "Hsalinarum-846asRNAs-deAlmeida2019.gff3",
                        type: "annotation",
                        format: "gff3",
                        name: "Antisense RNAs",
                        color: "#B07AA1",
                        displayMode: "EXPANDED"
                    },
                    {
                        url: STATIC_URL + "Hsalinarum-gene-annotation-pfeiffer2019-adjusted-names.gff3",
                        type: "annotation",
                        searchable: true,
                        format: "gff3",
                        name: "Genes",
                        color: "#4E79A7",
                        displayMode: "COLLAPSED"
                    },
                    {
                        url: STATIC_URL + "Hsalinarum-pfeiffer2019-mobileElements.gff3",
                        type: "annotation",
                        searchable: true,
                        format: "gff3",
                        name: "IS annotation",
                        color: "#59A14F",
                        displayMode: "COLLAPSED"
                    },
                    {
                        url: STATIC_URL + "br1biorep1-interaction-regions-entire-genome-rev.gff3",
                        type: "annotation",
                        format: "gff3",
                        name: "SmAP1 interaction (-) Rep 1",
                        height: 30,
                        color: "#E15759",
                        displayMode: "SQUISHED"
                    },
                    {
                        url: STATIC_URL + "br2biorep2-interaction-regions-entire-genome-rev.gff3",
                        type: "annotation",
                        format: "gff3",
                        name: "SmAP1 interaction (-) Rep 2",
                        height: 30,
                        color: "#E15759",
                        displayMode: "SQUISHED"
                    },
                    {
                        url: STATIC_URL + "TPS_gff_rev.gff3",
                        type: "annotation",
                        format: "gff3",
                        name: "TPS (-)",
                        height: 30,
                        color: "#59A14F",
                        displayMode: "SQUISHED"
                    },
                    {
                        url: STATIC_URL + "ribosomal_RNA_TP2-rev.bedgraph.gz",
                        type: "wig",
                        format: "bedgraph",
                        autoscaleGroup: "ribo",
                        name: "Ribo-Seq TP2 (-)",
                        color: "darkgrey"
                    },
                    /*
                    {
                        url: STATIC_URL + "total-RNA-TP2-fwd.bedgraph.gz",
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
            });
        }
    },
    mounted() {
        var gene = this.$route.params.gene;
        var microarrayApi = BASE_URL + '/microarray_data/' + gene;
        var proteinStructureApi = BASE_URL + '/proteinstructure/' + gene;
        this.transcriptPDFLink = 'http://networks.systemsbiology.net/projects/halo/transcript_structure/' +
            gene + '.pdf';
        this.downloadMicroarrayURL = BASE_URL + '/download_microarray_data/' + gene;
        fetch(microarrayApi)
            .then((response) => { return response.json();
                                }).then((result) => {
                                    this.microarrayData = result.expressions;
                                });
        fetch(proteinStructureApi)
            .then((response) => {
                return response.json();
            }).then((result) => {
                this.proteinStructureData = result.result;
                this.loadIGVBrowser(this.proteinStructureData.igv_loc);
            });
    },

  }

/* COG link https://www.ncbi.nlm.nih.gov/research/cog/cog/COG1136/ */

</script>
