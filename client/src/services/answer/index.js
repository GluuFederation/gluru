import APIService from '@/services/common/api.services'

const AnswerAPIService = {
  get (slug) {
    if (typeof slug !== 'string') {
      throw new Error('[Gluu] AnswerAPIService.get() ticket slug required to fetch answers')
    }
    return APIService.get('tickets', `${slug}/answers`)
  },

  post (slug, payload) {
    return APIService.post(
      `tickets/${slug}/answers`, { answer: { body: payload } })
  },

  destroy (slug, answerId) {
    return APIService
      .delete(`tickets/${slug}/answers/${answerId}`)
  }
}

export default AnswerAPIService
