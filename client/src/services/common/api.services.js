import Vue from 'vue'
import axios from 'axios'
import VueAxios from 'vue-axios'

import JwtService from '@/services/common/jwt.service'
import { API_URL } from '@/services/common/config'

const APIService = {
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
        throw new Error(`[Gluu] APIService ${error}`)
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

  update (resource, slug, params) {
    return Vue.axios.put(`${resource}/${slug}`, params)
  },

  put (resource, params) {
    return Vue.axios
      .put(`${resource}`, params)
  },

  delete (resource) {
    return Vue.axios
      .delete(resource)
      .catch((error) => {
        throw new Error(`[Gluu] APIService ${error}`)
      })
  }
}

export default APIService
