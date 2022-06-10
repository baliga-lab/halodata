<template>
<v-container>
  <v-spacer style="height: 32pt"></v-spacer>
  <v-row v-if="geneDoesNotExist">
    <v-col class="mb-4">
      <h2>Gene '{{$route.params.gene}}' not found</h2>
    </v-col>
  </v-row>
  <v-row v-if="newInfo">
    <span style="font-size: 16pt"><b>{{newInfo.gene}}</b> {{altGeneDesc}}</span>&nbsp;
    <span v-if="proteinStructureData" style="font-size: 16pt; vertical-align: bottom">{{newInfo.product}}</span>
  </v-row>
  <v-spacer style="height: 48pt"></v-spacer>
  <v-row  style="text-align: left" v-if="proteinStructureData">
    <h3>Annotations</h3>
  </v-row>

  <v-row class="text-center" v-if="annotationReady">
    <v-col class="mb-4">
      <v-simple-table>
        <template v-slot:default>
          <thead>
            <tr>
              <th class="text-left">Location</th>
              <th class="text-left">COG ID</th>
              <th class="text-left">Genbank ID</th>
              <th class="text-left">Gene Symbol</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td class="text-left">{{location}}</td>
              <td class="text-left"><a :href="cogLink" target="_blank">{{cogID}}</a></td>
              <td class="text-left">{{genbankID}}</td>
              <td class="text-left">{{commonName}}</td>
            </tr>
          </tbody>
        </template>
      </v-simple-table>
    </v-col>
  </v-row>

  <!-- IGV Browser -->
  <v-row v-if="newInfo">
    <h3>Genome Browser</h3>
  </v-row>
  <v-row v-if="newInfo">
    <v-col class="mb-4">
    <div>
      <v-checkbox v-model="isLogScale" @change="reloadIGVBrowser" label="Display tracks in Log Scale"></v-checkbox>
    </div>
    </v-col>
  </v-row>
  <v-row>
    <v-col class="mb-4">
      <div>&nbsp;</div>
    </v-col>
  </v-row>
  <v-row v-if="newInfo">
    <div id="igv" ref="igv"></div>
  </v-row>

  <v-row  style="text-align: left" v-if="hasCOGInfo">
    <h3>COG Information</h3>
  </v-row>
  <v-row class="text-center" v-if="hasCOGInfo">
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

  <v-row  style="text-align: left" v-if="hasPathway">
    <h3>Pathway Information</h3>
  </v-row>
  <v-row  style="text-align: left" v-if="hasPathway">
    <v-col class="mb-4">
      <ul>
        <li v-for="p in newInfo.pathways" :key="p">{{p}}</li>
      </ul>
    </v-col>
  </v-row>

  <v-row  style="text-align: left" v-if="hasGOBio">
    <h3>Gene ontology (biological process)</h3>
  </v-row>
  <v-row  style="text-align: left" v-if="hasGOBio">
    <v-col class="mb-4">
      <ul>
        <li v-for="go in newInfo.go_bio" :key="go">{{go}}</li>
      </ul>
    </v-col>
  </v-row>
  <v-row  style="text-align: left" v-if="hasGOCell">
    <h3>Gene ontology (cellular component)</h3>
  </v-row>
  <v-row  style="text-align: left" v-if="hasGOCell">
    <v-col class="mb-4">
      <ul>
        <li v-for="go in newInfo.go_cell" :key="go">{{go}}</li>
      </ul>
    </v-col>
  </v-row>
  <v-row  style="text-align: left" v-if="hasGOMol">
    <h3>Gene ontology (molecular function)</h3>
  </v-row>
  <v-row  style="text-align: left" v-if="hasGOMol">
    <v-col class="mb-4">
      <ul>
        <li v-for="go in newInfo.go_mol" :key="go">{{go}}</li>
      </ul>
    </v-col>
  </v-row>

  <!-- Cross references -->
  <v-row class="text-center" v-if="hasCrossReferences">
    <h3>Cross References</h3>
  </v-row>
  <v-row class="text-center" v-if="hasCrossReferences">
    <v-col class="mb-4">
      <v-simple-table>
        <template v-slot:default>
          <thead>
            <tr>
              <th class="text-left">Database</th>
              <th class="text-left">References</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="hasUniprot">
              <td class="text-left">Uniprot</td>
              <td class="text-left"><a :href="uniprotLink" target="_blank">{{newInfo.uniprot_id}}</a></td>
            </tr>
            <tr v-if="hasSTRING">
              <td class="text-left">STRING</td>
              <td class="text-left"><a :href="stringLink" target="_blank">{{newInfo.string_id}}</a></td>
            </tr>
            <tr v-if="hasCDD">
              <td class="text-left">CDD</td>
              <td class="text-left"><span v-for="cdd in newInfo.cdd" :key="cdd">{{cdd}}&nbsp;</span></td>
            </tr>
            <tr v-if="hasProsite">
              <td class="text-left">Prosite</td>
              <td class="text-left"><span v-for="prosite in newInfo.prosite" :key="prosite">{{prosite}}&nbsp;</span></td>
            </tr>
            <tr v-if="hasSMART">
              <td class="text-left">SMART</td>
              <td class="text-left"><span v-for="smart in newInfo.smart" :key="smart">{{smart}}&nbsp;</span></td>
            </tr>
            <tr v-if="hasPFAM">
              <td class="text-left">Pfam</td>
              <td class="text-left"><span v-for="pfam in newInfo.pfam" :key="pfam"><a :href="pfamLink(pfam)" target="_blank">{{pfam}}</a>&nbsp;</span></td>
            </tr>
            <tr v-if="hasUniPathway">
              <td class="text-left">UniPathway</td>
              <td class="text-left"><span v-for="uni in newInfo.uni_pathway" :key="uni">{{uni}}&nbsp;</span></td>
            </tr>
            <tr v-if="hasInterpro">
              <td class="text-left">Interpro</td>
              <td class="text-left"><span v-for="inter in newInfo.interpro" :key="inter">{{inter}}&nbsp;</span></td>
            </tr>
            <tr v-if="hasOrthoDB">
              <td class="text-left">OrthoDB</td>
              <td class="text-left">{{newInfo.orthodb_id}}</td>
            </tr>
          </tbody>
        </template>
      </v-simple-table>
    </v-col>
  </v-row>


  <!-- Proceinstructure data -->

  <v-spacer style="height: 40pt"></v-spacer>
  <v-row v-if="proteinStructureData">
    <h3>Gene Regulatory Network</h3>
  </v-row>
  <v-spacer style="height: 12pt"></v-spacer>
  <v-list-item v-if="proteinStructureData">
    <v-list-item-content>
      <v-list-item-subtitle>
        <a :href="egrinLink" target="_blank">EGRIN</a>&nbsp;
        <a :href="egrin2Link" target="_blank">EGRIN2.0</a>
      </v-list-item-subtitle>
    </v-list-item-content>
  </v-list-item>
  <v-spacer style="height: 12pt"></v-spacer>
  <v-row v-if="proteinStructureData">
    <h3>Transcript Structure</h3>
  </v-row>
  <v-list-item v-if="proteinStructureData">
    <v-list-item-content>
      <v-list-item-subtitle><a :href="transcriptPDFLink" target="_blank">PDF</a></v-list-item-subtitle>
    </v-list-item-content>
  </v-list-item>
  <v-spacer style="height: 12pt"></v-spacer>

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
  <v-row v-if="proteinStructureData">
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
        isLogScale: true,
        geneDoesNotExist: false,
        microarrayData: [],
        proteinStructureData: null,
        newInfo: null,
        altGeneDesc: '',
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
    computed: {
        annotationReady() { return this.proteinStructureData || this.newInfo; },
        hasCOGInfo() { return this.newInfo && (this.newInfo.cog_category || this.newInfo.cog_pathway); },
        cogID() { return this.newInfo != null ? this.newInfo.cog_id : ''; },
        genbankID() { return this.proteinStructureData != null ? this.proteinStructureData.Genbank_ID : '' },
        hasPathway() { return this.newInfo && this.newInfo.pathways.length > 0},
        hasGOBio() { return this.newInfo && this.newInfo.go_bio.length > 0 },
        hasGOCell() { return this.newInfo && this.newInfo.go_cell.length > 0 },
        hasGOMol() { return this.newInfo && this.newInfo.go_mol.length > 0 },
        // TODO: include unipathway
        hasCrossReferences() {
            return this.newInfo && (this.newInfo.cdd.length > 0 || this.newInfo.prosite.length > 0
                                    || this.newInfo.smart.length > 0 || this.newInfo.pfam.length > 0
                                    || this.newInfo.uni_pathway.length > 0 || this.newInfo.interpro.length > 0
                                    || this.newInfo.orthodb_id || this.newInfo.uniprot_id || this.newInfo.string_id);
        },
        hasUniprot() { return this.newInfo && this.newInfo.uniprot_id; },
        hasSTRING() { return this.newInfo && this.newInfo.string_id },
        hasCDD() { return this.newInfo && this.newInfo.cdd.length > 0; },
        hasProsite() { return this.newInfo && this.newInfo.prosite.length > 0; },
        hasSMART() { return this.newInfo && this.newInfo.smart.length > 0; },
        hasPFAM() { return this.newInfo && this.newInfo.pfam.length > 0; },
        hasUniPathway() { return this.newInfo && this.newInfo.uni_pathway.length > 0; },
        hasInterpro() { return this.newInfo && this.newInfo.interpro.length > 0; },
        hasOrthoDB() { return this.newInfo && this.newInfo.orthodb_id; },
        // also gene symbol from newInfo
        commonName() {
            if (this.newInfo != null) { return this.newInfo.gene_symbol; }
            return this.proteinStructureData != null ? this.proteinStructureData.common_name : ''
        },
        // also location from newInfo
        location() {
            console.log(this.newInfo);
            if (this.newInfo != null && this.newInfo.chrom) {
                return this.newInfo.chrom + ' ' + this.newInfo.start_pos + ' ' + this.newInfo.end_pos;
            }
            return this.proteinStructureData != null ? this.proteinStructureData.location : ''
        },
        uniprotLink() {
            return (this.newInfo) ? "https://www.uniprot.org/uniprot/" + this.newInfo.uniprot_id : '';
        },
        stringLink() {
            return this.newInfo ? "https://string-db.org/cgi/network?identifier=" + this.newInfo.string_id : '';
        },
        egrinLink() {
            return this.newInfo ? 'http://networks.systemsbiology.net/hal/gene/' + this.newInfo.locus_tag : '';
        },
        egrin2Link() {
            return this.newInfo ? 'http://egrin2.systemsbiology.net/genes/64091/' + this.newInfo.locus_tag : '';
        },
        downloadMicroarrayURL() {
            return this.newInfo ? BASE_URL + '/download_microarray_data/' + this.newInfo.locus_tag : '';
        },
        cogLink() {
            return this.newInfo ? "https://www.ncbi.nlm.nih.gov/research/cog/cog/" + this.newInfo.cog_id + "/" : '';
        },
        transcriptPDFLink() {
            return this.newInfo ? 'http://networks.systemsbiology.net/projects/halo/transcript_structure/' +
                this.newInfo.locus_tag + '.pdf' : '';
        }
    },
    methods: {
        pfamLink: function(pfamId) { return "https://pfam.xfam.org/family/" + pfamId; },
        // always take the coordinates from the new info structure unless there are none
        // WW: loading the browser too early results in the div not
        // existing sometimes, so we wrap it in a nextTick
        reloadIGVBrowser: function() {
            if (this.newInfo.chrom != '') {
                this.$nextTick(() => {
                    this.loadIGVBrowser(this.newInfo.igv_loc, this.newInfo.track_range);
                });
            }
        },
        loadIGVBrowser: function(igvLoc, trackRange) {
            console.log('track range: ' + trackRange);
            igv.removeAllBrowsers();
            var igvDiv = this.$refs.igv; //document.getElementById("igv");
            var self = this;
            var options = {
                locus: igvLoc,
                showNavigation: true,
                showSVGButton: false,
                reference: {
                    id: "Halobacterium salinarum NRC-1",
                    fastaURL: this.fastaURL,
                    indexURL: this.indexURL,
                    wholeGenomeView: false
                },
                tracks: [
                    {
                        type: "sequence",
                        order: -9007199254740991,
                        frameTranslate: true
                    },
                    {
                        url: STATIC_URL + "split_tracks/ribosomal_RNA_TP1-fwd_" + trackRange + ".bedgraph.gz",
                        type: "wig",
                        format: "bedgraph",
                        logScale: this.isLogScale,
                        autoscaleGroup: "ribo",
                        name: "Ribo-Seq TP1 (+)",
                        color: "darkgrey"
                    },
                    {
                        url: STATIC_URL + "split_tracks/ribosomal_RNA_TP2-fwd_" + trackRange + ".bedgraph.gz",
                        type: "wig",
                        logScale: this.isLogScale,
                        format: "bedgraph",
                        autoscaleGroup: "ribo",
                        name: "Ribo-Seq TP2 (+)",
                        color: "darkgrey"
                    },
                    {
                        url: STATIC_URL + "split_tracks/ribosomal_RNA_TP3-fwd_" + trackRange + ".bedgraph.gz",
                        type: "wig",
                        format: "bedgraph",
                        logScale: this.isLogScale,
                        autoscaleGroup: "ribo",
                        name: "Ribo-Seq TP3 (+)",
                        color: "darkgrey"
                        },
                    {
                        url: STATIC_URL + "split_tracks/ribosomal_RNA_TP4-fwd_" + trackRange + ".bedgraph.gz",
                        type: "wig",
                        format: "bedgraph",
                        logScale: this.isLogScale,
                        autoscaleGroup: "ribo",
                        name: "Ribo-Seq TP4 (+)",
                        color: "darkgrey"
                    },
                    {
                        url: STATIC_URL + "split_tracks/total-RNA-TP1-rev_" + trackRange + ".bedgraph.gz",
                        type: "wig",
                        format: "bedgraph",
                        logScale: this.isLogScale,
                        autoscaleGroup: "tot",
                        name: "RNA-Seq TP1 (+)",
                        color: "darkgrey"
                    },
                    {
                        url: STATIC_URL + "split_tracks/total-RNA-TP2-rev_" + trackRange + ".bedgraph.gz",
                        type: "wig",
                        format: "bedgraph",
                        logScale: this.isLogScale,
                        autoscaleGroup: "tot",
                        name: "RNA-Seq TP2 (+)",
                        color: "darkgrey"
                    },
                    {
                        url: STATIC_URL + "split_tracks/total-RNA-TP3-rev_" + trackRange + ".bedgraph.gz",
                        type: "wig",
                        format: "bedgraph",
                        logScale: this.isLogScale,
                        autoscaleGroup: "tot",
                        name: "RNA-Seq TP3 (+)",
                        color: "darkgrey"
                    },
                    {
                        url: STATIC_URL + "split_tracks/total-RNA-TP4-rev_" + trackRange + ".bedgraph.gz",
                        type: "wig",
                        format: "bedgraph",
                        logScale: this.isLogScale,
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
                        logScale: this.isLogScale,
                        autoscaleGroup: "ribo",
                        name: "Ribo-Seq TP1 (-)",
                        color: "darkgrey"
                    },
                    {
                        url: STATIC_URL + "split_tracks/ribosomal_RNA_TP2-rev_" + trackRange + ".bedgraph.gz",
                        type: "wig",
                        format: "bedgraph",
                        logScale: this.isLogScale,
                        autoscaleGroup: "ribo",
                        name: "Ribo-Seq TP2 (-)",
                        color: "darkgrey"
                    },
                    {
                        url: STATIC_URL + "split_tracks/ribosomal_RNA_TP3-rev_" + trackRange + ".bedgraph.gz",
                        type: "wig",
                        format: "bedgraph",
                        logScale: this.isLogScale,
                        autoscaleGroup: "ribo",
                        name: "Ribo-Seq TP3 (-)",
                        color: "darkgrey"
                    },
                    {
                        url: STATIC_URL + "split_tracks/ribosomal_RNA_TP4-rev_" + trackRange + ".bedgraph.gz",
                        type: "wig",
                        format: "bedgraph",
                        logScale: this.isLogScale,
                        autoscaleGroup: "ribo",
                        name: "Ribo-Seq TP4 (-)",
                        color: "darkgrey"
                    },
                    {
                        url: STATIC_URL + "split_tracks/total-RNA-TP1-fwd_" + trackRange + ".bedgraph.gz",
                        type: "wig",
                        format: "bedgraph",
                        logScale: this.isLogScale,
                        autoscaleGroup: "tot",
                        name: "RNA-Seq TP1 (-)",
                        color: "darkgrey"
                    },
                    {
                        url: STATIC_URL + "split_tracks/total-RNA-TP2-fwd_" + trackRange + ".bedgraph.gz",
                        type: "wig",
                        format: "bedgraph",
                        logScale: this.isLogScale,
                        autoscaleGroup: "tot",
                        name: "RNA-Seq TP2 (-)",
                        color: "darkgrey"
                    },
                    {
                        url: STATIC_URL + "split_tracks/total-RNA-TP3-fwd_" + trackRange + ".bedgraph.gz",
                        type: "wig",
                        format: "bedgraph",
                        logScale: this.isLogScale,
                        autoscaleGroup: "tot",
                        name: "RNA-Seq TP3 (-)",
                        color: "darkgrey"
                    },
                    {
                        url: STATIC_URL + "split_tracks/total-RNA-TP4-fwd_" + trackRange + ".bedgraph.gz",
                        type: "wig",
                        format: "bedgraph",
                        logScale: this.isLogScale,
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
        var newInfoApi = BASE_URL + '/gene_info/' + gene;
        var self = this;
        fetch(newInfoApi)
            .then((response) => { return response.json();
                                }).then((result) => {
                                    if (result.results.length > 0) {
                                        this.newInfo = result.results[0];

                                        // now we almost always have the old locus tag for sure, fetch the rest
                                        gene = this.newInfo.locus_tag;
                                        if (this.newInfo.locus_tag || this.newInfo.gene_symbol) {
                                            this.altGeneDesc = '(';
                                            this.altGeneDesc += this.newInfo.locus_tag;
                                            if (this.newInfo.gene_symbol) {
                                                if (this.altGeneDesc.length > 1) { this.altGeneDesc += ', '; }
                                                this.altGeneDesc += this.newInfo.gene_symbol;
                                            }
                                            this.altGeneDesc += ')';
                                        }

                                        var microarrayApi = BASE_URL + '/microarray_data/' + gene;
                                        var proteinStructureApi = BASE_URL + '/proteinstructure/' + gene;

                                        /*
                                        // always take the coordinates from the new info structure unless there are none
                                        // WW: loading the browser too early results in the div not
                                        // existing sometimes, so we wrap it in a nextTick
                                        if (this.newInfo.chrom != '') {
                                            this.$nextTick(() => {
                                                this.loadIGVBrowser(this.newInfo.igv_loc, this.newInfo.track_range);
                                            });
                                            }*/
                                        this.reloadIGVBrowser();

                                        if (!this.newInfo.is_extra) {
                                            // SBEAMS Microarray
                                            fetch(microarrayApi)
                                                .then((response) => { return response.json();
                                                                    }).then((result) => {
                                                                    this.microarrayData = result.expressions;
                                                                    });

                                            // SBEAMS protein structure
                                            fetch(proteinStructureApi)
                                                .then((response) => {
                                                    return response.json();
                                                }).then((result) => {
                                                    this.proteinStructureData = result.result;
                                                    // there is no location for this gene in the default database table -> retrieve
                                                    // from SBEAMS
                                                    if (this.newInfo.chrom == '') {
                                                        // WW: loading the browser too early results in the div not
                                                        // existing sometimes, so we wrap it in a nextTick
                                                        this.$nextTick(() => {
                                                            this.loadIGVBrowser(this.proteinStructureData.igv_loc, this.proteinStructureData.track_range);
                                                        });
                                                    }
                                                });
                                        }
                                    }
                                }).catch(function() {
                                    self.geneDoesNotExist = true;
                                    console.log('gene not found');
                                });
    },

  }

/* COG link https://www.ncbi.nlm.nih.gov/research/cog/cog/COG1136/ */

</script>
