import { createApp } from 'vue'
import App from './App.vue'
import {createRouter, createWebHistory} from 'vue-router'
import VueClipboard from 'vue3-clipboard'
import 'maplibre-gl/dist/maplibre-gl.css';
import 'mapbox-gl/dist/mapbox-gl.css';
import 'mapbox-gl-compare/dist/mapbox-gl-compare.css';

import axios from 'axios';
import './assets/styles.scss'
import DynamicModalWindows from "@/components/DynamicModalWindows";
import AboutPageComponent from "@/components/AboutPageComponent";
import PulseLoader from 'vue-spinner/src/PulseLoader.vue';
import BounceLoader from 'vue-spinner/src/BounceLoader.vue';

import VTooltipPlugin from 'v-tooltip';
import 'v-tooltip/dist/v-tooltip.css';
import "mapbox-layer-control/layerControl.css";
import MainPage from "@/components/MainPage";
import ParcelInfoPage from "@/components/ParcelInfoPage";
import UpdatesListPage from "@/components/UpdatesListPage";

// 2. Define some routes
// Each route should map to a component.
// We'll talk about nested routes later.
const routes = [
  { name: 'main', path: '', component: MainPage },
  { name: 'parcel', path: '/parcel/:pk?', component: ParcelInfoPage },
  { name: 'update', path: '/update/:pk?', component: UpdatesListPage },
  { name: 'about', path: '/about', component: AboutPageComponent },
]

// 3. Create the router instance and pass the `routes` option
// You can pass in additional options here, but let's
// keep it simple for now.
const router = createRouter({
  // 4. Provide the history implementation to use. We are using the hash history for simplicity here.
  history: createWebHistory(),
  routes, // short for `routes: routes`
});

const app = createApp(App);
app.use(router);
app.use(VTooltipPlugin);
app.use(VueClipboard, {
  autoSetContainer: true,
  appendToBody: true,
});
app.component('DynamicModalWindows', DynamicModalWindows);
app.component('PulseLoader', PulseLoader);
app.component('BounceLoader', BounceLoader);
// app.use(VueMapbox, { mapboxgl: Mapbox });
app.mount('#app');


// direct api requests to backend, not vue service
axios.defaults.baseURL = process.env.VUE_APP_BACKEND_HOST;