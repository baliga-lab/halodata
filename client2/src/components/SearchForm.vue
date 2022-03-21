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
    <v-row>
      <v-list-item v-for="(item, index) in results" :key="item.full_gene_name">
        <v-list-item-content>
          <v-list-item-title>{{index + 1}}. <router-link :to="{name: 'viewgene', params: {gene: item.full_gene_name}}">{{item.new_name}}</router-link>
            ({{item.full_gene_name}}, {{item.gene_symbol}})</v-list-item-title>
          <v-list-item-subtitle>{{item.functional_description}}</v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>
    </v-row>


  </v-container>
</template>

<script>
var BASE_URL = process.env.VUE_APP_API_BASE_URL;

export default {
    name: 'SearchForm',

    data: () => ({
        gene: '',
        results: [],
        noResults: false,

    }),
    methods: {
        onSubmit: function() {
            //this.$router.push({name: 'viewgene', params: { gene: this.gene}});
            var searchApi = BASE_URL + '/search/' + this.gene;
            fetch(searchApi)
                .then((response) => {
                    return response.json();
                }).then((result) => {
                    this.results = result.results;
                    this.noResults = this.results.length == 0;
                });
        }
    }

  }

/* COG link https://www.ncbi.nlm.nih.gov/research/cog/cog/COG1136/ */
</script>
