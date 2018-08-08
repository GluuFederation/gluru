<template>
  <div>
    <supp-ticket-preview
      v-for="(ticket, index) in tickets"
      :ticket="ticket"
      :key="ticket.id + index">
    </supp-ticket-preview>
    <paginate
      v-model="currentPage"
      :page-count="itemsPerPage"
      :prev-text="'Prev'"
      :next-text="'Next'"
      :container-class="'pagination'"
      :page-class="'page-item'"
      :prev-class="'page-item'"
      :next-class="'page-item'"
      :page-link-class="'page-link'"
      :prev-link-class="'page-link'"
      :next-link-class="'page-link'"
      :active-class="'active'">
    </paginate>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import SuppTicketPreview from '@/components/SuppTicketPreview'
import { FETCH_TICKETS } from '@/store/actions.type'
import Paginate from 'vuejs-paginate'

export default {
  name: 'SuppTicketList',
  components: {
    SuppTicketPreview,
    Paginate
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
    itemsPerPage: {
      type: Number,
      required: false,
      default: 2
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
        offset: (this.currentPage - 1) * this.itemsPerPage,
        limit: this.itemsPerPage
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
    ...mapGetters([
      'tickets',
      'ticketsCount',
      'isLoading'
    ])
  },
  watch: {
    currentPage (newValue) {
      this.listConfig.filters.offset = (newValue - 1) * this.itemsPerPage
      this.fetchTickets()
    }
  },
  mounted () {
    this.fetchTickets()
  },
  methods: {
    fetchTickets () {
      this.$store.dispatch(FETCH_TICKETS, this.listConfig)
    }
  }
}
</script>

<style lang="scss">

</style>
