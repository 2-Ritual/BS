<template>
  <div class="login-body">
    <div class="login-panel">
      <div class="login-title">用户登录</div>
      <el-form :model="formData" :rules="rules" ref="formDataRef">
        <el-form-item prop="username">
          <el-input placeholder="请输入账号" v-model="formData.username" size="large" type="text"
                    style="width: 60%; margin-bottom: 20px;margin-right: 100px">
            <template #suffix>
              <el-icon class="el-icon__input"><User /></el-icon>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item prop="password">
          <el-input placeholder="请输入密码" v-model="formData.password" size="large" type="password"
                    style="text-align: center; margin-bottom: 50px; width: 60%"
                    @keyup.enter="login()">
            <template #suffix>
              <el-icon style="font-size: 25px" class="el-icon__input"><Lock /></el-icon>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item label="">
          <div class="check-code-panel" style="text-align: center; margin-bottom: 20px;">
            <el-button type="primary" @click="login" style="width: 60%">登录</el-button>
            <Vcode :show="isShow" @success="success" @close="close" @fail="fail" :imgs="[Img]"></Vcode>
          </div>
        </el-form-item>
        <el-form-item label="" style="text-align: center; margin-bottom: 20px">
          <el-checkbox label="记住密码" name="keep_pwd" style="margin-right: 20px;"/>
          <el-checkbox label="自动登录" name="auto_login" style="margin-right: 20px;"/>
          <el-button type="info" style="">忘记密码</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, } from 'vue'
import Img from '@/assets/bg.jpg'
import request from '@/utils/request';
import { useRouter } from 'vue-router';
import {ElMessage} from "element-plus";
import Vcode from 'vue3-puzzle-vcode';
import {Lock, User} from "@element-plus/icons-vue";

// const checkCodeUrl = "api/checkCode?" + new Date().getTime();
const isShow = ref(false)
const formDataRef = ref();
let formData = reactive({
  username: "",
  password: ""
});
const rules = {
  username: [{
    required: true,
    message: "请输入用户名"
  }],
  password: [{
    required: true,
    message: "请输入密码"
  }],
}

const router = useRouter();

const login = () => {
  const form_obj = JSON.parse(JSON.stringify(formData));
  // console.log(form_obj);
  // console.log(form_obj.username);
  // console.log(form_obj.password);
  isShow.value = true
  request.post("/login", form_obj).then(res => {
    if (res) {
      ElMessage({
        message: '登录成功',
        type: 'success',
      })
      let tokenObj = { token: " isLogin", startTime: new Date().getTime() };
      window.localStorage.setItem("isLogin", JSON.stringify(tokenObj));
      localStorage.setItem("username", JSON.parse(JSON.stringify(formData.username)));
      router.push("/home")
    } else {
      ElMessage.error('账号或密码错误！！！登录失败！！！')
      router.push("/")
    }
  });
};

const success = (msg) => {
  isShow.value = false
  console.log('验证通过' + msg)
  router.push('/')
}
const close = () => {
  isShow.value = false
}
const fail = () => {
  console.log('验证失败')
}
</script>

<style lang="scss" scoped >
.login-body {
  //background: url("../assets/bg.jpg") no-repeat center center;
  height: 100%;
  width: 100%;
  background-size: cover;
  position: absolute;
  left: 0;
  top: 0;

  .login-panel {
    position: relative;
    top: 25%;
    bottom: 0;
    left: 0;
    right: 0;
    margin: auto;

    padding: 25px;
    width: 26%;
    min-width: 460px;
    height: 30%;
    min-height: 300px;
    background: rgba(255, 255, 255, 0.6);
    border-radius: 5%;
    box-shadow: 2px 2px 10px #ddd;

    .login-title {
      font-size: 22px;
      text-align: center;
      margin-bottom: 30px;
      margin-top: 20px;
    }
  }
}
</style>