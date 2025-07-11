<template>
  <div class="task-list-container">
    <el-card>
      <template #header>
        <div class="clearfix">
          <span>任务列表</span>
          <el-button style="float: right" type="primary" @click="navigateToCreate">
            创建任务
          </el-button>
        </div>
      </template>
      
      <el-row class="mb-20">
        <el-col :span="12">
          <el-input v-model="searchKey" placeholder="搜索任务名称或直播间ID" 
            suffix-icon="Search" @keyup.enter="fetchTasks">
            <template #append>
              <el-button @click="fetchTasks">搜索</el-button>
            </template>
          </el-input>
        </el-col>
        <el-col :span="4">
          <el-select v-model="statusFilter" placeholder="任务状态">
            <el-option label="全部" value=""></el-option>
            <el-option label="运行中" value="running"></el-option>
            <el-option label="已暂停" value="paused"></el-option>
            <el-option label="已停止" value="stopped"></el-option>
          </el-select>
        </el-col>
        <el-col :span="4">
          <el-button type="primary" @click="fetchTasks">刷新</el-button>
        </el-col>
      </el-row>
      
      <el-table :data="taskList" stripe border @row-click="handleRowClick">
        <el-table-column prop="name" label="任务名称"></el-table-column>
        <el-table-column prop="roomId" label="直播间ID"></el-table-column>
        <el-table-column prop="status" label="状态">
          <template #default="scope">
            <el-tag :type="getStatusType(scope.row.status)">{{ getStatusText(scope.row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="createTime" label="创建时间"></el-table-column>
        <el-table-column label="操作">
          <template #default="scope">
            <el-button size="mini" type="primary" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button size="mini" type="success" @click="handleStart(scope.row)" 
              v-if="scope.row.status !== 'running'">启动</el-button>
            <el-button size="mini" type="warning" @click="handlePause(scope.row)" 
              v-if="scope.row.status === 'running'">暂停</el-button>
            <el-button size="mini" type="danger" @click="handleDelete(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="currentPage"
        :page-sizes="[10, 20, 50, 100]"
        :page-size="pageSize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total">
      </el-pagination>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useTaskStore } from '@/stores/task'
import { ElMessage, ElMessageBox } from 'element-plus'  // 正确导入ElMessageBox
import { formatDateTime } from '@/utils/utils'

const router = useRouter()
const taskStore = useTaskStore()

const taskList = ref([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)
const searchKey = ref('')
const statusFilter = ref('')

const getStatusText = (status) => {
  const statusMap = {
    'running': '运行中',
    'paused': '已暂停',
    'stopped': '已停止'
  }
  return statusMap[status] || status
}

const getStatusType = (status) => {
  const typeMap = {
    'running': 'success',
    'paused': 'warning',
    'stopped': 'info'
  }
  return typeMap[status] || 'default'
}

const fetchTasks = async () => {
  try {
    const params = {
      page: currentPage.value,
      pageSize: pageSize.value,
      keyword: searchKey.value,
      status: statusFilter.value
    }
    
    const result = await taskStore.getTaskList(params)
    taskList.value = result.items.map(task => ({
      ...task,
      createTime: formatDateTime(task.createTime)
    }))
    total.value = result.total
  } catch (error) {
    console.error('获取任务列表失败:', error)
    ElMessage.error(error.message || '获取任务列表失败')
  }
}

const handleRowClick = (row) => {
  router.push({ name: 'TaskDetail', params: { id: row.id } })
}

const handleEdit = (row) => {
  router.push({ name: 'TaskDetail', params: { id: row.id, edit: true } })
}

const handleStart = async (row) => {
  try {
    await taskStore.startTask(row.id)
    ElMessage.success('任务启动成功')
    fetchTasks()
  } catch (error) {
    console.error('启动任务失败:', error)
    ElMessage.error(error.message || '启动任务失败')
  }
}

const handlePause = async (row) => {
  try {
    await taskStore.pauseTask(row.id)
    ElMessage.success('任务已暂停')
    fetchTasks()
  } catch (error) {
    console.error('暂停任务失败:', error)
    ElMessage.error(error.message || '暂停任务失败')
  }
}

const handleDelete = async (row) => {
  // 使用ElMessageBox.confirm显示确认对话框
  ElMessageBox.confirm(
    '确定要删除此任务吗？删除后将无法恢复',
    '提示',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      await taskStore.deleteTask(row.id)
      ElMessage.success('任务删除成功')
      fetchTasks()
    } catch (error) {
      console.error('删除任务失败:', error)
      ElMessage.error(error.message || '删除任务失败')
    }
  }).catch(() => {
    // 用户取消操作
  })
}

const handleSizeChange = (newSize) => {
  pageSize.value = newSize
  fetchTasks()
}

const handleCurrentChange = (newPage) => {
  currentPage.value = newPage
  fetchTasks()
}

const navigateToCreate = () => {
  router.push({ name: 'TaskCreate' })
}

onMounted(() => {
  fetchTasks()
})
</script>

<style scoped>
.task-list-container {
  padding: 20px;
}

.mb-20 {
  margin-bottom: 20px;
}
</style>
    