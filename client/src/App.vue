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

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
