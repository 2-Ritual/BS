<template>
  <div class="login-container">
    <el-tabs
      v-model="activeTab"
      class="custom-tabs-container"
      style="font-size: 18px"
    >
      <!-- 登录 Tab -->
      <el-tab-pane label="登录" name="login">
        <el-card class="login-card" shadow="hover">
          <h2 class="title">用户登录</h2>
          <el-form
            :model="loginForm"
            :rules="loginRules"
            ref="loginFormRef"
            label-width="100px"
          >
            <!-- 用户名 -->
            <el-form-item label="用户名" prop="username">
              <el-input
                v-model="loginForm.username"
                placeholder="请输入用户名"
              ></el-input>
            </el-form-item>

            <!-- 密码 -->
            <el-form-item label="密码" prop="password">
              <el-input
                v-model="loginForm.password"
                placeholder="请输入密码"
                show-password
                type="password"
              ></el-input>
            </el-form-item>

            <!-- 登录按钮 -->
            <el-form-item>
              <el-button type="primary" @click="submitLogin">登录</el-button>
              <el-button @click="forgetVisible = true">忘记密码</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-tab-pane>

      <!-- 注册 Tab -->
      <el-tab-pane label="注册" name="register">
        <el-card class="login-card" shadow="hover">
          <h2 class="title">用户注册</h2>

          <!-- 注册第一步：验证邮箱和验证码 -->
          <template v-if="!verificationRegisterPassed">
            <el-form
              :model="verifyForm"
              :rules="verifyRules"
              ref="verifyFormRef"
              label-width="100px"
            >
              <!-- 邮箱 -->
              <el-form-item label="邮箱" prop="email">
                <el-input v-model="verifyForm.email" placeholder="请输入邮箱">
                  <template #append>
                    <el-button type="primary" @click="getCode(verifyForm.email)"
                      >获取验证码</el-button
                    >
                  </template>
                </el-input>
              </el-form-item>

              <!-- 验证码 -->
              <el-form-item label="验证码" prop="verification">
                <el-input
                  v-model="verifyForm.verification"
                  placeholder="请输入验证码"
                ></el-input>
              </el-form-item>

              <!-- 验证按钮 -->
              <el-form-item>
                <el-button type="primary" @click="verifyRegisterCode">验证</el-button>
              </el-form-item>
            </el-form>
          </template>

          <!-- 注册第二步：填写注册信息 -->
          <template v-else>
            <el-form
              :model="registerForm"
              :rules="registerRules"
              ref="registerFormRef"
              label-width="100px"
            >
              <!-- 用户名 -->
              <el-form-item label="用户名" prop="username">
                <el-input
                  v-model="registerForm.username"
                  placeholder="请输入用户名"
                ></el-input>
              </el-form-item>

              <!-- 密码 -->
              <el-form-item label="密码" prop="password">
                <el-input
                  v-model="registerForm.password"
                  placeholder="请输入密码"
                  show-password
                  type="password"
                ></el-input>
              </el-form-item>

              <!-- 确认密码 -->
              <el-form-item label="确认密码" prop="confirmPassword">
                <el-input
                  v-model="registerForm.confirmPassword"
                  placeholder="请再次输入密码"
                  show-password
                  type="password"
                ></el-input>
              </el-form-item>

              <!-- 注册按钮 -->
              <el-form-item>
                <el-button type="primary" @click="submitRegister"
                  >注册</el-button
                >
              </el-form-item>
            </el-form>
          </template>
        </el-card>
      </el-tab-pane>
    </el-tabs>

    <!-- 忘记密码弹窗 -->
  <el-dialog v-model="forgetVisible" title="找回密码" width="600">
    <el-form
      :model="forgetForm"
      :rules="forgetRules"
      ref="forgetFormRef"
      label-width="100px"
    >
      <!-- 邮箱 -->
      <el-form-item label="邮箱" prop="email">
        <el-input v-model="forgetForm.email" placeholder="请输入邮箱">
          <template #append>
            <el-button
              type="primary"
              @click="getCode(forgetForm.email)"
            >
              获取验证码
            </el-button>
          </template>
        </el-input>
      </el-form-item>

      <!-- 验证码 -->
      <el-form-item label="验证码" prop="verification">
        <el-input
          v-model="forgetForm.verification"
          placeholder="请输入验证码"
        ></el-input>
        <el-button
          type="primary"
          size="mini"
          style="margin-top: 10px"
          @click="verifyPwdCode"
          :disabled="isVerified"
        >
          验证
        </el-button>
        <span v-if="isVerified" style="color: green; margin-left: 10px">
          验证成功
        </span>
      </el-form-item>

      <!-- 新密码 -->
      <el-form-item v-if="isVerified" label="新密码" prop="password">
        <el-input
          v-model="forgetForm.password"
          placeholder="请输入新密码"
          show-password
          type="password"
        ></el-input>
      </el-form-item>
    </el-form>
    <div style="text-align: right; margin-top: 20px">
      <el-button @click="forgetVisible = false">取消</el-button>
      <el-button type="primary" @click="submitForgetPassword">确认</el-button>
    </div>
  </el-dialog>
  </div>
</template>

<script lang="ts">
import { ref, reactive } from "vue";
import { ElMessage, type FormInstance } from "element-plus";
import {
  getUserLoginJudge,
  UserLoginResponse,
  UserLoginData,
  getUserRegisterJudge,
  postUserVerificationSent,
  getUserVerificationJudge,
  UserRegisterVerification,
  postUserPasswordReset,
  UserResetPasswordData,
} from "../../api/login";
import SHA256 from "crypto-js/sha256";
import router from "../../router";
import emitter from "../../eventBus/EventBus";

export default {
  name: "Login",
  setup() {
    const activeTab = ref("login");

    // 登录表单
    const loginForm = reactive({
      username: "",
      password: "",
    });

    // 验证表单（第一步）
    const verifyForm = reactive({
      email: "",
      verification: "",
    });

    // 注册表单（第二步）
    const registerForm = reactive({
      username: "",
      password: "",
      confirmPassword: "",
    });

    // 忘记密码表单
    const forgetForm = reactive({
      email: "",
      verification: "",
      password: "",
    });

    // 注册验证通过标识
    const verificationRegisterPassed = ref(false);

    // 定义非法字符正则表达式
    const illegalCharPattern = /[^\w!@#$%^&*()_+=-]/; // 示例：仅允许字母、数字及常用特殊字符

    // 表单校验规则
    const loginRules = {
      username: [{ required: true, message: "请输入用户名", trigger: "blur" }],
      password: [
        { required: true, message: "请输入密码", trigger: "blur" },
        {
          validator: (rule: any, value: string, callback: any) => {
            if (illegalCharPattern.test(value)) {
              callback(new Error("密码不能包含非法字符"));
            } else {
              callback();
            }
          },
          trigger: "blur",
        },
      ],
    };

    const verifyRules = {
      email: [{ required: true, message: "请输入邮箱", trigger: "blur" }],
      verification: [
        { required: true, message: "请输入验证码", trigger: "blur" },
      ],
    };

    const registerRules = {
      username: [{ required: true, message: "请输入用户名", trigger: "blur" }],
      password: [
        { required: true, message: "请输入密码", trigger: "blur" },
        {
          validator: (rule: any, value: string, callback: any) => {
            if (illegalCharPattern.test(value)) {
              callback(new Error("密码不能包含非法字符"));
            } else {
              callback();
            }
          },
          trigger: "blur",
        },
      ],
      confirmPassword: [
        { required: true, message: "请确认密码", trigger: "blur" },
        {
          validator: (rule: any, value: string, callback: any) => {
            if (value !== registerForm.password) {
              callback(new Error("两次输入密码不一致"));
            } else if (illegalCharPattern.test(value)) {
              callback(new Error("密码不能包含非法字符"));
            } else {
              callback();
            }
          },
          trigger: "blur",
        },
      ],
    };

    const forgetRules = {
      email: [{ required: true, message: "请输入邮箱", trigger: "blur" }],
      verification: [
        { required: true, message: "请输入验证码", trigger: "blur" },
      ],
      password: [
        { required: true, message: "请输入新密码", trigger: "blur" },
        {
          validator: (rule: any, value: string, callback: any) => {
            if (illegalCharPattern.test(value)) {
              callback(new Error("密码不能包含非法字符"));
            } else {
              callback();
            }
          },
          trigger: "blur",
        },
      ],
    };

    // 表单引用
    const loginFormRef = ref<FormInstance | null>(null);
    const verifyFormRef = ref<FormInstance | null>(null);
    const registerFormRef = ref<FormInstance | null>(null);
    const forgetFormRef = ref<FormInstance | null>(null);

    // 登录处理
    const submitLogin = () => {
      if (loginFormRef.value) {
        loginFormRef.value.validate(async (valid: boolean) => {
          if (!valid) return;
          const loginData: UserLoginData = {
            account: loginForm.username,
            password: SHA256(loginForm.password).toString(),
          };

          try {
            const response = await getUserLoginJudge(loginData);
            if (response.status === 200) {
              const userLoginResponse: UserLoginResponse = response.data;
              localStorage.setItem("uid", String(userLoginResponse.id));
              emitter.emit("login");
              router.push({ name: "User" });
            } else {
              ElMessage.error("用户名或密码错误");
            }
          } catch (error) {
            ElMessage.error("登录失败，请稍后重试");
          }
          // 登录逻辑省略
        });
      }
    };

    // 获取验证码
    const getCode = (email: string) => {
      if (!email) {
        ElMessage.error("请先输入邮箱");
        return;
      }
      postUserVerificationSent(email);
    };

    // 验证验证码
    const verifyRegisterCode = () => {
      if (verifyFormRef.value) {
        verifyFormRef.value.validate(async (valid: boolean) => {
          if (!valid) return;

          try {
            const response = await getUserVerificationJudge(verifyForm);
            if (response.status === 200) {
              ElMessage.success("验证成功");
              verificationRegisterPassed.value = true;
            } else {
              ElMessage.error("验证码错误或已过期");
            }
          } catch (error) {
            ElMessage.error("验证失败，请稍后重试");
          }
        });
      }
    };

    const isVerified = ref(false);
    // 验证验证码
    const verifyPwdCode = () => {
      if (forgetFormRef.value) {
        forgetFormRef.value.validate(async (valid: boolean) => {
          if (!valid) return;

          try {
            const data:UserRegisterVerification = {
              email: forgetForm.email,
              verification: forgetForm.verification,
            }
            const response = await getUserVerificationJudge(data);
            if (response.status === 200) {
              ElMessage.success("验证成功");
              isVerified.value = true;
            } else {
              ElMessage.error("验证码错误或已过期");
            }
          } catch (error) {
            ElMessage.error("验证失败，请稍后重试");
          }
        });
      }
    };
    // 注册处理
    const submitRegister = () => {
      if (registerFormRef.value) {
        registerFormRef.value.validate(async (valid: boolean) => {
          if (!valid) return;

          const registerData = {
            email: verifyForm.email,
            name: registerForm.username,
            account: registerForm.username,
            password: SHA256(registerForm.password).toString(),
          };

          try {
            const response = await getUserRegisterJudge(registerData);
            if (response.status !== 200) {
              ElMessage.error(response.data);
              return;
            }
            ElMessage.success("注册成功，请登录");
            activeTab.value = "login";
          } catch (error) {
            ElMessage.error("注册失败，请稍后重试");
          }
        });
      }
    };

    const forgetVisible = ref(false);

    // 忘记密码提交
    const submitForgetPassword = () => {
      if (forgetFormRef.value) {
        forgetFormRef.value.validate(async (valid: boolean) => {
          if (!valid) return;

          try {
            // 调用密码重置API
            const data:UserResetPasswordData = {
              email: forgetForm.email,
              password: SHA256(forgetForm.password).toString(),
            }
            const response = await postUserPasswordReset(data);
            if (response.status !== 200) {
              ElMessage.error(response.data);
              return;
            }
            ElMessage.success("密码修改成功，请登录");
            forgetVisible.value = false;
          } catch (error) {
            ElMessage.error("密码修改失败，请稍后重试");
          }
        });
      }
    };

    return {
      activeTab,
      loginForm,
      verifyForm,
      registerForm,
      forgetForm,
      loginRules,
      verifyRules,
      registerRules,
      forgetRules,
      loginFormRef,
      verifyFormRef,
      registerFormRef,
      forgetFormRef,
      submitLogin,
      getCode,
      verifyRegisterCode,
      submitRegister,
      submitForgetPassword,
      forgetVisible,
      verificationRegisterPassed,
      isVerified,
      verifyPwdCode,
    };
  },
};
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: url("@/assets/LoginBackground.png") no-repeat center center;
  background-size: cover;
}
.custom-tabs-container {
  justify-content: center;
}
.login-card {
  width: 600px;
  background-color: rgba(255, 255, 255, 0.9);
  border-radius: 8px;
  padding: 20px;
}
</style>
