<template>
  <div>
    <router-link
      :to="{ name: 'ticket', params: { 'ticketId': ticket.id } }"
      class="">
      <h1>{{ticket.title}}</h1>
      <p>{{ ticket.body }} </p>
    </router-link>
  </div>
</template>

<script>
export default {
  name: 'SuppTicketPreview',
  props: {
    ticket: { type: Object, required: true }
  }
}
</script>

<style lang="scss">

</style>
