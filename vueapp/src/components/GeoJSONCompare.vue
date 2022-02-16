<template>
  <div class="wrapper">
    <div ref="comparison-container">
      <div ref="before"></div>
      <div ref="after"></div>
    </div>
  </div>

</template>

<script>
import mapboxgl from "mapbox-gl";
import Compare from "mapbox-gl-compare";
import * as turf from "@turf/turf";

export default {
  name: "GeoJSONCompare",
  props: {
    leftGeoJson: null,
    rightGeoJson: null
  },
  mounted() {
    var before = new mapboxgl.Map({
      container: this.$refs.before, // Container ID
      style: 'mapbox://styles/mapbox/light-v9'
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
      before.fitBounds(bbox, {duration: 0, offset: [20, 20]});
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
            "fill-opacity": 0.5,
            "fill-color": "rgb(200,110,41)"
          }
        });
      }

    });

    var after = new mapboxgl.Map({
      container: this.$refs.after, // Container ID
      style: 'mapbox://styles/mapbox/light-v9'
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
          "fill-opacity": 0.5,
          "fill-color": "rgb(142,200,41)"
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