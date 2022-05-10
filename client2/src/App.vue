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

      <v-btn text></v-btn>
      <v-btn to="/" text>Home</v-btn>
      <v-btn to="/heatmap" text>Atlas</v-btn>
      <v-btn to="/datatables" text>Browse</v-btn>
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
      <router-view></router-view>
    </v-main>
    <v-footer>&copy; 2022 A. Lorenzetti et al. Funding provided by S&atilde;o Paulo Research Foundation</v-footer>
  </v-app>
</template>

<script>

export default {
    name: 'App',


    data: () => ({
    })
};
</script>
