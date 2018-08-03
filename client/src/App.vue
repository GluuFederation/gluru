<template>
  <div id="app">
    <supp-header></supp-header>
    <b-container class="main-container">
      <router-view/>
    </b-container>
    <supp-footer></supp-footer>
  </div>
</template>

<script>
import SuppHeader from '@/components/SuppHeader'
import SuppFooter from '@/components/SuppFooter'

export default {
  name: 'App',
  components: {
    SuppHeader,
    SuppFooter
  }
}
</script>

<style lang="scss">
  @import './assets/scss/main';
</style>
