<template>

  <div>
    {{ group.hint }}
    <FilterCheckbox v-for="option in group.options" :key="option.id"
                    :checked="option.checked"
                    :id="option.id"
                    @change="$emit('change', layer, option)"
    >
      {{ option.name }}
    </FilterCheckbox>

  </div>
</template>
<script>
import FilterCheckbox from "@/components/map/controls/filterControls/FilterCheckbox"

export default {
  name: 'LayerFilterItem',
  components: {FilterCheckbox},
  props: {
    group: null,
    layer: null
  },
  mounted() {

  }
}
</script>
