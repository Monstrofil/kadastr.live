<template>
  <div>
    <template v-if="feature">
      <div>
        <div class="row-item" v-if="feature.properties">
          <div class="title">
            Назва
          </div>
          <div class="value">
            {{feature.properties.NazObPZF}}
          </div>
        </div>
        <div class="row-item" v-if="feature.properties">
          <div class="title">
            Значення
          </div>
          <div class="value">
            {{feature.properties.ZnPZF}}
          </div>
        </div>
        <div class="row-item" v-if="feature.properties">
          <div class="title">
            Адреса власника
          </div>
          <div class="value">
            {{feature.properties.AdrAdmPZF}}
          </div>
        </div>
        <div class="row-item" v-if="feature.properties">
          <div class="title">
            Юридична основа
          </div>
          <div class="value">
            {{feature.properties.PidNPZF}}
          </div>
        </div>
        <div class="row-item" v-if="feature.properties">
          <div class="title">
            Оновлено
          </div>
          <div class="value">
            {{feature.properties.Updated}}
          </div>
        </div>
        <div class="row-item" v-if="feature.properties">
          <div class="title">
            Опис місця розташування
          </div>
          <div class="value">
            {{feature.properties.AdmRozPZF}}
          </div>
        </div>
      </div>

</template>
</div>
</template>

<script>
export default {
  name: "NatureInfo",
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
  width: 120px;

  font-weight: 600;
}

.row-item .value {
  align-self: center;
  flex: 1;
}



</style>
