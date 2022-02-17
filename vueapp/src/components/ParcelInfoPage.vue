<template>

  <div class="container" v-if="parcelInfo">
    <div class="row">
      <div class="col-md-12">
        <h1>Інформація про земельну ділянку</h1>
        <p>
          Інформація є довідковою, забороняється використання даних зі
          сторінки для офіційних дій щодо земельної ділянки.
          Для отримання офіційної інформації зверніться до <a href="https://land.gov.ua/" target="_blank">ДЗК</a>.
        </p>
        <h2>{{ parcelInfo.cadnum }}</h2>
      </div>
      <div class="col-md-8">
          <table class="table">
            <tbody>
            <tr>
              <td>Кадастровий номер</td>
              <td>{{ parcelInfo.cadnum }}</td>
            </tr>
            <tr>
              <td>площа</td>
              <td>{{ parcelInfo.area }} {{ parcelInfo.unit_area }}</td>
            </tr>
            <tr>
              <td>власність</td>
              <td>{{ parcelInfo.ownership || "немає даних" }}</td>
            </tr>
            <tr>
              <td>використання</td>
              <td>{{ parcelInfo.use || "немає даних" }}</td>
            </tr>
            <tr>
              <td>призначення</td>
              <td>{{ parcelInfo.purpose || "немає даних" }}</td>
            </tr>
            <tr>
              <td>категорія</td>
              <td>{{ parcelInfo.category || "немає даних" }}</td>
            </tr>
            <tr>
              <td>адреса</td>
              <td>{{ parcelInfo.address || "немає даних" }}</td>
            </tr>
            </tbody>
          </table>
        </div>
        <div class="col-md-4" style="min-height: 300px">
          <GeoJSONDisplay :geo-feature="parcelInfo.geometry"/>
        </div>

      <div>
        <h3>Історія</h3>
        <p>Відображаються зміни у інформації про земельну ділянку.</p>

        <ol>
          <div
              v-for="(item, index) in parcelInfo.history"
              :key="item"
              :set="previous = (index < parcelInfo.history.length - 1) ? parcelInfo.history[index + 1]: null"
          >

            <li v-if="previous">Зміна інформації</li>
            <li v-else>Інформацію додано до бази даних</li>

            <table class="table">
              <thead>
              <tr>
                <td>Значення</td>
                <td v-if="previous">До {{ moment(item.revision.created_at).format('YYYY-MM-DD') }}</td>
                <td>Після {{ moment(item.revision.created_at).format('YYYY-MM-DD') }}</td>
              </tr>
              </thead>
              <tbody>

              <tr v-if="previous?.purpose !== item.purpose">
                <td>Призначення</td>
                <td v-if="previous" style="background-color: #ffe7e7">{{ previous.purpose }}</td>
                <td style="background-color: #d2ffd2">{{ item.purpose }}</td>
              </tr>


              <tr v-if="previous?.ownership !== item.ownership ">
                <td>Власність</td>
                <td v-if="previous" style="background-color: #ffe7e7">{{ previous.ownership }}</td>
                <td style="background-color: #d2ffd2">{{ item.ownership }}</td>
              </tr>

              <tr v-if="previous?.use !== item.use">
                <td>Використання</td>
                <td v-if="previous" style="background-color: #ffe7e7">{{ previous.use }}</td>
                <td style="background-color: #d2ffd2">{{ item.use }}</td>
              </tr>

              <tr v-if="previous?.category !== item.category">
                <td>Категорія</td>
                <td v-if="previous" style="background-color: #ffe7e7">{{ previous.category }}</td>
                <td style="background-color: #d2ffd2">{{ item.category }}</td>
              </tr>

              <tr v-if="previous?.area !== item.area || previous?.unit_area !== item.unit_area">
                <td>Площа</td>
                <td v-if="previous" style="background-color: #ffe7e7">{{ previous.area }} {{ previous.unit_area }}</td>
                <td style="background-color: #d2ffd2">{{ item.area }} {{ item.unit_area }}</td>
              </tr>

              <tr v-if="JSON.stringify(previous?.geometry) !== JSON.stringify(item.geometry)">
                <td></td>
                <td colspan="2" v-if="previous" style="background-color: #ffe7e7; padding: 0;">
                  <GeoJSONCompare
                      style="height: 300px"
                      :left-geo-json="previous?.geometry"
                      :right-geo-json="item.geometry"
                  />
                </td>
              </tr>


              </tbody>

            </table>
          </div>
        </ol>

      </div>
    </div>

  </div>

</template>

<script>
import axios from "axios";
import GeoJSONCompare from "@/components/GeoJSONCompare";
import moment from "moment";
import GeoJSONDisplay from "@/components/GeoJSONDisplay";

export default {
  name: "ParcelInfoPage",
  components: {GeoJSONCompare, GeoJSONDisplay},
  data() {
    return {
      parcelInfo: null
    }
  },
  methods: {
    moment(dateTime) {
      return moment(dateTime);
    }
  },

  mounted() {
    axios.get(
        `/api/parcels/${this.$route.params.pk}/history/`
    ).then(response => {
      this.parcelInfo = response.data;
    });
  }
}
</script>

<style scoped>

</style>