<template>

  <div class="offcanvas offcanvas-end" tabindex="-1"
       id="offcanvasExample"
       aria-labelledby="offcanvasExampleLabel"
       ref="offcanvas"
  >
    <div class="offcanvas-header">
      <h5 class="offcanvas-title" id="offcanvasExampleLabel">
        <slot name="title"></slot>
      </h5>
      <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
    </div>
    <div class="offcanvas-body">
      <slot></slot>
    </div>
  </div>


</template>

<script>
import {Offcanvas} from "bootstrap";

export default {
  name: "WrapperOffcanvas",
  mounted() {
    this.canvas = new Offcanvas(this.$refs.offcanvas);
  }
}
</script>

<style scoped>

</style>