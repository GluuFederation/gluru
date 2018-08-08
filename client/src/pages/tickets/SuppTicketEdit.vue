<template>
  <div>
    <form v-on:submit.prevent="onSubmit">
      <div class="form-group">
        <label>company</label>
        <input name="company" type="text" class="form-control" placeholder="Company"
          v-model="ticket.company" v-validate="'required'" :class="{'errors': errors.has('company')}">
        <span v-show="errors.has('company')" class="errors">{{ errors.first('company') }}</span>
      </div>
      <div class="form-group">
        <label>createdFor</label>
        <input name="referer" type="text" class="form-control" placeholder="Created For"
          v-model="ticket.createdFor">
      </div>
      <div class="form-group">
        <label>serverVersion</label>
        <Select2 name="serverVersion" v-model="ticket.serverVersion" :options="serverOptions" :settings="{ theme: 'bootstrap4' }"
          v-validate="'required'" :class="{ 'errors': errors.has('serverVersion')}"/>
        <span v-show="errors.has('serverVersion')" class="errors">{{ errors.first('serverVersion') }}</span>
      </div>
      <div class="form-group">
        <label>os</label>
        <Select2 name="osVersion" v-model="ticket.osVersion" :options="osOptions" :settings="{ theme: 'bootstrap4' }"
          v-validate="'required'" :class="{ 'errors': errors.has('osVersion')}"/>
        <span v-show="errors.has('osVersion')" class="errors">{{ errors.first('osVersion') }}</span>
      </div>
      <div class="form-group">
        <label>osVersion</label>
        <input name="osVersionName" type="text" class="form-control" placeholder="Os Verson"
          v-model="ticket.osVersionName" v-validate="'required'" :class="{ 'errors': errors.has('osVersionName')}">
        <span v-show="errors.has('osVersionName')" class="errors">{{ errors.first('osVersionName') }}</span>
      </div>
      <div class="form-group">
        <label>issueType</label>
        <Select2 name="issueType" v-model="ticket.issueType" :options="issueOptions" :settings="{ theme: 'bootstrap4' }"
          v-validate="'required'" :class="{ 'errors': errors.has('issueType')}"/>
        <span v-show="errors.has('issueType')" class="errors">{{ errors.first('issueType') }}</span>
      </div>
      <div class="form-group">
        <label>category</label>
        <Select2 name="category" v-model="ticket.category" :options="categoryOptions" :settings="{ theme: 'bootstrap4' }"
          v-validate="'required'" :class="{ 'errors': errors.has('category')}"/>
        <span v-show="errors.has('category')" class="errors">{{ errors.first('category') }}</span>
      </div>
      <div class="form-group">
        <label>Title</label>
        <input name="title" type="text" class="form-control" placeholder="Title"
          v-model="ticket.title" v-validate="'required'" :class="{ 'errors': errors.has('title')}">
        <span v-show="errors.has('title')" class="errors">{{ errors.first('title') }}</span>
      </div>
      <div class="form-group">
        <label>description</label>
        <input name="body" type="text" class="form-control" placeholder="Title"
          v-model="ticket.body" v-validate="'required'" :class="{ 'errors': errors.has('body')}">
        <span v-show="errors.has('body')" class="errors">{{ errors.first('body') }}</span>
      </div>
      <div class="form-group">
        <label>asignee</label>
        <input name="assignee" type="text" class="form-control" placeholder="Title"
          v-model="ticket.assignee" v-validate="'required'" :class="{ 'errors': errors.has('assignee') }">
        <span v-show="errors.has('assignee')" class="errors">{{ errors.first('assignee') }}</span>
      </div>
      <div class="form-group">
        <label>status</label>
        <Select2 name="status" v-model="ticket.status" :options="statusOptions" :settings="{ theme: 'bootstrap4' }"
          v-validate="'required'" :class="{ 'errors': errors.has('status')}"/>
        <span v-show="errors.has('status')" class="errors">{{ errors.first('status') }}</span>
      </div>
      <div class="form-group">
        <label>colleagues</label>
        <input name="colleagues" type="text" class="form-control" placeholder="Title"
          v-model="ticket.sendCopy" v-validate="'required'" :class="{ 'errors': errors.has('colleagues') }">
        <span v-show="errors.has('colleagues')" class="errors">{{ errors.first('colleagues') }}</span>
      </div>
      <div class="form-group">
        <label>Privacy</label>
        <Select2 v-model="ticket.isPrivate" :options="privacyOptions" :settings="{ theme: 'bootstrap4' }"/>
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
import 'select2/dist/css/select2.css'
import 'select2-bootstrap4-theme/dist/select2-bootstrap4.css'

export default {
  name: 'SuppTicketEdit',
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
        { id: 'IN', text: 'Installation' },
        { id: 'OA', text: 'Outages' },
        { id: 'SO', text: 'Single Sign-On' },
        { id: 'AU', text: 'Authentication' },
        { id: 'AZ', text: 'Authorization' },
        { id: 'AM', text: 'Access Management' },
        { id: 'UG', text: 'Upgrade' },
        { id: 'MT', text: 'Maintenance' },
        { id: 'IM', text: 'Identity Management' },
        { id: 'CZ', text: 'Customization' },
        { id: 'FR', text: 'Feature Request' },
        { id: 'LO', text: 'Logout' },
        { id: 'OH', text: 'Other' }
      ],
      osOptions: [
        { id: '', text: 'Select Operating System' },
        { id: 'UT', text: 'Ubuntu' },
        { id: 'CO', text: 'CentOS' },
        { id: 'RH', text: 'RHEL' },
        { id: 'DB', text: 'Debian' }
      ],
      issueOptions: [
        { id: '', text: 'Please specify the kind of issue you have encountered' },
        { id: 'PO', text: 'Production Outage' },
        { id: 'PI', text: 'Production Impaired' },
        { id: 'PP', text: 'Pre-Production Issue' },
        { id: 'MI', text: 'Minor Issue' },
        { id: 'NI', text: 'New Development Issue' }
      ],
      statusOptions: [
        { id: '', text: 'Select a Status' },
        { id: 'NW', text: 'New' },
        { id: 'AS', text: 'Assigned' },
        { id: 'IP', text: 'In Progress' },
        { id: 'PI', text: 'Pending Input' },
        { id: 'CL', text: 'Closed' }
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
      this.$validator.validate().then(result => {
        if (!result) {
          return
        }
        this.$store.dispatch(TICKET_CREATE)
      })
    }
  }
}
</script>

<style>

</style>
