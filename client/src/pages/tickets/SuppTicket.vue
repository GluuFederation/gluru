<template>
  <div>
    <form>
      <div class="form-group">
        <label>Title</label>
        <input type="text" class="form-control" placeholder="Title" v-model="ticket.title">
      </div>
      <div class="form-group">
        <label>description</label>
        <input type="text" class="form-control" placeholder="Title" v-model="ticket.description">
      </div>
      <div class="form-group">
        <label>category</label>
        <input type="text" class="form-control" placeholder="Title" v-model="ticket.category">
      </div>
      <div class="form-group">
        <label>company</label>
        <input type="text" class="form-control" placeholder="Title" v-model="ticket.company">
      </div>
      <div class="form-group">
        <label>createdFor</label>
        <input type="text" class="form-control" placeholder="Title" v-model="ticket.createdFor">
      </div>
      <div class="form-group">
        <label>serverVersion</label>
        <input type="text" class="form-control" placeholder="Title" v-model="ticket.serverVersion">
      </div>
      <div class="form-group">
        <label>os</label>
        <input type="text" class="form-control" placeholder="Title" v-model="ticket.os">
      </div>
      <div class="form-group">
        <label>osVersion</label>
        <input type="text" class="form-control" placeholder="Title" v-model="ticket.osVersion">
      </div>
      <div class="form-group">
        <label>issueType</label>
        <input type="text" class="form-control" placeholder="Title" v-model="ticket.issueType">
      </div>
      <div class="form-group">
        <label>asignee</label>
        <input type="text" class="form-control" placeholder="Title" v-model="ticket.asignee">
      </div>
    </form>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import { TICKET_CREATE } from '@/store/actions.type'

// import SuppTicketAnswer from '@/components/SuppTicketAnswer'
// import SuppTicketAnswerEdit from '@/components/SuppTicketAnswerEdit'

export default {
  name: 'SuppTicket',
  components: {

  },
  computed: {
    ...mapGetters([
      'ticket'
    ])
  },
  mounted () {
    this.$store.dispatch(TICKET_CREATE)
  }
}
</script>

<style>

</style>
