<template>
<iframe width="100%" height="100%" :src="heatmapURL"></iframe>
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
