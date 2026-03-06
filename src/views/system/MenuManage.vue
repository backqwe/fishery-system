<template>
  <div class="menu-manage">
    <el-card shadow="never">
      <template #header>
        <div class="card-header">
          <span class="title">菜单管理</span>
          <el-button type="primary" @click="openAddDialog(null)">
            <el-icon><Plus /></el-icon>新增菜单
          </el-button>
        </div>
      </template>

      <!-- 工具栏 -->
      <div class="toolbar">
        <el-input v-model="filterText" placeholder="搜索菜单名称" clearable style="width:220px">
          <template #prefix><el-icon><Search /></el-icon></template>
        </el-input>
        <div>
          <el-button @click="expandAll">展开全部</el-button>
          <el-button @click="collapseAll">收起全部</el-button>
        </div>
      </div>

      <!-- 树形表格 -->
      <!-- Mock 菜单数据：树形结构，包含系统管理、基础信息管理等模块 -->
      <el-table
        ref="tableRef"
        :data="filteredMenuTree"
        row-key="id"
        :tree-props="{ children: 'children', hasChildren: 'hasChildren' }"
        :default-expand-all="defaultExpand"
        border
        stripe
        style="width:100%"
      >
        <el-table-column prop="name" label="菜单名称" min-width="180">
          <template #default="{ row }">
            <el-icon v-if="row.icon" style="vertical-align:-2px;margin-right:4px">
              <component :is="row.icon" />
            </el-icon>
            {{ row.name }}
          </template>
        </el-table-column>
        <el-table-column prop="type" label="类型" width="90" align="center">
          <template #default="{ row }">
            <el-tag :type="row.type === '目录' ? '' : row.type === '菜单' ? 'success' : 'info'" size="small">
              {{ row.type }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="path" label="路由地址" min-width="180" />
        <el-table-column prop="component" label="组件路径" min-width="200" />
        <el-table-column prop="permission" label="权限标识" min-width="180" />
        <el-table-column prop="sort" label="排序" width="70" align="center" />
        <el-table-column prop="status" label="状态" width="80" align="center">
          <template #default="{ row }">
            <el-switch v-model="row.statusBool" size="small" @change="toggleStatus(row)" />
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180" align="center" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="openAddDialog(row)">新增子项</el-button>
            <el-button type="warning" link size="small" @click="openEditDialog(row)">编辑</el-button>
            <el-button type="danger" link size="small" @click="deleteMenu(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 新增/编辑弹窗 -->
    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="560px" destroy-on-close>
      <el-form :model="form" :rules="rules" ref="formRef" label-width="100px">
        <el-form-item label="上级菜单" prop="parentId">
          <el-tree-select
            v-model="form.parentId"
            :data="treeSelectData"
            :props="{ label: 'name', value: 'id', children: 'children' }"
            placeholder="顶级菜单"
            clearable
            style="width:100%"
          />
        </el-form-item>
        <el-form-item label="菜单类型" prop="type">
          <el-radio-group v-model="form.type">
            <el-radio label="目录">目录</el-radio>
            <el-radio label="菜单">菜单</el-radio>
            <el-radio label="按钮">按钮</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="菜单名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入菜单名称" />
        </el-form-item>
        <el-form-item label="菜单图标" prop="icon" v-if="form.type !== '按钮'">
          <el-input v-model="form.icon" placeholder="Element Plus 图标名称，如 House" />
        </el-form-item>
        <el-form-item label="路由地址" prop="path" v-if="form.type !== '按钮'">
          <el-input v-model="form.path" placeholder="如 /system/user" />
        </el-form-item>
        <el-form-item label="组件路径" prop="component" v-if="form.type === '菜单'">
          <el-input v-model="form.component" placeholder="如 views/system/UserManage" />
        </el-form-item>
        <el-form-item label="权限标识" prop="permission">
          <el-input v-model="form.permission" placeholder="如 system:user:list" />
        </el-form-item>
        <el-form-item label="显示排序" prop="sort">
          <el-input-number v-model="form.sort" :min="1" :max="999" controls-position="right" />
        </el-form-item>
        <el-form-item label="菜单状态" prop="status">
          <el-radio-group v-model="form.statusBool">
            <el-radio :label="true">启用</el-radio>
            <el-radio :label="false">禁用</el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitForm">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

// ===================== Mock 菜单数据 =====================
const menuList = ref([
  {
    id: 1, name: '实时监测', type: '目录', icon: 'Monitor', path: '/monitor', component: '', permission: '', sort: 1, statusBool: true,
    children: [
      { id: 11, name: '实时监测数据', type: '菜单', icon: 'DataAnalysis', path: '/monitor/realtime', component: 'views/monitor/RealtimeMonitor', permission: 'monitor:realtime:list', sort: 1, statusBool: true, children: [] }
    ]
  },
  {
    id: 2, name: '系统管理', type: '目录', icon: 'Setting', path: '/system', component: '', permission: '', sort: 2, statusBool: true,
    children: [
      { id: 21, name: '用户管理', type: '菜单', icon: 'User', path: '/system/user', component: 'views/system/UserManage', permission: 'system:user:list', sort: 1, statusBool: true, children: [] },
      { id: 22, name: '角色管理', type: '菜单', icon: 'UserFilled', path: '/system/role', component: 'views/system/RoleManage', permission: 'system:role:list', sort: 2, statusBool: true, children: [] },
      { id: 23, name: '菜单管理', type: '菜单', icon: 'Menu', path: '/system/menu', component: 'views/system/MenuManage', permission: 'system:menu:list', sort: 3, statusBool: true, children: [] },
      { id: 24, name: '生物类别设置', type: '菜单', icon: 'Fish', path: '/system/bio-category', component: 'views/system/BioCategory', permission: 'system:bio:list', sort: 4, statusBool: true, children: [] },
      { id: 25, name: '报警值设置', type: '菜单', icon: 'Bell', path: '/system/alarm-setting', component: 'views/system/AlarmSetting', permission: 'system:alarm:list', sort: 5, statusBool: true, children: [] },
    ]
  },
  {
    id: 3, name: '基础信息管理', type: '目录', icon: 'Grid', path: '/info', component: '', permission: '', sort: 3, statusBool: true,
    children: [
      { id: 31, name: '养殖场管理', type: '菜单', icon: 'OfficeBuilding', path: '/info/farm', component: 'views/info/FarmManage', permission: 'info:farm:list', sort: 1, statusBool: true, children: [] },
      { id: 32, name: '车间管理', type: '菜单', icon: 'House', path: '/info/workshop', component: 'views/info/WorkshopManage', permission: 'info:workshop:list', sort: 2, statusBool: true, children: [] },
      { id: 33, name: '池塘管理', type: '菜单', icon: 'Watermelon', path: '/info/pond', component: 'views/info/PondManage', permission: 'info:pond:list', sort: 3, statusBool: true, children: [] },
      { id: 34, name: '监测点管理', type: '菜单', icon: 'LocationFilled', path: '/info/monitor-point', component: 'views/info/MonitorPointManage', permission: 'info:point:list', sort: 4, statusBool: true, children: [] },
      { id: 35, name: '设备管理', type: '菜单', icon: 'Cpu', path: '/info/equipment', component: 'views/info/EquipmentManage', permission: 'info:equipment:list', sort: 5, statusBool: true, children: [] },
    ]
  },
  {
    id: 4, name: '历史监测数据', type: '菜单', icon: 'Clock', path: '/history', component: 'views/history/HistoryData', permission: 'history:data:list', sort: 4, statusBool: true, children: []
  },
  {
    id: 5, name: '水质预测数据', type: '菜单', icon: 'TrendCharts', path: '/prediction', component: 'views/prediction/WaterPrediction', permission: 'prediction:data:list', sort: 5, statusBool: true, children: []
  }
])

const filterText = ref('')
const defaultExpand = ref(true)
const tableRef = ref(null)

const filteredMenuTree = computed(() => {
  if (!filterText.value) return menuList.value
  const filter = filterText.value.toLowerCase()
  const filterTree = (nodes) => {
    return nodes.filter(node => {
      const match = node.name.toLowerCase().includes(filter)
      if (node.children?.length) {
        node.children = filterTree(node.children)
        return match || node.children.length > 0
      }
      return match
    })
  }
  return filterTree(JSON.parse(JSON.stringify(menuList.value)))
})

const treeSelectData = computed(() => [{ id: 0, name: '顶级菜单', children: menuList.value }])

// 展开收起
const expandAll = () => { defaultExpand.value = true }
const collapseAll = () => { defaultExpand.value = false }

// 弹窗
const dialogVisible = ref(false)
const dialogTitle = ref('新增菜单')
const formRef = ref(null)
let editId = null
const form = reactive({ parentId: null, type: '菜单', name: '', icon: '', path: '', component: '', permission: '', sort: 1, statusBool: true })
const rules = {
  name: [{ required: true, message: '请输入菜单名称', trigger: 'blur' }],
  type: [{ required: true, message: '请选择类型', trigger: 'change' }]
}

const openAddDialog = (parent) => {
  editId = null
  Object.assign(form, { parentId: parent?.id || null, type: '菜单', name: '', icon: '', path: '', component: '', permission: '', sort: 1, statusBool: true })
  dialogTitle.value = parent ? `新增子菜单（${parent.name}）` : '新增菜单'
  dialogVisible.value = true
}

const openEditDialog = (row) => {
  editId = row.id
  Object.assign(form, { ...row })
  dialogTitle.value = '编辑菜单'
  dialogVisible.value = true
}

const submitForm = () => {
  formRef.value?.validate(valid => {
    if (!valid) return
    if (editId) {
      ElMessage.success('菜单信息已更新（Mock）')
    } else {
      ElMessage.success('菜单新增成功（Mock）')
    }
    dialogVisible.value = false
  })
}

const deleteMenu = (row) => {
  ElMessageBox.confirm(`确认删除菜单 "${row.name}"？`, '提示', { type: 'warning' }).then(() => {
    ElMessage.success('删除成功（Mock）')
  }).catch(() => {})
}

const toggleStatus = (row) => {
  ElMessage.success(`菜单 "${row.name}" 状态已${row.statusBool ? '启用' : '禁用'}（Mock）`)
}
</script>

<style scoped>
.menu-manage {}
.card-header { display: flex; align-items: center; justify-content: space-between; }
.title { font-size: 16px; font-weight: 600; }
.toolbar { display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px; flex-wrap: wrap; gap: 8px; }
</style>
