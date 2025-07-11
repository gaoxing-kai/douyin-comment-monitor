<template>
  <div class="home-container">
    <el-card class="box-card">
      <template #header>
        <div class="clearfix">
          <span>抖音直播间评论监控系统</span>
        </div>
      </template>
      <div v-if="!user" class="login-prompt">
        <p>请先登录以开始监控直播间评论</p>
        <el-button type="primary" @click="navigateToLogin">登录</el-button>
      </div>
      <div v-else class="dashboard">
        <el-row :gutter=20>
          <el-col :span=8>
            <el-card class="stat-card">
              <div slot="header" class="clearfix">
                <span>活跃任务</span>
              </div>
              <div class="stat-value">{{ activeTasksCount }}</div>
            </el-card>
          </el-col>
          <el-col :span=8>
            <el-card class="stat-card">
              <div slot="header" class="clearfix">
                <span>今日监控评论</span>
              </div>
              <div class="stat-value">{{ todayCommentsCount }}</div>
            </el-card>
          </el-col>
          <el-col :span=8>
            <el-card class="stat-card">
              <div slot="header" class="clearfix">
                <span>语音播报次数</span>
              </div>
              <div class="stat-value">{{ voiceBroadcastCount }}</div>
            </el-card>
          </el-col>
        </el-row>
        
        <el-row class="mt-20">
          <el-col :span=24>
            <el-card>
              <div slot="header" class="clearfix">
                <span>最近监控的评论</span>
                <el-button style="float: right; padding: 3px 0" type="text">查看全部</el-button>
              </div>
              <el-table :data="latestComments" stripe>
                <el-table-column prop="username" label="用户名"></el-table-column>
                <el-table-column prop="content" label="评论内容"></el-table-column>
                <el-table-column prop="createdAt" label="时间"></el-table-column>
                <el-table-column label="操作">
                  <template #default="scope">
                    <el-button size="mini" @click="playVoice(scope.row)">语音播报</el-button>
                  </template>
                </el-table-column>
              </el-table>
            </el-card>
          </el-col>
        </el-row>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useCommentStore } from '@/stores/comment'
import { formatTime } from '@/utils/utils'

const router = useRouter()
const authStore = useAuthStore()
const commentStore = useCommentStore()

const user = computed(() => authStore.user)
const activeTasksCount = ref(0)
const todayCommentsCount = ref(0)
const voiceBroadcastCount = ref(0)
const latestComments = ref([])

const navigateToLogin = () => {
  router.push('/login')
}

const playVoice = (comment) => {
  // 调用语音播报API
  console.log('播放语音:', comment.content)
}

onMounted(async () => {
  if (user.value) {
    // 获取统计数据
    activeTasksCount.value = 5 // 示例数据
    todayCommentsCount.value = 128 // 示例数据
    voiceBroadcastCount.value = 32 // 示例数据
    
    // 获取最近评论
    latestComments.value = [
      { id: 1, username: '用户12345', content: '这个产品真不错！', createdAt: new Date() },
      { id: 2, username: '测试用户', content: '请问什么时候发货？', createdAt: new Date(Date.now() - 3600000) },
      { id: 3, username: '粉丝123', content: '主播好漂亮！', createdAt: new Date(Date.now() - 7200000) }
    ].map(comment => ({
      ...comment,
      createdAt: formatTime(comment.createdAt)
    }))
  }
})
</script>

<style scoped>
.home-container {
  padding: 20px;
}

.login-prompt {
  text-align: center;
  padding: 20px;
}

.stat-card {
  text-align: center;
}

.stat-value {
  font-size: 28px;
  color: #303133;
  padding: 10px 0;
}

.mt-20 {
  margin-top: 20px;
}
</style>
    