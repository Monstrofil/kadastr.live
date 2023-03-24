<template>
  <div>
    <template v-if="feature">
      <div>
        <div class="row-item" v-if="feature.properties">
          <div class="title">
            Назва
          </div>
          <div class="value">
            {{feature.properties.name_ua}}
          </div>
        </div>
        <div class="row-item" v-if="feature.properties">
          <div class="title">
            Альтернативна назва
          </div>
          <div class="value">
            {{feature.properties.alt_name || '-'}}
          </div>
        </div>
        <div class="row-item" v-if="feature.properties">
          <div class="title">
            Класифікація
          </div>
          <div class="value">
            {{feature.properties.type}} {{feature.properties.class}}
          </div>
        </div>
        <div class="row-item" v-if="feature.properties">
          <div class="title">
            Гирло
          </div>
          <div class="value">
            {{feature.properties.destination}}
          </div>
        </div>
        <div class="row-item" v-if="feature.properties">
          <div class="title">
            Довжина
          </div>
          <div class="value">
            {{feature.properties.length}} км
          </div>
        </div>
        <div class="row-item" v-if="feature.properties">
          <div class="title">
            Площа басейну
          </div>
          <div class="value">
            {{feature.properties.basin_sq}} км2
          </div>
        </div>
      </div>

</template>
</div>
</template>

<script>
export default {
  name: "RiverInfo",
  props: {
    feature: null,
    is_touchable: null
  }
}
</script>

<style scoped>

.row-item {
  display: flex;
  align-items:flex-end;
}

.row-item:not(:last-child) {
  margin-bottom: 2px;
  border-bottom: 1px dashed #cccccc;
}

.row-item .title {
  align-self: start;
  width: 150px;

  font-weight: 600;
}
.row-item .value {
  width: 150px;
}

.row-item .value {
  align-self: center;
  flex: 1;
}



</style>
