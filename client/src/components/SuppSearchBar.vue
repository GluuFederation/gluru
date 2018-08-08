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
      statusSelected: null,
      statusOptions: [
        { value: null, text: 'Select a Status' },
        { id: 'NW', text: 'New' },
        { id: 'AS', text: 'Assigned' },
        { id: 'IP', text: 'In Progress' },
        { id: 'PI', text: 'Pending Input' },
        { id: 'CL', text: 'Closed' }
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
        { id: 'UT', text: 'Ubuntu' },
        { id: 'CO', text: 'CentOS' },
        { id: 'RH', text: 'RHEL' },
        { id: 'DB', text: 'Debian' }
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
