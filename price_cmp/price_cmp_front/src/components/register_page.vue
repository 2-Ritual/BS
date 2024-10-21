<template>
  <div class="register">
    <form @submit.prevent="submitRegister">
      <div>
        <label for="username">Username</label>
        <input v-model="username" type="text" id="username" />
        <span v-if="!isUsernameValid">Username is required</span>
      </div>

      <div>
        <label for="email">Email</label>
        <input v-model="email" type="email" id="email" />
        <span v-if="!isEmailValid">Invalid email format</span>
      </div>

      <div>
        <label for="password">Password</label>
        <input v-model="password" type="password" id="password" />
        <span v-if="!isPasswordValid">Password must be at least 6 characters</span>
      </div>

      <button type="submit">Register</button>
    </form>
  </div>
</template>

<script>
import { ref, computed } from 'vue'

export default {
  setup() {
    const username = ref('')
    const email = ref('')
    const password = ref('')

    // 验证逻辑
    const trim = (str) => str.replace(/^\s+|\s+$/g, '');
    const isUsernameValid = computed(() => trim(username.value) !== '')
    const isEmailValid = computed(() => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value))
    const isPasswordValid = computed(() => password.value.length >= 6)

    const submitRegister = () => {
      if (isUsernameValid.value && isEmailValid.value && isPasswordValid.value) {
        // 处理成功注册
        console.log('Register success with:', { username: username.value, email: email.value, password: password.value })
      } else {
        alert('Please fill in the form correctly.')
      }
    }

    return {
      username,
      email,
      password,
      isUsernameValid,
      isEmailValid,
      isPasswordValid,
      submitRegister
    }
  }
}
</script>

<style scoped>
/* Add your custom styles here */
</style>
