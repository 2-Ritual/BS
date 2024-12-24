import axiosInstance from "../axios/axiosInstance";

export interface SearchResultItem {
    id: number;
    name: string;
    description: string;
    price: number;
    image: string;
    brand: string;
    url: string;
    tags: Array<string>;
    year: number;
}

export interface SearchResult {
    data: Array<SearchResultItem>;
    total: number;
    page: number;
    pageSize: number;
}

export interface SearchConditions {
    keywords?: string;
    brands?: Array<string>;
    minPrice?: number;
    maxPrice?: number;
    tags: Array<string>;
    minYear?: number;
    maxYear?: number;
    // 以下是12.10新增的字段
    name?: string;
    models?: Array<string>;
    page: number;
    pageSize: number;
}

// 注意！！！前端应该在进入搜索页面时要调用一次条件为空的搜索，以获取初始结果

// 此函数用于获取搜索结果
// 返回值：搜索结果数组
// 注意！！！前端应该在调用此函数之后，根据total和pageSize来判断总页数，并提示用户非法的页号输入
export function getSearchResult(data: SearchConditions){
    return axiosInstance.get<SearchResult>('/search/common', {params: data});
}

// 此函数用于获取推荐结果
// 参数：mask_id
// 根据mask分析可能会对哪些汽车感兴趣
// 返回值：推荐结果数组
export interface RecommendConditions {
    mask_id: number;
    page: number;
    pageSize: number;
}
export function getReconmendedResult(data:RecommendConditions){
    return axiosInstance.get<SearchResult>('/search/recommend', {params: data});
}