<template>

  <MapComponent
      :mapStyle="'/style/vector_style_28_09_2022.json'"
      style="width: 100%; height: 100vh"
  >

  </MapComponent>
</template>

<script>
import MapComponent from "@/components/map/MapComponent";

export default {
  name: "MainPage",
  components: {MapComponent}
}
</script>

