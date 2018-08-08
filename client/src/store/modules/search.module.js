import SearchAPIService from '@/services/search'
import {
  FETCH_TICKETS
} from '@/store/actions.type'

import {
  FETCH_TICKETS_START,
  FETCH_TICKETS_END
} from '@/store/mutations.type'

export const state = {
  tickets: [],
  isLoading: true,
  ticketsCount: 0
}

export const getters = {
  tickets (state) {
    return state.tickets
  },

  ticketsCount (state) {
    return state.ticketsCount
  },

  isLoading (state) {
    return state.isLoading
  }
}

export const actions = {
  [FETCH_TICKETS] (context, params) {
    context.commit(FETCH_TICKETS_START)
    return SearchAPIService.query(params.filters)
      .then(({data}) => {
        context.commit(FETCH_TICKETS_END, data)
      })
  }
}

export const mutations = {
  [FETCH_TICKETS_START] (state) {
    state.isLoading = true
  },

  [FETCH_TICKETS_END] (state, data) {
    state.isLoading = false
    state.tickets = data.results
    state.ticketsCount = data.count
  }
}

export default {
  state,
  actions,
  mutations,
  getters
}
