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
        <input name="description" type="text" class="form-control" placeholder="Title"
          v-model="ticket.description" v-validate="'required'" :class="{ 'errors': errors.has('description')}">
        <span v-show="errors.has('description')" class="errors">{{ errors.first('description') }}</span>
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
