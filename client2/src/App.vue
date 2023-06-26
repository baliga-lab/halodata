<template>
  <v-app>
    <v-app-bar
      app
      color="primary"
      hide-on-scroll
      dark
    >
      <div class="d-flex align-center">
        <span style="font-size: 14pt; font-weight: bold"><i>H. salinarum</i> NRC-1 Atlas&nbsp;&nbsp;&nbsp;</span>
      </div>

      <v-btn to="/" text>Home</v-btn>
      <v-btn to="/heatmap" text>Atlas</v-btn>
      <!-- <v-btn to="/heatmapstatic" text>Atlas (Static)</v-btn> -->
      <v-btn to="/about" text>About</v-btn>
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
          src="@/assets/isb_logo-002.png"
          transition="scale-transition"
          width="200"
        />
      </v-btn>
    </v-app-bar>

    <v-main>
      <router-view></router-view>
    </v-main>
    <v-footer>Developed by Baliga Lab at the Institute for Systems Biology</v-footer>
    <div ref="scriptHolder"></div>
  </v-app>
</template>

<script>
export default {
    name: 'App',
    created() {
        document.title = "H. salinarum NRC-1 Atlas";
    },
    mounted() {
        let gaScript1 = document.createElement('script');
        gaScript1.setAttribute("src", "https://www.googletagmanager.com/gtag/js?id=G-23G880QVFQ");
        let gaScript2 = document.createElement('script');
        gaScript2.textContent = "window.dataLayer=window.dataLayer || [];" +
            "function gtag(){dataLayer.push(arguments);}" +
            "gtag('js', new Date());" +
            "gtag('config', 'G-23G880QVFQ');";
        this.$refs.scriptHolder.append(gaScript1);
        this.$refs.scriptHolder.append(gaScript2);
    },
    data: () => ({
    }),
};
</script>
