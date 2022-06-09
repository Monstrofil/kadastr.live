<template>
  <div ref="map" style="height: 30vh; width: 100%">
    <SearchBox
        :downloadAvailable="isDownloadAvailable"
        @select="onSelectParcel"
        @download="onDownloadClick"
        ref="searchBox"
    />

    <component
        :is="selectedItem !== null ? renderer[selectedItem.sourceLayer] : 'ParcelInfo'"
        :feature="selectedItem"
        :is_touchable="false"
        id="popup-content"/>
  </div>

</template>
<script>
import maplibregl from "maplibre-gl";
import { ref } from "vue";
import {layerControlGrouped} from "@/layerControlGrouped";
import SearchBox from "@/components/SearchBox";
import ParcelInfo from "@/components/ParcelInfo";
import NatureInfo from "@/components/NatureInfo";
import IndexInfo from "@/components/IndexInfo";

export default {
  name: 'MapComponent',
  components: {
    ParcelInfo,
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
    const pzfInfo = ref(null);

    return { searchBox, pzfInfo };
  },
  data() {
    return {
      highlightedParcels: null,
      popup: null,
      isDownloadAvailable: null,
      ignoreClick: null,
      touchInsideParcel: null,
      selectedItem: null,
      renderer: {
        'land_polygons': ParcelInfo,
        'pzf_data': NatureInfo,
        'index_data': IndexInfo,
        null: NatureInfo,
      }
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
    highlightParcels(e) {
      const features = this.map.queryRenderedFeatures(e.point);
      if(!features){
        this.selectedItem = null;
        return
      }
      this.selectedItem = features[0];
      console.log('Selected: ', this.selectedItem)
      this.enter_point(e);
      // Change the cursor style as a UI indicator.
      this.map.getCanvas().style.cursor = 'pointer';

      if (this.highlightedParcels) {
        this.highlightedParcels.forEach((feature) => {
          this.map.setFeatureState(
              {source: feature.source, id: feature.id, sourceLayer: this.selectedItem.sourceLayer},
              {hover: false}
          );
        })
      }

      this.highlightedParcels = [];
      features.forEach((feature) => {
        this.map.setFeatureState(
            {source: feature.source, id: feature.id, sourceLayer: this.selectedItem.sourceLayer},
            {hover: true}
        );
        this.highlightedParcels.push(feature)
      })
    },
    enter_point: function (e) {
        var coordinates = e.lngLat;

        // Populate the popup and set its coordinates
        // based on the feature found.
        this.popup
            .setLngLat(coordinates)
            .addTo(this.map);
    },

    leave_point: function() {
        this.selectedItem = null;
        this.popup.remove();
    }
  },
  mounted() {
    this.map = new maplibregl.Map({
      container: this.$refs.map,
      style: this.mapStyle,
      center: this.location,
      zoom: 5,
      hash: true
    });

    this.map.on('load', () => {
      // Create a popup, but don't add it to the map yet.
      this.popup = new maplibregl.Popup({
          closeButton: true,
          closeOnClick: false,
          focusAfterOpen: true
      });
      this.popup
            .setDOMContent(document.getElementById('popup-content'))

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
            id: "dzk__pzf",
            name: "Заповідний фонд",
            hidden: false,
            group: "ДЗК",
            directory: "Оверлей"
          },
          {
            id: "dzk__index_map_lines",
            chain: "dzk__index_map_poly",
            name: "Індексна карта",
            hidden: false,
            group: "ДЗК",
            directory: "Оверлей"
          },
          {
            id: "orto-ersi",
            name: "Ортофото Ersi (2018+)",
            hidden: false,
            group: "Фонові зображення",
            directory: "Базові шари"
          },
          // {
          //   id: "dzk",
          //   name: "WMS шар ДЗК",
          //   hidden: false,
          //   group: "Фонові зображення",
          //   directory: "Базові шари"
          // },
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
      this.map.addControl(new maplibregl.NavigationControl(), "bottom-right");

      this.enableLayers.forEach((item) => {
        this.map.setLayoutProperty(item, 'visibility', 'visible')
      })

      this.map.on('touchstart', () => {
        this.ignoreClick = true;
      });

      this.map.on('click', 'land_polygones', (e) => {
        if(this.ignoreClick) {
          return
        }

        const feature = e.features[0];
        const url = this.$router.resolve({
          name: 'parcel', params: { pk: feature.properties.cadnum }
        })
        window.open(url.href, '_blank');
      });


      function mouseleave_layer() {
        if(this.ignoreClick) {
          return
        }
        this.leave_point();
        this.map.getCanvas().style.cursor = 'auto';
        if (this.highlightedParcels) {
          this.highlightedParcels.forEach((feature) => {
            this.map.setFeatureState(
                {source: feature.source, id: feature.id, sourceLayer: feature.sourceLayer},
                {hover: false}
            );
          })
        }
        this.highlightedParcels = [];
      }
      this.map.on('mouseleave', 'land_polygones', mouseleave_layer.bind(this));
      this.map.on('mouseleave', 'dzk__pzf', mouseleave_layer.bind(this));
      this.map.on('mouseleave', 'dzk__index_map_poly', mouseleave_layer.bind(this));

      function touchend_layer(e) {
        this.touchInsideParcel = true;
        if(this.ignoreClick) {
          this.highlightParcels(e);
        }
      }
      this.map.on('touchend', 'land_polygones', touchend_layer.bind(this))
      this.map.on('touchend', 'dzk__pzf', touchend_layer.bind(this))
      this.map.on('touchend', 'dzk__index_map_poly', touchend_layer.bind(this))

      function touchend() {
        if(this.touchInsideParcel){
          this.touchInsideParcel = false;
          return;
        }
        if(this.ignoreClick) {
          this.leave_point()
        }
      }
      this.map.on('touchend', touchend.bind(this))

      function mousemove(e) {
        if(this.ignoreClick) {
          return
        }
        this.highlightParcels(e);
      }
      this.map.on('mousemove', 'land_polygones', mousemove.bind(this));
      this.map.on('mousemove', 'dzk__pzf', mousemove.bind(this));
      this.map.on('mousemove', 'dzk__index_map_poly', mousemove.bind(this));
    });
  }
}
</script>
<style>

.mapboxgl-ctrl-top-left {
  width: 100%;
}

.mapboxgl-ctrl-top-left .mapboxgl-ctrl {
  margin: 0;
  border-color: transparent;
}

  .mgl-searchControl {
    width: 100%;
  }

@media (min-width: 550px) {
  .mapboxgl-ctrl-top-left {
    width: 450px;
  }
  .mapboxgl-ctrl-top-left .mapboxgl-ctrl {
    margin: 10px 10px 0 10px;
  }
}

  .mapboxgl-ctrl-top-right {
    /*width: 500px;*/
  }

@media (min-width: 650px) {
  .mapboxgl-ctrl-top-right {
    display: block;
  }
}

@media (max-width: 650px) {
  .mgl-layerControl {
    margin: 45px 10px 0 0 !important;
    width: 300px;
  }

  .mgl-layerControl.hiddenRight {
    margin-right: calc(-100% + 50px) !important;
    width: 100%;
  }
}

@media (min-width: 650px) {
  /*.mgl-layerControl {*/
  /*  width: 400px !important;*/
  /*}*/

  /*.mgl-layerControl.hiddenRight {*/
  /*  margin-right: calc(-100% + 50px) !important;*/
  /*  width: 100%;*/
  /*}*/

  .mgl-breadcrumb {
    display: none !important;
  }

}
@media (min-width: 1600px) {
  .mgl-layerControl {
    margin: 65px 10px 0 0 !important;
    width: 450px !important;
  }

  .mgl-layerControl.hiddenRight {
    margin: 65px 10px 0 0 !important;
    width: 450px !important;
  }

  .mgl-breadcrumb {
    display: none !important;
  }

  .mapboxgl-ctrl-zoom-in, .mapboxgl-ctrl-zoom-out, .mapboxgl-ctrl-compass {
    display: none !important;
  }
}

@media (min-width: 750px) {
  .mapboxgl-ctrl-top-right {
    /*width: 300px;*/
  }
}
@media (min-width: 1250px) {
  .mapboxgl-ctrl-top-right {
    /*width: 500px;*/
  }
}

.mgl-layerControl {
  max-width: calc(100vw - 90px) !important;
  overflow: visible !important;
  transition: margin 700ms;

  overflow-y: scroll !important;
  max-height: calc(100vh - 100px);

  background: transparent;
  box-shadow: none !important;
}

.mgl-layerControl.hiddenRight {
    overflow-y: hidden !important;
}

.mgl-layerControlDirectory {
  margin-left: 50px;
}

.mgl-breadcrumb {
  display: block;
  background-color: black;
  width: 50px;
  height: 50px;
  position: absolute;
  margin-left: 0;
  cursor: pointer;
}

.mgl-layerControl .checkbox {
   display: flex;
   align-items:flex-end;
}

input.slide-toggle {
  align-self: center;
}

.mapboxgl-popup {
  max-width: 300px !important;
}


</style>
