import APIService from '@/services/common/api.services'

const SearchAPIService = {
  query (params) {
    return APIService
      .query('tickets/', { params: params })
  }
}

export default SearchAPIService
