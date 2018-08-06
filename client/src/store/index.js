import Vue from 'vue'
import Vuex from 'vuex'

import ticket from './modules/ticket.module'
import constant from './modules/constant.module'
Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    ticket,
    constant
  }
})
