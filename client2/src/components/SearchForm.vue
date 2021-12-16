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


  </v-container>
</template>

<script>
//var BASE_URL = process.env.VUE_APP_API_BASE_URL;
//var STATIC_URL = process.env.VUE_APP_STATIC_URL;

export default {
    name: 'SearchForm',

    data: () => ({
        gene: '',
        noResults: false,

    }),
    methods: {
        onSubmit: function() {
            this.$router.push({name: 'viewgene', params: { gene: this.gene}});
        }
    }

  }

/* COG link https://www.ncbi.nlm.nih.gov/research/cog/cog/COG1136/ */
</script>
