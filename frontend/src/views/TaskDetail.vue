<!-- src/views/TaskDetail.vue -->
<template>
  <div class="task-detail-container">
    <el-card>
      <template #header>
        <div class="clearfix">
          <span>{{ isEditMode ? '编辑任务' : '任务详情' }}</span>
          <el-button style="float: right" type="primary" v-if="!isEditMode" @click="editTask">
            编辑
          </el-button>
        </div>
      </template>
      
      <el-form :model="task" label-width="120px" v-if="task.id">
        <el-form-item label="任务名称">
          <el-input v-model="task.name" :disabled="!isEditMode"></el-input>
        </el-form-item>
        
        <el-form-item label="直播间ID">
          <el-input v-model="task.roomId" :disabled="!isEditMode"></el-input>
        </el-form-item>
        
        <el-form-item label="监控类型">
          <el-radio-group v-model="task.monitorType" :disabled="!isEditMode">
            <el-radio :label="1">全部评论</el-radio>
            <el-radio :label="2">包含关键词</el-radio>
            <el-radio :label="3">排除关键词</el-radio>
          </el-radio-group>
        </el-form-item>
        
        <el-form-item label="关键词" v-if="task.monitorType !== 1">
          <el-input v-model="task.keywords" type="textarea" rows="3" :disabled="!isEditMode"></el-input>
        </el-form-item>
        
        <el-form-item label="语音播报">
          <el-switch v-model="task.voiceEnable" active-text="开启" inactive-text="关闭" 
            :disabled="!isEditMode"></el-switch>
        </el-form-item>
        
        <el-form-item label="语音类型" v-if="task.voiceEnable">
          <el-select v-model="task.voiceType" placeholder="请选择语音类型" :disabled="!isEditMode">
            <el-option label="女声" value="female"></el-option>
            <el-option label="男声" value="male"></el-option>
            <el-option label="童声" value="child"></el-option>
          </el-select>
        </el-form-item>
        
        <el-form-item label="自动回复">
          <el-switch v-model="task.autoReplyEnable" active-text="开启" inactive-text="关闭" 
            :disabled="!isEditMode"></el-switch>
        </el-form-item>
        
        <el-form-item label="回复内容" v-if="task.autoReplyEnable">
          <el-input v-model="task.replyContent" type="textarea" rows="3" :disabled="!isEditMode"></el-input>
        </el-form-item>
        
        <el-form-item label="创建时间">
          <el-input v-model="task.createTime" disabled></el-input>
        </el-form-item>
        
        <el-form-item label="状态">
          <el-tag :type="getStatusType(task.status)">{{ getStatusText(task.status) }}</el-tag>
        </el-form-item>
        
        <el-form-item v-if="isEditMode">
          <el-button type="primary" @click="saveTask">保存</el-button>
          <el-button @click="cancelEdit">取消</el-button>
        </el-form-item>
        
        <el-form-item v-if="!isEditMode">
          <el-button type="success" @click="startTask" v-if="task.status !== 'running'">启动</el-button>
          <el-button type="warning" @click="pauseTask" v-if="task.status === 'running'">暂停</el-button>
          <el-button type="danger" @click="deleteTask">删除</el-button>
        </el-form-item>
      </el-form>
      
      <div v-else class="loading-text">
        加载中...
      </div>
    </el-card>
    
    <el-card class="mt-20">
      <template #header>
        <div class="clearfix">
          <span>评论监控记录</span>
        </div>
      </template>
      
      <el-table :data="commentList" stripe border>
        <el-table-column prop="username" label="用户名"></el-table-column>
        <el-table-column prop="content" label="评论内容"></el-table-column>
        <el-table-column prop="createTime" label="时间"></el-table-column>
        <el-table-column label="操作">
          <template #default="scope">
            <el-button size="mini" @click="playVoice(scope.row)">语音播报</el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="commentPage"
        :page-sizes="[10, 20, 50]"
        :page-size="commentPageSize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="commentTotal">
      </el-pagination>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useTaskStore } from '@/stores/task'
import { useCommentStore } from '@/stores/comment'
import { ElMessage, ElMessageBox } from 'element-plus'  // 正确导入ElMessageBox
import { formatDateTime } from '@/utils/utils'

const router = useRouter()
const route = useRoute()
const taskStore = useTaskStore()
const commentStore = useCommentStore()

const taskId = route.params.id
const isEditMode = ref(route.query.edit === 'true')
const originalTask = ref(null)

const task = reactive({
  id: '',
  name: '',
  roomId: '',
  monitorType: 1,
  keywords: '',
  voiceEnable: true,
  voiceType: 'female',
  autoReplyEnable: false,
  replyContent: '',
  createTime: '',
  status: 'stopped'
})

const commentList = ref([])
const commentTotal = ref(0)
const commentPage = ref(1)
const commentPageSize = ref(10)

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

const fetchTaskDetail = async () => {
  try {
    const result = await taskStore.getTaskDetail(taskId)
    originalTask.value = { ...result }
    
    // 复制到表单数据
    Object.assign(task, result, {
      createTime: formatDateTime(result.createTime)
    })
    
    // 获取评论记录
    fetchComments()
  } catch (error) {
    console.error('获取任务详情失败:', error)
    ElMessage.error(error.message || '获取任务详情失败')
  }
}

const fetchComments = async () => {
  try {
    const params = {
      taskId: taskId,
      page: commentPage.value,
      pageSize: commentPageSize.value
    }
    
    const result = await commentStore.getCommentsByTask(params)
    commentList.value = result.items.map(comment => ({
      ...comment,
      createTime: formatDateTime(comment.createTime)
    }))
    commentTotal.value = result.total
  } catch (error) {
    console.error('获取评论记录失败:', error)
    ElMessage.error(error.message || '获取评论记录失败')
  }
}

const editTask = () => {
  router.push({ name: 'TaskDetail', params: { id: taskId }, query: { edit: 'true' } })
}

const saveTask = async () => {
  try {
    await taskStore.updateTask(taskId, {
      name: task.name,
      roomId: task.roomId,
      monitorType: task.monitorType,
      keywords: task.keywords,
      voiceEnable: task.voiceEnable,
      voiceType: task.voiceType,
      autoReplyEnable: task.autoReplyEnable,
      replyContent: task.replyContent
    })
    
    ElMessage.success('任务更新成功')
    isEditMode.value = false
    fetchTaskDetail()
  } catch (error) {
    console.error('更新任务失败:', error)
    ElMessage.error(error.message || '更新任务失败')
  }
}

const cancelEdit = () => {
  // 恢复原始数据
  Object.assign(task, originalTask.value)
  isEditMode.value = false
}

const startTask = async () => {
  try {
    await taskStore.startTask(taskId)
    ElMessage.success('任务启动成功')
    fetchTaskDetail()
  } catch (error) {
    console.error('启动任务失败:', error)
    ElMessage.error(error.message || '启动任务失败')
  }
}

const pauseTask = async () => {
  try {
    await taskStore.pauseTask(taskId)
    ElMessage.success('任务已暂停')
    fetchTaskDetail()
  } catch (error) {
    console.error('暂停任务失败:', error)
    ElMessage.error(error.message || '暂停任务失败')
  }
}

const deleteTask = async () => {
  ElMessageBox.confirm(  // 使用ElMessageBox.confirm
    '确定要删除此任务吗？删除后将无法恢复',
    '提示',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      await taskStore.deleteTask(taskId)
      ElMessage.success('任务删除成功')
      router.push({ name: 'TaskList' })
    } catch (error) {
      console.error('删除任务失败:', error)
      ElMessage.error(error.message || '删除任务失败')
    }
  }).catch(() => {
    // 用户取消操作
  })
}

const playVoice = (comment) => {
  // 调用语音播报API
  console.log('播放语音:', comment.content)
}

const handleSizeChange = (newSize) => {
  commentPageSize.value = newSize
  fetchComments()
}

const handleCurrentChange = (newPage) => {
  commentPage.value = newPage
  fetchComments()
}

onMounted(() => {
  fetchTaskDetail()
})

watch(() => route.query.edit, (newVal) => {
  isEditMode.value = newVal === 'true'
  if (!isEditMode.value && originalTask.value) {
    // 从编辑模式切换到查看模式时，恢复原始数据
    Object.assign(task, originalTask.value)
  }
})
</script>

<style scoped>
.task-detail-container {
  padding: 20px;
}

.mt-20 {
  margin-top: 20px;
}

.loading-text {
  text-align: center;
  padding: 20px;
}
</style>