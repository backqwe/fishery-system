<template>
  <div class="login-page">
    <div class="login-bg">
      <!-- 背景装饰气泡 -->
      <div class="bubble" v-for="i in 8" :key="i" :class="`bubble-${i}`"></div>
    </div>

    <div class="login-container">
      <!-- Logo区域 -->
      <div class="login-logo">
        <div class="logo-icon">
          <el-icon size="48" color="#fff"><Setting /></el-icon>
        </div>
        <h1 class="system-title">精准渔业生产数据综合分析系统</h1>
        <p class="system-subtitle">Precision Fishery Production Data Analysis System</p>
      </div>

      <!-- 登录表单 -->
      <el-card class="login-card" shadow="always">
        <div class="card-header">
          <h2>用户登录</h2>
          <p>请输入您的账号信息</p>
        </div>

        <el-form
          ref="loginFormRef"
          :model="loginForm"
          :rules="loginRules"
          label-position="top"
          class="login-form"
          @keyup.enter="handleLogin"
        >
          <el-form-item prop="username">
            <el-input
              v-model="loginForm.username"
              placeholder="请输入用户名"
              size="large"
              clearable
            >
              <template #prefix>
                <el-icon><User /></el-icon>
              </template>
            </el-input>
          </el-form-item>

          <el-form-item prop="password">
            <el-input
              v-model="loginForm.password"
              type="password"
              placeholder="请输入密码"
              size="large"
              show-password
              clearable
            >
              <template #prefix>
                <el-icon><Lock /></el-icon>
              </template>
            </el-input>
          </el-form-item>

          <el-form-item prop="captcha">
            <div class="captcha-row">
              <el-input
                v-model="loginForm.captcha"
                placeholder="请输入验证码"
                size="large"
                clearable
                style="flex:1"
              >
                <template #prefix>
                  <el-icon><Key /></el-icon>
                </template>
              </el-input>
              <div class="captcha-img" @click="refreshCaptcha" title="点击刷新">
                <span class="captcha-text" :style="captchaStyle">{{ captchaCode }}</span>
              </div>
            </div>
          </el-form-item>

          <div class="login-options">
            <el-checkbox v-model="rememberMe">记住密码</el-checkbox>
            <a class="forget-pwd" href="javascript:void(0)">忘记密码?</a>
          </div>

          <el-button
            type="primary"
            size="large"
            class="login-btn"
            :loading="loading"
            @click="handleLogin"
          >
            <span v-if="!loading">登 录</span>
            <span v-else>登录中...</span>
          </el-button>
        </el-form>

        <div class="login-tip">
          <el-icon><InfoFilled /></el-icon>
          <!-- 演示提示：账号 admin / 密码 123456 / 验证码任意4位 -->
          演示账号：admin &nbsp;|&nbsp; 密码：123456 &nbsp;|&nbsp; 验证码：任意4位
        </div>
      </el-card>

      <div class="login-footer">
        Copyright © 2024 精准渔业生产数据综合分析系统 All Rights Reserved
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const router = useRouter()
const loginFormRef = ref(null)
const loading = ref(false)
const rememberMe = ref(false)

// 登录表单数据（Mock 演示数据）
const loginForm = reactive({
  username: 'admin',
  password: '123456',
  captcha: ''
})

// 表单验证规则
const loginRules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }, { min: 6, message: '密码长度不能少于6位', trigger: 'blur' }],
  captcha: [{ required: true, message: '请输入验证码', trigger: 'blur' }, { len: 4, message: '验证码为4位', trigger: 'blur' }]
}

// 随机生成验证码（Mock 前端验证码，仅作演示）
const captchaChars = 'ABCDEFGHJKLMNPQRSTUVWXYZabcdefghjkmnpqrstuvwxyz23456789'
const generateCaptcha = () => {
  let result = ''
  for (let i = 0; i < 4; i++) {
    result += captchaChars[Math.floor(Math.random() * captchaChars.length)]
  }
  return result
}
const captchaCode = ref(generateCaptcha())
const captchaColors = ['#1a6af7', '#0f9e68', '#e6740a', '#b027cc', '#c0392b']
const captchaStyle = computed(() => ({
  color: captchaColors[Math.floor(Math.random() * captchaColors.length)],
  letterSpacing: '4px',
  fontWeight: 'bold',
  fontSize: '20px',
  fontStyle: 'italic',
  userSelect: 'none'
}))

const refreshCaptcha = () => {
  captchaCode.value = generateCaptcha()
  loginForm.captcha = ''
}

// 登录处理（Mock 验证逻辑）
const handleLogin = () => {
  loginFormRef.value?.validate(async (valid) => {
    if (!valid) return
    // 验证码校验（大小写不敏感）
    if (loginForm.captcha.toLowerCase() !== captchaCode.value.toLowerCase()) {
      ElMessage.error('验证码错误，请重新输入')
      refreshCaptcha()
      return
    }
    loading.value = true
    // Mock 登录延迟
    await new Promise(resolve => setTimeout(resolve, 800))
    // Mock 账号验证：admin/123456 或任意用户名密码>=6位均可登录（演示用）
    if (loginForm.username === 'admin' && loginForm.password === '123456') {
      localStorage.setItem('fishery_token', 'mock_token_' + Date.now())
      localStorage.setItem('fishery_user', JSON.stringify({ name: '管理员', username: 'admin', role: '超级管理员' }))
      ElMessage.success('登录成功，欢迎回来！')
      router.push('/')
    } else {
      ElMessage.error('用户名或密码错误')
      refreshCaptcha()
    }
    loading.value = false
  })
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #0a1628 0%, #0d2b5e 30%, #1565c0 60%, #1976d2 80%, #0288d1 100%);
  position: relative;
  overflow: hidden;
}

/* 背景气泡动画 */
.login-bg {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.bubble {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.05);
  animation: float 8s ease-in-out infinite;
}
.bubble-1 { width: 300px; height: 300px; top: -80px; left: -80px; animation-delay: 0s; }
.bubble-2 { width: 180px; height: 180px; top: 20%; right: 5%; animation-delay: 1s; }
.bubble-3 { width: 120px; height: 120px; bottom: 10%; left: 10%; animation-delay: 2s; }
.bubble-4 { width: 80px; height: 80px; top: 40%; left: 3%; animation-delay: 3s; }
.bubble-5 { width: 250px; height: 250px; bottom: -60px; right: -60px; animation-delay: 1.5s; }
.bubble-6 { width: 60px; height: 60px; top: 60%; right: 20%; animation-delay: 4s; }
.bubble-7 { width: 160px; height: 160px; top: 5%; left: 30%; animation-delay: 2.5s; }
.bubble-8 { width: 100px; height: 100px; bottom: 20%; right: 30%; animation-delay: 0.5s; }

@keyframes float {
  0%, 100% { transform: translateY(0) scale(1); opacity: 0.05; }
  50% { transform: translateY(-20px) scale(1.05); opacity: 0.1; }
}

.login-container {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 24px;
  padding: 20px;
  width: 100%;
  max-width: 460px;
}

.login-logo {
  text-align: center;
  color: #fff;
}

.logo-icon {
  width: 80px;
  height: 80px;
  background: rgba(255,255,255,0.15);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 16px;
  backdrop-filter: blur(10px);
  border: 2px solid rgba(255,255,255,0.3);
}

.system-title {
  font-size: 22px;
  font-weight: bold;
  margin: 0 0 8px;
  text-shadow: 0 2px 10px rgba(0,0,0,0.3);
  letter-spacing: 1px;
}

.system-subtitle {
  font-size: 12px;
  opacity: 0.7;
  margin: 0;
  letter-spacing: 2px;
}

.login-card {
  width: 100%;
  border-radius: 16px;
  overflow: hidden;
  border: none;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4), 0 0 0 1px rgba(255,255,255,0.1);
}

.login-card :deep(.el-card__body) {
  padding: 36px 40px 28px;
}

.card-header {
  text-align: center;
  margin-bottom: 28px;
}
.card-header h2 {
  margin: 0 0 6px;
  font-size: 22px;
  color: #1a3a6e;
  font-weight: 700;
}
.card-header p {
  margin: 0;
  font-size: 13px;
  color: #888;
}

.login-form :deep(.el-form-item) {
  margin-bottom: 18px;
}
.login-form :deep(.el-input__wrapper) {
  border-radius: 8px;
  height: 44px;
}

.captcha-row {
  display: flex;
  gap: 12px;
  align-items: center;
  width: 100%;
}

.captcha-img {
  width: 120px;
  height: 44px;
  background: linear-gradient(135deg, #e8f0fe, #f0f4ff);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  border: 1px solid #dce3f0;
  flex-shrink: 0;
  transition: all 0.2s;
  overflow: hidden;
}
.captcha-img:hover {
  border-color: #409eff;
  box-shadow: 0 0 0 2px rgba(64,158,255,0.2);
}
.captcha-text {
  font-size: 20px;
  font-weight: bold;
  font-style: italic;
  letter-spacing: 4px;
  user-select: none;
  filter: blur(0.3px);
}

.login-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  margin-top: -4px;
}

.forget-pwd {
  font-size: 13px;
  color: #409eff;
  text-decoration: none;
}
.forget-pwd:hover { text-decoration: underline; }

.login-btn {
  width: 100%;
  height: 46px;
  font-size: 16px;
  border-radius: 8px;
  background: linear-gradient(135deg, #1565c0, #0288d1);
  border: none;
  letter-spacing: 4px;
}
.login-btn:hover {
  background: linear-gradient(135deg, #1976d2, #039be5);
}

.login-tip {
  margin-top: 16px;
  padding: 10px 14px;
  background: #f0f7ff;
  border-radius: 6px;
  font-size: 12px;
  color: #5a7aaa;
  display: flex;
  align-items: center;
  gap: 6px;
  line-height: 1.5;
}

.login-footer {
  color: rgba(255,255,255,0.5);
  font-size: 12px;
  text-align: center;
  margin-top: 8px;
}
</style>
