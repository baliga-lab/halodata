<template>
<v-container>
  <h1>Heatmap</h1>
  <v-row class="text-center">
    <div id="inchlib"></div>
  </v-row>
</v-container>
</template>

<script>
  import jquery from 'jquery';
  import Kinetic from 'kinetic';
import inchlib2 from 'biojs-vis-inchlib';
var STATIC_URL = process.env.VUE_APP_STATIC_URL;

export default {
    name: 'HeatMap',

    data: () => ({
        gene: '',
    }),
    mounted() {
        window.$ = jquery;
        window.Kinetic = Kinetic;
        var inchlib = new inchlib2({ //instantiate InCHlib
            target: "inchlib", //ID of a target HTML element
            metadata: true, //turn on the metadata
            column_metadata: true, //turn on the column metadata
            max_height: 600, //set maximum height of visualization in pixels
            width: 1000, //set width of visualization in pixels
            heatmap_colors: "RdYlBu", //set color scale for clustered data
            metadata_colors: "BuWhRd", //set color scale for metadata
        });
        inchlib.read_data_from_file(STATIC_URL + "atlas_data2.json");
        inchlib.draw(); //draw cluster heatmap
    }

  }
</script>
