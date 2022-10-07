<template>
  <div class="directory" id="АТУ" data-name="АТУ" style="line-height: 30px;">
    <button
        data-toggle="collapse"
        data-directory-toggle="true"
        :class="{'collapsed': collapsed }"
        @click="toggler.toggle()"
    ></button>
    <span>
      Фільтри
    </span>
  </div>
  <div class="collapse multi-collapse" ref="collapsableFilters"
       style="padding-left: 10px">
    <template v-for="(group, group_id) in layer?.metadata?.filterSchema"
              :key="group_id">
      <LayerFilterItem :group="group" :layer="layer" @change="(layer, option) => {
        $emit('change', layer, option)
      }"/>
    </template>
  </div>

</template>
<script>
import LayerFilterItem from "@/components/map/controls/filterControls/LayerFilterItem";
import {Collapse} from "bootstrap";

export default {
  name: 'LayerFilterList',
  components: {LayerFilterItem},
  props: {
    layer: {}
  },
  mounted() {
    this.toggler = new Collapse(this.$refs.collapsableFilters);
  },
  methods: {

  },
  data() {
    return {
      toggler: null,
      collapsed: false
    }
  }
}
</script>
<style lang="scss" scoped>

.directory {
  font-size: 16px;
  background: #f8f9fa;
  //padding: 5px;/
  cursor: pointer;
  line-height: 30px;
}

</style>