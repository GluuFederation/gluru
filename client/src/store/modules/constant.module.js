import APIService from '@/services/common/api.services'

import {
  FETCH_COMPANIES,
  FETCH_USERS,
  FETCH_CONSTANT
} from '@/store/actions.type'

import {
  SET_COMPANIES,
  SET_USERS,
  SET_CONSTANT
} from '@/store/mutations.type'

export const state = {
  companies: [],
  users: [],
  constants: {}
}

export const getters = {
  companies (state) {
    return state.companies
  },

  users (state) {
    return state.users
  },

  constants (state) {
    return state.constants
  }
}

export const actions = {
  [FETCH_COMPANIES] () {

  },
  [FETCH_USERS] () {

  },
  [FETCH_CONSTANT] (context) {
    return APIService.get('constants')
      .then(({ data }) => {
        context.commit(SET_CONSTANT, data)
      })
  }
}

export const mutations = {
  [SET_COMPANIES] (state, companies) {
    state.companies = companies
  },

  [SET_USERS] (state, users) {
    state.users = users
  },

  [SET_CONSTANT] (state, constants) {
    state.constants = constants
  }
}

export default {
  state,
  getters,
  actions,
  mutations
}
