<template>
  <div>
    <template v-if="feature">
      <div>
        <div class="row-item" v-if="feature.properties">
          <div class="title">
            Назва
          </div>
          <div class="value">
            {{feature.properties.name}}
          </div>
        </div>
        <div class="row-item" v-if="feature.properties">
          <div class="title">
            Код
          </div>
          <div class="value">
            {{feature.properties.code}}
          </div>
        </div>

        <div class="row-item" v-if="feature.properties">
          <div class="title">
            Площа водозбору
          </div>
          <div class="value">
            {{feature.properties.square}} км<sup>2</sup>
          </div>
        </div>
      </div>

</template>
</div>
</template>

<script>
export default {
  name: "RiverSubBasinInfo",
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
  width: 100px;

  font-weight: 600;
}
.row-item .value {
  width: 250px;
}

.row-item .value {
  align-self: center;
  flex: 1;
}



</style>
