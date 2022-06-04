<template>
  <vue-pdf-embed :source="source2"></vue-pdf-embed>
</template>
<style>
</style>
<script>
import VuePdfEmbed from 'vue-pdf-embed/dist/vue2-pdf-embed'
var STATIC_URL = process.env.VUE_APP_STATIC_URL;

export default {
    name: 'HeatMapStatic',
    components: { VuePdfEmbed },
    data: () => ({
        source1: 'https://raw.githubusercontent.com/mozilla/pdf.js/ba2edeae/examples/learning/helloworld.pdf',
        source2: STATIC_URL + 'S_Atlas_heat_map_expanded.pdf'
    }),
    mounted() {
        console.log(this.source2);
    }
  }
</script>
