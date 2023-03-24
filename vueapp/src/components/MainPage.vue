<template>

  <MapComponent
      :mapStyle="'/style/vector_style_24_03_2023.json'"
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

