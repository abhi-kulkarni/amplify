
const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '/home',name:"home", component: () => import('pages/Home.vue') },
      { path: '/profile', name:"profile",component: () => import('pages/profile.vue') },
      { path: '/todo', name:"todo",component: () => import('pages/todo.vue') },
      { path: '/change_password', name:"change_password",component: () => import('pages/change_password.vue') },
     ]
  },
  {
    path: '/login',
    component: () => import('pages/login.vue'),
  },
  {
    path: '/signup',
    component: () => import('pages/signup.vue'),
  }

];

// Always leave this as last one
if (process.env.MODE !== 'ssr') {
  routes.push({
    path: '*',
    component: () => import('pages/Error404.vue')
  })
}

export default routes
