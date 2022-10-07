<template>
  <div class="mgl-layerControl">

    <div class="row">
      <div class="directory" id="АТУ" data-name="АТУ" style="line-height: 30px;">
        <button
            data-toggle="collapse"
            data-directory-toggle="true"
            :class="{'collapsed': !collapsed }"
            @click="() => {toggler.toggle(); this.collapsed = !collapsed}"
        ></button>
        <span>
          {{ directory.name }}
        </span>
        <span class="mgl-layerControlDirectoryCounter"
              style="background: rgb(13, 132, 179);
            display: block;
            float: right;
            color: white;
            padding: 1px 4px 0;">
        {{ directory.groups.map((group) => {
          return group.layers.filter(layer => layer.checked).length
        }).reduce((a, b) => a + b) }}
      </span>
      </div>
    </div>
    <div class="collapse multi-collapse" ref="collapsable">
      <LayerGroup
          v-for="group in directory.groups"
          :key="group.id"
          :group="group"
          :map="map"
      >
      </LayerGroup>
    </div>
  </div>
</template>

<style lang="scss">

.directory {
  font-size: 16px;
  background: #f8f9fa;
  cursor: pointer;
  line-height: 30px;
}

.mgl-layerControlGroupHeading {
    font-weight: 500;
    font-size: 16px !important;
}
</style>

<script>
import LayerGroup from "@/components/map/controls/filterControls/LayerGroup"
import {Collapse} from "bootstrap";

export default {
  name: 'LayerDirectory',
  components: {LayerGroup},
  props: {
    directory: {},
    map: {}
  },
  data() {
    return {
      toggler: null,
      collapsed: false
    }
  },
  mounted() {
    this.toggler = new Collapse(this.$refs.collapsable);
    this.collapsed = this.directory.collapsed;
    if (this.collapsed) {
      this.toggler.hide();
    }
  }
}
</script>
