<template>
  <el-menu
    :default-active="activeIndex"
    class="topNavbar"
    mode="horizontal"
    v-if="menuVisible"
    @select="handleSelect"
  >
    <img class="logo" src="../public/logo.png" alt="logo" />
    <el-menu-item index="1"
      ><router-link to="/user">个人中心</router-link></el-menu-item
    >
    <el-menu-item index="2"
      ><router-link to="/search">搜索</router-link></el-menu-item
    >

    <!-- 添加用户头像和登出选项，靠右显示 -->
    <div class="user-menu">
      <el-sub-menu index="5">
        <template #title>
          <el-avatar
            src="https://img.icons8.com/ios/452/user-male-circle.png"
            alt="User Avatar"
            size="medium"
          />
        </template>
        <el-menu-item index="5-1" @click="logout">登出</el-menu-item>
      </el-sub-menu>
    </div>
  </el-menu>
  <RouterView/>
</template>

<script lang="ts">
import { RouterView } from "vue-router";
import { onMounted, ref } from "vue";
import { getUserLogoutJudge } from "./api/login";
import router from "./router";
import EventBus from "./eventBus/EventBus";

export default {
  name: "App",
  setup() {
    const menuVisible = ref(false);
    const logout = async () => {
      const res = await getUserLogoutJudge(Number(localStorage.getItem("uid")));
      if (res.status === 200) {
        localStorage.removeItem("uid");
        localStorage.removeItem("mask_id");
        menuVisible.value = false;
        router.push({ name: "Login" });
      }
    };
    // 在组件创建时监听事件
    onMounted(() => {
      EventBus.on('login', () => {
        menuVisible.value = true; // 登录成功后显示导航栏
      });
    });

    const activeIndex = ref("1");
    const handleSelect = (key: string, keyPath: string[]) => {
      console.log(key, keyPath);
    };
    return {
      activeIndex,
      menuVisible,
      handleSelect,
      logout,
      RouterView,
    };
  },
  components: {
    RouterView,
  },
};
</script>
<style scoped>
.topNavbar {
  position: absolute;
  z-index: 10;
  top: 0;
  left: 0;
  padding-left: 10px;
  width: 100%;
  height: 60px;
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
.logo {
  height: 40px;
  margin-top: 10px;
  margin-right: 50px;
}
</style>
