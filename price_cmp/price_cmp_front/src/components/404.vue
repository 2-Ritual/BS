<template>
  <div class="not-found">
    <div class="content">
      <h1>404</h1>
      <p>Oops! The page you're looking for doesn't exist.</p>
      <el-button type="primary" @click="goHome">Go Home</el-button>
    </div>
  </div>
</template>

<script>
import { ElButton } from 'element-plus';

export default {
  name: 'NotFound',
  components: {
    ElButton
  },
  methods: {
    goHome() {
      this.$router.push('/');
    }
  }
}
</script>

<style scoped>
.not-found {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: linear-gradient(135deg, #e0f7fa, #e3f2fd);
}

.content {
  text-align: center;
  color: #424242;
}

h1 {
  font-size: 10rem;
  margin: 0;
  color: #1976d2;
}

p {
  font-size: 1.5rem;
  margin-bottom: 20px;
}

.el-button {
  font-size: 1rem;
  padding: 10px 20px;
}
</style>
