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
      name: 'ticket',
      component: () => import('@/pages/tickets/SuppTicket'),
      props: (route) => ({ ticketId: parseInt(route.params.ticketId) })
    },
    {
      path: '/search',
      component: () => import('@/pages/search/SuppSearch')
    }
  ]
})
