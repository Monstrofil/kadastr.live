<template>
  <div ref="map" style="height: 30vh; width: 100%">
    <SearchBox
        :downloadAvailable="isDownloadAvailable"
        @select="onSelectParcel"
        @download="onDownloadClick"
        ref="searchBox"
    />
    <FilterToggleButton
        ref="filterToggle"
    />


  <WayBackMachine ref="waybackButton"
                  @revisionChanged="onRevisionChange"/>

    <WrapperOffcanvas>
      <template v-slot:title>Фільтр</template>
      <template v-slot:default>
        <MapFilter :map="map" v-if="map"></MapFilter>
      </template>
    </WrapperOffcanvas>

    <div class="mapboxgl-ctrl mapboxgl-ctrl-bottom-left" style="background-color: white; padding: 15px;">

      <TerhromadInfo :feature="selectedATU" v-if="selectedATU"></TerhromadInfo>
    </div>

    <component
        :is="selectedItem !== null ? renderer[selectedItem.sourceLayer] : 'ParcelInfo'"
        :feature="selectedItem"
        :is_touchable="ignoreClick"
        id="popup-content"/>
  </div>

</template>
<script>
import maplibregl from "maplibre-gl";
import { ref } from "vue";
import SearchBox from "@/components/map/controls/SearchBox";
import ParcelInfo from "@/components/map/controls/previewTooltip/ParcelInfo";
import NatureInfo from "@/components/map/controls/previewTooltip/NatureInfo";
import IndexInfo from "@/components/map/controls/previewTooltip/IndexInfo";
import RiverInfo from "@/components/map/controls/previewTooltip/RiverInfo";
import WrapperOffcanvas from "@/components/WrapperOffcanvas";
import FilterToggleButton from "@/components/map/controls/FilterToggleButton";
import TerhromadInfo from "@/components/TerhromadInfo";
import MapFilter from "@/components/map/controls/MapFilter";
import WayBackMachine from "@/components/map/controls/WayBackMachine";
import RiverBasinInfo from "@/components/map/controls/previewTooltip/RiverBasinInfo.vue";
import NatureSmaragdInfo from "@/components/map/controls/previewTooltip/NatureSmaragdInfo.vue";
import RiverSubBasinInfo from "@/components/map/controls/previewTooltip/RiverSubBasinInfo";
import ManageParcelInfo from "@/components/map/controls/previewTooltip/ManageParcelInfo";

export default {
  name: 'MapComponent',
  components: {
    MapFilter,
    TerhromadInfo,
    FilterToggleButton,
    WayBackMachine,
    WrapperOffcanvas,
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
    const filterToggle = ref(null);
    const pzfInfo = ref(null);
    const waybackButton = ref(null);

    return { searchBox, pzfInfo, filterToggle, waybackButton };
  },
  data() {
    return {
      highlightedParcels: null,
      popup: null,
      mapLoaded: false,
      isDownloadAvailable: null,
      ignoreClick: null,
      touchInsideParcel: null,
      selectedItem: null,
      selectedATU: null,
      requestedParcelsRevision: null,
      renderer: {
        'land_polygons': ParcelInfo,
        'pzf_data': NatureInfo,
        'nsdi_sm_merega': NatureSmaragdInfo,
        'index_data': IndexInfo,
        'river_line': RiverInfo,
        'nsdi_river_basin': RiverBasinInfo,
        'nsdi_river_subbasin': RiverSubBasinInfo,
        'nsdi_manage_parcel': ManageParcelInfo,
        null: NatureInfo,
      },
      map: null
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
    onRevisionChange(e) {
      this.requestedParcelsRevision = e;
      // Remove the tiles for a particular source
      this.map.style.sourceCaches['cadastr'].clearTiles()

      // Load the new tiles for the current viewport (map.transform -> viewport)
      this.map.style.sourceCaches['cadastr'].update(this.map.transform)

      // Force a repaint, so that the map will be repainted without you having to touch the map
      this.map.triggerRepaint()
    },
    highlightParcels(e) {
      let features = this.map.queryRenderedFeatures(e.point);

      // lookup for atu information
      features.forEach((feature) => {
        if (feature && feature.sourceLayer === 'atu_terhromad_data'){
          this.selectedATU = feature;
        }
      })

      // check for all other tooltipped items
      function filterFeatures(feature) {
        if(feature) {
          return this.renderer[feature.sourceLayer] !== undefined
        }
        return false;
      }
      features = features.filter(filterFeatures.bind(this));

      if(features.length === 0){
        this.selectedItem = null;
        return
      }
      this.selectedItem = features[0];

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
    },

    leave_atu: function () {
        this.selectedATU = null;
    }
  },
  mounted() {
    this.map = new maplibregl.Map({
      container: this.$refs.map,
      style: this.mapStyle,
      center: this.location,
      zoom: 5,
      hash: true,
        transformRequest: (url, resourceType) => {
            let parsedUrl = new URL(url, location);

            if (resourceType === 'Source' || resourceType === 'Style') {
                parsedUrl.searchParams.append('version', process.build.version);
            }
            // TODO: wayback machine props here
            // TODO: remove hardcoded domain name here
            if (
                this.requestedParcelsRevision !== null &&
                resourceType === 'Tile' &&
                url.startsWith('https://cdn.kadastr.live/tiles/maps/kadastr')
            ) {
                parsedUrl.hostname = 'cdn.kadastr.live'
                parsedUrl.href = parsedUrl.href.replace('tiles/maps/kadastr', 'wayback_tiles/maps/kadastr');
                parsedUrl.searchParams.append('revision', this.requestedParcelsRevision)
            }

            return {
                url: parsedUrl.toString()
            }
        }
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

      this.isDownloadAvailable = this.map.getZoom() > 13;
      this.map.on('zoomend', () => {
        this.isDownloadAvailable = this.map.getZoom() > 13;
      });

      this.map.addControl(this.searchBox, "top-left");
      this.map.addControl(this.filterToggle, "top-right");
      this.map.addControl(this.waybackButton, "top-right");

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
      this.map.on('mouseleave', 'dzk__atu_terhromad', this.leave_atu.bind(this));
      this.map.on('mouseleave', 'dzk__index_map_poly', mouseleave_layer.bind(this));
      this.map.on('mouseleave', 'water_lines_other', mouseleave_layer.bind(this));
      this.map.on('mouseleave', 'water_lines_middle_rivers', mouseleave_layer.bind(this));
      this.map.on('mouseleave', 'water_lines_large', mouseleave_layer.bind(this));
      this.map.on('mouseleave', 'water_lines_text', mouseleave_layer.bind(this));
      this.map.on('mouseleave', 'river_basin', mouseleave_layer.bind(this));
      this.map.on('mouseleave', 'nsdi_sm_merega', mouseleave_layer.bind(this));
      this.map.on('mouseleave', 'river_subbasin', mouseleave_layer.bind(this));
      this.map.on('mouseleave', 'manage_parcel', mouseleave_layer.bind(this));

      function touchend_layer(e) {
        this.touchInsideParcel = true;
        if(this.ignoreClick && !this.map.isMoving()) {
          this.highlightParcels(e);
        }
      }
      this.map.on('touchend', 'land_polygones', touchend_layer.bind(this))
      this.map.on('touchend', 'dzk__pzf', touchend_layer.bind(this))
      // this.map.on('touchend', 'dzk__atu_terhromad', touchend_layer.bind(this))
      this.map.on('touchend', 'dzk__index_map_poly', touchend_layer.bind(this))
      this.map.on('touchend', 'water_lines_other', touchend_layer.bind(this))
      this.map.on('touchend', 'water_lines_middle_rivers', touchend_layer.bind(this))
      this.map.on('touchend', 'water_lines_large', touchend_layer.bind(this))
      this.map.on('touchend', 'water_lines_text', touchend_layer.bind(this))
      this.map.on('touchend', 'river_basin', touchend_layer.bind(this))
      this.map.on('touchend', 'nsdi_sm_merega', touchend_layer.bind(this))
      this.map.on('touchend', 'river_subbasin', touchend_layer.bind(this))
      this.map.on('touchend', 'manage_parcel', touchend_layer.bind(this))

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
      this.map.on('mousemove', 'dzk__atu_terhromad', mousemove.bind(this));
      this.map.on('mousemove', 'dzk__index_map_poly', mousemove.bind(this));
      this.map.on('mousemove', 'water_lines_other', mousemove.bind(this));
      this.map.on('mousemove', 'water_lines_middle_rivers', mousemove.bind(this));
      this.map.on('mousemove', 'water_lines_large', mousemove.bind(this));
      this.map.on('mousemove', 'water_lines_text', mousemove.bind(this));
      this.map.on('mousemove', 'river_basin', mousemove.bind(this));
      this.map.on('mousemove', 'nsdi_sm_merega', mousemove.bind(this));
      this.map.on('mousemove', 'river_subbasin', mousemove.bind(this));
      this.map.on('mousemove', 'manage_parcel', mousemove.bind(this));
    });
  }
}
</script>
<style>

.mapboxgl-ctrl-top-left {
  width: 80%;
}

.mapboxgl-ctrl-top-left .mapboxgl-ctrl {
  //margin-top: 0;
  border-color: transparent;
}

.mgl-searchControl {
  width: 100%;
}

@media (min-width: 550px) {
  .mapboxgl-ctrl-top-left {
    width: 475px;
  }
  .mapboxgl-ctrl-top-left .mapboxgl-ctrl {
    margin: 10px 10px 0 10px;
  }
}


@media (min-width: 650px) {
  .mgl-breadcrumb {
    display: none !important;
  }

}
@media (min-width: 1600px) {
  .mgl-breadcrumb {
    display: none !important;
  }

  .mapboxgl-ctrl-zoom-in, .mapboxgl-ctrl-zoom-out, .mapboxgl-ctrl-compass {
    display: none !important;
  }
}

.mgl-layerControl {
  max-width: 100%;
  overflow: visible !important;
  transition: margin 700ms;

  /*overflow-y: scroll !important;*/
  /*max-height: calc(100vh - 100px);*/

  background: transparent;
  box-shadow: none !important;
}

/*.mgl-layerControlDirectory {*/
/*  margin-left: 50px;*/
/*}*/

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
