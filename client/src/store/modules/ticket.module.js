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

import TicketService from '@/services/ticket'
import AnswerService from '@/services/answer'

const initialState = {
  ticket: {
    title: '',
    description: '',
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

    return TicketService.get(ticketSlug)
      .then(({ data }) => {
        console.log(data)
        context.commit(SET_TICKET, data)
        return data
      })
  },

  [FETCH_ANSWERS] (context, ticketSlug) {
    return AnswerService.get(ticketSlug)
      .then(({ data }) => {
        context.commit(SET_ANSWERS, data)
      })
  },

  [TICKET_CREATE] ({ state }) {
    return TicketService.create(state.ticket)
  },

  [TICKET_UPDATE] ({ state }) {
    return TicketService.update(state.ticket.slug, state.ticket)
  },

  [TICKET_DELETE] (context, slug) {
    return TicketService.destroy(slug)
  },

  [ANSWER_CREATE] (context, payload) {
    return AnswerService
      .post(payload.slug, payload.comment)
      .then(() => { context.dispatch(FETCH_ANSWERS, payload.slug) })
  },

  [ANSWER_UPDATE] (context, payload) {

  },

  [ANSWER_DELETE] (context, payload) {
    return AnswerService
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
