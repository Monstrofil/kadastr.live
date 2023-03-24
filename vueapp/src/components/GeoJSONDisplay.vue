<template>
  <div class="wrapper">
    <div ref="map_container"></div>
  </div>

</template>

<script>
import maplibregl from "maplibre-gl";
import * as turf from "@turf/turf";

export default {
  name: "GeoJSONDisplay",
  props: {
    geoFeature: null
  },
  mounted() {
    var map = new maplibregl.Map({
      container: this.$refs.map_container, // Container ID
      style: '/style/vector_style_24_03_2023.json'
    });

    map.on('load', () => {
      let bbox = turf.bbox({
        "type": "FeatureCollection",
        "features": [
          {
            "type": "Feature",
            "properties": {},
            "geometry": this.geoFeature
          }
        ]
      });

      map.fitBounds(bbox, {duration: 0, padding: 50});
      if (this.geoFeature) {
        map.addSource('geojson', {
          type: 'geojson',
          data: {
            "type": "Feature",
            "properties": {},
            "geometry": this.geoFeature
          }
        });

        map.addLayer({
          'id': 'geojson-layer',
          'type': 'fill',
          'source': 'geojson',
          'paint': {
            "fill-opacity": .8,
            "fill-color": "rgb(175,0,0)"
          }
        });
      }

    });
  }
}
</script>

<style scoped>
#comparison-container {
  width: 100%;
}

.mapboxgl-map {
  height: 300px;
  width: 100%;
  position: absolute;
}

.wrapper {
  position: relative;
}


</style>
