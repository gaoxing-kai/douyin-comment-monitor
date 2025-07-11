<template>
  <div id="app">
    <el-container>
      <!-- 顶部导航栏 -->
      <el-header>
        <div class="header-container">
          <div class="logo">抖音直播间评论监控系统</div>
          <el-menu
            :default-active="activeMenu"
            class="el-menu-demo"
            mode="horizontal"
            @select="handleSelect"
          >
            <el-menu-item index="home">首页</el-menu-item>
            <el-menu-item index="tasks">任务管理</el-menu-item>
            <el-menu-item index="profile">个人中心</el-menu-item>
          </el-menu>
          <div class="user-info">
            <span>{{ username }}</span>
            <el-button size="small" type="primary" @click="logout">退出登录</el-button>
          </div>
        </div>
      </el-header>
      
      <!-- 主体内容 -->
      <el-main>
        <router-view />
      </el-main>
      
      <!-- 底部 -->
      <el-footer>© 2025 抖音直播间评论监控系统</el-footer>
    </el-container>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const activeMenu = ref('home');
const username = ref('');

// 根据当前路由设置活动菜单
onMounted(() => {
  const path = router.currentRoute.value.path;
  if (path.startsWith('/tasks')) {
    activeMenu.value = 'tasks';
  } else if (path.startsWith('/profile')) {
    activeMenu.value = 'profile';
  } else {
    activeMenu.value = 'home';
  }
  
  // 从本地存储获取用户名
  username.value = localStorage.getItem('username') || '用户';
});

// 处理菜单选择
const handleSelect = (key) => {
  switch (key) {
    case 'home':
      router.push('/');
      break;
    case 'tasks':
      router.push('/tasks');
      break;
    case 'profile':
      router.push('/profile');
      break;
  }
};

// 退出登录
const logout = () => {
  localStorage.removeItem('token');
  localStorage.removeItem('username');
  router.push('/login');
};
</script>

<style scoped>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  height: 100vh;
}

.el-header {
  background-color: #2c3e50;
  color: #fff;
  line-height: 60px;
}

.header-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 100%;
  padding: 0 20px;
}

.logo {
  font-size: 20px;
  font-weight: bold;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.el-main {
  padding: 20px;
}

.el-footer {
  background-color: #f0f2f5;
  line-height: 60px;
}
</style>    