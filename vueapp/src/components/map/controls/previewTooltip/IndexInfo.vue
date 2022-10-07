<template>
  <div>
    <template v-if="feature">
      <div>

        <div class="row-item" v-if="feature.properties.koatuu">
          <div class="title">
            КОАТУУ
          </div>
          <div class="value">
            {{ feature.properties.koatuu }}
          </div>
        </div>
        <div class="row-item" v-if="feature.properties">
          <div class="title">
            Зона
          </div>
          <div class="value">
            {{ feature.properties.zona }}
          </div>
        </div>
        <div class="row-item" v-if="feature.properties.kvart">
          <div class="title">
            Квартал
          </div>
          <div class="value">
            {{ feature.properties.kvart }}
          </div>
        </div>

      </div>
</template>
</div>
</template>

<script>
export default {
  name: "IndexInfo",
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
  width: 80px;

  font-weight: 600;
}

.row-item .value {
  align-self: center;
  flex: 1;
}



</style>
