<template>
  <v-container fill-height fluid style="margin: 0px; padding: 0px; width: 100%">
<v-row style="height: 50px">
  <v-col class="mb-4"><i>Note: Loading might take a while, please wait until loaded</i></v-col>
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
export default {
    name: 'HeatMap',

    data: () => ({
        heatmapURL: 'https://parlak.systemsbiology.net/haloheatmap/'
    })
  }
</script>
