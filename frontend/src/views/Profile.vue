<!-- src/views/Profile.vue -->
<template>
  <div class="profile-container">
    <el-card>
      <template #header>
        <div class="clearfix">
          <span>个人信息</span>
        </div>
      </template>
      
      <el-form :model="userInfo" label-width="120px" v-if="userInfo.username">
        <el-form-item label="用户名">
          <el-input v-model="userInfo.username" disabled></el-input>
        </el-form-item>
        
        <el-form-item label="昵称">
          <el-input v-model="userInfo.nickname"></el-input>
        </el-form-item>
        
        <el-form-item label="邮箱">
          <el-input v-model="userInfo.email"></el-input>
        </el-form-item>
        
        <el-form-item label="头像">
          <el-upload
            class="avatar-uploader"
            action="https://jsonplaceholder.typicode.com/posts/"
            :show-file-list="false"
            :on-success="handleAvatarSuccess"
            :before-upload="beforeAvatarUpload">
            <img v-if="userInfo.avatarUrl" :src="userInfo.avatarUrl" class="avatar">
            <i v-else class="el-icon-plus avatar-uploader-icon"></i>
          </el-upload>
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" @click="saveProfile">保存</el-button>
          <el-button @click="resetProfile">重置</el-button>
        </el-form-item>
      </el-form>
      
      <div v-else class="loading-text">
        加载中...
      </div>
    </el-card>
    
    <el-card class="mt-20">
      <template #header>
        <div class="clearfix">
          <span>修改密码</span>
        </div>
      </template>
      
      <el-form :model="passwordForm" :rules="passwordRules" ref="passwordFormRef" label-width="120px">
        <el-form-item label="当前密码" prop="oldPassword">
          <el-input type="password" v-model="passwordForm.oldPassword"></el-input>
        </el-form-item>
        
        <el-form-item label="新密码" prop="newPassword">
          <el-input type="password" v-model="passwordForm.newPassword"></el-input>
        </el-form-item>
        
        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input type="password" v-model="passwordForm.confirmPassword"></el-input>
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" @click="changePassword">修改</el-button>
          <el-button @click="resetPasswordForm">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, toRefs } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { ElMessage } from 'element-plus'

const authStore = useAuthStore()

const userInfo = reactive({
  username: '',
  nickname: '',
  email: '',
  avatarUrl: 'https://picsum.photos/200/200' // 默认头像
})

const originalUserInfo = reactive({})

const passwordForm = reactive({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
})

const passwordRules = reactive({
  oldPassword: [
    { required: true, message: '请输入当前密码', trigger: 'blur' }
  ],
  newPassword: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度在 6 到 20 个字符', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认新密码', trigger: 'blur' },
    { validator: (rule, value) => {
        if (value !== passwordForm.newPassword) {
          return new Error('两次输入的密码不一致')
        }
        return true
      }, trigger: 'blur' }
  ]
})

const passwordFormRef = ref(null)

const fetchUserInfo = async () => {
  try {
    // 实际项目中应调用API获取用户信息
    // 这里使用模拟数据
    const mockUserInfo = {
      username: authStore.user.username,
      nickname: 'Doubao User',
      email: 'user@example.com',
      avatarUrl: 'https://picsum.photos/200/200'
    }
    
    Object.assign(userInfo, mockUserInfo)
    Object.assign(originalUserInfo, mockUserInfo)
  } catch (error) {
    console.error('获取用户信息失败:', error)
    ElMessage.error(error.message || '获取用户信息失败')
  }
}

const saveProfile = async () => {
  try {
    // 实际项目中应调用API保存用户信息
    console.log('保存用户信息:', userInfo)
    
    // 模拟保存成功
    await new Promise(resolve => setTimeout(resolve, 500))
    
    Object.assign(originalUserInfo, userInfo)
    ElMessage.success('个人信息保存成功')
  } catch (error) {
    console.error('保存用户信息失败:', error)
    ElMessage.error(error.message || '保存用户信息失败')
  }
}

const resetProfile = () => {
  Object.assign(userInfo, originalUserInfo)
}

const changePassword = () => {
  passwordFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        // 实际项目中应调用API修改密码
        console.log('修改密码:', passwordForm)
        
        // 模拟修改成功
        await new Promise(resolve => setTimeout(resolve, 500))
        
        resetPasswordForm()
        ElMessage.success('密码修改成功')
      } catch (error) {
        console.error('修改密码失败:', error)
        ElMessage.error(error.message || '修改密码失败')
      }
    } else {
      console.log('表单验证失败')
      return false
    }
  })
}

const resetPasswordForm = () => {
  passwordFormRef.value.resetFields()
}

const handleAvatarSuccess = (res, file) => {
  userInfo.avatarUrl = URL.createObjectURL(file.raw)
}

const beforeAvatarUpload = (file) => {
  const isJpgOrPng = file.type === 'image/jpeg' || file.type === 'image/png'
  if (!isJpgOrPng) {
    ElMessage.error('请上传JPG/PNG格式的图片')
    return false
  }
  
  const isLt2M = file.size / 1024 / 1024 < 2
  if (!isLt2M) {
    ElMessage.error('图片大小不能超过2MB')
    return false
  }
  
  return true
}

onMounted(() => {
  fetchUserInfo()
})
</script>

<style scoped>
.profile-container {
  padding: 20px;
}

.mt-20 {
  margin-top: 20px;
}

.loading-text {
  text-align: center;
  padding: 20px;
}

.avatar-uploader .el-upload {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

.avatar-uploader .el-upload:hover {
  border-color: #409EFF;
}

.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 178px;
  height: 178px;
  line-height: 178px;
  text-align: center;
}

.avatar {
  width: 178px;
  height: 178px;
  display: block;
}
</style>