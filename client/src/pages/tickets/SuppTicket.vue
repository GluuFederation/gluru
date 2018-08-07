<template>
  <div>
    <supp-ticket-answer
      v-for="(answer, index) in answers"
      :ticketId="ticketId"
      :answer="answer"
      :key="index">
    </supp-ticket-answer>
    <supp-ticket-answer-edit></supp-ticket-answer-edit>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import SuppTicketAnswer from '@/components/SuppTicketAnswer'
import SuppTicketAnswerEdit from '@/components/SuppTicketAnswerEdit'
import { FETCH_TICKET, FETCH_ANSWERS } from '@/store/actions.type'

export default {
  name: 'SuppTicket',
  props: {
    ticketId: {
      type: String,
      required: true
    }
  },
  components: {
    SuppTicketAnswer,
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
