<template>
  <div>
    <supp-ticket-answer
      ticketId="a"
      :answer="{}"
    ></supp-ticket-answer>
    <supp-ticket-answer-edit></supp-ticket-answer-edit>
  </div>
</template>

<script>
import SuppTicketAnswer from '@/components/SuppTicketAnswer'
import SuppTicketAnswerEdit from '@/components/SuppTicketAnswerEdit'

export default {
  name: 'SuppTicket',
  components: {
    SuppTicketAnswer,
    SuppTicketAnswerEdit
  }
}
</script>

<style>

</style>
