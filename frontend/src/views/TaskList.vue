<template>
  <div class="task-list-container">
    <el-header>
      <el-button type="primary" @click="createTask">创建任务</el-button>
    </el-header>
    
    <el-table :data="tasks" stripe style="width: 100%">
      <el-table-column prop="name" label="任务名称"></el-table-column>
      <el-table-column prop="room_url" label="直播间链接"></el-table-column>
      <el-table-column prop="status" label="状态">
        <template #default="scope">
          <el-tag :type="getStatusType(scope.row.status)">{{ scope.row.status }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="创建时间"></el-table-column>
      <el-table-column prop="comments_count" label="评论数量"></el-table-column>
      <el-table-column label="操作">
        <template #default="scope">
          <el-button size="small" @click="viewTask(scope.row.id)">查看</el-button>
          <el-button 
            size="small" 
            type="primary" 
            :disabled="scope.row.status === 'running'"
            @click="startTask(scope.row.id)"
          >启动</el-button>
          <el-button 
            size="small" 
            type="warning" 
            :disabled="scope.row.status !== 'running'"
            @click="stopTask(scope.row.id)"
          >停止</el-button>
          <el-button size="small" type="danger" @click="deleteTask(scope.row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useTaskStore } from '@/stores/task'
import { useRouter } from 'vue-router'

const router = useRouter()
const taskStore = useTaskStore()
const tasks = ref([])

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

// 创建任务
const createTask = () => {
  router.push('/tasks/create')
}

// 查看任务
const viewTask = (id) => {
  router.push(`/tasks/${id}`)
}

// 启动任务
const startTask = async (id) => {
  const result = await taskStore.startTask(id)
  if (result) {
    ElMessage.success('任务已启动')
  } else {
    ElMessage.error('启动任务失败')
  }
}

// 停止任务
const stopTask = async (id) => {
  const result = await taskStore.stopTask(id)
  if (result) {
    ElMessage.success('任务已停止')
  } else {
    ElMessage.error('停止任务失败')
  }
}

// 删除任务
const deleteTask = async (id) => {
  ElMessageBox.confirm(
    '确定要删除此任务吗？删除后将无法恢复。',
    '提示',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    const success = await taskStore.deleteTask(id)
    if (success) {
      ElMessage.success('任务已删除')
    } else {
      ElMessage.error('删除任务失败')
    }
  }).catch(() => {
    // 取消操作
  })
}

// 页面加载时获取任务列表
onMounted(async () => {
  tasks.value = await taskStore.fetchTasks()
})
</script>

<style scoped>
.task-list-container {
  padding: 20px;
}
</style>