<template>
  <div class="search">
    <b-form @submit.prevent="onSubmit">
      <b-row class="text-center">
        <b-col v-bind:class="where === 'home'? 'col-md-7' : 'col-md-9'">
          <input type="text" class="form-control" id="id_q" v-model="queryString">
        </b-col>
        <b-col md="3" v-if="where === 'home'">
          <b-form-select v-model="categorySelected" :options="categoryOptions"/>
        </b-col>
        <b-col v-bind:class="where === 'home'? 'col-md-2' : 'col-md-3'">
          <b-button type="submit" variant="info">Search</b-button>
        </b-col>
      </b-row>

      <b-row v-if="where === 'search'">
        <b-col md="3">
          <b-form-select v-model="categorySelected" :options="categoryOptions"/>
        </b-col>
        <b-col md="3">
          <b-form-select v-model="statusSelected" :options="statusOptions"/>
        </b-col>
        <b-col md="3">
          <b-form-select v-model="versionSelected" :options="versionOptions"/>
        </b-col>
        <b-col md="3">
          <b-form-select v-model="osSelected" :options="osOptions"/>
        </b-col>
      </b-row>
    </b-form>
  </div>
</template>

<script>
import { FETCH_TICKETS } from '@/store/actions.type'
export default {
  name: 'SuppSearchBar',
  props: {
    where: String,
    default: 'home'
  },
  data () {
    return {
      queryString: '',
      categorySelected: null,
      categoryOptions: [
        { value: null, text: 'Select a Category' },
        { value: 'OUTAGE', text: 'Outages' },
        { value: 'IDNTY', text: 'Identity Management' },
        { value: 'SSO', text: 'Single Sign-On' },
        { value: 'MFA', text: 'Authentication' },
        { value: 'ACCESS', text: 'Access Management' },
        { value: 'CUSTOM', text: 'Customization' },
        { value: 'FEATURE', text: 'Feature Request' },
        { value: 'INSTALLATION', text: 'Installation' },
        { value: 'UPGRADE', text: 'Upgrade' },
        { value: 'MAINTENANCE', text: 'Maintenance' },
        { value: 'OTHER', text: 'Other' },
        { value: 'LOGOUT', text: 'Log Out' }
      ],
      statusSelected: null,
      statusOptions: [
        { value: null, text: 'Select a Status' },
        { value: 'new', text: 'New' },
        { value: 'assigned', text: 'Assigned' },
        { value: 'inprogress', text: 'In Progress' },
        { value: 'pending', text: 'Pending Input' },
        { value: 'closed', text: 'Closed' }
      ],
      versionSelected: null,
      versionOptions: [
        { value: null, text: 'Select Gluu Server Version' },
        { value: '3.1.4', text: '3.1.4' },
        { value: '3.1.3', text: '3.1.3' },
        { value: '3.1.2', text: '3.1.2' },
        { value: '3.1.1', text: '3.1.1' },
        { value: '3.1.0', text: '3.1.0' },
        { value: '3.0.2', text: '3.0.2' },
        { value: '3.0.1', text: '3.0.1' },
        { value: '2.4.4', text: '2.4.4' },
        { value: '2.4.3', text: '2.4.3' },
        { value: '2.4.2', text: '2.4.2' },
        { value: 'Other', text: 'Other' }
      ],
      osSelected: null,
      osOptions: [
        { value: null, text: 'Select Operating System' },
        { value: 'Ubuntu', text: 'Ubuntu' },
        { value: 'CentOS', text: 'CentOS' },
        { value: 'Rhel', text: 'RHEL' },
        { value: 'Debian', text: 'Debian' }
      ]
    }
  },
  methods: {
    onSubmit () {
      this.$store.dispatch(FETCH_TICKETS, {
        status: this.statusSelected,
        category: this.categorySelected,
        server: this.versionSelected,
        os: this.osSelected,
        q: this.queryString
      })
    }
  }
}
</script>

<style>

</style>
