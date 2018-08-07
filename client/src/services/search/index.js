import ApiService from '@/services/common/api.services'

const SearchService = {
  query (params) {
    return ApiService
      .query('search', { params: params })
  },
}

export default SearchService
