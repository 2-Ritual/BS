//src/api/user.ts
import axiosInstance from "../axios/axiosInstance";

export interface UserData{
    id: number;
    name: string;
    account: string;// 和username一样
    email: string;
    state: string;// 用户的状态，可以是active（线上）、inactive（离线）、locked（锁定）
    salt: string;
    password: string;
    masks: Array<MaskData>;// 用户偏好（mask），是一个数组
    /* 已在12.6的更新中弃用，原因是不改的话，用户操作一次，我们将会发送两个包，降低效率
    mask_id: Array<number>;// 用户偏好（mask），是一个数组，表示用户偏好（mask）的标签id
    */
}

// 用于获取用户信息
// @data: 用户id
// 返回值：用户信息
export function getUserInfo(data: number){
    return axiosInstance.get<UserData>('/user/info', {params: {id: data}});
}

export interface UserModifyData{
    id: number;
    // email: string;
    account: string;
    name: string;
    // 以下字段暂时不用,在12.6的更新中已被弃用,因为修改密码已有方法实现,直接调用即可
    // password: string;
}

export interface UserChangePwd{
    id: number;
    old_password: string;
    new_password: string;
}
// 用于修改用户密码
// @data: 用户id、旧密码、新密码
// 返回值：一个不包含任何信息的回应，按照它的status判断是否修改成功
export function getUserInfoChangePwd(data: UserChangePwd){
    return axiosInstance.get('/user/changepwd', {params: data});
}

// 用于修改用户信息
// @data: 用户信息
// 返回值：一个不包含任何信息的回应，按照它的status判断是否修改成功
export function getUserInfoModify(data: UserModifyData){
    return axiosInstance.get('/user/modify', {params: data});
}

export interface NewMaskData{
    name: string;
    description: string;
    u_id: number;// 用户id

    likes: Array<string>;// 用户喜欢的名词
    dislikes: Array<string>;// 用户不喜欢的名词
    // 以下字段暂时不用,在12.6的更新中已被弃用,更新为只有汽车,没有标签
    //因为用户不会对某个标签say no,只会对汽车say no
    /*
    likes: Array<string>;// 用户喜欢的标签或汽车
    dislikes: Array<string>;// 用户不喜欢的标签或汽车
    */
}

// 用于添加新的mask标签
// @data: 新的mask标签数据
// 返回值：一个包含用户id的回应，按照它的status判断是否添加成功
export function postAddMask(data: NewMaskData){
    return axiosInstance.get('/user/addmask', {params: data});
}

export interface MaskData{
    id: number;
    name: string;
    description: string;
    likes: Array<string>;// 用户喜欢的标签
    dislikes: Array<string>;// 用户不喜欢的标签
}

// 此函数在12.4的更新中被弃用，因为在获得用户信息时就已经包含了mask标签列表
// // 用于获取mask标签列表
// // @data: 用户id
// // 返回值：mask标签列表
// export function getMaskList(data: number){
//     return axiosInstance.get<Array<MaskData>>('/user/masklist', {params: {id: data}});
// }

// 用于更新mask标签
// @data: 更新后的mask标签数据
// 返回值：一个不包含任何信息的回应，按照它的status判断是否更新成功
export function getUpdateMask(data: MaskData){
    return axiosInstance.get('/user/updatemask', {params: data});
}

// 用于删除mask标签
// @data: 要删除的mask标签id
// 返回值：一个不包含任何信息的回应，按照它的status判断是否删除成功
export function getDeleteMask(data: number){
    return axiosInstance.get('/user/deletemask', {params: {id: data}});
}

export interface TagData{
    id: number;
    name: string;
    description: string;
}

// 用于获取标签列表
// 返回值：标签列表
export function getTagList(){
    return axiosInstance.get<Array<TagData>>('/tag/list');
}
