<template>
  <div class="search-page">
    <div class="container">
      <h1 class="title">比价网</h1>
      <div class="search-container">
        <input
          v-model="searchQuery"
          type="text"
          class="search-input"
          placeholder="请输入商品名称"
          @keydown.enter="handleSearch"
        />
        <button class="search-btn" @click="handleSearch">搜索</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HomePage',
  data() {
    return {
      username: '',
      searchQuery: "",
    };
  },
  methods: {
    handleSearch() {
      if (this.searchQuery.trim() !== "") {
        this.$router.push({
          path: "/result",
          query: { query: this.searchQuery },
        });
        this.searchQuery = ''
      } else {
        alert("请输入商品名称");
      }
    },
  },

  created() {
    this.username = sessionStorage.getItem('username');
    if (this.username === null || this.username === '') {
      window.alert("请先登录！")
      this.$router.push({ path: '/', });
    }
  }
};
</script>

<style scoped>
.search-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(to right, #4facfe, #00f2fe); /* 背景渐变 */
}

.container {
  width: 100%;
  max-width: 500px; /* 限制最大宽度 */
  text-align: center;
  padding: 20px;
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

.title {
  font-size: 2rem;
  font-weight: bold;
  color: #333;
  margin-bottom: 20px;
}

.search-container {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px; /* 按钮和输入框之间的间距 */
}

.search-input {
  width: 70%;
  padding: 10px;
  font-size: 16px;
  border: 2px solid #ccc;
  border-radius: 5px;
  outline: none;
}

.search-input:focus {
  border-color: #4facfe;
}

.search-btn {
  padding: 10px 20px;
  font-size: 16px;
  background-color: #4facfe;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.search-btn:hover {
  background-color: #00f2fe;
}

.search-btn:focus {
  outline: none;
}

@media (max-width: 576px) {
  .search-input {
    width: 60%;
  }
  .search-btn {
    font-size: 14px;
    padding: 8px 16px;
  }
}
</style>
