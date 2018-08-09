<template>
  <div>
    <h1> {{ ticket.title }} </h1>
    <supp-ticket-panel
      :isTicket="true"
      :ticketId="ticketId"
      :data="ticket">
    </supp-ticket-panel>
    <supp-ticket-panel
      v-for="(answer, index) in answers"
      :isTicket="false"
      :ticketId="ticketId"
      :data="answer"
      :key="index">
    </supp-ticket-panel>
    <supp-ticket-answer-edit
      :ticketId="ticketId">
    </supp-ticket-answer-edit>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import SuppTicketPanel from '@/components/SuppTicketPanel'
import SuppTicketAnswerEdit from '@/components/SuppTicketAnswerEdit'
import { FETCH_TICKET, FETCH_ANSWERS } from '@/store/actions.type'

export default {
  name: 'SuppTicket',
  props: {
    ticketId: {
      type: Number,
      required: true
    }
  },
  components: {
    SuppTicketPanel,
    SuppTicketAnswerEdit
  },
  computed: {
    ...mapGetters([
      'ticket',
      'answers'
    ])
  },
  mounted () {
    this.$store.dispatch(FETCH_TICKET, this.ticketId)
    this.$store.dispatch(FETCH_ANSWERS, this.ticketId)
  }
}
</script>

<style>

</style>
