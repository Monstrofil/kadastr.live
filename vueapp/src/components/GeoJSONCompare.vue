<template>
  <div class="wrapper">
    <div ref="comparison-container">
      <div ref="before"></div>
      <div ref="after"></div>
    </div>
  </div>

</template>

<script>
import maplibregl from "maplibre-gl";
import Compare from "mapbox-gl-compare";
import * as turf from "@turf/turf";

export default {
  name: "GeoJSONCompare",
  props: {
    leftGeoJson: null,
    rightGeoJson: null
  },
  mounted() {
    var before = new maplibregl.Map({
      container: this.$refs.before, // Container ID
      style: '/style/vector_style_28_09_2022.json'
    });

    before.on('load', () => {

      let bbox = turf.bbox({
        "type": "FeatureCollection",
        "features": [
          {
            "type": "Feature",
            "properties": {},
            "geometry": this.leftGeoJson
          },
          {
            "type": "Feature",
            "properties": {},
            "geometry": this.rightGeoJson
          }
        ]
      });
      before.fitBounds(bbox, {duration: 0, padding: 30});
      if (this.leftGeoJson) {
        before.addSource('geojson', {
          type: 'geojson',
          data: {
            "type": "Feature",
            "properties": {},
            "geometry": this.leftGeoJson
          }
        });

        before.addLayer({
          'id': 'geojson-layer',
          'type': 'fill',
          'source': 'geojson',
          'paint': {
            "fill-opacity": .8,
            "fill-color": "#ff9b9b"
          }
        });
      }

    });

    var after = new maplibregl.Map({
      container: this.$refs.after, // Container ID
      style: '/style/vector_style_28_09_2022.json'
    });

    after.on('load', () => {
      after.addSource('geojson', {
        type: 'geojson',
        data: {
          "type": "Feature",
          "properties": {},
          "geometry": this.rightGeoJson
        }
      });

      after.addLayer({
        'id': 'geojson-layer',
        'type': 'fill',
        'source': 'geojson',
        'paint': {
          "fill-opacity": .8,
          "fill-color": "#93ff93"
        }
      });
    });

    // A selector or reference to HTML element
    var container = this.$refs["comparison-container"];

    new Compare(before, after, container, {
      // mousemove: true, // Optional. Set to true to enable swiping during cursor movement.
      orientation: 'vertical' // Optional. Sets the orientation of swiper to horizontal or vertical, defaults to vertical
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

<style>
.mapboxgl-compare .compare-swiper-vertical {
  width: 30px;
  height: 30px;
  top: 50%;
  left: -15px;
  margin: -15px 1px 0;
  cursor: ew-resize;
  background-size: contain;
}
</style>