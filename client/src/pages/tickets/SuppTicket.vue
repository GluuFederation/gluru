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
        <Select2 v-model="ticket.serverVersion" :options="serverOptions" />
      </div>
      <div class="form-group">
        <label>os</label>
        <Select2 v-model="ticket.osVersion" :options="osOptions"/>
      </div>
      <div class="form-group">
        <label>osVersion</label>
        <input type="text" class="form-control" placeholder="Title" v-model="ticket.osVersionName">
      </div>
      <div class="form-group">
        <label>issueType</label>
        <Select2 v-model="ticket.issueType" :options="issueOptions"/>
      </div>
      <div class="form-group">
        <label>category</label>
        <Select2 v-model="ticket.category" :options="categoryOptions"/>
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
        <Select2 v-model="ticket.status" :options="statusOptions"/>
      </div>
      <div class="form-group">
        <label>colleagues</label>
        <input type="text" class="form-control" placeholder="Title" v-model="ticket.sendCopy">
      </div>
      <div class="form-group">
        <label>Privacy</label>
        <Select2 v-model="ticket.isPrivate" :options="privacyOptions"/>
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
import Select2 from 'v-select2-component'

// import SuppTicketAnswer from '@/components/SuppTicketAnswer'
// import SuppTicketAnswerEdit from '@/components/SuppTicketAnswerEdit'

export default {
  name: 'SuppTicket',
  components: {
    Select2
  },
  data () {
    return {
      serverOptions: [
        { id: '', text: 'Select Gluu Server Version' },
        { id: '3.1.2', text: 'Gluu Server 3.1.2' },
        { id: '3.1.1', text: 'Gluu Server 3.1.1' },
        { id: '3.1.0', text: 'Gluu Server 3.1.0' },
        { id: '3.0.2', text: 'Gluu Server 3.0.2' },
        { id: '3.0.1', text: 'Gluu Server 3.0.1' },
        { id: '2.4.4.3', text: 'Gluu Server 2.4.4.3' },
        { id: '2.4.4.2', text: 'Gluu Server 2.4.4.2' },
        { id: '2.4.4', text: 'Gluu Server 2.4.4' },
        { id: '2.4.3', text: 'Gluu Server 2.4.3' },
        { id: '2.4.2', text: 'Gluu Server 2.4.2' },
        { id: 'Other', text: 'Other' }
      ],
      categoryOptions: [
        { id: '', text: 'Select an issue category' },
        { id: 'installation', text: 'Installation' },
        { id: 'outages', text: 'Outages' },
        { id: 'single_sign_on', text: 'Single Sign-On' },
        { id: 'authentication', text: 'Authentication' },
        { id: 'authorization', text: 'Authorization' },
        { id: 'access_management', text: 'Access Management' },
        { id: 'upgrade', text: 'Upgrade' },
        { id: 'maintenance', text: 'Maintenance' },
        { id: 'identity_management', text: 'Identity Management' },
        { id: 'customization', text: 'Customization' },
        { id: 'feature_request', text: 'Feature Request' },
        { id: 'log_out', text: 'Logout' },
        { id: 'other', text: 'Other' }
      ],
      osOptions: [
        { id: '', text: 'Select Operating System' },
        { id: 'Ubuntu', text: 'Ubuntu' },
        { id: 'CentOS', text: 'CentOS' },
        { id: 'Rhel', text: 'RHEL' },
        { id: 'Debian', text: 'Debian' }
      ],
      issueOptions: [
        { id: '', text: 'Please specify the kind of issue you have encountered' },
        { id: 'outage', text: 'Production Outage' },
        { id: 'impaired', text: 'Production Impaired' },
        { id: 'pre_production', text: 'Pre-Production Issue' },
        { id: 'minor', text: 'Minor Issue' },
        { id: 'new_development', text: 'New Development Issue' }
      ],
      statusOptions: [
        { id: '', text: 'Select a Status' },
        { id: 'new', text: 'New' },
        { id: 'assigned', text: 'Assigned' },
        { id: 'inprogress', text: 'In Progress' },
        { id: 'pending', text: 'Pending Input' },
        { id: 'closed', text: 'Closed' }
      ],
      privacyOptions: [
        { id: false, text: 'Public' },
        { id: true, text: 'Private' }
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
