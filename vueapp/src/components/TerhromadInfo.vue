<template>
  <div>
    <template v-if="feature">
      <div>

        <div class="row-item" v-if="feature.properties.ADMIN_1">
          <div class="title">
            Назва області
          </div>
          <div class="value">
            {{ feature.properties.ADMIN_1 }}
          </div>
        </div>
        <div class="row-item" v-if="feature.properties.ADMIN_2">
          <div class="title">
            Назва району
          </div>
          <div class="value">
            {{ feature.properties.ADMIN_2 }}
          </div>
        </div>
        <div class="row-item" v-if="feature.properties.ADMIN_3">
          <div class="title">
            Назва громади
          </div>
          <div class="value">
            {{ feature.properties.ADMIN_3 }} {{ feature.properties.TYPE }}
          </div>
        </div>
        <div class="row-item" v-if="feature.properties.KOATUU_old">
          <div class="title">
            КОАТУУ
          </div>
          <div class="value">
            {{ feature.properties.KOATUU_old }}
          </div>
        </div>

      </div>
</template>
</div>
</template>

<script>
export default {
  name: "TerhromadInfo",
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
  align-self: center;
  flex: 1;
}



</style>
