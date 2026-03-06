<template>
  <div class="pond-form">
    <el-card shadow="never">
      <template #header>
        <div class="card-header">
          <span class="title">新增鱼塘</span>
          <el-button @click="$router.push('/pond/list')" link>
            <el-icon><ArrowLeft /></el-icon>返回列表
          </el-button>
        </div>
      </template>

      <el-form :model="form" :rules="rules" ref="formRef" label-width="120px" class="form-body">
        <el-row :gutter="24">
          <el-col :span="12">
            <el-form-item label="鱼塘名称" prop="name">
              <el-input v-model="form.name" placeholder="请输入鱼塘名称" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="类型" prop="type">
              <el-select v-model="form.type" placeholder="请选择类型" style="width:100%">
                <el-option label="草鱼塘" value="草鱼塘" />
                <el-option label="鲤鱼塘" value="鲤鱼塘" />
                <el-option label="鲫鱼塘" value="鲫鱼塘" />
                <el-option label="鲈鱼塘" value="鲈鱼塘" />
                <el-option label="鲢鱼塘" value="鲢鱼塘" />
                <el-option label="混养塘" value="混养塘" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="面积(亩)" prop="area">
              <el-input-number v-model="form.area" :min="0.1" :max="1000" :precision="1" style="width:100%" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="水深(m)" prop="depth">
              <el-input-number v-model="form.depth" :min="0.5" :max="10" :precision="1" style="width:100%" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="位置" prop="location">
              <el-input v-model="form.location" placeholder="如：东区A-01" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="负责人" prop="manager">
              <el-select v-model="form.manager" placeholder="请选择负责人" style="width:100%">
                <el-option label="张三" value="张三" />
                <el-option label="李四" value="李四" />
                <el-option label="王五" value="王五" />
                <el-option label="赵六" value="赵六" />
                <el-option label="钱七" value="钱七" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="24">
            <el-form-item label="备注">
              <el-input v-model="form.remark" type="textarea" :rows="3" placeholder="请输入备注信息（选填）" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item>
          <el-button type="primary" @click="handleSubmit" :loading="submitting">保存</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const router = useRouter()
const formRef = ref(null)
const submitting = ref(false)

const form = ref({
  name: '',
  type: '',
  area: 5.0,
  depth: 2.0,
  location: '',
  manager: '',
  remark: ''
})

const rules = {
  name: [{ required: true, message: '请输入鱼塘名称', trigger: 'blur' }],
  type: [{ required: true, message: '请选择类型', trigger: 'change' }],
  area: [{ required: true, message: '请输入面积', trigger: 'blur' }],
  depth: [{ required: true, message: '请输入水深', trigger: 'blur' }],
  location: [{ required: true, message: '请输入位置', trigger: 'blur' }],
  manager: [{ required: true, message: '请选择负责人', trigger: 'change' }]
}

const handleSubmit = async () => {
  await formRef.value.validate()
  submitting.value = true
  setTimeout(() => {
    submitting.value = false
    ElMessage.success('鱼塘信息保存成功！')
    router.push('/pond/list')
  }, 800)
}

const handleReset = () => {
  formRef.value.resetFields()
}
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.title {
  font-size: 16px;
  font-weight: 600;
}
.form-body {
  max-width: 900px;
  margin-top: 8px;
}
</style>
