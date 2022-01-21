<template>
  <div class="breadcrumbs">
    <div class="container">
      <ul>
        <li>
          <router-link class="bread-link" active-class="active" to="/">Головна</router-link>
        </li>
        <li v-for="crumb in crumbs" :key="crumb">
          <a class="bread-link" :href="crumb.href">{{crumb.name}}</a>
        </li>
      </ul>
    </div>
  </div>
</template>
<script>
export default {
  name: 'Breadcrumbs',
  data() {
    return {
      crumbs: []
    }
  },
  methods: {
    addBreadcrumb(crumb) {
      this.crumbs.push(crumb);
    },
    clear() {
      this.crumbs = [];
    }
  }
}
</script>

<style>
  .bread-link {
    border-bottom: 1px dashed black;
    padding: 2px;
  }

</style>