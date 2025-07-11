<template>
  <div class="task-detail-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>{{ task.name }}</span>
          <el-tag :type="getStatusType(task.status)">{{ task.status }}</el-tag>
        </div>
      </template>
      
      <div class="task-info">
        <p>直播间链接: <a :href="task.room_url" target="_blank">{{ task.room_url }}</a></p>
        <p>创建时间: {{ task.created_at }}</p>
        <p>更新时间: {{ task.updated_at }}</p>
      </div>
      
      <div class="task-actions">
        <el-button 
          type="primary" 
          :disabled="task.status === 'running'"
          @click="startTask"
        >启动任务</el-button>
        <el-button 
          type="warning" 
          :disabled="task.status !== 'running'"
          @click="stopTask"
        >停止任务</el-button>
        <el-button type="danger" @click="deleteTask">删除任务</el-button>
      </div>
    </el-card>
    
    <el-card class="comments-card">
      <template #header>
        <div class="card-header">评论列表</div>
      </template>
      
      <el-tabs v-model="activeTab" type="card">
        <el-tab-pane label="全部评论" name="all">
          <el-table :data="comments" stripe style="width: 100%">
            <el-table-column label="用户头像">
              <template #default="scope">
                <img :src="scope.row.user_avatar || 'https://picsum.photos/40/40'" alt="用户头像" class="avatar">
              </template>
            </el-table-column>
            <el-table-column prop="user_name" label="用户名称"></el-table-column>
            <el-table-column prop="content" label="评论内容"></el-table-column>
            <el-table-column prop="sentiment" label="情感分析">
              <template #default="scope">
                <el-tag :type="getSentimentType(scope.row.sentiment)">{{ scope.row.sentiment }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="keywords" label="关键词">
              <template #default="scope">
                <span v-for="keyword in scope.row.keywords" :key="keyword" class="keyword-tag">
                  {{ keyword }}
                </span>
              </template>
            </el-table-column>
            <el-table-column prop="created_at" label="时间"></el-table-column>
            <el-table-column label="操作">
              <template #default="scope">
                <el-button 
                  size="mini" 
                  type="primary" 
                  @click="generateVoice(scope.row.id)"
                >生成语音</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>
        <el-tab-pane label="积极评论" name="positive">
          <el-table :data="filteredComments('positive')" stripe style="width: 100%">
            <!-- 与全部评论相同的列定义 -->
            <el-table-column label="用户头像">
              <template #default="scope">
                <img :src="scope.row.user_avatar || 'https://picsum.photos/40/40'" alt="用户头像" class="avatar">
              </template>
            </el-table-column>
            <el-table-column prop="user_name" label="用户名称"></el-table-column>
            <el-table-column prop="content" label="评论内容"></el-table-column>
            <el-table-column prop="sentiment" label="情感分析">
              <template #default="scope">
                <el-tag type="success">{{ scope.row.sentiment }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="keywords" label="关键词">
              <template #default="scope">
                <span v-for="keyword in scope.row.keywords" :key="keyword" class="keyword-tag">
                  {{ keyword }}
                </span>
              </template>
            </el-table-column>
            <el-table-column prop="created_at" label="时间"></el-table-column>
            <el-table-column label="操作">
              <template #default="scope">
                <el-button 
                  size="mini" 
                  type="primary" 
                  @click="generateVoice(scope.row.id)"
                >生成语音</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>
        <el-tab-pane label="消极评论" name="negative">
          <el-table :data="filteredComments('negative')" stripe style="width: 100%">
            <!-- 与全部评论相同的列定义 -->
            <el-table-column label="用户头像">
              <template #default="scope">
                <img :src="scope.row.user_avatar || 'https://picsum.photos/40/40'" alt="用户头像" class="avatar">
              </template>
            </el-table-column>
            <el-table-column prop="user_name" label="用户名称"></el-table-column>
            <el-table-column prop="content" label="评论内容"></el-table-column>
            <el-table-column prop="sentiment" label="情感分析">
              <template #default="scope">
                <el-tag type="danger">{{ scope.row.sentiment }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="keywords" label="关键词">
              <template #default="scope">
                <span v-for="keyword in scope.row.keywords" :key="keyword" class="keyword-tag">
                  {{ keyword }}
                </span>
              </template>
            </el-table-column>
            <el-table-column prop="created_at" label="时间"></el-table-column>
            <el-table-column label="操作">
              <template #default="scope">
                <el-button 
                  size="mini" 
                  type="primary" 
                  @click="generateVoice(scope.row.id)"
                >生成语音</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>
        <el-tab-pane label="中性评论" name="neutral">
          <el-table :data="filteredComments('neutral')" stripe style="width: 100%">
            <!-- 与全部评论相同的列定义 -->
            <el-table-column label="用户头像">
              <template #default="scope">
                <img :src="scope.row.user_avatar || 'https://picsum.photos/40/40'" alt="用户头像" class="avatar">
              </template>
            </el-table-column>
            <el-table-column prop="user_name" label="用户名称"></el-table-column>
            <el-table-column prop="content" label="评论内容"></el-table-column>
            <el-table-column prop="sentiment" label="情感分析">
              <template #default="scope">
                <el-tag type="info">{{ scope.row.sentiment }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="keywords" label="关键词">
              <template #default="scope">
                <span v-for="keyword in scope.row.keywords" :key="keyword" class="keyword-tag">
                  {{ keyword }}
                </span>
              </template>
            </el-table-column>
            <el-table-column prop="created_at" label="时间"></el-table-column>
            <el-table-column label="操作">
              <template #default="scope">
                <el-button 
                  size="mini" 
                  type="primary" 
                  @click="generateVoice(scope.row.id)"
                >生成语音</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>
      </el-tabs>
    </el-card>
    
    <!-- 语音播放模态框 -->
    <el-dialog :visible.sync="voiceDialogVisible" title="语音回复">
      <template #content>
        <div class="voice-content">
          <p>{{ currentVoiceText }}</p>
          <audio controls :src="currentVoiceUrl"></audio>
        </div>
      </template>
      <template #footer>
        <el-button @click="voiceDialogVisible = false">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, inject } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useTaskStore } from '@/stores/task'
import { useCommentStore } from '@/stores/comment'
import { useSocket } from '@/composables/useSocket'

const route = useRoute()
const router = useRouter()
const taskStore = useTaskStore()
const commentStore = useCommentStore()
const socket = inject('socket')

const taskId = ref(route.params.id)
const task = ref(null)
const comments = ref([])
const activeTab = ref('all')
const voiceDialogVisible = ref(false)
const currentVoiceUrl = ref('')
const currentVoiceText = ref('')
const loading = ref(false)

// 获取任务详情
const fetchTaskDetail = async () => {
  loading.value = true
  try {
    task.value = await taskStore.fetchTask(taskId.value)
    if (!task.value) {
      ElMessage.error('任务不存在')
      router.push('/tasks')
      return
    }
  } catch (error) {
    ElMessage.error('获取任务详情失败')
    console.error(error)
  } finally {
    loading.value = false
  }
}

// 获取评论列表
const fetchComments = async () => {
  loading.value = true
  try {
    comments.value = await commentStore.fetchComments(taskId.value)
  } catch (error) {
    ElMessage.error('获取评论列表失败')
    console.error(error)
  } finally {
    loading.value = false
  }
}

// 获取状态标签类型
const getStatusType = (status) => {
  switch (status) {
    case 'pending':
      return 'info'
    case 'running':
      return 'success'
    case 'stopped':
      return 'warning'
    case 'failed':
      return 'danger'
    default:
      return 'info'
  }
}

// 获取情感标签类型
const getSentimentType = (sentiment) => {
  switch (sentiment) {
    case 'positive':
      return 'success'
    case 'negative':
      return 'danger'
    case 'neutral':
      return 'info'
    default:
      return 'info'
  }
}

// 启动任务
const startTask = async () => {
  try {
    const result = await taskStore.startTask(taskId.value)
    if (result) {
      ElMessage.success('任务已启动')
      fetchTaskDetail()
    } else {
      ElMessage.error('启动任务失败')
    }
  } catch (error) {
    ElMessage.error('启动任务失败')
    console.error(error)
  }
}

// 停止任务
const stopTask = async () => {
  try {
    const result = await taskStore.stopTask(taskId.value)
    if (result) {
      ElMessage.success('任务已停止')
      fetchTaskDetail()
    } else {
      ElMessage.error('停止任务失败')
    }
  } catch (error) {
    ElMessage.error('停止任务失败')
    console.error(error)
  }
}

// 删除任务
const deleteTask = async () => {
  ElMessageBox.confirm(
    '确定要删除此任务吗？删除后将无法恢复。',
    '提示',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      const success = await taskStore.deleteTask(taskId.value)
      if (success) {
        ElMessage.success('任务已删除')
        router.push('/tasks')
      } else {
        ElMessage.error('删除任务失败')
      }
    } catch (error) {
      ElMessage.error('删除任务失败')
      console.error(error)
    }
  }).catch(() => {
    // 取消操作
  })
}

// 生成语音
const generateVoice = async (commentId) => {
  const comment = comments.value.find(c => c.id === commentId)
  if (!comment) return
  
  try {
    const voiceUrl = await commentStore.generateVoice(commentId)
    if (voiceUrl) {
      currentVoiceUrl.value = voiceUrl
      currentVoiceText.value = comment.content
      voiceDialogVisible.value = true
    } else {
      ElMessage.error('生成语音失败')
    }
  } catch (error) {
    ElMessage.error('生成语音失败')
    console.error(error)
  }
}

// 过滤评论
const filteredComments = (sentiment) => {
  return comments.value.filter(comment => comment.sentiment === sentiment)
}

// 使用socket监听实时评论
const { connected, error } = useSocket(taskId)

// 监听评论事件
socket.on('new_comment', (comment) => {
  comments.value.unshift(comment)
  // 限制评论数量，避免内存溢出
  if (comments.value.length > 100) {
    comments.value.pop()
  }
})

// 监听评论分析事件
socket.on('comments_analyzed', (data) => {
  if (data.task_id === taskId.value) {
    // 更新评论的分析结果
    data.comments.forEach(analyzedComment => {
      const index = comments.value.findIndex(c => c.id === analyzedComment.id)
      if (index !== -1) {
        comments.value[index] = { ...comments.value[index], ...analyzedComment }
      }
    })
  }
})

// 生命周期钩子
onMounted(async () => {
  await fetchTaskDetail()
  await fetchComments()
  
  // 加入任务房间，接收实时评论
  socket.emit('join_task_room', taskId.value)
})

// 组件卸载时
const onUnmounted = () => {
  // 离开任务房间
  socket.emit('leave_task_room', taskId.value)
}
</script>

<style scoped>
.task-detail-container {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.task-info {
  margin: 10px 0;
}

.task-actions {
  margin-top: 15px;
  display: flex;
  gap: 10px;
}

.comments-card {
  margin-top: 20px;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
}

.keyword-tag {
  background-color: #f0f2f5;
  color: #606266;
  padding: 2px 5px;
  margin-right: 5px;
  border-radius: 3px;
  font-size: 12px;
}

.voice-content {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
</style>
    