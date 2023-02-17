<template>
  <div>
    <template v-if="feature">
      <div>
        <div class="row-item" v-if="feature.properties.cadnum">
          <div class="title">
            Номер
          </div>
          <div class="value">
            {{ feature.properties.cadnum }}
          </div>
        </div>
        <div class="row-item" v-if="feature.properties.address">
          <div class="title">
            Адреса
          </div>
          <div class="value">
            {{ feature.properties.address }}
          </div>
        </div>
        <div class="row-item" v-if="feature.properties.purpose_code">
          <div class="title">
            Призначення
          </div>
          <div class="value">
            {{ feature.properties.purpose_code }}
          </div>
        </div>
        <div class="row-item" v-if="feature.properties.category">
          <div class="title">
            Категорія
          </div>
          <div class="value">
            {{ feature.properties.category }}
          </div>
        </div>
        <div class="row-item" v-if="feature.properties.ownership">
          <div class="title">
            Власність
          </div>
          <div class="value">
            {{ feature.properties.ownership }}
          </div>

        </div>
      </div>


      <div class="text-end">
        <a v-if="is_touchable" class="btn btn-light" role="button" target="_blank"
           :href="'/parcel/' + feature.properties.cadnum">
          Детальніше
        </a>
      </div>
    </template>
  </div>
</template>

<script>
export default {
  name: "ParcelInfo",
  props: {
    feature: null,
    is_touchable: null
  }
}
</script>

<style scoped>

.row-item {
  display: flex;
  align-items: flex-end;
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
