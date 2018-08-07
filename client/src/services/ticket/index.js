import APIService from '@/services/common/api.services'

const TicketAPIService = {
  query (params) {
    return APIService
      .query('tickets', { params: params }
      )
  },

  get (slug) {
    return APIService
      .get('tickets', slug)
  },

  create (params) {
    return APIService
      .post('tickets', { ticket: params })
  },

  update (slug, params) {
    return APIService
      .update('tickets', slug, { ticket: params })
  },

  destory (slug) {
    return APIService
      .delete(`tickets/${slug}`)
  }
}

export default TicketAPIService
