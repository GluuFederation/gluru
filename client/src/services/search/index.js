import APIService from '@/services/common/api.services'

const SearchAPIService = {
  query (params) {
    return APIService
      .query('search', { params: params })
  },
}

export default SearchAPIService
