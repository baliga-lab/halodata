<template>
  <v-app>
    <v-app-bar
      app
      color="primary"
      dark
    >
      <div class="d-flex align-center">
      <span style="font-size: 18pt">HaloData</span>
      </div>

      <v-spacer></v-spacer>

      <v-btn
        href="https://isbscience.org"
        target="_blank"
        text
      >
        <v-img
          alt="Vuetify Logo"
          class="shrink mr-2"
          contain
          src="@/assets/isb_logo-001.png"
          transition="scale-transition"
          width="200"
        />
        <v-icon>mdi-open-in-new</v-icon>
      </v-btn>
    </v-app-bar>

    <v-main>
      <SearchForm/>
    </v-main>
  </v-app>
</template>

<script>
import SearchForm from './components/SearchForm';

export default {
  name: 'App',

  components: {
    SearchForm,
  },

  data: () => ({
    //
  }),
};
</script>
