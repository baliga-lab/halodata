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
    <v-row v-if="annotations.length" class="text-center">
      <h2>Results</h2>
    </v-row>
    <v-row v-if="annotations.length" class="text-center">
      <v-col class="mb-4">
        <v-simple-table>
          <template v-slot:default>
            <thead>
              <tr>
                <th class="text-left">Aliases</th>
                <th class="text-left">Functional Description</th>
                <th class="text-left">Gene Symbol</th>
                <th class="text-left">Location</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="item in annotations" :key="item.full_gene_name">
                <td>{{item.aliases}}</td>
                <td>{{item.functional_description}}</td>
                <td>{{item.gene_symbol}}</td>
                <td>{{item.location}}</td>
              </tr>
            </tbody>
          </template>
        </v-simple-table>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
  var BASE_URL = 'http://localhost:5000';
  export default {
    name: 'SearchForm',

    data: () => ({
        gene: '',
        annotations: []
    }),
    methods: {
        onSubmit: function() {
            var api = BASE_URL + '/annotations/' + this.gene;
            console.log('submitting: ' + api);
            fetch(api)
                .then((response) => { return response.json();
                                    }).then((result) => {
                                        this.annotations = result.annotations;
                });
      }
    }
  }
</script>
