<template>
<v-container>
  <h1>Heatmap</h1>
  <v-row class="text-center">
    <div id="inchlib"><v-progress-circular
                        color="blue" indeterminate
                        size="60" width="8"></v-progress-circular></div>
  </v-row>
</v-container>
</template>
<style>
  .v-progress-circular {
  margin: 1rem;
  }
</style>
<script>
  import jQuery from 'jquery';
  import Kinetic from 'kinetic';
import inchlib2 from '@baliga-lab/inchlib.js';
var STATIC_URL = process.env.VUE_APP_STATIC_URL;

export default {
    name: 'HeatMap',

    data: () => ({
        gene: '',
    }),
    mounted() {
        window.jQuery = jQuery;
        window.$ = jQuery;
        window.Kinetic = Kinetic;
        console.log(inchlib2);
        console.log(jQuery);
        window.inchlib = new inchlib2(jQuery, { //instantiate InCHlib
            target: "inchlib", //ID of a target HTML element
            metadata: true, //turn on the metadata
            column_metadata: true, //turn on the column metadata
            max_height: 600, //set maximum height of visualization in pixels
            width: 1000, //set width of visualization in pixels
            heatmap_colors: "RdYlBu", //set color scale for clustered data
            metadata_colors: "BuWhRd", //set color scale for metadata
        });
        var heatmap_url = STATIC_URL + "atlas_data2.json"
        // TODO: read async
        fetch(heatmap_url).then(r => r.json()).then(json => {
            window.inchlib.read_data(json);
            window.inchlib.draw(); //draw cluster heatmap
        });
    }

  }
</script>
