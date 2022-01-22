<style>

.road-num {
  padding: 0.25em 0.25em 0.05em;
  margin: 0 0.1em;
  font-weight: 600;
  border-radius: 0.25em;
  color: #FFF;
  font-size: smaller;
  text-transform: uppercase;
  white-space: nowrap;
}

.road-num.red, .road-num.n, .road-num.m {
  background-color: #E40428;
}

.road-num.copiable {
  cursor: pointer;
}

.road-num.green, .road-num.e {
  background-color: #3AAA35;
}

.road-num.blue, .road-num.r, .road-num.t {
  background-color: #033878;
}

.road-num.yellow {
  background-color: #FFE054;
  padding: 0.25em 0.25em 0.05em;
  border: solid 0.11em;
  border-color: #000;
  color: #000;
}

.road-num.transp {
  background-color: none;
  padding: 0.25em 0.25em 0.05em;
  border: solid 0.11em;
  border-color: #033878;
  color: #033878;
}

.road-num.transp.w {
  background-color: none;
  padding: 0.25em 0.25em 0.05em;
  border: solid 0.11em;
  border-color: #fff;
  color: #fff;
}

.wait-wrap {
  position: fixed;
  width: 100%;
  height: 100%;
  left: 0px;
  top: 0px;
  background: rgba(51, 51, 51, 0.7);
  z-index: 9999;
}

.v-center {
  top: 50%;
  transform: translate(0, -50%);
}

.h-center {
  left: 50%;
  transform: translate(-50%, 0);
}

.wait-center {
  left: 50%;
  position: absolute;
  top: 50%;
  transform: translate(-50%, -50%);
}

</style>


<template>
  <div class="container-fluid h-100 p-0">
<!--    <ul class="nav nav-header navbar fixed-top navbar-expand-lg navbar-dark primary-color">-->
<!--      <li class="nav-item header-nav-item">-->
<!--        <router-link :exact="true" exact-active-class="active" :to="'/'">Головна</router-link>-->
<!--      </li>-->
<!--      <li class="nav-item header-nav-item">-->
<!--        <router-link active-class="active" :to="'/list'">Перелік</router-link>-->
<!--      </li>-->
<!--      <li class="nav-item header-nav-item">-->
<!--        <router-link active-class="active" :to="'/parcels'">Земельні ділянки</router-link>-->
<!--      </li>-->
<!--      <li class="nav-item header-nav-item">-->
<!--        <router-link active-class="active" :to="'/foo'">Аналітика</router-link>-->
<!--      </li>-->
<!--      <li class="nav-item header-nav-item">-->
<!--        <router-link active-class="active" :to="'/about'">Про проект</router-link>-->
<!--      </li>-->
<!--    </ul>-->
<!--    <a class="button-to button-to__back" data-back-button="" data-ga-event-click="back_button" data-translate=""><span-->
<!--        class="ng-scope">Назад</span></a>-->

    <router-view></router-view>
  </div>

  <DynamicModalWindows ref="modalManager"/>

  <div class="wait-wrap" v-if="workingRequests >= 1">
    <div class="wait-center" style="text-align: center">
      <div style="display: inline-block">
        <BounceLoader :loading="true" :color="color" :size="size"></BounceLoader>
      </div>
      <p class="text-white">Дані завантажуються</p>
    </div>
  </div>
</template>

<script>


import mapboxgl from "mapbox-gl";
import DynamicModalWindows from "@/components/DynamicModalWindows";
import {computed, provide, reactive} from "vue";
import axios from "axios";

export default {
  name: 'App',
  data() {
    return {
      workingRequests: 0
    }
  },
  components: {
    DynamicModalWindows
  },
  setup() {
    const state = reactive({
      modalManager: null
    });

    // Getters
    const getModalManager = computed(() => state.modalManager);
    provide('modalManager', getModalManager)

    return {state}
  },
  methods: {
    setupAxiosInterceptor: function () {
      axios.interceptors.request.use(function (config) {
        this.onRequestBegin();
        return config;
      }.bind(this), function (error) {
        this.onRequestEnd();
        return Promise.reject(error);
      }.bind(this));

      axios.interceptors.response.use(function (response) {
        this.onRequestEnd();
        return response;
      }.bind(this), function (error) {
        this.onRequestEnd();
        return Promise.reject(error);
      }.bind(this));
    },
    onRequestBegin: function () {
      console.log('onRequestBegin')
      this.workingRequests += 1;
    },
    onRequestEnd: function () {
      this.workingRequests -= 1;
    },
  },
  mounted() {
    this.setupAxiosInterceptor();
    this.state.modalManager = this.$refs.modalManager;
  }

}

mapboxgl.accessToken = "pk.eyJ1IjoibW9uc3Ryb2ZpbCIsImEiOiJjazVjbHc0ZWoxczNpM2xsamlsb2Vla3U3In0.D_AounEf87Va3Zq6Z8tTsg";
</script>

<style>
#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.button-to {
  background-color: #232323;
  background-repeat: no-repeat;
  box-sizing: border-box;
  position: fixed;
  font-size: 0;
  height: 45px;
  line-height: 45px;
  letter-spacing: 0;
  padding: 0 0 0 45px;
  z-index: 10;
  white-space: nowrap;
  color: transparent;
  cursor: pointer;
  text-transform: uppercase;
  transition: background-color .2s, font-size .2s, color 0s;
}

.button-to:after {
  background-repeat: no-repeat;
  content: "";
  position: absolute;
  opacity: .55;
  transition: opacity .2s;
}

.button-to__back {
  left: 0;
  top: 220px;
}

.button-to__back:after {
  background-image: url(data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0idXRmLTgiPz4KPCEtLSBHZW5lcmF0b3I6IEFkb2JlIElsbHVzdHJhdG9yIDE3LjEuMCwgU1ZHIEV4cG9ydCBQbHVnLUluIC4gU1ZHIFZlcnNpb246IDYuMDAgQnVpbGQgMCkgIC0tPgo8IURPQ1RZUEUgc3ZnIFBVQkxJQyAiLS8vVzNDLy9EVEQgU1ZHIDEuMS8vRU4iICJodHRwOi8vd3d3LnczLm9yZy9HcmFwaGljcy9TVkcvMS4xL0RURC9zdmcxMS5kdGQiPgo8c3ZnIHZlcnNpb249IjEuMSIgaWQ9IkxheWVyXzEiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgeG1sbnM6eGxpbms9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkveGxpbmsiIHg9IjBweCIgeT0iMHB4IgoJIHdpZHRoPSIxMnB4IiBoZWlnaHQ9IjE5cHgiIHZpZXdCb3g9IjAgMCAxMiAxOSIgZW5hYmxlLWJhY2tncm91bmQ9Im5ldyAwIDAgMTIgMTkiIHhtbDpzcGFjZT0icHJlc2VydmUiPgo8Zz4KCTxnPgoJCTxnPgoJCQk8cG9seWdvbiBmaWxsPSIjRkZGRkZGIiBwb2ludHM9IjEyLDIuNSA5LjUsMCAwLDkuNSA5LjUsMTkgMTIsMTYuNiA0LjksOS41IAkJCSIvPgoJCTwvZz4KCTwvZz4KPC9nPgo8L3N2Zz4K);
  top: 13px;
  left: 15px;
  height: 20px;
  width: 13px;
}
</style>
