import Vue from 'vue'
import axios from 'axios'
import VueAxios from 'vue-axios'

import JwtService from '@/services/common/jwt.service'
import { API_URL } from '@/services/common/config'

const ApiService = {
  init () {
    Vue.use(VueAxios, axios)
    Vue.axios.defaults.baseURL = API_URL
  },

  setHeader () {
    Vue.axios.defaults.headers.common['Authorization'] = `Token ${JwtService.getToken()}`
  },

  query (resource, params) {
    return Vue.axios
      .get(resource, params)
      .catch((error) => {
        throw new Error(`[Gluu] ApiService ${error}`)
      })
  },

  get (resource, slug = '') {
    return Vue.axios
      .get(`${resource}/${slug}`)
      .catch((error) => {
        throw new Error(`[Gluu ApiServer ${error}`)
      })
  },

  post (resource, params) {
    return Vue.axios
      .post(`${resource}`, params)
  },

  put (resource, params) {
    return Vue.axios
      .put(`${resource}`, params)
  },

  update (resource, params) {
    return Vue.axios
      .update(`${resource}`, params)
  }
}

export default ApiService
