<template>
  <v-container fill-height fluid style="margin: 0px; padding: 0px; width: 100%">
<v-row style="height: 50px">
  <v-col class="mb-4"><i>Note: Loading might take a while. Please wait. Meanwhile you can <a :href="pdfURL" target="_blank">download a static version</a></i></v-col>
</v-row>
<v-row class="fill-height">
  <iframe width="100%" height="100%" :src="heatmapURL"></iframe>
</v-row>
</v-container>
</template>
<style>
  .v-progress-circular {
  margin: 1rem;
  }
</style>
<script>
var STATIC_URL = process.env.VUE_APP_STATIC_URL;

export default {
    name: 'HeatMap',

    data: () => ({
        heatmapURL: 'https://parlak.systemsbiology.net/haloheatmap/',
        pdfURL: STATIC_URL + 'S_Atlas_heat_map_expanded.pdf'
    })
  }
</script>
