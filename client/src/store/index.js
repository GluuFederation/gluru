import Vue from 'vue'
import Vuex from 'vuex'

import ticket from './modules/ticket.module'
import constant from './modules/constant.module'
import search from './modules/search.module'

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    ticket,
    search,
    constant
  }
})
