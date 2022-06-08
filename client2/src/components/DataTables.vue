<template>
  <v-container>
    <v-row class="text-center">
      <v-col class="mb-4">
        <h2 class="display-2 font-weight-bold mb-3"><i>Halobacterium salinarum</i> NRC-1 Atlas</h2>
      </v-col>
    </v-row>
    <v-row class="text-left">
      <v-col class="mb-4">
        <p style="font-style: italic">Type the gene locus tag or protein product in the search box to query for representative genes. Once you find the target representative gene, click on the locus tag (first or third column) to see it in the genome browser.</p>
      </v-col>
    </v-row>

    <v-row>
      <v-tabs v-model="tab">
        <v-tab key="locus">Locus Tag</v-tab>
        <v-tab key="cog">COG Info</v-tab>
        <v-tab key="is">IS Info</v-tab>
      </v-tabs>
      <v-tabs-items v-model="tab">
        <v-tab-item key="locus">
          <v-card>
            <v-card-title>
              Locus Tag Dictionary
              <v-spacer></v-spacer>
              <v-text-field
                v-model="ltSearch"
                append-icon="mdi-magnify"
                label="Search"
                single-line
                hide-details
                ></v-text-field>
            </v-card-title>
            <v-data-table
              :headers="ltHeaders"
              :items="locusTagData"
              :search="ltSearch"
              item-key="representative">
              <template v-slot:item="{item}">
                <tr>
                  <td style="text-align: left"><router-link :to="{name: 'viewgene', params: {gene: item.representative}}">{{item.representative}}</router-link></td>
                  <td >{{item.product}}</td>
                  <td><span style="margin-right: 3pt" v-for="locus_tag in item.locus_tag" :key="locus_tag"><span v-if="isInternalGene(locus_tag)"><router-link :to="{name: 'viewgene', params: {gene: locus_tag}}">{{locus_tag}}</router-link></span><span v-else>{{locus_tag}}</span></span></td>
                </tr>
              </template>
            </v-data-table>
          </v-card>
        </v-tab-item>

        <v-tab-item key="cog">

          <v-card>
            <v-card-title>
              COG Information
              <v-spacer></v-spacer>
              <v-text-field
                v-model="cogSearch"
                append-icon="mdi-magnify"
                label="Search"
                single-line
                hide-details
                ></v-text-field>
            </v-card-title>

            <v-data-table
              :headers="cogHeaders"
              :items="cogData"
              :search="cogSearch"
              item-key="representative">
              <template v-slot:item="{item}">
                <tr>
                  <td style="text-align: left"><router-link :to="{name: 'viewgene', params: {gene: item.old_name}}">{{item.representative}}</router-link></td>
                  <td><span style="margin-right: 3pt;" v-for="cog_id in item.cog_ids" :key="cog_id"><a :href="makeCOGLink(cog_id)" target="_blank">{{cog_id}}</a></span></td>
                  <td>{{item.cog_name}}</td>
                  <td>{{item.cog_category}}</td>
                  <td>{{item.cog_pathway}}</td>
                </tr>
              </template>
            </v-data-table>
          </v-card>
        </v-tab-item>

        <v-tab-item key="is">


          <v-card>
            <v-card-title>
              Insertion Sequence Information
              <v-spacer></v-spacer>
              <v-text-field
                v-model="isSearch"
                append-icon="mdi-magnify"
                label="Search"
                single-line
                hide-details
                ></v-text-field>
            </v-card-title>

            <v-data-table
              :headers="isHeaders"
              :items="isData"
              :search="isSearch"
              item-key="representative">
              <template v-slot:item="{item}">
                <tr>
                  <td style="text-align: left"><router-link :to="{name: 'viewgene', params: {gene: item.old_name}}">{{item.representative}}</router-link></td>
                  <td >{{item.is_name}}</td>
                  <td>{{item.is_family}}</td>
                  <td>{{item.is_subgroup}}</td>
                </tr>
              </template>
            </v-data-table>
          </v-card>
        </v-tab-item>

      </v-tabs-items>
    </v-row>


  </v-container>
</template>

<script>
var BASE_URL = process.env.VUE_APP_API_BASE_URL;
var COG_BASE_URL = "https://www.ncbi.nlm.nih.gov/research/cog/cog/";

export default {
    name: 'DataTables',

    data: () => ({
        tab: null,
        ltSearch: '',
        locusTagData: [],
        cogLink: '',
        ltHeaders: [
          {text: 'Representative', value: 'representative'},
          {text: 'Product', value: 'product'},
          {text: 'Locus Tag', value: 'locus_tag'}
        ],
        cogSearch: '',
        cogData: [],
        cogHeaders: [
          {text: 'Representative', value: 'representative'},
          {text: 'COG ID', value: 'cog_id'},
          {text: 'COG Name', value: 'cog_name'},
          {text: 'COG Category', value: 'cog_category'},
          {text: 'Functional Pathway', value: 'cog_pathway'}
        ],
        isSearch: '',
        isData: [],
        isHeaders: [
          {text: 'Representative', value: 'representative'},
          {text: 'IS Name', value: 'is_name'},
          {text: 'IS Family', value: 'is_family'},
          {text: 'IS Subgroup', value: 'is_subgroup'}
        ],

    }),
    methods: {
        makeCOGLink(cogID) {
            return COG_BASE_URL + cogID + "/";
        },
        isInternalGene(locus_tag) {
            return locus_tag.startsWith('VNG_') && !locus_tag.startsWith('VNG_RS');
        }
    },
    mounted() {
        fetch(BASE_URL + '/locus_tag_entries')
            .then((response) => { return response.json();
                                }).then((result) => {
                                    this.locusTagData = result.entries;
                                });
        fetch(BASE_URL + '/cog_info_entries')
            .then((response) => { return response.json();
                                }).then((result) => {
                                    this.cogData = result.entries;
                                });
        fetch(BASE_URL + '/is_info_entries')
            .then((response) => { return response.json();
                                }).then((result) => {
                                    this.isData = result.entries;
                                });
    }
  }

/* COG link https://www.ncbi.nlm.nih.gov/research/cog/cog/COG1136/ */
</script>
