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
import { FETCH_TICKETS } from '@/store/actions.type'

export default {
  name: 'SuppTicketList',
  components: {
    SuppTicketPreview
  },
  props: {
    status: {
      type: String,
      required: false
    },
    category: {
      type: String,
      required: false
    },
    server: {
      type: String,
      required: false
    },
    os: {
      type: String,
      required: false
    },
    q: {
      type: String,
      required: false
    },
    itemPerPage: {
      type: Number,
      required: false
    }
  },
  data () {
    return {
      currentPage: 1
    }
  },
  computed: {
    listConfig () {
      const filters = {
        offset: (this.currentPage - 1) * this.itemPerPage,
        limit: this.itemPerPage
      }

      if (this.status) {
        filters.status = this.status
      }

      if (this.category) {
        filters.category = this.category
      }

      if (this.server) {
        filters.server = this.server
      }

      if (this.os) {
        filters.os = this.os
      }

      if (this.q) {
        filters.q = this.q
      }
      return {
        filters
      }
    },
    pages () {

    },
    ...mapGetters([
      'tickets',
      'ticketsCount',
      'isLoading'
    ])
  },
  methods: {
    fetchTickets () {
      this.$store.dispatch(FETCH_TICKETS, this.listConfig())
    }
  }
}
</script>

<style lang="scss">

</style>
