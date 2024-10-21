<template>
  <div class="login">
    <form @submit.prevent="submitLogin">
      <div>
        <label for="username">Username</label>
        <input v-model="username" type="text" id="username" />
        <span v-if="!isUsernameValid">Username is required</span>
      </div>

      <div>
        <label for="password">Password</label>
        <input v-model="password" type="password" id="password" />
        <span v-if="!isPasswordValid">Password must be at least 6 characters</span>
      </div>

      <button type="submit">Login</button>
    </form>
  </div>
</template>

<script>
import { ref, computed } from 'vue'

export default {
  setup() {
    const username = ref('')
    const password = ref('')

    // 验证逻辑
    const trim = (str) => str.replace(/^\s+|\s+$/g, '');
    const isUsernameValid = computed(() => trim(username.value) !== '')
    const isPasswordValid = computed(() => password.value.length >= 6)

    const submitLogin = () => {
      if (isUsernameValid.value && isPasswordValid.value) {
        // 处理成功登录
        console.log('Login success with:', { username: username.value, password: password.value })
      } else {
        alert('Please fill in the form correctly.')
      }
    }

    return {
      username,
      password,
      isUsernameValid,
      isPasswordValid,
      submitLogin
    }
  }
}
</script>

<style scoped>
/* Add your custom styles here */
</style>
