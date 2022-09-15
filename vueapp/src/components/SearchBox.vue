<template>
  <div id="searchBox"
       ref="element"
       class="mapboxgl-ctrl mgl-searchControl"
       @focusout="onSearchEnded">
    <div class="row d-flex justify-content-center align-items-center">
      <div class="col-md-12">
        <div class="search autocomplete">
          <div class="form">
            <i class="fa fa-search"></i>
            <input type="text"
                   class="form-control form-input"
                   autocomplete="off"
                   @input="onSearchChanged"
                   v-model="searchText"
                   placeholder="Введіть дані для пошуку...">
            <span class="stick-right">
              <span class="left-pan">
              <VTooltip

                  :offset="[0, 16]"
              >
                <a target="_blank" href="#" @click.prevent="downloadGeoJson">
                  <i class="fa fa-download"></i>
                </a>

                <!-- This will be the content of the popover -->
                <template #popper>
                  Завантажити геометрію у вигляді GeoJson файлу.
                  <span v-if="! downloadAvailable" class="button-error">Наблизьте мапу для завантаження</span>
                </template>
              </VTooltip>

            </span>
            <span class="left-pan">
              <VDropdown
                  :offset="[0, 16]"
              >
                <a style="cursor: pointer">
                  <i class="fa fa-exclamation-triangle fa-warning"></i>
                </a>

                <!-- This will be the content of the popover -->
                <template #popper>
                  <div style="max-width: 350px; word-break: break-word">
                    Увага! Останнє оновлення даних відбулось <b>19 лютого 2022 р. о 21:14</b>.
                    Подальші оновлення неможливі через блокування
                    <a href="http://wikimap.dzk.gov.ua/wiki/API_%D0%95-%D1%81%D0%B5%D1%80%D0%B2%D1%96%D1%81%D0%B8">API ДЗК</a>
                    на час воєнного стану.<br>
                    <br>Звертаємо також увагу на те, що сервіс не є офіційним джерелом та не має використовуватись у професійній діяльності.
                  </div>
                </template>
              </VDropdown>

            </span>
            </span>

          </div>
          <ul class="autocomplete-results" v-if="searchResults">
            <li class="autocomplete-result" v-for="result in searchResults.results" :key="result">
              <a class="autocomplete-link" href="#" @click="onSelectParcel(result)">
                <div class="cadnum_result_data">{{ result.cadnum }}</div>
                <div class="address_result_data"><b>Адреса: </b>{{ result.address ? result.address : 'Дані відсутні' }}
                </div>
                <!--                <div class="use_result_data" v-if="result.use"><b>Використання: </b>{{ result.use }}</div>-->
                <div class="area_result_data">{{ result.area }} {{ result.unit_area }}</div>
              </a>
            </li>
          </ul>
        </div>
      </div>
    </div>
    <div style="height: 55px"></div>
  </div>

</template>

<script>
import axios from "axios";

export default {
  name: 'SearchBox',
  data() {
    return {
      searchText: null,
      lastCall: null,
      lastCallTimer: null,
      searchResults: null
    }
  },
  props: {
    downloadAvailable: null
  },
  methods: {
    onAdd() {
      return this.$refs.element
    },
    onRemove() {

    },
    onInputEnd() {

    },
    downloadGeoJson() {
      if (this.downloadAvailable) {
        this.$emit('download');
      }
    },
    onSelectParcel(parcelData) {
      this.$emit('select', parcelData);
      this.searchResults = null;
    },
    debounce(f, t) {
      return function (args) {
        let previousCall = this.lastCall;
        this.lastCall = Date.now();
        if (previousCall && ((this.lastCall - previousCall) <= t)) {
          clearTimeout(this.lastCallTimer);
        }
        this.lastCallTimer = setTimeout(() => f(args), t);
      }.bind(this)
    },
    search() {
      return this.debounce((searchText) => {
        axios.get(
            `/search/${searchText}`
        ).then(response => {
          this.searchResults = response.data;
        });
      }, 500)
    },
    onSearchChanged() {
      this.search()(this.searchText);
    },
    onSearchEnded(e) {
      if (e.relatedTarget && e.relatedTarget.className !== "maplibregl-canvas") {
        return;
      }
      this.searchResults = null;
    }
  }
}
</script>

<style scoped>

.autocomplete-results {
  background: white;
  border: 1px solid #ced4da;
  padding-left: 15px;
  padding-right: 15px;
  max-width: 95%;
}

.autocomplete-result {
  list-style: none;
  margin-top: 3px;
  margin-bottom: 3px;
}

.autocomplete-link {
  display: block;
  position: relative;
}

.autocomplete-link .area_result_data {
  right: 0;
  top: 0;
  position: absolute;
}

.cadnum_result_data {
  font-weight: 600;
}

.autocomplete-result:not(:last-child) {
  border-bottom: 1px solid #fafafa;
}

.autocomplete-result:hover {
  background: #ecebeb;
}

.form {
  position: relative
}

.form .fa-search {
  position: absolute;
  top: 13px;
  left: 20px;
  color: #9ca3af
}

.form .left-pan {
  display: inline-block;
  border-left: 1px solid #d1d5db;
  margin-right: 1px;
}

.form .stick-right {
  position: absolute;
  right: 7px;
  top: 10px;
  padding: 2px;
}

.left-pan {
  padding-left: 10px;
  padding-right: 10px;
}

.form-input {
  height: 40px;
  text-indent: 33px;
  border-radius: 0;
  font-size: 14px;
}

.form-input:focus {
  box-shadow: none;
  border: none
}

.fa-warning {
  color: #ff9966;
  font-size: 120%;
}

</style>