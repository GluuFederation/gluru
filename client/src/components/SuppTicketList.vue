<template>
  <div>
    <supp-ticket-preview
      v-for="(ticket, index) in tickets"
      :ticket="ticket"
      :key="ticket.id + index">
    </supp-ticket-preview>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import SuppTicketPreview from '@/components/SuppTicketPreview'
export default {
  name: 'SuppTicketList',
  components: {
    SuppTicketPreview
  },
  computed: {
    ...mapGetters([
      'tickets'
    ])
  }
}
</script>

<style lang="scss">

</style>
