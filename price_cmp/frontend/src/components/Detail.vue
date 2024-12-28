<template>
  <div class="product-detail" v-if="product">
    <button @click="goBack" class="btn btn-primary back-button" style="margin-left: 90%; width: 80px; height:50px; font-size: 24px">
      返回
    </button>

    <div class="product-info">
      <img :src="product.image" alt="商品图片" class="product-image" />
      <div class="product-details">
        <h2>{{ product.product_name }}</h2>
        <p><strong>来源：</strong>{{ product.origin }}</p>
        <p><strong>价格：</strong>{{ priceLabel }}</p>
      </div>
    </div>

    <div style="margin-top: 100px">
      <div ref="chartContainer" style="height: 400px;"></div>
    </div>
  </div>
</template>

<script>
import * as echarts from 'echarts';

export default {
  name: "ProductDetail",
  data() {
    return {
      username: '',
      current_query: '',
      product: [],  // 商品详情数据
      currentMonth: new Date().getMonth() + 1,
      chartData: {
        labels: [],
        datasets: [
          {
            label: "价格",
            data: [],
            type: "line",
            smooth: true,
          },
        ],
      },
      dataLoaded: false,
    };
  },

  computed: {
    priceLabel() {
      const price = this.product[`price_${this.currentMonth}`];
      return price && price !== "0.00" ? `${price}元` : "暂无价格";
    },
  },

  methods: {
    async getDetailInfo() {
      console.log(this.$route)
      const productId = this.$route.query.product_id;
      this.current_query = this.$route.query.current_query;
      console.log(this.current_query);
      if (!productId) {
        this.$router.push('/result');
        return;
      }

      try {
        const response = await this.axios.get("http://127.0.0.1:8000/api/detail_info", {
          params: { query: productId },
        });
        this.product = response.data;

        const months = [
          "1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"
        ];

        const prices = [];
        console.log(this.product)
        months.forEach((month, index) => {
          const price = this.product[`price_${index + 1}`];
          prices.push(price && price !== "0.00" ? parseFloat(price) : null);
        });

        this.chartData.labels = months;
        this.chartData.datasets[0].data = prices;

        this.dataLoaded = true;

        if (this.dataLoaded) {
          this.initChart();
        }

      } catch (error) {
        console.error("获取商品详情失败:", error);
      }
    },

    initChart() {
      const chart = echarts.init(this.$refs.chartContainer);
      const chartOptions = {
        title: {
          text: '价格变化趋势',
        },
        tooltip: {
          trigger: 'axis',
        },
        xAxis: {
          type: 'category',
          data: this.chartData.labels,
        },
        yAxis: {
          type: 'value',
          name: '价格 (元)',
        },
        series: [
          {
            name: '价格',
            type: 'line',
            data: this.chartData.datasets[0].data,
            smooth: true,
          },
        ],
      };
      chart.setOption(chartOptions);
    },

    // 返回上一页
    goBack() {
      const query = this.current_query;
      sessionStorage.setItem('previousQuery', query);
      this.$router.go(-1);
    },
  },

  created() {
    this.username = sessionStorage.getItem('username');
    if (this.username === null || this.username === '') {
      window.alert("请先登录！")
      this.$router.push({ path: '/', });
    }
    this.getDetailInfo();
  },

  mounted() {
    if (this.current_query) {
      this.getDetailInfo();
      this.current_query = '';
    }
  },
};
</script>

<style scoped>
.product-detail {
  padding: 20px;
}

.product-info {
  display: flex;
  flex-direction: row;
  align-items: center;
  margin-bottom: 20px;
}

.product-image {
  width: 150px;
  height: 150px;
  object-fit: cover;
  margin-right: 20px;
}

.product-details h2 {
  margin: 0;
  font-size: 24px;
}

.product-details p {
  font-size: 18px;
}

h3 {
  font-size: 20px;
  margin-bottom: 20px;
}

canvas {
  width: 100%;
  height: 100%;
}
</style>
