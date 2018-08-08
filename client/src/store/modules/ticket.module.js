import {
  FETCH_TICKET,
  FETCH_ANSWERS,
  TICKET_CREATE,
  TICKET_UPDATE,
  TICKET_DELETE,
  ANSWER_CREATE,
  ANSWER_UPDATE,
  ANSWER_DELETE
} from '@/store/actions.type'

import {
  SET_TICKET,
  SET_ANSWERS
} from '@/store/mutations.type'

import TicketAPIService from '@/services/ticket'
import AnswerAPIService from '@/services/answer'

const initialState = {
  ticket: {
    title: '',
    body: '',
    category: '',
    createdBy: 'aaa',
    createdFor: '',
    company: '',
    updatedBy: '',
    assignee: '',
    status: '',
    issueType: '',
    serverVersion: '',
    osVersion: '',
    osVersionName: '',
    link: '',
    sendCopy: '',
    isPrivate: false
  },
  answers: []
}

export const state = Object.assign({}, initialState)

export const getters = {
  ticket (state) {
    return state.ticket
  },
  answers (state) {
    return state.answers
  }
}

export const actions = {
  [FETCH_TICKET] (context, ticketSlug, prevTicket) {
    if (prevTicket !== undefined) {
      return context.commit(SET_TICKET, prevTicket)
    }

    return TicketAPIService.get(ticketSlug)
      .then(({ data }) => {
        context.commit(SET_TICKET, data)
        return data
      })
  },

  [FETCH_ANSWERS] (context, ticketSlug) {
    return AnswerAPIService.get(ticketSlug)
      .then(({ data }) => {
        context.commit(SET_ANSWERS, data)
      })
  },

  [TICKET_CREATE] ({ state }) {
    return TicketAPIService.create(state.ticket)
  },

  [TICKET_UPDATE] ({ state }) {
    return TicketAPIService.update(state.ticket.slug, state.ticket)
  },

  [TICKET_DELETE] (context, slug) {
    return TicketAPIService.destroy(slug)
  },

  [ANSWER_CREATE] (context, payload) {
    return AnswerAPIService
      .post(payload.slug, payload.comment)
      .then(() => { context.dispatch(FETCH_ANSWERS, payload.slug) })
  },

  [ANSWER_UPDATE] (context, payload) {

  },

  [ANSWER_DELETE] (context, payload) {
    return AnswerAPIService
      .destroy(payload.ticketId, payload.answerId)
      .then(() => {
        // context.dispatch(FETCH_ANSWERS, payload.ticketId)
        console.log('Deleted successfully')
      })
  }
}

export const mutations = {
  [SET_TICKET] (state, ticket) {
    state.ticket = ticket
  },

  [SET_ANSWERS] (state, answers) {
    state.answers = answers.results
  }
}

export default {
  state,
  actions,
  mutations,
  getters
}
