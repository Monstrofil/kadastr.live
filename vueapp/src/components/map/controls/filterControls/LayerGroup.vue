<template>
  <div class="row">
    <div class="col-12 nopadding">
      <input type="checkbox" id="layerGroup_АТУ" data-layergroup="АТУ" style="display: none">
      <label for="layerGroup_АТУ" class="mgl-layerControlGroupHeading">
        {{ group.name }}
      </label>

      <template v-for="layer in group.layers" :key="layer.id">
        <FilterCheckbox
            :checked="layer.checked"
            :id="layer.id"
            @change="onLayerToggle(layer)"
        >
          <icon
              v-if="layer.paint"
              :class='layer.paint.icon'
              :style='{
                color: layer.paint.color,
                "margin-right": "6px"
              }'></icon>
          {{ layer.name }}
        </FilterCheckbox>

        <LayerFilterList
            v-if="layer?.metadata?.filterSchema"
            :collapsed="collapsed"
            :layer="layer"
            @change="onLayerFilter"/>

      </template>
    </div>
  </div>
</template>

<script>
import FilterCheckbox from "@/components/FilterCheckbox";
import LayerFilterList from "@/components/map/controls/filterControls/LayerFilterList";

export default {
  name: "LayerGroup",
  components: {LayerFilterList, FilterCheckbox},
  data() {
    return {
      collapsed: false,
      toggler: null
    }
  },
  props: {
    group: null,
    map: null
  },
  mounted() {
    let params = new URLSearchParams(window.location.search);

    this.group.layers.forEach((layer) => {
      let mapStyle = this.map.getLayer(layer.id);
      layer.type = mapStyle.type;

      let legend = null
      if (layer.type === 'line') {
        const color = this.map.getPaintProperty(layer.id, 'line-color');
        legend = {
          'color': color,
          'icon': 'fa fa-minus'
        }
      } else if (layer.type === 'fill') {
        const color = this.map.getPaintProperty(layer.id, 'fill-color');
        legend = {
          'color': color,
          'icon': 'fa fa-square'
        }
      }
      // find better icon
      // else if ( layer.type === 'raster' ) {
      //   legend = {
      //     'color': 'rgba(1, 1, 1, 1)',
      //     'icon': 'fa fa-picture-o'
      //   }
      // }
      layer.paint = legend;
      if (params.get(layer.id)) {
        layer.checked = params.get(layer.id) === 'true';
      }
      this.configureLayerVisibility(layer);
      this.onLayerFilter(layer);
    })
  },
  methods: {
    configureLayerVisibility(layer) {
      this.map.setLayoutProperty(
          layer.id, 'visibility', layer.checked ? 'visible' : 'none');

      if (layer.chain) {
        this.map.setLayoutProperty(
            layer.chain, 'visibility', layer.checked ? 'visible' : 'none');
      }
    },
    onLayerToggle(layer) {
      layer.checked = !layer.checked;
      this.configureLayerVisibility(layer);

      let params = new URLSearchParams(window.location.search);
      if(layer.checked) {
        params.set(layer.id, true);
      }
      else {
        params.set(layer.id, false);
      }

      let url = window.location.protocol + "//" + window.location.host +
          window.location.pathname + "?" + params.toString() + window.location.hash;
      window.history.replaceState({
        path: url
      }, '', url);
    },
    onLayerFilter(layer, option = null) {
      if (option) {
        option.checked = !option.checked;
      }

      let allFilters = layer?.metadata?.filterSchema;
      if (allFilters === undefined) {
        return
      }

      let allMapFilters = ["all"];
      for (const property in allFilters) {
        const filter = allFilters[property];

        let valueFilters = ["any"];
        Array.from(filter.options).forEach((option) => {
          if (!option.checked)
            return

          valueFilters.push(option?.customFilter || [
            "==", ["get", property], option.id]);
        })
        allMapFilters.push(valueFilters);
      }

      this.map.setFilter(layer.id, allMapFilters);
    }
  }
}
</script>

<style lang="scss" scoped>

</style>