<template>
  <div class="result-container">
    <div class="search-box">
      <input
        v-model="query"
        @keyup.enter="handleSearch"
        type="text"
        class="form-control form-control-lg"
        placeholder="请输入商品名称"
      />
      <button @click="handleSearch" class="search-button">搜索</button>
    </div>

    <div class="category-buttons">
      <button
        :class="{ active: selectedCategory === '全部' }"
        @click="selectCategory('全部')">全部</button>
      <button
        :class="{ active: selectedCategory === '京东' }"
        @click="selectCategory('京东')">京东</button>
      <button
        :class="{ active: selectedCategory === '淘宝' }"
        @click="selectCategory('淘宝')">淘宝</button>
    </div>

    <div class="reminder-button-container">
      <button @click="toggleReminderList" class="btn btn-info">
        查看提醒列表
      </button>
    </div>

    <div v-if="showReminderList" class="reminder-dropdown">
      <div class="reminder-header">
        <span>{{ reminderCount }}/{{ 5 }} </span>
      </div>

      <div class="reminder-items">
        <div
          v-for="(product, index) in reminderProducts"
          :key="index"
          class="reminder-item"
        >
          <a :href=product.product_url target="_blank">
            <span>{{ product.product_name.trim() }} - {{ product.cur_price }}元</span>
          </a>
          <button @click="deletePriceAlert(product)" class="remove-button">-</button>
        </div>
      </div>
    </div>

    <h1>商品搜索结果</h1>
    <div v-if="is_loading" class="loading-spinner">
      <div class="spinner"></div>
      <span>加载中...</span>
    </div>

    <div class="product-list" ref="productList" v-if="!is_loading">
      <div
        v-for="(product, index) in paginatedProducts"
        :key="index"
        class="product-item"
      >
        <div class="product">
          <img :src="product.image" alt="商品图片" class="product-image" />
          <div class="product-info">
            <p class="product-name">{{ product.product_name }}</p>
            <p class="product-price">{{ product.cur_price }}元</p>
            <p class="product-origin">来源：{{ product.origin }}</p>

            <div class="product-buttons">
              <button @click="addPriceAlert(product)" class="btn btn-warning" style="margin-left: 500px">加入降价提醒</button>
              <button @click="goToMerchant(product)" class="btn btn-info" style="margin-left: 50px">跳转至商家</button>
              <button @click="viewDetails(product)" class="btn btn-success" style="margin-left: 50px">查看详情</button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="pagination">
      <button
        :disabled="currentPage === 1"
        @click="goToPage(currentPage - 1)"
      >
        上一页
      </button>
      <span>第 {{ currentPage }} 页</span>
      <button
        :disabled="currentPage === totalPages"
        @click="goToPage(currentPage + 1)"
      >
        下一页
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ResultPage',
  data() {
    return {
      username: null,
      query: "",
      alert_queue: [0, 0, 0, 0, 0],
      products: [],
      filteredProducts: [],
      currentPage: 1,
      selectedCategory: '全部',
      itemsPerPage: 10,
      is_loading: false,
      reminderProducts: [],
      showReminderList: false,
    };
  },
  computed: {
    totalPages() {
      return Array.isArray(this.filteredProducts) ? Math.ceil(this.filteredProducts.length / this.itemsPerPage) : 0;
    },
    paginatedProducts() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return Array.isArray(this.filteredProducts) ? this.filteredProducts.slice(start, end) : [];
    },
    reminderCount() {
      return Array.isArray(this.reminderProducts) ? this.reminderProducts.length : 0;
    },
  },
  methods: {
    toggleReminderList() {
      this.showReminderList = !this.showReminderList;
    },

    selectCategory(category) {
      this.selectedCategory = category;
      this.filterProducts();
    },

    filterProducts() {
      if (this.selectedCategory === '全部') {
        this.filteredProducts = this.products;
      } else {
        this.filteredProducts = this.products.filter(
          (product) => product.origin === this.selectedCategory
        );
      }
      this.currentPage = 1;
    },

    goToMerchant(product) {
      window.location.href = product.product_url;
    },

    goToPage(page) {
      if (page < 1 || page > this.totalPages) return;
      this.currentPage = page;
      this.scrollToTop();
    },

    scrollToTop() {
      this.$refs.productList.scrollTop = 0;
    },

    handleSearch() {
      this.is_loading = true;
      this.products = [];

      this.axios.get('http://127.0.0.1:8000/api/get_products', {
          params: { query: this.query }
        })
        .then(response => {
          this.products = response.data.list;
          this.filterProducts();
        })
        .catch(error => {
          console.error('Error:', error);
        })
        .finally(() => {
          this.is_loading = false;
        });
    },

    addPriceAlert(product) {
      if (this.reminderCount === 5) {
        window.alert('提醒队列已满')
        return;
      }
      const data = {
          product_id: product.product_id,
          username: this.username
        };
      this.axios
          .post('http://127.0.0.1:8000/api/add_reminder', data, {
            headers: {
              'Content-Type': 'application/json'
            }
          })
          .then((res) => {
            console.log(res.data.respCode)
            let respCode = res.data.respCode;
            if (respCode === '000004') {
              window.alert('添加成功')
              this.queryReminder()
            } else if (respCode === '400001') {
              window.alert('登陆状态异常');
              this.$router.push({ path: '/' });
            } else if (respCode === '400022') {
              window.alert('该商品已在队列中');
            } else if (respCode === '400021') window.alert('提醒队列已满')
          })
          .catch(() => {
            window.alert('信息查询失败');
          });
    },

    deletePriceAlert(product) {
      if (this.reminderCount === 0) {
        window.alert('无法删除不存在项')
        return;
      }
      const data = {
          product_id: product.product_id,
          username: this.username
        };
      this.axios
          .post('http://127.0.0.1:8000/api/delete_reminder', data, {
            headers: {
              'Content-Type': 'application/json'
            }
          })
          .then((res) => {
            let respCode = res.data.respCode;
            if (respCode === '000005') {
              window.alert('删除成功')
              this.queryReminder()
            } else if (respCode === '400001') {
              window.alert('登陆状态异常');
              this.$router.push({ path: '/' });
            } else if (respCode === '400022') {
              window.alert('该商品不已在队列中');
            }
          })
          .catch(() => {
            window.alert('信息查询失败');
          });
    },

    viewDetails(product) {
      console.log(this.query);
      this.$router.push({
        path: "/detail",
        query: {
          product_id: product.product_id,
          current_query: this.query,
        }
      });
    },

    queryReminder() {
      this.reminderProducts = []
      this.axios.get('http://127.0.0.1:8000/api/get_reminder', {
          params: { username: this.username }
        })
        .then(response => {
          if (response.data.respCode === '000006') this.reminderProducts = response.data.list;
          else window.alert('提醒列表获取失败')
        })
        .catch(error => {
          console.error('Error:', error);
        })
    }
  },

  created() {
    this.username = sessionStorage.getItem('username');
    if (this.username === null || this.username === '') {
      window.alert("请先登录！")
      this.$router.push({ path: '/', });
    }
    this.products = []
    this.query = this.$route.query.query;
    this.handleSearch();
    this.queryReminder();
    this.$router.replace({
          path: this.$route.path,
          query: {},
        });
  },

  mounted() {
    this.products = []
    this.queryReminder();
    console.log(this.reminderProducts);
    if (this.query) {
      this.products = []
      this.handleSearch();
      this.query = '';
    }
  },
};
</script>

<style scoped>
.result-container {
  margin-top: 20px;
  text-align: center;
  padding: 0 10px;
}

.search-box {
  margin-bottom: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.search-box input {
  width: 250px;
  padding: 10px;
  border-radius: 4px;
  border: 1px solid #ccc;
}

.search-button {
  padding: 10px 20px;
  margin-left: 10px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.search-button:hover {
  background-color: #0056b3;
}

.reminder-button-container {
  position: absolute;
  top: 20px;
  right: 20px;
  z-index: 10;
}

.reminder-dropdown {
  position: absolute;
  top: 50px;
  right: 20px;
  background: #fff;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 10px;
  width: 300px;
  max-height: 400px;
  overflow-y: auto;
  border-radius: 8px;
  z-index: 999;
}

.reminder-header {
  font-weight: bold;
  margin-bottom: 10px;
}

.reminder-items {
  max-height: 350px;
  overflow-y: auto;
}

.reminder-item {
  display: flex;
  padding: 10px;
  justify-content: space-between;
  margin: 5px 0;
}

.reminder-item a {
  text-decoration: none;
  color: #007bff;
}

.reminder-item a:hover {
  text-decoration: underline;
}

.remove-button {
  background-color: #ff4d4f;
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 20px;
  height: 18px;
}

.remove-button:hover {
  background-color: #ff0000;
}

.category-buttons button {
  border: 2px solid #007bff;
  background-color: transparent;
  color: #007bff;
  padding: 10px 20px;
  font-size: 16px;
  border-radius: 4px;
  cursor: pointer;
  margin: 0 10px;
  transition: all 0.3s ease;
}

.category-buttons button.active {
  background-color: #007bff;
  color: white;
}

.category-buttons button:hover {
  background-color: #e6f2ff;
}

h1 {
  font-size: 24px;
  color: #333;
}

.product-list {
  height: 600px;
  overflow-y: auto;
  padding: 10px;
  margin-top: 20px;
}

.product-buttons {
  margin-top: 10px;
}

.product-item {
  margin-bottom: 20px;
  display: flex;
  border: 1px solid #ccc;
  border-radius: 6px;
  padding: 10px;
  background-color: #f9f9f9;
}

.product-item .product {
  display: flex;
  flex-direction: row;
  align-items: center;
}

.product-image {
  width: 120px;
  height: 120px;
  object-fit: cover;
  border-radius: 8px;
}

.product-info {
  margin-left: 20px;
  text-align: left;
}

.product-name {
  font-size: 18px;
  color: #007bff;
  text-decoration: none;
}

.product-price {
  font-size: 16px;
  color: #333;
}

.product-origin {
  font-size: 14px;
  color: #777;
}

.pagination {
  margin-top: 20px;
}

.pagination button {
  padding: 8px 20px;
  margin: 0 10px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.pagination button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.pagination span {
  font-size: 18px;
  color: #333;
}

.loading-spinner {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  height: 100px;
}

.spinner {
  border: 4px solid rgba(255, 255, 255, 0.3); /* 背景颜色 */
  border-top: 4px solid #3498db; /* 动画的颜色 */
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite; /* 设置旋转动画 */
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>
