<!-- src/views/TaskCreate.vue -->
<template>
  <div class="task-create-container">
    <el-card>
      <template #header>
        <div class="clearfix">
          <span>创建监控任务</span>
        </div>
      </template>
      <el-form :model="taskForm" :rules="taskRules" ref="formRef" label-width="120px">
        <el-form-item label="任务名称" prop="name">
          <el-input v-model="taskForm.name" placeholder="请输入任务名称"></el-input>
        </el-form-item>
        
        <el-form-item label="直播间ID" prop="roomId">
          <el-input v-model="taskForm.roomId" placeholder="请输入抖音直播间ID"></el-input>
        </el-form-item>
        
        <el-form-item label="监控类型" prop="monitorType">
          <el-radio-group v-model="taskForm.monitorType">
            <el-radio :label="1">全部评论</el-radio>
            <el-radio :label="2">包含关键词</el-radio>
            <el-radio :label="3">排除关键词</el-radio>
          </el-radio-group>
        </el-form-item>
        
        <el-form-item label="关键词" prop="keywords" v-if="taskForm.monitorType !== 1">
          <el-input v-model="taskForm.keywords" type="textarea" rows="3" 
            placeholder="多个关键词用逗号分隔"></el-input>
        </el-form-item>
        
        <el-form-item label="语音播报" prop="voiceEnable">
          <el-switch v-model="taskForm.voiceEnable" active-text="开启" inactive-text="关闭"></el-switch>
        </el-form-item>
        
        <el-form-item label="语音类型" prop="voiceType" v-if="taskForm.voiceEnable">
          <el-select v-model="taskForm.voiceType" placeholder="请选择语音类型">
            <el-option label="女声" value="female"></el-option>
            <el-option label="男声" value="male"></el-option>
            <el-option label="童声" value="child"></el-option>
          </el-select>
        </el-form-item>
        
        <el-form-item label="自动回复" prop="autoReplyEnable">
          <el-switch v-model="taskForm.autoReplyEnable" active-text="开启" inactive-text="关闭"></el-switch>
        </el-form-item>
        
        <el-form-item label="回复内容" prop="replyContent" v-if="taskForm.autoReplyEnable">
          <el-input v-model="taskForm.replyContent" type="textarea" rows="3" 
            placeholder="请输入自动回复内容"></el-input>
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" @click="submitForm">提交</el-button>
          <el-button @click="resetForm">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useTaskStore } from '@/stores/task'
import { ElMessage } from 'element-plus'

const router = useRouter()
const taskStore = useTaskStore()
const formRef = ref(null)

const taskForm = reactive({
  name: '',
  roomId: '',
  monitorType: 1,
  keywords: '',
  voiceEnable: true,
  voiceType: 'female',
  autoReplyEnable: false,
  replyContent: ''
})

const taskRules = reactive({
  name: [
    { required: true, message: '请输入任务名称', trigger: 'blur' }
  ],
  roomId: [
    { required: true, message: '请输入直播间ID', trigger: 'blur' }
  ]
})

const resetForm = () => {
  formRef.value.resetFields()
}

const submitForm = () => {
  formRef.value.validate(async (valid) => {
    if (valid) {
      try {
        // 提交表单数据到API
        const result = await taskStore.createTask(taskForm)
        
        ElMessage.success('任务创建成功')
        router.push({ name: 'TaskList' })
      } catch (error) {
        console.error('创建任务失败:', error)
        ElMessage.error(error.message || '创建任务失败，请重试')
      }
    } else {
      console.log('表单验证失败')
      return false
    }
  })
}
</script>

<style scoped>
.task-create-container {
  padding: 20px;
}
</style>