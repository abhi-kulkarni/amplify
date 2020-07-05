
const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '/',name:"/", component: () => import('pages/Index.vue') },
      { path: '/usermanagement', name:"usermanagement",component: () => import('pages/userManagement.vue') },
      { path: '/add_user', name:"add_user",component: () => import('pages/add_user.vue') },
      { path: '/edit_user/:user_id/', name:"edit_user",component: () => import('pages/add_user.vue') },
      { path: '/changePassword', name:"change_password",component: () => import('pages/change_password.vue') },
     ]
  },
  {
    path: '/login',
    component: () => import('pages/login.vue'),
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
