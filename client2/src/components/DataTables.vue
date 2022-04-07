<template>
  <v-container>
    <v-row class="text-center">

      <v-col class="mb-4">
        <h2 class="display-2 font-weight-bold mb-3">Browsable Tables</h2>
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
                  <td style="text-align: left"><router-link :to="{name: 'viewgene', params: {gene: item.old_name}}">{{item.representative}}</router-link></td>
                  <td >{{item.product}}</td>
                  <td>{{item.locus_tag}}</td>
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
                  <td ><a :href="makeCOGLink(item.cog_id)" target="_blank">{{item.cog_id}}</a></td>
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