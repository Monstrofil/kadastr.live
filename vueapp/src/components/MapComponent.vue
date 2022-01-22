<template>
  <div ref="map" style="height: 30vh; width: 100%">
    <SearchBox
        :downloadAvailable="isDownloadAvailable"
        @select="onSelectParcel"
        @download="onDownloadClick"
        ref="searchBox"
    />
  </div>

</template>
<script>
import mapboxgl from "mapbox-gl";
import { ref } from "vue";
import {layerControlGrouped} from "@/layerControlGrouped";
import SearchBox from "@/components/SearchBox";

export default {
  name: 'MapComponent',
  components: {
    SearchBox
  },
  props: {
    location: {
      type: Object,
      default: () => {
        return {lng: 32.77207908430876, lat: 48.428743769294925}
      }
    },
    mapStyle: {
      type: String,
      default: "mapbox://styles/mapbox/light-v9"
    },
    enableLayers: {
      type: Array,
      default: function () {
        return [];
      }
    }
  },
  setup() {
    const searchBox = ref(null);
    return { searchBox };
  },
  data() {
    return {
      highlightedRoads: null,
      popup: null,
      isDownloadAvailable: null
    }
  },
  methods: {
    onDownloadClick: function () {
        const bounds = this.map.getBounds();
        const url = '/export/' + bounds._sw.lat + '/' + bounds._sw.lng + '/' + bounds._ne.lat + '/' + bounds._ne.lng + '/'
        window.open(url, '_blank');
    },
    onSelectParcel: function (parcel) {
      this.map.flyTo({
        center: [
          parcel.location[0],
          parcel.location[1]
        ],
        speed: 4,
        screenSpeed: 4,
        zoom: 19,
        essential: true
      })
    },
    enter_point: function (e) {
        var coordinates = e.lngLat;
        var description = 'Номер: ' + e.features[0].properties.cadnum;
        if (e.features[0].properties.address) {
            description += '<br>Адреса: ' + e.features[0].properties.address;
        }
        if (e.features[0].properties.purpose_code) {
            description += '<br>Призначення: ' + e.features[0].properties.purpose_code;
        }
        if (e.features[0].properties.category) {
            description += '<br>Категорія: ' + e.features[0].properties.category;
        }
        if (e.features[0].properties.ownership) {
            description += '<br>Власність: ' + e.features[0].properties.ownership;
        }

        // Populate the popup and set its coordinates
        // based on the feature found.
        this.popup.setLngLat(coordinates).setHTML(description).addTo(this.map);
    },

    leave_point: function() {
        this.popup.remove();
    }
  },
  mounted() {
    this.map = new mapboxgl.Map({
      container: this.$refs.map,
      style: this.mapStyle,
      center: this.location,
      zoom: 5,
      hash: true
    });

    this.map.on('load', () => {
      // Create a popup, but don't add it to the map yet.
      this.popup = new mapboxgl.Popup({
          closeButton: false,
          closeOnClick: false
      });

      var config = {
        collapsed: false,
        layers: [
          {
            id: "land_polygones",
            name: "Геометрія ділянок",
            hidden: false,
            group: "ДЗК",
            directory: "Оверлей",
            metadata: {
              filterSchema: {
                "ownership": {
                  type: "select",
                  hint: "Форма власності",
                  options: [
                    {
                      id: "Державна власність",
                      name: "Державна власність"
                    },
                    {
                      id: "Комунальна власність",
                      name: "Комунальна власність"
                    },
                    {
                      id: "Приватна власність",
                      name: "Приватна власність"
                    },
                    {
                      id: "Не визначено",
                      name: "Не визначено",
                      customFilter: ["any", ["==", ["get", "ownership"], ""], ["==", ["get", "ownership"], "Не визначено"]]
                    }
                  ]
                }
                ,
                "category": {
                  type: "select",
                  hint: "Категорія земель",
                  options: [
                    {
                      id: "Землі водного фонду",
                      name: "Водний фонд"
                    },
                    {
                      id: "Землі житлової та громадської забудови",
                      name: "Житлова та громадська забудова"
                    },
                    {
                      id: "Землі історико-культурного призначення",
                      name: "Історико-культурні ділянки"
                    },
                    {
                      id: "Землі лісогосподарського призначення",
                      name: "Лісове господарство"
                    },
                    {
                      id: "Землі оздоровчого призначення",
                      name: "Оздоровчого призначення"
                    },
                    {
                      id: "Землі природно-заповідного та іншого природоохоронного призначення",
                      name: "Природоохоронного призначення"
                    },
                    {
                      id: "Землі промисловості, транспорту, зв’язку, енергетики, оборони та іншого призначення",
                      name: "Промисловості, транспорту, оборони"
                    },
                    {
                      id: "Землі рекреаційного призначення",
                      name: "Рекреаційного призначення"
                    },
                    {
                      id: "Землі сільськогосподарського призначення",
                      name: "Сільськогосподарського призначення"
                    },
                    {
                      id: "Не визначено",
                      name: "Інше",
                      customFilter: ["any", ["==", ["get", "category"], ""], ["==", ["get", "category"], "Не визначено"]]
                    },
                  ]
                }
              },
              lazyLoading: true
            }
          },
          {
            id: "orto-tiles",
            name: "Ортофото ДЗК (2011)",
            hidden: false,
            group: "Фонові зображення",
            directory: "Базові шари"
          },
          {
            id: "orto-ersi",
            name: "Ортофото Ersi (2018+)",
            hidden: false,
            group: "Фонові зображення",
            directory: "Базові шари"
          },
          {
            id: "dzk",
            name: "WMS шар ДЗК",
            hidden: false,
            group: "Фонові зображення",
            directory: "Базові шари"
          },
          {
            id: "openstreetmap",
            name: "OpenStreetMap",
            hidden: false,
            group: "Фонові зображення",
            directory: "Базові шари"
          },
        ]
      }

      this.isDownloadAvailable = this.map.getZoom() > 13;
      this.map.on('zoomend', () => {
        this.isDownloadAvailable = this.map.getZoom() > 13;
      });

      this.map.addControl(this.searchBox, "top-left");
      this.map.addControl(new layerControlGrouped(config), "top-right");

      this.enableLayers.forEach((item) => {
        this.map.setLayoutProperty(item, 'visibility', 'visible')
      })

      this.map.on('click', 'land_polygones', (e) => {
        const feature = e.features[0];
        console.log(feature)

        // hack to save map location in history
        // this.$router.replace({hash: window.location.hash}).finally(() => {
        //   this.$router.push({
        //     name: 'road_info',
        //     params: {pk: feature.id}
        //   })
        // });
      });

      this.map.on('mouseleave', 'land_polygones', () => {
        this.leave_point();
        this.$emit('unselected');
        this.map.getCanvas().style.cursor = 'auto';
        if (this.highlightedRoads) {
          this.highlightedRoads.forEach((featureId) => {
            this.map.setFeatureState(
                {source: 'cadastr', id: featureId, sourceLayer: 'land_polygons'},
                {hover: false}
            );
          })
        }
        this.highlightedRoads = [];
      });
      // this.map.on('mouseenter', 'land_polygones', (e) => {
      //   this.enter_point(e);
      // })
      this.map.on('mousemove', 'land_polygones', (e) => {
        this.enter_point(e);
        // Change the cursor style as a UI indicator.
        this.map.getCanvas().style.cursor = 'pointer';

        if (this.highlightedRoads) {
          this.highlightedRoads.forEach((featureId) => {
            this.map.setFeatureState(
                {source: 'cadastr', id: featureId, sourceLayer: 'land_polygons'},
                {hover: false}
            );
          })
        }

        this.highlightedRoads = [];
        e.features.forEach((feature) => {
          this.map.setFeatureState(
              {source: 'cadastr', id: feature.id, sourceLayer: 'land_polygons'},
              {hover: true}
          );
          this.highlightedRoads.push(feature.id)
        })
        this.$emit('selected', e.features);
      });
    });
  }
}
</script>
<style>

.mapboxgl-ctrl-top-left {
  width: 450px;
}
.mapboxgl-ctrl-top-right {
  width: 500px;
}

.mgl-layerControl {
  width: calc(70% + 20px) !important;
}

</style>
