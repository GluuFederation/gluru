<template>
  <div>
    <form v-on:submit.prevent="onSubmit">
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
        <b-form-select v-model="ticket.serverVersion" :options="serverOptions"/>
      </div>
      <div class="form-group">
        <label>os</label>
        <b-form-select v-model="ticket.osVersion" :options="osOptions"/>
      </div>
      <div class="form-group">
        <label>osVersion</label>
        <input type="text" class="form-control" placeholder="Title" v-model="ticket.osVersionName">
      </div>
      <div class="form-group">
        <label>issueType</label>
        <b-form-select v-model="ticket.issueType" :options="issueOptions"/>
      </div>
      <div class="form-group">
        <label>category</label>
        <b-form-select v-model="ticket.category" :options="categoryOptions"/>
      </div>
      <div class="form-group">
        <label>Title</label>
        <input type="text" class="form-control" placeholder="Title" v-model="ticket.title">
      </div>
      <div class="form-group">
        <label>description</label>
        <input type="text" class="form-control" placeholder="Title" v-model="ticket.description">
      </div>
      <div class="form-group">
        <label>asignee</label>
        <input type="text" class="form-control" placeholder="Title" v-model="ticket.assignee">
      </div>
      <div class="form-group">
        <label>status</label>
        <b-form-select v-model="ticket.status" :options="statusOptions"/>
      </div>
      <div class="form-group">
        <label>colleagues</label>
        <input type="text" class="form-control" placeholder="Title" v-model="ticket.sendCopy">
      </div>
      <div class="form-group">
        <label>Privacy</label>
        <b-form-select v-model="ticket.isPrivate" :options="privacyOptions"/>
      </div>
      <div class="form-group">
        <b-button type="submit" variant="info">Submit</b-button>
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
  data () {
    return {
      serverOptions: [
        { value: null, text: 'Select Gluu Server Version' },
        { value: '3.1.2', text: 'Gluu Server 3.1.2' },
        { value: '3.1.1', text: 'Gluu Server 3.1.1' },
        { value: '3.1.0', text: 'Gluu Server 3.1.0' },
        { value: '3.0.2', text: 'Gluu Server 3.0.2' },
        { value: '3.0.1', text: 'Gluu Server 3.0.1' },
        { value: '2.4.4.3', text: 'Gluu Server 2.4.4.3' },
        { value: '2.4.4.2', text: 'Gluu Server 2.4.4.2' },
        { value: '2.4.4', text: 'Gluu Server 2.4.4' },
        { value: '2.4.3', text: 'Gluu Server 2.4.3' },
        { value: '2.4.2', text: 'Gluu Server 2.4.2' },
        { value: 'Other', text: 'Other' }
      ],
      categoryOptions: [
        { value: null, text: 'Select an issue category' },
        { value: 'installation', text: 'Installation' },
        { value: 'outages', text: 'Outages' },
        { value: 'single_sign_on', text: 'Single Sign-On' },
        { value: 'authentication', text: 'Authentication' },
        { value: 'authorization', text: 'Authorization' },
        { value: 'access_management', text: 'Access Management' },
        { value: 'upgrade', text: 'Upgrade' },
        { value: 'maintenance', text: 'Maintenance' },
        { value: 'identity_management', text: 'Identity Management' },
        { value: 'customization', text: 'Customization' },
        { value: 'feature_request', text: 'Feature Request' },
        { value: 'log_out', text: 'Logout' },
        { value: 'other', text: 'Other' }
      ],
      osOptions: [
        { value: null, text: 'Select Operating System' },
        { value: 'Ubuntu', text: 'Ubuntu' },
        { value: 'CentOS', text: 'CentOS' },
        { value: 'Rhel', text: 'RHEL' },
        { value: 'Debian', text: 'Debian' }
      ],
      issueOptions: [
        { value: null, text: 'Please specify the kind of issue you have encountered' },
        { value: 'outage', text: 'Production Outage' },
        { value: 'impaired', text: 'Production Impaired' },
        { value: 'pre_production', text: 'Pre-Production Issue' },
        { value: 'minor', text: 'Minor Issue' },
        { value: 'new_development', text: 'New Development Issue' }
      ],
      statusOptions: [
        { value: null, text: 'Select a Status' },
        { value: 'new', text: 'New' },
        { value: 'assigned', text: 'Assigned' },
        { value: 'inprogress', text: 'In Progress' },
        { value: 'pending', text: 'Pending Input' },
        { value: 'closed', text: 'Closed' }
      ],
      privacyOptions: [
        { value: false, text: 'Public' },
        { value: true, text: 'Private' }
      ]
    }
  },
  computed: {
    ...mapGetters([
      'ticket'
    ])
  },
  methods: {
    onSubmit () {
      this.$store.dispatch(TICKET_CREATE)
    }
  }
}
</script>

<style>

</style>
