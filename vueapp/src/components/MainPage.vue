<template>

  <div class="col-md-6">
  </div>
  <MapComponent
      :mapStyle="'https://test.kadastr.live/static/vector_style.json'"
      style="width: 100%; height: 100vh"
  >

  </MapComponent>
</template>

<script>
import MapComponent from "@/components/MapComponent";

export default {
  name: "MainPage",
  components: {MapComponent}
}
</script>

