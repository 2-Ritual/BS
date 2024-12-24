import axiosInstance from '../axios/axiosInstance';

// 此函数用于调用发送邮件的脚本，自动发送后端生成的验证码
// @data：用户的邮箱名
// 返回一个不携带任何负载的回应，按照它的status判断验证码是否发送成功
// 12.18新增接口
export interface UserVerificationResponse{
    exist: boolean;// 邮箱是否已经被注册
}
export function postUserVerificationSent(data:string){
    return axiosInstance.post<UserVerificationResponse>('/login/verify/', {email: data});
}

export interface UserRegisterVerification{
    email: string;// 邮箱
    verification: string;// 验证码
}

// 此函数用于判断验证码是否正确
// 返回一个不携带任何负载的回应，按照它的status判断是否验证成功
export function getUserVerificationJudge(data:UserRegisterVerification){
    return axiosInstance.get('/login/verify', {params: data});
}

export interface UserRegisterData{
    // 已在12.6更新中取消，原因是已有验证验证码的接口
    // verification: string;// 通过邮箱发送的验证码
    email: string;// 邮箱
    name: string;// 姓名
    account: string;// 账号名
    password: string;// 密码（不能以明文传输，所以在最终交付时此处应当加密）
}

// 此函数用于存储用户注册信息
// 返回一个不携带任何负载的回应，按照它的status判断是否存储成功
export function getUserRegisterJudge(data:UserRegisterData){
    return axiosInstance.get('/login/register', {params: data});
}

export interface UserLoginData{
    account: string;// 账号名
    password: string;// 密码（不能以明文传输，所以在最终交付时此处应当加密）
}

export interface UserLoginResponse{
    id: number;// 用户的id
    token: string;// 用户的token
}
// 此函数用于用户登录
// 返回一个包含用户id的回应，按照它的status判断是否登录成功
export function getUserLoginJudge(data:UserLoginData){
    return axiosInstance.get<UserLoginResponse>('/login/login', {params: data});
}

// 此函数用于用户登出
// 返回一个不携带任何负载的回应，按照它的status判断是否登出成功
export function getUserLogoutJudge(data:number){
    return axiosInstance.get('/login/logout', {params: {id:data}});
}

export interface UserResetPasswordData{
    email: string;// 邮箱
    password: string;// 密码（不能以明文传输，所以在最终交付时此处应当加密）
}
// 此函数用于忘记密码之后修改密码
// 前提是使用验证码验证
// 返回一个不携带任何负载的回应，按照它的status判断是否修改成功
export function postUserPasswordReset(data:UserResetPasswordData){
    return axiosInstance.post('/login/password/', data);
}