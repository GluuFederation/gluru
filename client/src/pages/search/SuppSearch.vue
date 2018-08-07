<template>
  <div>
    <supp-search-bar where="search"></supp-search-bar>
    <supp-ticket-list></supp-ticket-list>
  </div>
</template>

<script>
import SuppSearchBar from '@/components/SuppSearchBar'
import SuppTicketList from '@/components/SuppTicketList'
export default {
  name: 'SuppSearch',
  components: {
    SuppSearchBar,
    SuppTicketList
  }
}
</script>

<style>

</style>
