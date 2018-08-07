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
      path: '/ticket/:id',
      component: () => import('@/pages/tickets/SuppTicket')
    }
  ]
})
