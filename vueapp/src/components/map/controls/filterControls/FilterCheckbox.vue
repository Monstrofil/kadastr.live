<template>
  <div class="checkbox" title="Map Layer">

    <label :for="id"
           class="mgl-layerControlLegend legend-text"
           data-layer-toggle="true">
      <input name="Межі громад"
           type="checkbox"
           :id="id"
           class="layer slide-toggle"
           :checked="checked"
      >
      <slot></slot>
    </label>
  </div>
</template>

<script>
export default {
  name: "FilterCheckbox",
  props: {
    checked: null,
    id: null
  }
}
</script>

<style lang="scss" scoped>

.checkbox {
   display: flex;
   align-items:flex-end;
}


input.slide-toggle {
  align-self: center;

  background-color: rgb(219, 220, 220);
  border-color: rgba(163, 193, 203, 1);

  &:checked {
    background-color: rgba(41, 162, 200, 1);
    border-color: rgba(41, 162, 200, 1);
  }
}

.legend-text {
  flex-grow: 1;
}
</style>