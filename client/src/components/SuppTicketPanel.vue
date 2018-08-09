<template>
  <div class="card">
    <div class="card-header">
      <div class="float-left">
        <h6 class="panel-title">By Ralph Prieto
          <span data-toggle="tooltip" title="aaaa">
            <icon name="info-circle"></icon>
          </span>
          <span class="copy-email" style="display:none">rprieto@flvc.org</span>
          <b-badge variant="user">user</b-badge>
          <span class="header_date">25 Jul 2018 at 2:04 p.m. CDT</span>
        </h6>
      </div>
      <div class="float-right">
        <p v-if="isTicket">
          2 responses
        </p>
        <b-button variant="info" v-else>
          <icon name="copy"></icon>Copy
        </b-button>
      </div>
    </div>
    <div class="card-body">
      <div class="float-left">
        <img src="https://secure.gravatar.com/avatar/6814702d0fdfe4df707d6a0b32d4e9a6.jpg?s=80&amp;amp;r=g" alt="William Lowe gravatar">
      </div>
      <div style="padding-left: 100px;">
          {{ data.body }}
      </div>
    </div>
    <div class="card-footer">
      <div v-if="isTicket">
      </div>
      <div class="float-right" v-else>
        <b-button variant="info" v-on:click="deleteAnswer(ticketId, data.id)">
          <icon name="trash-alt"></icon>Delete
        </b-button>
        <b-button variant="info" v-on:click="editAnswer(ticketId, data.id)">
          <icon name="edit"></icon>Edit
        </b-button>
      </div>
    </div>
  </div>
</template>

<script>
import 'vue-awesome/icons/info-circle'
import 'vue-awesome/icons/copy'
import 'vue-awesome/icons/edit'
import 'vue-awesome/icons/trash-alt'

import {
  ANSWER_EDIT,
  ANSWER_DELETE
} from '@/store/actions.type'

export default {
  name: 'SuppTicketPanel',
  props: {
    isTicket: {
      type: Boolean,
      required: true
    },
    ticketId: {
      type: Number,
      required: true
    },
    data: {
      type: Object,
      required: true
    }
  },
  methods: {
    deleteAnswer (ticketId, answerId) {
      this.$store.dispatch(ANSWER_DELETE, { ticketId, answerId })
    },
    editAnswer (ticketId, answerId) {
      console.log(ticketId, answerId)
      this.$store.dispatch(ANSWER_EDIT, { ticketId, answerId })
    }
  }
}
</script>

<style lang="scss">
  .card {
    svg {
      margin-right: 5px;
    }
  }
</style>
