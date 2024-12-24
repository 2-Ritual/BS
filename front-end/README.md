# 软工管项目前端
``Vue3 + Vite + TS + ElementPlus``
## 页面保存在views文件夹下.

## 运行
`npm install`
`npm run dev`

## 接口使用示例
### ts语法
```typescript
import {UserRegisterData, getUserRegisterJudge} from "../../api/login";
  const Register = async() => {
        console.log('注册');
        const data: UserRegisterData = {
          name: '123',
          email: '123',
          verification: '123',
          account: '123',
          password: '123'
        };
        getUserRegisterJudge(data).then(res => {
          console.log(res.data);
        }).catch(err => {
          console.error(err);
          alert(err.response.data.msg);
        });
      };
```

---

# 12.6接口更新（by：张皓翔）

在12月6号的接口更新中，我更改了几处地方，使得逻辑更加严密。

---

## login模块

### 1. UserRegisterData接口结构体更新

```typescript
export interface UserRegisterData{
    // 已在12.6更新中取消，原因是已有验证验证码的接口
    // verification: string;// 通过邮箱发送的验证码
    email: string;// 邮箱
    name: string;// 姓名
    account: string;// 账号名
    password: string;// 密码（不能以明文传输，所以在最终交付时此处应当加密）
}
```

### 2. 添加UserLoginResponse

```typescript
export interface UserLoginResponse{
    id: number;// 用户的id
    token: string;// 用户的token
}
// 将login的返回值规范了一下
export function getUserLoginJudge(data:UserLoginData){
    return axiosInstance.get<UserLoginResponse>('/login/login', {params: data});
}
```

### 3.添加Logout

```typescript
export interface UserLogoutData{
    id: number;// 用户的id
    token: string;// 用户的token
}
// 此函数用于用户登出
// 返回一个不携带任何负载的回应，按照它的status判断是否登出成功
export function getUserLogoutJudge(data:UserLogoutData){
    return axiosInstance.get('/login/logout', {params: data});
}
```

---

## user模块

### 1.修改UserData携带的Mask数据

```typescript
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
```

### 2.修改UserModifyData

```typescript
export interface UserModifyData{
    email: string;
    account: string;
    name: string;
    // 以下字段暂时不用,在12.6的更新中已被弃用,因为修改密码已有方法实现,直接调用即可
    // password: string;
}
```

### 3.修改NewMaskData（有争议）

```typescript
export interface NewMaskData{
    name: string;
    description: string;
    id: number;// 用户id

    likes: Array<number>;// 用户喜欢的汽车
    dislikes: Array<number>;// 用户不喜欢的汽车
    // 以下字段暂时不用,在12.6的更新中已被弃用,更新为只有汽车,没有标签
    //因为用户不会对某个标签say no,只会对汽车say no
    /*
    likes: Array<string>;// 用户喜欢的标签或汽车
    dislikes: Array<string>;// 用户不喜欢的标签或汽车
    */
}
```

### 4.弃用getMaskList

```typescript
// 此函数在12.4的更新中被弃用，因为在获得用户信息时就已经包含了mask标签列表
// // 用于获取mask标签列表
// // @data: 用户id
// // 返回值：mask标签列表
// export function getMaskList(data: number){
//     return axiosInstance.get<Array<MaskData>>('/user/masklist', {params: {id: data}});
// }
```





