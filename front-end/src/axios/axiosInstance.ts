// src/axios.js
import axios from 'axios';
import { ElMessage } from 'element-plus';
 
// 配置 Axios 实例
const axiosInstance = axios.create({
  baseURL: 'http://localhost:8000', // 设置基础请求路径
  timeout: 20000, // 请求超时时间
});
 
// 添加请求拦截器
axiosInstance.interceptors.request.use(config => {
  // 可以在这里添加请求头部或其他配置
  return config;
}, error => {
  return Promise.reject(error);
});
 
// 添加响应拦截器
axiosInstance.interceptors.response.use(response => {
  // 可以在这里对响应数据做处理
  return response;
}, error => {
  // 可以在这里处理请求错误
  if(error.response.data.msg){
    ElMessage.error(error.response.data.msg);
  }
  return Promise.reject(error);
});
 
export default axiosInstance;