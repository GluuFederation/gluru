import ApiService from '@/services/common/api.services'
const AnswersService = {
  get (slug) {
    if (typeof slug !== 'string') {
      throw new Error('[Gluu] AnswerService.get() ticket slug required to fetch answers')
    }
    return ApiService.get('tickets', `${slug}/answers`)
  },

  post (slug, payload) {
    return ApiService.post(
      `tickets/${slug}/answers`, { answer: { body: payload } })
  },

  destroy (slug, answerId) {
    return ApiService
      .delete(`tickets/${slug}/answers/${answerId}`)
  }
}

export default AnswersService
