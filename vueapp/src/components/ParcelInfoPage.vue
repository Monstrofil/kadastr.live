<template>

<div class="container" v-if="parcelInfo">
  <div class="row">
    <div class="col-md-12">
      <h1>Земельна ділянка №{{ parcelInfo.cadnum }}</h1>
    </div>
  </div>



    <div>
        <div style="display: inline-block; vertical-align: top;">
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
        <div style="display: inline-block;">
            <div id="mapid"></div>
        </div>
    </div>

    <div>
        <h2>Історія</h2>
        <p>Відображаються зміни у інформації про земельну ділянку.</p>

        <div
            v-for="(item, index) in parcelInfo.history"
            :key="item"
            :set="previous = (index > 0) ? parcelInfo.history[index - 1]: null"
        >

          <span>Зміна інформації</span>
          <table class="table">
            <thead>
                <tr>
                <td v-if="previous">До {{ item.revision.created_at }}</td>
                <td>Після {{ item.revision.created_at }}</td>
                </tr>
            </thead>
            <tbody>

            <tr v-if="previous?.purpose !== item.purpose">
                <td v-if="previous" style="background-color: #ffe7e7">{{ previous.purpose }}</td>
                <td style="background-color: #d2ffd2">{{ item.purpose }}</td>
            </tr>


            <tr v-if="previous?.ownership !== item.ownership ">
                <td v-if="previous"  style="background-color: #ffe7e7">{{ previous.ownership }}</td>
                <td style="background-color: #d2ffd2">{{ item.ownership }}</td>
            </tr>

            <tr v-if="previous?.use !== item.use">
                <td v-if="previous"  style="background-color: #ffe7e7">{{ previous.use }}</td>
                <td style="background-color: #d2ffd2">{{ item.use }}</td>
            </tr>

            <tr v-if="JSON.stringify(previous?.geometry) !== JSON.stringify(item.geometry)">
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

    </div>

</div>

</template>

<script>
import axios from "axios";
import GeoJSONCompare from "@/components/GeoJSONCompare";

export default {
  name: "ParcelInfoPage",
  components: {GeoJSONCompare},
  data() {
    return {
      parcelInfo: null
    }
  },
  methods: {
  },

  mounted() {
    console.log(this.$route.params)
    axios.get(
        `/api/parcels/${this.$route.params.pk}/history/`
      ).then(response => {
        console.log(response)
        this.parcelInfo = response.data;
      });
  }
}
</script>

<style scoped>

</style>