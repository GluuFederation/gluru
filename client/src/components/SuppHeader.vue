<template>
  <b-navbar toggleable="md" sticky>
      <div class="container d-flex justify-content-between">
      <b-navbar-brand href="http://www.gluu.org/">
        <img src="../assets/img/logo.png">
      </b-navbar-brand>
      <b-navbar-toggle target="nav_collapse"></b-navbar-toggle>
      <b-collapse is-nav id="nav_collapse">
        <b-navbar-nav class="ml-auto">
          <b-nav-item-dropdown right>
            <template slot="button-content">
              Doc
            </template>
            <b-dropdown-item href="https://support.gluu.org/docs">Support Portal</b-dropdown-item>
            <b-dropdown-item href="https://gluu.org/docs">Gluu Server CE</b-dropdown-item>
            <b-dropdown-item href="https://oxd.gluu.org/docs">oxd</b-dropdown-item>
          </b-nav-item-dropdown>
          <b-nav-item-dropdown right>
            <template slot="button-content">
              Levan Begashvili
            </template>
            <b-dropdown-item href="#">My Dashboard</b-dropdown-item>
            <b-dropdown-item href="#">My Profile</b-dropdown-item>
            <b-dropdown-divider></b-dropdown-divider>
            <b-dropdown-item href="#">Logout</b-dropdown-item>
          </b-nav-item-dropdown>
          <b-nav-item href="#" class="nav-ticket-btn">New Ticket</b-nav-item>
          <b-nav-item href="#" class="nav-home-btn"><icon name="home"></icon></b-nav-item>
        </b-navbar-nav>
      </b-collapse>
      </div>
  </b-navbar>
</template>

<script>
import 'vue-awesome/icons/home'

export default {
  name: 'SuppHeader'
}
</script>
