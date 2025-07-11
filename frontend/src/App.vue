<template>
  <div id="app">
    <el-container class="app-container">
      <el-header>
        <div class="header-container">
          <div class="logo">抖音直播间评论监控系统</div>
          <el-menu
            :default-active="activeMenu"
            mode="horizontal"
            background-color="#545c64"
            text-color="#fff"
            active-text-color="#ffd04b"
            @select="handleSelect">
            <el-menu-item index="1" route="/">
              <i class="el-icon-s-home"></i>
              <span>首页</span>
            </el-menu-item>
            <el-menu-item index="2" route="/tasks">
              <i class="el-icon-s-management"></i>
              <span>任务管理</span>
            </el-menu-item>
            <el-menu-item index="3" route="/profile">
              <i class="el-icon-user"></i>
              <span>个人中心</span>
            </el-menu-item>
            <el-menu-item index="logout" style="float: right;">
              <i class="el-icon-switch-button"></i>
              <span>退出登录</span>
            </el-menu-item>
          </el-menu>
        </div>
      </el-header>
      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const activeMenu = ref('1')

const handleSelect = (key) => {
  if (key === 'logout') {
    authStore.logout()
    router.push('/login')
  } else {
    const menuItem = document.querySelector(`el-menu-item[index="${key}"]`)
    const routePath = menuItem?.getAttribute('route')
    if (routePath) {
      router.push(routePath)
    }
  }
}

onMounted(() => {
  // 根据当前路由设置激活菜单
  const pathToMenuIndex = {
    '/': '1',
    '/tasks': '2',
    '/profile': '3'
  }
  
  activeMenu.value = pathToMenuIndex[route.path] || '1'
})
</script>

<style scoped>
.app-container {
  height: 100vh;
}

.header-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  font-size: 1.5rem;
  color: #fff;
  padding: 0 20px;
}
</style>
    