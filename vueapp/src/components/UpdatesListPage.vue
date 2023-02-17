<template>
  <div class="breadcrumbs">
    <div class="container">
      <ul>
        <li>
          <router-link to="/">Головна</router-link>
        </li>
        <li>
          <router-link active-class="active" to="/update">Оновлення даних</router-link>
        </li>
      </ul>
    </div>
  </div>
  <div class="container text-block">
    <div class="row">
      <div class="col-md-12">
        <h1>Оновлення даних</h1>
         <div class="alert alert-warning">
          Інформація є довідковою, забороняється використання даних зі
          сторінки для офіційних дій щодо земельної ділянки. Оновлення даних не гарантується.
           <br>
          Для отримання офіційної інформації зверніться до <a href="https://land.gov.ua/" target="_blank">ДЗК</a>.
        </div>
        <p><s>Дані земельного кадастру оновлюються щотижня</s>, перелік успішних оновлень та статистика наведена нижче.</p>
      </div>
      <div class="col-md-12">
        <div class="row">
          <div class="col-xs-12 col-md-3" v-for="item in updatesInfo" :key="item">
            <div class="card w-100" style="margin-bottom: 10px">
              <div class="card-header">
                {{ moment(item.created_at).format('DD.MM.YYYY HH:MM') }}
                <span class="badge bg-success" style="float: right">{{item.status}}</span>
              </div>
            <div class="card-body">

              <div class="card-text">
                <b>Статистика ділянок</b>
                <div class="row" style="margin-top: 10px">
                  <div class="col-md-6 text-capitalize">
                    Нові
                  </div>
                  <div class="col-md-6 text-end">
                    {{ item.statistics.create || '--' }}
                  </div>
                <div class="row">
                </div>
                  <div class="col-md-6">
                    Оновлені
                  </div>
                  <div class="col-md-6 text-end">
                    {{ item.statistics.update || '--' }}
                  </div>
                <div class="row">
                </div>
                  <div class="col-md-6">
                    Видалені
                  </div>
                  <div class="col-md-6 text-end">
                    {{ item.statistics.delete || '--' }}
                  </div>
                </div>
              </div>
              <!--<div class="card-text">
                <span class="text-muted" v-if="item.statistics.create">Деталі</span>
              </div>-->
            </div>
          </div>
          </div>
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