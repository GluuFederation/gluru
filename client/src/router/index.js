import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      redirect: '/add-ticket'
    },
    {
      path: '/add-ticket',
      component: () => import('@/pages/tickets/SuppTicketEdit')
    },
    {
      path: '/ticket/:ticketId',
      component: () => import('@/pages/tickets/SuppTicket'),
      props: true
    },
    {
      path: '/search',
      component: () => import('@/pages/search/SuppSearch')
    }
  ]
})
