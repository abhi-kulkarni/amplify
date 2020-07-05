import Vue from 'vue'
import VueRouter from 'vue-router'

import store from '../store/index.js';
import axios from 'axios'
import routes from './routes'

Vue.use(VueRouter)

/*
 * If not building with SSR mode, you can
 * directly export the Router instantiation
 */


const Router = new VueRouter({
  scrollBehavior: () => ({y: 0}),
  routes,

  // Leave these as is and change from quasar.conf.js instead!
  // quasar.conf.js -> build -> vueRouterMode
  // quasar.conf.js -> build -> publicPath
  mode: process.env.VUE_ROUTER_MODE,
  base: process.env.VUE_ROUTER_BASE
})


export default Router

Router.beforeEach((to, from, next) => {
  var api = process.env.API;
  if (to.path == "/login" || to.path == "/forgot_password") {
    next()
  }
  else {
    if (store.state.session.is_logged_in) {
      next()
    } else {
      axios.get('/api/get_authenticated_user_information', {
        // baseURL: process.env.API,
        withCredentials: true
      }).then((response) => {
        if (response.data.ok) {
          store.dispatch('setLoginSession', response.data.user_data);

          if (response.data.is_logged_in)
            next();
          else {
            console.log('else')
            next('/login');
          }
        }
        else {
          next('/login');
        }
      }).catch((error) => {
        // handle error
        if (error.response.status === 401)
          return next('/login');
        else
          return Promise.reject(error);
      })
    }
  }
})



