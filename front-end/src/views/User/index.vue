<!--src/views/User/index.vue-->
<template>
  <div class="user-container">
    <h1 class="title" style="font-size: 36px">用户设置</h1>
    <el-tabs
      v-model="activeTab"
      class="custom-tabs-container"
      style="font-size: 18px"
    >
    <!-- Tab 1: 偏好管理 -->
    <el-tab-pane label="偏好管理" name="mask-management">
        <div class="tab-content">
          <el-card class="card dynamic-card">
            <h2>偏好管理</h2>
            <div class="mask-actions">
              <el-button type="primary" @click="addMaskDialogVisible = true"
                >添加新标签</el-button
              >
            </div>
            <el-table :data="masks" border style="margin-top: 20px">
              <el-table-column
                prop="name"
                label="名称"
                width="100"
              ></el-table-column>
              <el-table-column
                prop="description"
                label="描述"
                show-overflow-tooltip
              ></el-table-column>
              <!-- 新增标签列 -->
              <el-table-column prop="likes" label="标签"> </el-table-column>
              <el-table-column label="操作">
                <template #default="scope">
                  <!-- 按钮 -->
                  <el-icon
                    :size="20"
                    class="icon-edit"
                    @click="editMask(scope.$index)"
                  >
                    <Edit />
                  </el-icon>
                  <el-icon
                    :size="20"
                    class="icon-delete"
                    @click="deleteMask(scope.$index)"
                  >
                    <Delete />
                  </el-icon>
                  <el-icon
                    :size="20"
                    class="icon-search"
                    @click="searchMask(scope.$index)"
                  >
                    <Search />
                  </el-icon>
                </template>
              </el-table-column>
            </el-table>

            <!--增加 Mask 弹窗-->
            <el-dialog
              v-model="addMaskDialogVisible"
              title="添加偏好标签"
              width="600"
            >
              <el-form :model="newMask" label-width="100px">
                <el-form-item label="名称">
                  <el-input v-model="newMask.name"></el-input>
                </el-form-item>
                <el-form-item label="描述">
                  <el-input v-model="newMask.description"></el-input>
                </el-form-item>
                <!-- 喜欢的标签 -->
                <el-form-item label="喜欢的标签">
                  <div class="tag-input-wrapper">
                    <div class="tags">
                      <el-tag
                        v-for="(tag, index) in newMask.likes"
                        :key="'like-' + index"
                        closable
                        @close="removeTag('likes', index, true)"
                      >
                        {{ tag }}
                      </el-tag>
                      <el-input
                        v-model="newTagInput.likes"
                        placeholder="输入并按空格添加"
                        @keyup.space="addTag('likes', true)"
                        clearable
                        class="tag-input"
                        size="small"
                        maxlength="20"
                      ></el-input>
                    </div>
                  </div>
                </el-form-item>
                <!-- 不喜欢的标签 -->
                <el-form-item label="不喜欢的标签">
                  <div class="tag-input-wrapper">
                    <div class="tags">
                      <el-tag
                        v-for="(tag, index) in newMask.dislikes"
                        :key="'dislike-' + index"
                        closable
                        @close="removeTag('dislikes', index, true)"
                      >
                        {{ tag }}
                      </el-tag>
                      <el-input
                        v-model="newTagInput.dislikes"
                        placeholder="输入并按空格添加"
                        @keyup.space="addTag('dislikes', true)"
                        clearable
                        class="tag-input"
                        size="small"
                        maxlength="20"
                      ></el-input>
                    </div>
                  </div>
                </el-form-item>
              </el-form>
              <div slot="footer" class="dialog-footer">
                <el-button @click="addMaskDialogVisible = false"
                  >取消</el-button
                >
                <el-button type="primary" @click="addNewMask">保存</el-button>
              </div>
            </el-dialog>

            <!-- 编辑 Mask 弹窗 -->
            <el-dialog
              v-model="editMaskDialogVisible"
              title="编辑偏好标签"
              width="600"
            >
              <el-form :model="currentMask" label-width="100px">
                <el-form-item label="名称">
                  <el-input v-model="currentMask.name"></el-input>
                </el-form-item>
                <el-form-item label="描述">
                  <el-input v-model="currentMask.description"></el-input>
                </el-form-item>
                <!-- 喜欢的标签 -->
                <el-form-item label="喜欢的标签">
                  <div class="tag-input-wrapper">
                    <div class="tags">
                      <el-tag
                        v-for="(tag, index) in currentMask.likes"
                        :key="'edit-like-' + index"
                        closable
                        @close="removeTag('likes', index)"
                      >
                        {{ tag }}
                      </el-tag>
                      <el-input
                        v-model="newTagInput.likes"
                        placeholder="输入并按空格添加"
                        @keyup.space="addTag('likes')"
                        clearable
                        class="tag-input"
                        size="small"
                        maxlength="20"
                      ></el-input>
                    </div>
                  </div>
                </el-form-item>
                <!-- 不喜欢的标签 -->
                <el-form-item label="不喜欢的标签">
                  <div class="tag-input-wrapper">
                    <div class="tags">
                      <el-tag
                        v-for="(tag, index) in currentMask.dislikes"
                        :key="'edit-dislike-' + index"
                        closable
                        @close="removeTag('dislikes', index)"
                      >
                        {{ tag }}
                      </el-tag>
                      <el-input
                        v-model="newTagInput.dislikes"
                        placeholder="输入并按空格添加"
                        @keyup.space="addTag('dislikes')"
                        clearable
                        class="tag-input"
                        size="small"
                        maxlength="20"
                      ></el-input>
                    </div>
                  </div>
                </el-form-item>
              </el-form>
              <div slot="footer" class="dialog-footer">
                <el-button @click="editMaskDialogVisible = false"
                  >取消</el-button
                >
                <el-button type="primary" @click="saveMask">保存</el-button>
              </div>
            </el-dialog>
          </el-card>
        </div>
      </el-tab-pane>
      <!-- Tab 2: 修改密码 -->
      <el-tab-pane label="修改密码" name="change-password">
        <div class="tab-content">
          <el-card class="card fixed-card">
            <h2>修改密码</h2>
            <el-form
              :model="passwordForm"
              :rules="passwordRules"
              ref="passwordFormRef"
              label-width="120px"
            >
              <el-form-item label="当前密码" prop="currentPassword">
                <el-input
                  type="password"
                  v-model="passwordForm.currentPassword"
                  autocomplete="off"
                  show-password
                  placeholder="请输入当前密码"
                ></el-input>
              </el-form-item>
              <el-form-item label="新密码" prop="newPassword">
                <el-input
                  type="password"
                  v-model="passwordForm.newPassword"
                  autocomplete="off"
                  placeholder="请输入新密码"
                ></el-input>
              </el-form-item>
              <el-form-item label="确认新密码" prop="confirmPassword">
                <el-input
                  type="password"
                  v-model="passwordForm.confirmPassword"
                  autocomplete="off"
                  placeholder="请确认新密码"
                ></el-input>
              </el-form-item>
              <el-form-item>
                <el-button
                  type="primary"
                  :disabled="!passwordFormValid"
                  @click="submitPasswordForm"
                  >提交</el-button
                >
                <el-button @click="resetPasswordForm">重置</el-button>
              </el-form-item>
            </el-form>
          </el-card>
        </div>
      </el-tab-pane>

      <!-- Tab 3: 修改个人信息 -->
      <el-tab-pane label="个人信息" name="profile">
        <div class="tab-content">
          <el-card class="card fixed-card">
            <h2>修改个人信息</h2>
            <el-form
              :model="profileForm"
              ref="profileFormRef"
              label-width="120px"
            >
              <el-form-item label="用户名" prop="username">
                <el-input
                  v-model="profileForm.username"
                  placeholder="请输入用户名"
                ></el-input>
              </el-form-item>
              <el-form-item label="账号名" prop="email">
                <el-input
                  v-model="profileForm.account"
                  placeholder="请输入账号名"
                ></el-input>
              </el-form-item>
              <!-- <el-form-item label="电话号码" prop="phone">
                <el-input
                  v-model="profileForm.phone"
                  placeholder="请输入电话号码"
                ></el-input>
              </el-form-item> -->
              <el-form-item>
                <el-button
                  type="primary"
                  :disabled="!profileFormValid"
                  @click="submitProfileForm"
                  >保存更改</el-button
                >
              </el-form-item>
            </el-form>
          </el-card>
        </div>
      </el-tab-pane>

      
    </el-tabs>
  </div>
</template>

<script lang="ts">
import { computed, defineComponent, reactive, ref } from "vue";
import { ElMessage } from "element-plus";
import { Edit, Delete, Search } from "@element-plus/icons-vue";
import type { FormInstance } from "element-plus";
import {
  getUserInfo,
  getUserInfoModify,
  postAddMask,
  getUpdateMask,
  getDeleteMask,
  NewMaskData,
  MaskData,
  UserChangePwd,
  getUserInfoChangePwd,
} from "../../api/user.ts";
import router from "../../router";
import { SHA256 } from "crypto-js";

export default defineComponent({
  name: "User",
  components: {
    Edit,
    Delete,
    Search,
  },
  setup() {
    const activeTab = ref("mask-management");

    // 修改密码
    const passwordForm = reactive({
      currentPassword: "",
      newPassword: "",
      confirmPassword: "",
    });
    const passwordRules = {
      currentPassword: [
        { required: true, message: "请输入当前密码", trigger: "input" },
      ],
      newPassword: [
        { required: true, message: "请输入新密码", trigger: "input" },
      ],
      confirmPassword: [
        { required: true, message: "请确认新密码", trigger: "input" },
        {
          validator: (rule: any, value: string, callback: Function) => {
            if (value !== passwordForm.newPassword) {
              callback(new Error("两次输入密码不一致"));
            } else {
              callback();
            }
          },
        },
      ],
    };

    const passwordFormRef = ref<FormInstance | null>(null);

    const passwordFormValid = computed(() => {
      return (
        passwordForm.currentPassword &&
        passwordForm.newPassword &&
        passwordForm.confirmPassword
      );
    });

    const submitPasswordForm = async () => {
      if (passwordFormRef.value) {
        console.log(passwordForm);
        passwordFormRef.value.validate(async (valid) => {
          if (valid) {
            console.log(passwordForm);
            try {
              const data:UserChangePwd = {
                id: Number(localStorage.getItem("uid")),
                old_password: SHA256(passwordForm.currentPassword).toString(),
                new_password: SHA256(passwordForm.newPassword).toString(),
              };
              const response = await getUserInfoChangePwd(data);
              if (response.status === 200) {
                ElMessage.success("密码修改成功！");
              } else {
                ElMessage.error("密码修改失败，请重试！");
              }
            } catch (error) {
              ElMessage.error("密码修改失败，请重试！");
            }
          }
        });
      }
    };

    const resetPasswordForm = () => {
      Object.assign(passwordForm, {
        currentPassword: "",
        newPassword: "",
        confirmPassword: "",
      });
    };

    // 修改个人信息表单数据
    const profileForm = reactive({
      username: "",
      account: "",
    });

    const profileFormRef = ref<FormInstance | null>(null);

    const profileFormValid = computed(() => {
      return profileForm.username && profileForm.account
    });

    const submitProfileForm = async () => {
      if (profileFormRef.value) {
        profileFormRef.value.validate(async (valid) => {
          if (valid) {
            try {
              const updatedUser = {
                id: Number(localStorage.getItem("uid")),
                account: profileForm.account,
                name: profileForm.username,
              };
              await getUserInfoModify(updatedUser);
              ElMessage.success("个人信息保存成功！");
            } catch (error) {
              ElMessage.error("保存失败，请重试！");
            }
          }
        });
      }
    };

    // 偏好设置
    const preferencesForm = ref({
      themeColor: "light",
      notifications: true,
      language: "zh",
    });

    // 偏好管理
    const masks = ref<Array<MaskData>>([]);

    const editMaskDialogVisible = ref(false);
    const addMaskDialogVisible = ref(false);
    const newMask = ref<NewMaskData>({
      name: "",
      description: "",
      u_id: 1,
      likes: [],
      dislikes: [],
    });
    const currentMask = ref<MaskData>({
      id: 1,
      name: "",
      description: "",
      likes: [],
      dislikes: [],
    });

    const newTagInput = ref({
      likes: "",
      dislikes: "",
    });
    // 定义类型
    type TagType = "likes" | "dislikes";
    // 添加标签函数
    const addTag = (type: TagType, isNew: boolean = false): void => {
      const input = newTagInput.value[type].trim(); // 读取输入框内容
      if (!input) return; // 如果输入为空直接返回

      // 按空格分割输入并去除空白项
      const tags = input
        .split(/\s+/)
        .filter((tag) => tag && !newMask.value[type].includes(tag)); // 过滤掉空标签和已存在的标签

      // 将新标签添加到对应的数组
      if(isNew){
        newMask.value[type].push(...tags);
      }else{
        currentMask.value[type].push(...tags);
      }

      // 清空输入框
      newTagInput.value[type] = "";
    };

    // 移除标签函数
    const removeTag = (type: TagType, index: number, isNew: boolean = false): void => {
      if(isNew){
        newMask.value[type].splice(index, 1); // 根据索引删除对应的标签
      }else{
        currentMask.value[type].splice(index, 1); // 根据索引删除对应的标签
      }
    };

    const addNewMask = async () => {
      try {
        // 调用 API 提交数据
        newMask.value.u_id = Number(localStorage.getItem("uid"));
        const response = await postAddMask(newMask.value);
        if (response.status === 200) {
          ElMessage.success("新标签添加成功！");
          addMaskDialogVisible.value = false; // 关闭弹窗
          loadUserInfo();
        } else {
          ElMessage.error("添加失败");
        }
      } catch (error) {
        console.error("添加新标签失败:", error);
        ElMessage.error("添加新标签失败，请重试！");
      }
    };

    const editMask = (index: number) => {
      currentMask.value = masks.value[index];
      editMaskDialogVisible.value = true;
    };

    const deleteMask = async (index: number) => {
      try {
        const maskId = masks.value[index].id;
        await getDeleteMask(maskId);
        masks.value.splice(index, 1);
        ElMessage.success("标签已删除");
      } catch (error) {
        ElMessage.error("标签删除失败！");
      }
    };

    const saveMask = async () => {
      try {
        const response = await getUpdateMask(currentMask.value);
        if (response.status == 200) {
          console.log(response);
          ElMessage.success("标签更新成功！");
          editMaskDialogVisible.value = false;
          loadUserInfo();
        } else {
          console.error(response);
          ElMessage.error("标签更新失败！");
        }
      } catch (error) {
        ElMessage.error("标签保存失败！");
      }
    };

    // 操作：搜索标签
    const searchMask = (index: number) => {
      const mask = masks.value[index]; // 获取当前选中的 mask

      if (mask.id) {
        localStorage.setItem("mask_id", mask.id.toString()); // 保存当前 mask 的 ID 到 localStorage
        router.push({
          name: "Search", // 跳转到 Search 页面
        });
      } else {
        ElMessage.error("未找到该标签的 ID！");
      }
    };
    /*
  Search 页面接收参数
  import { useRoute } from 'vue-router';
  import { onMounted } from 'vue';

  export default {
    name: 'Search',
    setup() {
      const route = useRoute(); // 获取路由参数

      onMounted(() => {
        const maskId = route.query.maskId; // 读取 query 参数中的 maskId
        console.log('接收到的 Mask ID:', maskId);

        // 根据 maskId 执行相关逻辑，如获取详细数据
      });
    },
  };
  * */
    // 加载用户信息
    const loadUserInfo = async () => {
      try {
        const userId = Number(localStorage.getItem("uid")); // 假设用户 ID 是 1，可以动态获取
        const response = await getUserInfo(userId);
        profileForm.username = response.data.name;
        profileForm.account = response.data.account;
        masks.value = [];
        response.data.masks.forEach((mask) => {
          const newMaskData: MaskData = {
            id: mask.id,
            name: mask.name,
            description: mask.description,
            likes: mask.likes,
            dislikes: mask.dislikes,
          };
          masks.value.push(newMaskData);

        });
        ElMessage.success("用户信息加载成功！");
      } catch (error) {
        ElMessage.error("用户信息加载失败！");
      }
    };
    // 调用加载函数
    loadUserInfo();

    // // 加载mask信息
    // const loadMasks = async () => {
    //   try {
    //     const userId = 1; // 假设用户 ID 是 1，可以动态获取
    //     const response = await getUserInfo(userId);
    //     currentMasks.value= response.data.masks;
    //     ElMessage.success('偏好数据加载成功！');
    //   } catch (error) {
    //     ElMessage.error('偏好数据加载失败！');
    //   }
    // };

    // // 调用加载函数
    // loadMasks();

    return {
      activeTab,
      passwordForm,
      passwordRules,
      passwordFormValid,
      profileForm,
      preferencesForm,
      profileFormValid,
      masks,
      editMaskDialogVisible,
      addMaskDialogVisible,
      currentMask,
      newMask,
      removeTag,
      newTagInput,
      addTag,
      addNewMask,
      editMask,
      deleteMask,
      saveMask,
      submitPasswordForm,
      resetPasswordForm,
      submitProfileForm,
      searchMask,
      passwordFormRef,
      profileFormRef,
    };
  },
});
</script>

<style scoped>
.user-container::before {
  content: "";
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: url("../../assets/UserBackground.jpg") no-repeat center center
    fixed;
  background-size: cover;
  z-index: -1;
  pointer-events: none;
  opacity: 0.65;
}
/* 内部容器：内容容器 */
.user-container {
  display: flex; /* 启用 flex 布局 */
  flex-direction: column; /* 垂直排列内容 */
  align-items: center; /* 水平方向居中 */
  min-height: 100vh; /* 确保内容最小高度为视口高度 */
  box-sizing: border-box; /* 包括 padding */
  padding-top: 100px;
}

.title {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 20px;
  text-align: center;
}

/* 居中 el-tabs */
.custom-tabs-container {
  display: flex; /* 使用 flex 布局 */
  justify-content: center; /* 水平居中 */
  position: relative;
}

.custom-tabs-container /deep/ .el-tabs__nav {
  display: inline-flex;
  justify-content: center;
}

.tab-content {
  display: flex;
  justify-content: center; /* 居中对齐卡片内容 */
}

.card {
  width: 600px; /* 保证所有卡片的宽度一致 */
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  background-color: rgba(255, 255, 255, 0.9); /* 半透明白色 */
}

.fixed-card {
  width: 600px;
  position: relative;
}

.dynamic-card {
  min-width: 600px;
  min-height: 300px;
  padding: 20px;
  overflow: auto; /* 滚动处理 */
  position: relative;
}

.mask-actions {
  margin-bottom: 20px;
}

.dialog-footer {
  text-align: right;
}

.el-table .el-icon {
  display: inline-block;
  margin: 0 8px;
  vertical-align: middle;
}
.icon-edit {
  color: #409eff; /* Element Plus 的 primary 颜色 */
  cursor: pointer;
}
.icon-delete {
  color: #f56c6c; /* 红色，表示删除 */
  cursor: pointer;
}
.icon-search {
  color: #67c23a; /* 绿色，表示搜索 */
  cursor: pointer;
}

.el-icon:hover {
  color: #000000; /* 鼠标悬停颜色 */
  transform: scale(1.1); /* 轻微放大 */
  cursor: pointer;
}

::v-deep(.el-tabs__item.is-active) {
  font-size: 18px; /* 你可以根据需求调整大小 */
  font-weight: bold; /* 如果需要加粗 */
}
.tag-input-wrapper {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  padding: 5px;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
  flex-grow: 1;
}

.tag-input {
  flex-grow: 1;
  min-width: 120px;
  border: none;
}

.el-tag {
  margin-right: 5px;
}
</style>
