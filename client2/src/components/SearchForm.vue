<template>
  <v-container>
    <v-row class="text-center">

      <v-col class="mb-4">
        <h2 class="display-2 font-weight-bold mb-3">Gene Search</h2>
        <div>
          <v-form ref="form" @submit.prevent>
            <v-text-field
              v-model="gene"
              label="Search (e.g. VNG00001)"
              @keydown.enter="onSubmit">
            </v-text-field>
          </v-form>
        </div>

      </v-col>
    </v-row>
    <v-row v-if="noResults" class="text-center">
      <h2>No results found</h2>
    </v-row>
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
      <v-row>
        <h4>DNA</h4>
        <p style="font-family: Courier; font-size: 8pt; text-align: left">
          {{proteinStructureData.dna}}
        </p>
      </v-row>
      <v-row>
        <h4>Peptide</h4>
        <p style="font-family: Courier; font-size: 8pt; text-align: left">
          {{proteinStructureData.peptide}}
        </p>
      </v-row>
    </div>
    <v-spacer style="height: 12pt"></v-spacer>

    <!-- Microarray data -->
    <v-row v-if="microarrayData.length" class="text-center">
      <h4>Microarray Data</h4>
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
    name: 'SearchForm',

    data: () => ({
        gene: '',
        microarrayData: [],
        proteinStructureData: null,
        maHeaders: [
          {text: 'Condition', value: 'condition'},
          {text: 'Log10 Ratio', value: 'log10_ratio'},
          {text: 'Lambda', value: 'lambda'}
        ],
        noResults: false,

        // IGV Browser stuff
        locus: "NC_002607.1:1400-2165",
        fastaURL: STATIC_URL + "Hsalinarum.fa",
        indexURL: STATIC_URL + "Hsalinarum.fa.fai",
        igv: null

    }),
    methods: {
        onSubmit: function() {
            //var annotationApi = BASE_URL + '/annotations/' + this.gene;
            var microarrayApi = BASE_URL + '/microarray_data/' + this.gene;
            var proteinStructureApi = BASE_URL + '/proteinstructure/' + this.gene;
            /*
            fetch(annotationApi)
                .then((response) => { return response.json();
                                    }).then((result) => {
                                        this.annotations = result.annotations;
                                        this.noResults = this.annotations.length == 0;
                });
*/
            fetch(microarrayApi)
                .then((response) => { return response.json();
                                    }).then((result) => {
                                        this.microarrayData = result.expressions;
                });
            fetch(proteinStructureApi)
                .then((response) => { return response.json();
                                    }).then((result) => {
                                        this.proteinStructureData = result.result;
                                        this.loadIGVBrowser(this.proteinStructureData.igv_loc);
                });
        },
        loadIGVBrowser: function(igvLoc) {
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
                        url: STATIC_URL + "Hsalinarum-gene-annotation-pfeiffer2019-adjusted-names.gff3",
                        type: "annotation",
                        searchable: true,
                        format: "gff3",
                        name: "Genes",
                        color: "#4E79A7",
                        displayMode: "COLLAPSED"
                    },
                ]
            };
            igv.createBrowser(igvDiv, options)
                .then(function (browser) {
                    self.igv = browser;
            });
        }
    },
    mounted() {
    },

  }

/* COG link https://www.ncbi.nlm.nih.gov/research/cog/cog/COG1136/ */
</script>
