import {
  TICKET_CREATE,
  TICKET_UPDATE
} from '@/store/actions.type'
import TicketService from '@/services/ticket'

const initialState = {
  ticket: {
    title: 'title',
    description: 'description',
    category: 'installation',
    company: '',
    createdFor: '',
    serverVersion: '',
    os: '',
    osVersion: '',
    issueType: '',
    asignee: '',
    status: '',
    colleagues: '',
    private: '',
    link: ''
  }
}

export const state = Object.assign({}, initialState)

export const getters = {
  ticket (state) {
    return state.ticket
  }
}

export const actions = {
  [TICKET_CREATE] ({ state }) {
    console.log('create')
    return TicketService.create(state.ticket)
  },

  [TICKET_UPDATE] ({ state }) {
    return TicketService.update(state.ticket.slug, state.ticket)
  }
}

export const mutations = {

}

export default {
  state,
  actions,
  mutations,
  getters
}
