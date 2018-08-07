import ApiService from '@/services/common/api.services'

const TicketService = {
  query (params) {
    return ApiService
      .query('tickets', { params: params }
      )
  },

  get (slug) {
    return ApiService
      .get('tickets', slug)
  },

  create (params) {
    return ApiService
      .post('tickets', { ticket: params })
  },

  update (slug, params) {
    return ApiService
      .update('tickets', slug, { ticket: params })
  },

  destory (slug) {
    return ApiService
      .delete(`tickets/${slug}`)
  }
}

export default TicketService
