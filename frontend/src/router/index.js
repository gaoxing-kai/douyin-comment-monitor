import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '@/views/Home.vue';
import LoginView from '@/views/Login.vue';
import TaskListView from '@/views/TaskList.vue';
import TaskCreateView from '@/views/TaskCreate.vue';
import TaskDetailView from '@/views/TaskDetail.vue';
import ProfileView from '@/views/Profile.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomeView,
    meta: { requiresAuth: true }
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginView
  },
  {
    path: '/tasks',
    name: 'TaskList',
    component: TaskListView,
    meta: { requiresAuth: true }
  },
  {
    path: '/tasks/create',
    name: 'TaskCreate',
    component: TaskCreateView,
    meta: { requiresAuth: true }
  },
  {
    path: '/tasks/:id',
    name: 'TaskDetail',
    component: TaskDetailView,
    meta: { requiresAuth: true }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: ProfileView,
    meta: { requiresAuth: true }
  }
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
});

// 路由守卫
router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth && !localStorage.getItem('token')) {
    next({ name: 'Login' });
  } else {
    next();
  }
});

export default router;    