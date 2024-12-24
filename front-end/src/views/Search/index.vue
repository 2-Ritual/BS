<template>
  <div class="car-search">
    <!-- 搜索框 -->
    <el-row class="search-box" :gutter="20" style="margin-top: 50px">
      <el-col :span="24" class="search-header">
        <el-input
          v-model="searchKeyword"
          placeholder="请输入品牌或车型名称"
          clearable
          class="search-input"
          size="medium"
        >
          <template #prepend>
            <el-icon><i class="el-icon-search"></i></el-icon>
          </template>
        </el-input>
        <el-button type="primary" @click="performSearch">搜索</el-button>
      </el-col>
    </el-row>

    <!-- 筛选条件 -->
    <el-card class="filter" shadow="hover">
      <el-tag type="info" class="section-header">筛选条件</el-tag>

      <el-row class="filter-section" :gutter="20">
        <!-- 品牌选择 -->
        <el-col :span="8">
          <el-tag type="info" class="section-title">品牌</el-tag>
          <el-select
            v-model="selectedBrand"
            placeholder="请选择品牌"
            clearable
            class="filter-dropdown"
            size="small"
          >
            <el-option
              v-for="brand in brands"
              :key="brand"
              :label="brand"
              :value="brand"
            />
          </el-select>
        </el-col>

        <!-- 排量选择 -->
        <el-col :span="8">
          <el-tag type="info" class="section-title">排量</el-tag>
          <el-select
            v-model="selectedDisplacement"
            placeholder="请选择排量"
            clearable
            class="filter-dropdown"
            size="small"
          >
            <el-option
              v-for="displacement in displacements"
              :key="displacement"
              :label="displacement"
              :value="displacement"
            />
          </el-select>
        </el-col>

        <!-- 座位数选择 -->
        <el-col :span="8">
          <el-tag type="info" class="section-title">座位数</el-tag>
          <el-select
            v-model="selectedSeat"
            placeholder="请选择座位数"
            clearable
            class="filter-dropdown"
            size="small"
          >
            <el-option
              v-for="seat in seats"
              :key="seat"
              :label="seat"
              :value="seat"
            />
          </el-select>
        </el-col>
      </el-row>

      <el-row class="filter-section" :gutter="20">
        <!-- 价格选择 -->
        <el-col :span="8">
          <el-tag type="info" class="section-title">价格</el-tag>
          <el-row class="custom-price" align="middle" style="margin-top: 10px">
            <el-col>
              <el-input-number
                v-model="customPrice.min"
                placeholder="最低价"
                size="small"
                controls-position="right"
                :step="1"
              />
              <span>万</span>
              <span style="margin: 0 8px"> - </span>
              <el-input-number
                v-model="customPrice.max"
                placeholder="最高价"
                size="small"
                controls-position="right"
                :step="1"
              />
              <span>万</span>
              <el-button type="primary" size="small" @click="applyCustomPrice"
                >确定</el-button
              >
            </el-col>
          </el-row>
        </el-col>

        <!-- 级别与车型 (级联选择) -->
        <el-col :span="8">
          <el-tag type="info" class="section-title">级别与车型</el-tag>
          <el-cascader
            v-model="selectedCategory"
            :options="categoryToModelsCascader"
            placeholder="请选择级别与车型"
            size="small"
            clearable
          />
        </el-col>

        <!-- 国别与产地 (级联选择) -->
        <el-col :span="8">
          <el-tag type="info" class="section-title">国别与产地</el-tag>
          <el-cascader
            v-model="selectedCountry"
            :options="countryToOriginsCascader"
            placeholder="请选择国别与产地"
            size="small"
            clearable
          />
        </el-col>
      </el-row>

      <!-- 操作按钮 -->
      <el-row class="action-row" justify="center">
        <el-button type="warning" @click="resetFilters">重置筛选条件</el-button>
        <el-button
          type="primary"
          @click="
            currentPage = 1;
            performSearch();
          "
          >立即搜索</el-button
        >
        <el-button
          type="primary"
          @click="
            {
              currentPage = 1;
              performRecommandSearch();
            }
          "
          >AI搜索</el-button
        >
        <el-button
          type="primary"
          @click="returnToUser"
          >管理偏好</el-button
        >
      </el-row>
    </el-card>

    <!-- 汽车展示部分 -->
    <el-row class="car-list" :gutter="20">
      <el-col
        :span="6"
        v-for="(car, index) in cars"
        :key="car.id"
        class="car-card"
      >
        <el-card :body-style="{ padding: '10px' }" shadow="hover">
          <img :src="car.image" alt="car-image" class="car-image" />
          <h3 class="car-name">{{ car.name }}</h3>
          <p class="car-price">价格: {{ car.price }} 万</p>
          <el-button type="primary" size="small" @click="goToDetail(index)"
            >查看详情</el-button
          >
        </el-card>
      </el-col>
    </el-row>

    <!-- 翻页控制 -->
    <el-pagination
      class="pagination"
      :current-page="currentPage"
      :page-size="pageSize"
      :total="total"
      @current-change="handlePageChange"
      layout="total, prev, pager, next"
    ></el-pagination>
  </div>
</template>


<script lang="ts">
import { defineComponent, ref } from "vue";
import { ElMessage } from "element-plus";
import router from "../../router";
import {
  getSearchResult,
  RecommendConditions,
  SearchResultItem,
  getReconmendedResult,
  SearchConditions,
  SearchResult,
} from "../../api/search";

export default defineComponent({
  name: "CarSearch",
  setup() {
    const brands = [
      "不限",
      "奔驰",
      "宝马",
      "本田",
      "特斯拉",
      "五菱汽车",
      "奥迪",
      "大众",
      "日产",
      "坦克",
    ];
    // const prices = [
    //   "不限",
    //   "5万以下",
    //   "5-8万",
    //   "8-10万",
    //   "10-15万",
    //   "15-20万",
    //   "20-25万",
    //   "25-35万",
    //   "50-100万",
    //   "100万以上",
    // ];
    const categories = [
      "不限",
      "轿车(全部)",
      "SUV(全部)",
      "MPV(全部)",
      "跑车",
      "微面",
      "微卡",
      "轻客",
      "皮卡",
    ];
    const countries = ["不限", "中国", "欧美", "日本", "韩国", "美国"];
    const seats = ["不限", "2座", "4座", "5座", "6座", "7座", "8座", "9座"];
    const displacements = [
      "不限",
      "1.0L及以下",
      "1.1-1.6L",
      "1.7-2.0L",
      "2.1-2.5L",
      "2.6-3.0L",
      "3.1-4.0L",
      "4.0L以上",
    ];
    const selectedDisplacement = ref("不限");
    const selectedSeat = ref("不限");
    const selectedBrand = ref("不限");
    const selectedPrice = ref("不限");
    const selectedCategory = ref("不限");
    const selectedCountry = ref("不限");
    const searchKeyword = ref("");
    const modelOptions = ref([]);
    const customPrice = ref({ min: 0, max: 0 });
    const categoryToModelsCascader = [
      {
        value: "不限",
        label: "不限",
      },
      {
        value: "轿车(全部)",
        label: "轿车(全部)",
        children: [
          {
            value: "微型车",
            label: "微型车",
          },
          {
            value: "小型车",
            label: "小型车",
          },
          {
            value: "紧凑型车",
            label: "紧凑型车",
          },
          {
            value: "中型车",
            label: "中型车",
          },
          {
            value: "中大型车",
            label: "中大型车",
          },
          {
            value: "大型车",
            label: "大型车",
          },
        ],
      },
      {
        value: "SUV(全部)",
        label: "SUV(全部)",
        children: [
          {
            value: "小型SUV",
            label: "小型SUV",
          },
          {
            value: "紧凑型SUV",
            label: "紧凑型SUV",
          },
          {
            value: "中型SUV",
            label: "中型SUV",
          },
          {
            value: "中大型SUV",
            label: "中大型SUV",
          },
          {
            value: "大型SUV",
            label: "大型SUV",
          },
        ],
      },
      {
        value: "MPV(全部)",
        label: "MPV(全部)",
        children: [
          {
            value: "紧凑型MPV",
            label: "紧凑型MPV",
          },
          {
            value: "中型MPV",
            label: "中型MPV",
          },
          {
            value: "中大型MPV",
            label: "中大型MPV",
          },
          {
            value: "大型MPV",
            label: "大型MPV",
          },
        ],
      },
      {
        value: "跑车",
        label: "跑车",
      },
      {
        value: "微面",
        label: "微面",
      },
      {
        value: "微卡",
        label: "微卡",
      },
      {
        value: "轻客",
        label: "轻客",
      },
      {
        value: "皮卡",
        label: "皮卡",
      },
    ];

    const countryToOriginsCascader = [
      {
        value: "不限",
        label: "不限",
      },
      {
        value: "中国",
        label: "中国",
      },
      {
        value: "日本",
        label: "日本",
      },
      {
        value: "欧系",
        label: "欧系",
        children: [
          {},
          {
            value: "德国",
            label: "德国",
          },
          {
            value: "法国",
            label: "法国",
          },
          {
            value: "意大利",
            label: "意大利",
          },
          {
            value: "瑞典",
            label: "瑞典",
          },
          {
            value: "捷克",
            label: "捷克",
          },
          {
            value: "英国",
            label: "英国",
          },
        ],
      },
      {
        value: "韩国",
        label: "韩国",
      },
      {
        value: "美国",
        label: "美国",
      },
    ];
    const applyCustomPrice = () => {
      if (
        customPrice.value.min >= 0 &&
        customPrice.value.max >= customPrice.value.min
      ) {
        ElMessage.success(
          `价格区间设置为: ${customPrice.value.min}-${customPrice.value.max} 万`
        );
      } else {
        ElMessage.error("请输入有效的价格区间！");
      }
    };
    const resetFilters = () => {
      selectedBrand.value = "不限";
      selectedPrice.value = "不限";
      selectedCategory.value = "不限";
      selectedCountry.value = "不限";
      selectedDisplacement.value = "不限";
      selectedSeat.value = "不限";
      selectedCategory.value = "不限";
      selectedCountry.value = "不限";
      customPrice.value = { min: 0, max: 0 };
      ElMessage.success("筛选条件已重置");
    };

    const selectOption = (type: string, value: string) => {
      switch (type) {
        case "brand":
          selectedBrand.value = value;
          break;
        case "price":
          selectedPrice.value = value;
          break;
        case "category":
          selectedCategory.value = value;
          break;
        case "country":
          selectedCountry.value = value;
          break;
        case "seat":
          selectedSeat.value = value;
          break;
        case "displacement":
          selectedDisplacement.value = value;
          break;
      }
    };

    const cars = ref<SearchResultItem[]>([
      {
        id: 1,
        name: "奔驰 E级",
        description: "2021款 2.0T 自动 舒适型 2021款 2.0T 自动 舒适型",
        price: 50,
        image: "https://via.placeholder.com/300x200", // 替换为实际图片地址
        brand: "奔驰",
        url: "https://www.baidu.com",
        tags: ["奔驰", "E级"],
        year: 2021,
      },
    ]);

    const currentPage = ref(1);
    const pageSize = ref(6);
    const total = ref(6);
    const SearchCommonLastTime = ref(true);
    const handlePageChange = (newPage: number) => {
      currentPage.value = newPage;
      if (SearchCommonLastTime.value) {
        performSearch();
      } else {
        performRecommandSearch();
      }
    };
    const performSearch = async () => {
      ElMessage.info("正在搜索...");
      
      
      // 模拟筛选逻辑，更新 cars 列表
      const conditions: SearchConditions = {
        brands: selectedBrand.value === "不限" ? [] : [selectedBrand.value],
        models:
          selectedCategory.value === "不限" ? [] : [selectedCategory.value[selectedCategory.value.length-1]],
        minPrice:
          customPrice.value.min === 0 ? undefined : customPrice.value.min,
        maxPrice:
          customPrice.value.max === 0 ? undefined : customPrice.value.max,
        tags: [],
        keywords: searchKeyword.value === ""?undefined:searchKeyword.value,
        page: currentPage.value,
        pageSize: pageSize.value,
      };
      if(selectedDisplacement.value !== "不限") {
        conditions.tags.push(selectedDisplacement.value);
      }
      if(selectedSeat.value !== "不限") {
        conditions.tags.push(selectedSeat.value);
      }
      console.log(conditions);

      const response = await getSearchResult(conditions);
      if (response.status === 200) {
        SearchCommonLastTime.value = true;
        cars.value = [];
        const result: SearchResult = response.data;
        cars.value = result.data;
        total.value = result.total;

        ElMessage.success("搜索完成");
      } else {
        ElMessage.error("搜索失败");
      }
    };
    const returnToUser = () => {
      router.push({ name: "User" });
    };
    const performRecommandSearch = async () => {
      ElMessage.info("正在搜索...");

      const conditions: RecommendConditions = {
        mask_id: Number(localStorage.getItem("mask_id")),
        page: currentPage.value,
        pageSize: pageSize.value,
      };
      const response = await getReconmendedResult(conditions);
      if (response.status === 200) {
        resetFilters();
        SearchCommonLastTime.value = false;
        cars.value = [];
        const result: SearchResult = response.data;
        cars.value = result.data;
        total.value = result.total;

        ElMessage.success("搜索完成");
      } else {
        ElMessage.error("搜索失败");
      }
    };
    performSearch();
    const goToDetail = (index: number) => {
      console.log(cars.value[index].url);
      window.open(cars.value[index].url, "_blank");
    };

    return {
      cars,
      brands,
      // prices,
      categories,
      countries,
      searchKeyword,
      seats,
      displacements,
      selectedSeat,
      selectedBrand,
      selectedPrice,
      selectedCategory,
      selectedCountry,
      selectedDisplacement,
      customPrice,
      currentPage,
      pageSize,
      total,
      modelOptions,
      countryToOriginsCascader,
      categoryToModelsCascader,
      applyCustomPrice,
      performSearch,
      resetFilters,
      selectOption,
      goToDetail,
      handlePageChange,
      performRecommandSearch,
      returnToUser,
    };
  },
});
</script>

<style scoped>
.car-list {
  margin: 10px 0; /* 增加上下的间隔 */
  display: flex;
  flex-wrap: wrap; /* 自动换行 */
  gap: 20px; /* 卡片之间的间距 */
  justify-content: space-between; /* 平均分布 */
}

.car-card {
  flex: 1 1 calc(33.333% - 20px); /* 每行3个卡片，留出间距 */
  max-width: calc(33.333% - 20px); /* 每个卡片最大宽度 */
  margin: 10px 0; /* 增加上下的间隔 */
  box-sizing: border-box;
  transition: transform 0.2s, box-shadow 0.2s; /* 添加过渡效果 */
}

.car-card:hover {
  transform: translateY(-5px); /* 悬停效果 */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* 悬停阴影 */
}

.car-image {
  width: 100%;
  height: auto;
  margin-bottom: 10px;
  border-radius: 5px;
}

.car-name {
  font-size: 16px;
  font-weight: bold;
  margin: 10px 0 5px;
  text-align: center; /* 居中显示 */
}

.car-price {
  font-size: 14px;
  color: #666;
  margin-bottom: 10px;
  text-align: center; /* 居中显示 */
}

.el-card {
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between; /* 保持按钮固定位置 */
  padding: 10px;
}

.el-button {
  align-self: center; /* 居中显示按钮 */
  transition: background-color 0.3s; /* 添加过渡效果 */
}

.el-button:hover {
  background-color: #0056b3; /* 悬停时的深色效果 */
}

.car-search {
  padding: 20px;
}

.search-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 20px;
}

.filter {
  padding: 5px 10px; /* 减少内边距 */
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* 添加阴影 */
}

.filter-section {
  margin-bottom: 10px; /* 减少每个筛选块之间的间距 */
}

.option-row {
  display: flex; /* 使用弹性布局，让按钮紧贴 */
  flex-wrap: wrap; /* 如果空间不足，按钮自动换行 */
  gap: 5px; /* 增加按钮间的间隔 */
}

.option-row .el-button {
  padding: 15px 15px; /* 扩大按钮的点击区域 */
  font-size: 18px; /* 增大字体 */
  width: 90%; /* 每个按钮宽度占据整个父容器 */
  margin: 0; /* 去除按钮之间的间隔 */
  border-radius: 5px; /* 可选，增加圆角，让按钮更美观 */
}

.option-col {
  text-align: left;
  margin-bottom: 5px; /* 减少每个按钮之间的间距 */
  padding: 0 5px; /* 减少按钮左右的间隔 */
}

.custom-price {
  display: flex;
  align-items: center;
  gap: 30px; /* 缩小输入框和按钮之间的间距 */
}

.action-row {
  margin-top: 15px; /* 缩小操作按钮部分与上方的间隔 */
}

.selected-option {
  background-color: #007bff !important;
  color: #fff !important;
  padding: 5px 10px; /* 缩小按钮内边距，减少按钮尺寸 */
}

.section-header {
  margin-bottom: 10px; /* 减少标题与按钮之间的间隔 */
  font-size: 16px;
  font-weight: bold;
  color: #333;
}

.section-title {
  font-size: 14px; /* 放大筛选标题字体 */
  margin-bottom: 5px; /* 减少标题和选项之间的距离 */
}

.pagination {
  margin: 20px auto; /* 上下间隔，并居中 */
}

/* 响应式调整 */
@media (max-width: 768px) {
  .car-card {
    flex: 1 1 calc(50% - 20px); /* 在小屏幕上每行显示2个卡片 */
    max-width: calc(50% - 20px);
  }
}

@media (max-width: 480px) {
  .car-card {
    flex: 1 1 100%; /* 在超小屏幕上每行显示1个卡片 */
    max-width: 100%;
  }
}
</style>
