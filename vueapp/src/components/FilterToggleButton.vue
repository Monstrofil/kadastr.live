<template>
<div ref="element" class="mapboxgl-ctrl mgl-filterControl">
    <a class="btn filter-button" data-bs-toggle="offcanvas" href="#offcanvasExample" role="button" aria-controls="offcanvasExample">
      <i class="fa fa-filter"></i>
      <span class="fa-filter-caption">&nbsp;Керування</span>
    </a>
</div>
</template>

<script>
export default {
  name: "FilterToggleButton",
  methods: {
    onAdd() {
      return this.$refs.element
    },
    onRemove() {

    },
    onInputEnd() {

    },
  }
}
</script>

<style scoped>
.filter-button {
  display: block;
  width: 100%;
  padding: 0.375rem 0.75rem;
  font-size: 1.2rem;
  font-weight: 400;
  line-height: 1.5;
  color: #212529;
  background-color: #fff;
  background-clip: padding-box;
  border: 1px solid #ced4da;
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
  border-radius: 0.25rem;
  transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
}

.mapboxgl-ctrl-top-right {
  width: 15%;
}

.fa-filter-caption {
  display: none;
}

.mapboxgl-ctrl-top-right .mapboxgl-ctrl {
  border-color: transparent;
}

@media (min-width: 650px) {
  .mapboxgl-ctrl-top-right {
    max-width: 475px;
  }
  .mapboxgl-ctrl-top-right .mapboxgl-ctrl {
    margin: 10px 10px 0 10px;
  }

  .fa-filter-caption {
    display: inline-block;
  }
}
</style>