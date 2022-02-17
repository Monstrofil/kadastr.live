<template>

  <div class="container">
    <div class="row">
      <div class="col-md-12">
        <h1>Оновлення бази даних</h1>
        <p>
          Інформація є довідковою, забороняється використання даних зі
          сторінки для офіційних дій щодо земельної ділянки.
          Для отримання офіційної інформації зверніться до <a href="https://land.gov.ua/" target="_blank">ДЗК</a>.


        </p>
        <p>Дані земельного кадастру оновлюються щотижня, перелік успішних оновлень та статистика наведена нижче.</p>
      </div>
      <div class="col-md-12">
        <div>
          <table class="table">
            <tbody>
            <tr v-for="(item, index) in updatesInfo" :key="item">
              <td>{{index + 1}}</td>
              <td>{{item.status}}</td>
              <td>{{ moment(item.created_at).format('DD.MM.YYYY HH:MM') }}</td>
              <td>
                <div v-if="item.statistics.create">
                  <span>Створено нових: {{ item.statistics.create }}</span><br>
                  <span>Оновлено: {{ item.statistics.update }}</span><br>
                  <span>Видалено: {{ item.statistics.delete }}</span><br>
                </div>
                <div v-else>--</div>
              </td>
            </tr>
            </tbody>
          </table>

        </div>
      </div>

    </div>

  </div>

</template>

<script>
import axios from "axios";
import moment from "moment";

export default {
  name: "UpdatesListPage",
  components: {},
  data() {
    return {
      updatesInfo: null
    }
  },
  methods: {
    moment(dateTime) {
      return moment(dateTime);
    }
  },

  mounted() {
    axios.get(
        `/api/updates/`
    ).then(response => {
      this.updatesInfo = response.data;
    });
  }
}
</script>

<style scoped>

</style>