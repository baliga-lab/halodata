<template>
  <v-container>
    <v-row class="text-center">

      <v-col class="mb-4">
        <h2 class="display-2 font-weight-bold mb-3">Gene Search</h2>
        <div v-if="false">
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
    <v-row class="text-center">
      <v-col class="mb-4">
        <v-autocomplete v-model="autocompleteModel"
                        :items="autocompleteItems"
                        :loading="isAutocompleteLoading"
                        :search-input.sync="autocompleteSearch"
                        color="white"
                        item-text="Description"
                        item-value="API"
                        label="Search (e.g. VNG0002G)"
                        placeholder="Search (e.g. VNG0002G)"
                        prepend-icon="mdi-database-search"
                        @change="onAutocompleteChange"
                        clearable
                        return-object>
        </v-autocomplete>
        <v-expand-transition>
          <v-list v-if="autocompleteModel">
            <v-list-item
              v-for="(field, i) in fields"
              :key="i">
              <v-list-item-content>
                <v-list-item-title v-text="field.value"></v-list-item-title>
                <v-list-item-subtitle v-text="field.key"></v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
          </v-list>
        </v-expand-transition>
      </v-col>
    </v-row>
    <v-row v-if="noResults" class="text-center">
      <h2>No results found</h2>
    </v-row>
    <v-row>
      <v-list-item v-for="(item, index) in results" :key="item.coords">
        <v-list-item-content>
          <v-list-item-title>{{((page - 1) * perPage) + index + 1}}. <router-link :to="{name: 'viewgene', params: {gene: item.full_gene_name}}">{{item.new_name}}</router-link>
            ({{item.full_gene_name}}, {{item.gene_symbol}})</v-list-item-title>
          <v-list-item-subtitle>{{item.functional_description}}</v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>
    </v-row>
    <v-row v-if="results.length > 0">
      <v-pagination @input="onPageClicked" v-model="page" :length="Math.ceil(numEntries/perPage)"></v-pagination>
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
        page: 1,
        perPage: 10,
        numEntries: 0,

        // autocomplete
        autocompleteCount: 0,
        autocompleteEntries: [],
        autocompleteModel: null,
        isAutocompleteLoading: false,
        autocompleteSearch: null
    }),
    computed: {
        fields () {
            if (!this.model) return [];
            return Object.keys(this.model).map(key => {
                return {
                    key, value: this.model[key] || 'n/a'
                }
            })
        },
        autocompleteItems () {
            return this.autocompleteEntries.map(entry => {
                const Description = entry.Description.length > this.descriptionLimit
                      ? entry.Description.slice(0, this.descriptionLimit) + '...'
                      : entry.Description;
                return Object.assign({}, entry, {Description});
            });
        }
    },
    watch: {
        autocompleteSearch (val) {
            if (val == null || val.length < 3) return;
            if (this.isAutocompleteLoading) return;
            this.isAutocompleteLoading = true;
            fetch(BASE_URL + '/autocomplete/' + val)
                .then(res => { return res.json() })
                .then(res => {
                    const { count, entries } = res;
                    var finalCount = count;
                    if (count > 1) {
                        entries.unshift({'Description': val + '*' });
                        finalCount += 1;
                    }
                    this.autocompleteCount = finalCount;
                    this.autocompleteEntries = entries;
                })
                .catch (err => {
                    console.log(err)
                })
                .finally(() => (this.isAutocompleteLoading = false))
        }
    },
    methods: {
        doSearch(searchTerm) {
            var searchApi = BASE_URL + '/search2/' + searchTerm + '&start=' + ((this.page - 1) * this.perPage);
            fetch(searchApi)
                .then((response) => {
                    return response.json();
                }).then((result) => {
                    this.results = result.results;
                    this.noResults = this.results.length == 0;
                    this.numEntries = result.total;
                });
        },
        onPageClicked: function() {
            this.doSearch(this.gene);
        },
        onSubmit: function() {
            this.page = 1;
            this.doSearch(this.gene);
        },
        onAutocompleteChange: function() {
            if (this.autocompleteModel) {
                this.doSearch(this.autocompleteModel.Description);
            } else {
                console.log('not found');
            }
        }
    }

  }

/* COG link https://www.ncbi.nlm.nih.gov/research/cog/cog/COG1136/ */
</script>
