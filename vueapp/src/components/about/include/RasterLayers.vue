<template>
  <div class="row row-cols-1 row-cols-md-1 row-cols-lg-2 row-cols-xl-3 g-4">
     <div class="col" v-for="layer in layersIndex" :key="layer">
      <div class="card w-100">
        <img class="card-img-right" :src="'https://cdn.kadastr.live' + layer.preview" alt="Превью цього слою">
        <div class="card-body">
          <h5 class="card-title">{{ layer.description }}</h5>
          <div class="card-text">
            <div class="row">
              <div class="col-md-12 col-xs-12 my-auto">
                <b>Мінімальний зум:</b> {{layer.minzoom}}<br>
                <b>Максимальний зум:</b> {{layer.maxzoom}}<br>
              </div>
            </div>
          </div>
        </div>
        <div class="card-footer text-muted">
          <!-- TODO: replace all domains hardcode -->
        {{layer.tiles[0].replace('kadastr.live', 'cdn.kadastr.live')}}
        </div>
      </div>
   </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "RasterLayers",
  data() {
    return {
      layersIndex: []
    }
  },
  mounted() {
    axios.get(
        '/tiles/raster/index.json'
    ).then(response => {
      this.layersIndex = response.data;
    });
  }
}
</script>

<style scoped>

</style>