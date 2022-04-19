<template>
<v-container>
  <v-spacer style="height: 32pt"></v-spacer>
  <v-row v-if="newInfo">
    <span style="font-size: 16pt"><b>{{newInfo.gene}}</b> ({{$route.params.gene}}, {{newInfo.gene_symbol}})</span>&nbsp;
    <span v-if="proteinStructureData" style="font-size: 16pt; vertical-align: bottom">{{proteinStructureData.function}}</span>
  </v-row>
  <v-row v-else-if="proteinStructureData">
    <span style="font-size: 16pt"><b>{{$route.params.gene}}</b> ({{proteinStructureData.common_name}})</span>&nbsp;
    <span style="font-size: 16pt; vertical-align: bottom">{{proteinStructureData.function}}</span>
  </v-row>
  <v-spacer style="height: 48pt"></v-spacer>
  <v-row  style="text-align: left" v-if="proteinStructureData">
    <h3>Annotations</h3>
  </v-row>
  <v-row class="text-center" v-if="proteinStructureData">
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
              <td class="text-left"><a :href="cogLink" target="_blank">{{proteinStructureData.COG_ID}}</a></td>
              <td class="text-left">{{proteinStructureData.Genbank_ID}}</td>
              <td class="text-left">{{proteinStructureData.common_name}}</td>
              <td class="text-left">{{proteinStructureData.location}}</td>
            </tr>
          </tbody>
        </template>
      </v-simple-table>
    </v-col>
  </v-row>

  <v-row  style="text-align: left" v-if="newInfo">
    <h3>COG Information</h3>
  </v-row>
  <v-row class="text-center" v-if="newInfo">
    <v-col class="mb-4">
      <v-simple-table>
        <template v-slot:default>
          <thead>
            <tr>
              <th class="text-left">COG Category</th>
              <th class="text-left">Pathway</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td class="text-left">{{newInfo.cog_category}}</td>
              <td class="text-left">{{newInfo.cog_pathway}}</td>
            </tr>
          </tbody>
        </template>
      </v-simple-table>
    </v-col>
  </v-row>

    <!-- IGV Browser -->
  <v-row  style="text-align: left" v-if="proteinStructureData">
    <h3>Genome Browser</h3>
  </v-row>
  <v-row>
    <div id="igv" ref="igv"></div>
  </v-row>

    <!-- Proceinstructure data -->
    <div style="text-align: left" v-if="proteinStructureData">

      <v-row>
        <h3>Gene Regulatory Network</h3>
      </v-row>
      <v-spacer style="height: 12pt"></v-spacer>
      <v-list-item>
        <v-list-item-content>
          <v-list-item-subtitle>
            <a :href="egrinLink" target="_blank">EGRIN</a>&nbsp;
            <a :href="egrin2Link" target="_blank">EGRIN2.0</a>
          </v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>
      <v-spacer style="height: 12pt"></v-spacer>
      <v-row>
        <h3>Transcript Structure</h3>
      </v-row>
      <v-list-item>
        <v-list-item-content>
          <v-list-item-subtitle><a :href="transcriptPDFLink" target="_blank">PDF</a></v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>
      <v-spacer style="height: 12pt"></v-spacer>

    </div>

    <v-spacer style="height: 20pt"></v-spacer>

    <!-- Microarray data -->
    <v-row v-if="microarrayData.length" class="text-center">
      <h3>Data</h3> 
    </v-row>
    <v-row v-if="microarrayData.length" class="text-center">
      <v-expansion-panels>
        <v-expansion-panel>
          <v-expansion-panel-header>Microarray Data &nbsp; <a :href="downloadMicroarrayURL">Download</a></v-expansion-panel-header>
          <v-expansion-panel-content>
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
          </v-expansion-panel-content>
        </v-expansion-panel>
      </v-expansion-panels>
    </v-row>
    <v-spacer style="height: 20pt"></v-spacer>

    <v-row>
      <h3>Sequences</h3>
    </v-row>
    <v-row v-if="proteinStructureData">
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
    </v-row>
    <v-spacer style="height: 20pt"></v-spacer>
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
        egrinLink: '',
        egrin2Link: '',
        cogLink: '',
        microarrayData: [],
        downloadMicroarrayURL: BASE_URL + '/download_microarray_data',
        proteinStructureData: null,
        newInfo: null,
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
        loadIGVBrowser: function(igvLoc, trackRange) {
            console.log('track range: ' + trackRange);
            igv.removeAllBrowsers();
            var igvDiv = this.$refs.igv; //document.getElementById("igv");
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
                        url: STATIC_URL + "split_tracks/ribosomal_RNA_TP1-fwd_" + trackRange + ".bedgraph.gz",
                        type: "wig",
                        format: "bedgraph",
                        autoscaleGroup: "ribo",
                        name: "Ribo-Seq TP1 (+)",
                        color: "darkgrey"
                    },
                    {
                        url: STATIC_URL + "split_tracks/ribosomal_RNA_TP2-fwd_" + trackRange + ".bedgraph.gz",
                        type: "wig",
                        format: "bedgraph",
                        autoscaleGroup: "ribo",
                        name: "Ribo-Seq TP2 (+)",
                        color: "darkgrey"
                    },
                    {
                        url: STATIC_URL + "split_tracks/ribosomal_RNA_TP3-fwd_" + trackRange + ".bedgraph.gz",
                        type: "wig",
                        format: "bedgraph",
                        autoscaleGroup: "ribo",
                        name: "Ribo-Seq TP3 (+)",
                        color: "darkgrey"
                        },
                    {
                        url: STATIC_URL + "split_tracks/ribosomal_RNA_TP4-fwd_" + trackRange + ".bedgraph.gz",
                        type: "wig",
                        format: "bedgraph",
                        autoscaleGroup: "ribo",
                        name: "Ribo-Seq TP4 (+)",
                        color: "darkgrey"
                    },
                    {
                        url: STATIC_URL + "split_tracks/total-RNA-TP1-rev_" + trackRange + ".bedgraph.gz",
                        type: "wig",
                        format: "bedgraph",
                        autoscaleGroup: "tot",
                        name: "RNA-Seq TP1 (+)",
                        color: "darkgrey"
                    },
                    {
                        url: STATIC_URL + "split_tracks/total-RNA-TP2-rev_" + trackRange + ".bedgraph.gz",
                        type: "wig",
                        format: "bedgraph",
                        autoscaleGroup: "tot",
                        name: "RNA-Seq TP2 (+)",
                        color: "darkgrey"
                    },
                    {
                        url: STATIC_URL + "split_tracks/total-RNA-TP3-rev_" + trackRange + ".bedgraph.gz",
                        type: "wig",
                        format: "bedgraph",
                        autoscaleGroup: "tot",
                        name: "RNA-Seq TP3 (+)",
                        color: "darkgrey"
                    },
                    {
                        url: STATIC_URL + "split_tracks/total-RNA-TP4-rev_" + trackRange + ".bedgraph.gz",
                        type: "wig",
                        format: "bedgraph",
                        autoscaleGroup: "tot",
                        name: "RNA-Seq TP4 (+)",
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
                        url: STATIC_URL + "mergedBRs_interaction-regions-entire-genome-fwd.gff3",
                        type: "annotation",
                        format: "gff3",
                        name: "SmAP1 interaction (+)",
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
                        url: STATIC_URL + "mergedBRs_interaction-regions-entire-genome-rev.gff3",
                        type: "annotation",
                        format: "gff3",
                        name: "SmAP1 interaction (-)",
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
                        url: STATIC_URL + "split_tracks/ribosomal_RNA_TP1-rev_" + trackRange + ".bedgraph.gz",
                        type: "wig",
                        format: "bedgraph",
                        autoscaleGroup: "ribo",
                        name: "Ribo-Seq TP1 (-)",
                        color: "darkgrey"
                    },
                    {
                        url: STATIC_URL + "split_tracks/ribosomal_RNA_TP2-rev_" + trackRange + ".bedgraph.gz",
                        type: "wig",
                        format: "bedgraph",
                        autoscaleGroup: "ribo",
                        name: "Ribo-Seq TP2 (-)",
                        color: "darkgrey"
                    },
                    {
                        url: STATIC_URL + "split_tracks/ribosomal_RNA_TP3-rev_" + trackRange + ".bedgraph.gz",
                        type: "wig",
                        format: "bedgraph",
                        autoscaleGroup: "ribo",
                        name: "Ribo-Seq TP3 (-)",
                        color: "darkgrey"
                    },
                    {
                        url: STATIC_URL + "split_tracks/ribosomal_RNA_TP4-rev_" + trackRange + ".bedgraph.gz",
                        type: "wig",
                        format: "bedgraph",
                        autoscaleGroup: "ribo",
                        name: "Ribo-Seq TP4 (-)",
                        color: "darkgrey"
                    },
                    {
                        url: STATIC_URL + "split_tracks/total-RNA-TP1-fwd_" + trackRange + ".bedgraph.gz",
                        type: "wig",
                        format: "bedgraph",
                        autoscaleGroup: "tot",
                        name: "RNA-Seq TP1 (-)",
                        color: "darkgrey"
                    },
                    {
                        url: STATIC_URL + "split_tracks/total-RNA-TP2-fwd_" + trackRange + ".bedgraph.gz",
                        type: "wig",
                        format: "bedgraph",
                        autoscaleGroup: "tot",
                        name: "RNA-Seq TP2 (-)",
                        color: "darkgrey"
                    },
                    {
                        url: STATIC_URL + "split_tracks/total-RNA-TP3-fwd_" + trackRange + ".bedgraph.gz",
                        type: "wig",
                        format: "bedgraph",
                        autoscaleGroup: "tot",
                        name: "RNA-Seq TP3 (-)",
                        color: "darkgrey"
                    },
                    {
                        url: STATIC_URL + "split_tracks/total-RNA-TP4-fwd_" + trackRange + ".bedgraph.gz",
                        type: "wig",
                        format: "bedgraph",
                        autoscaleGroup: "tot",
                        name: "RNA-Seq TP4 (-)",
                        color: "darkgrey"
                    }
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
        var newInfoApi = BASE_URL + '/newinfo_for_old/' + gene;
        var proteinStructureApi = BASE_URL + '/proteinstructure/' + gene;
        this.transcriptPDFLink = 'http://networks.systemsbiology.net/projects/halo/transcript_structure/' +
            gene + '.pdf';
        this.egrinLink = 'http://networks.systemsbiology.net/hal/gene/' + gene;
        this.egrin2Link = 'http://egrin2.systemsbiology.net/genes/64091/' + gene;
        this.downloadMicroarrayURL = BASE_URL + '/download_microarray_data/' + gene;
        fetch(newInfoApi)
            .then((response) => { return response.json();
                                }).then((result) => {
                                    console.log(result.results);
                                    if (result.results.length > 0) {
                                        this.newInfo = result.results[0];
                                    }
                                });
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
                // WW: loading the browser too early results in the div not
                // existing sometimes, so we wrap it in a nextTick
                this.$nextTick(() => {
                    this.loadIGVBrowser(this.proteinStructureData.igv_loc, this.proteinStructureData.track_range);
                });
                this.cogLink = "https://www.ncbi.nlm.nih.gov/research/cog/cog/" + this.proteinStructureData.COG_ID + "/"
            });
    },

  }

/* COG link https://www.ncbi.nlm.nih.gov/research/cog/cog/COG1136/ */

</script>
