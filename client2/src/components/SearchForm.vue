<template>
  <v-container>
    <v-row class="text-center">

      <v-col class="mb-4">
        <h2 class="display-2 font-weight-bold mb-3">Gene Search</h2>
        <div>
          <v-form ref="form" v-model="valid"
                  lazy-validation>
            <v-text-field
              v-model="gene"
              :counter="10"
              label="Search (e.g. VNG00001)"
              required>
            </v-text-field>
          </v-form>
        </div>

      </v-col>

    </v-row>
  </v-container>
</template>

<script>
  export default {
    name: 'SearchForm',

  data: () => ({
  gene: ''
    }),
  }
</script>
