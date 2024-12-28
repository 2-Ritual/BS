<template>
  <div class="register-page">
    <div class="container d-flex flex-column">
      <div class="row no-gutters text-center align-items-center justify-content-center min-vh-100">
        <div class="col-12 col-md-6 col-lg-5 col-xl-4">
          <div class="card shadow-lg p-4 rounded">
            <h1 class="font-weight-bold text-primary mb-4">用户注册</h1>
            <div class="mb-4">

              <div class="form-group mb-3">
                <label for="username" class="sr-only">账号</label>
                <input
                  type="text"
                  class="form-control form-control-lg"
                  id="username"
                  placeholder="请输入账号"
                  v-model="username"
                  style="margin-left: 42px;"
                  :class="{'is-valid': username}"
                />
              </div>

              <div class="form-group mb-3">
                <label for="password" class="sr-only">密码</label>
                <input
                  type="password"
                  class="form-control form-control-lg"
                  id="password"
                  placeholder="请输入密码"
                  v-model="password"
                  style="margin-left: 42px;"
                  :class="{
                    'is-invalid': password && !(password.length > 5 && password.length < 17),
                    'is-valid': password && password.length > 5 && password.length < 17
                  }"
                />
              </div>

              <div class="form-group mb-3">
                <label for="confirmPassword" class="sr-only">确认密码</label>
                <input
                  type="password"
                  class="form-control form-control-lg"
                  id="confirmPassword"
                  placeholder="请确认密码"
                  v-model="confirmPassword"
                  :class="{'is-invalid': confirmPassword && confirmPassword !== password,
                           'is-valid': confirmPassword && confirmPassword === password
                  }"
                />
              </div>
              <div class="form-group mb-3">
                <label for="confirmPassword" class="sr-only">邮箱</label>
                <input
                  type="text"
                  class="form-control form-control-lg"
                  id="email"
                  placeholder="请输入邮箱"
                  v-model="email"
                  style="margin-left: 42px;"
                  :class="{
                    'is-invalid': email && !isValidEmail(email),
                    'is-valid': email && isValidEmail(email)
                  }"
                />
              </div>

              <div class="form-group mb-3">
                <label for="verificationCode" class="sr-only">验证码</label>
                <input
                  type="text"
                  class="form-control form-control-lg"
                  id="verificationCode"
                  placeholder="请输入验证码"
                  v-model="verificationCode"
                  style="margin-left: 26px; width: 100px"
                  :class="{
                    'is-invalid': verificationCode && verificationCode.length !== 6,
                    'is-valid': verificationCode && verificationCode.length === 6
                  }"
                />
              </div>

              <button
                class="btn btn-info btn-sm mt-2"
                style="margin-left:60px"
                @click="sendVerificationCode"
                :disabled="!isValidEmail(email) || countdown > 0"
              >
                {{ countdown > 0 ? countdown + '秒后重新发送' : '发送验证码' }}
              </button>

              <button
                class="btn btn-primary btn-lg btn-block text-uppercase font-weight-semibold"
                type="submit"
                style="margin-left:30px"
                @click="register"
              >
                注册
              </button>
              <p class="mt-3" style="margin-left:87px">
                已有账号？ <router-link to="/" class="text-primary">去登录</router-link>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'RegisterPage',
  data() {
    return {
      username: '',
      password: '',
      confirmPassword: '',
      email: '',
      verificationCode: '',
      verificationCodeSent: false,
      isVerified: false,
      countdown: 0,
    };
  },
  methods: {
    async register() {
      if (this.username.length > 0 && this.password.length > 0 && this.password === this.confirmPassword && this.email.length > 0) {
        await this.verifyCode()
        if (!this.isVerified) return;

        const hashedPassword = await this.hashPassword(this.password);
        const data = {
          username: this.username,
          password: hashedPassword,
          email: this.email,
        };

        this.axios
          .post('http://127.0.0.1:8000/api/register_user', data, {
            headers: {
              'Content-Type': 'application/json'
            }
          })
          .then((res) => {
            console.log(res.data);
            let respCode = res.data.respCode;
            if (respCode === '000002') {
              window.confirm("注册成功!")
              this.$router.push('/');
            } else if (respCode === '400012') {
              window.alert('注册失败，邮箱已被注册');
              this.email = ''
            } else if (respCode === '400011') {
              window.alert('注册失败，用户名已被注册');
              this.username = ''
            } else {
              window.alert('注册失败');
              this.username = '';
              this.password = '';
              this.confirmPassword = '';
              this.email = '';
            }
          })
          .catch(() => {
            window.alert('注册请求失败');
          });
      } else {
        if (this.password && !(this.password.length > 5 && this.password.length < 17)) window.alert('密码格式错误！');
        else if (this.email && !this.isValidEmail(this.email)) window.alert('邮箱格式错误！');
        else if (this.username.length === 0) window.alert('用户名不能为空！');
        else if (this.password.length === 0) window.alert('密码不能为空！');
        else if (this.confirmPassword.length === 0) window.alert('确认密码不能为空！');
        else if (this.email.length === 0) window.alert('邮箱不能为空！');
        else window.alert('信息不能为空！');
      }
    },

    async hashPassword(password) {
      const encoder = new TextEncoder();
      const data = encoder.encode(password);
      const hashBuffer = await crypto.subtle.digest('SHA-256', data);
      const hashArray = Array.from(new Uint8Array(hashBuffer));
      return hashArray.map(byte => byte.toString(16).padStart(2, '0')).join('');
    },

    isValidEmail(email) {
      const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
      return emailPattern.test(email);
    },

    async sendVerificationCode() {
      if (!this.isValidEmail(this.email)) {
        alert("请输入有效的邮箱地址！");
        return;
      }

      try {
        await this.axios.post('http://127.0.0.1:8000/api/send_code', { email: this.email }, )
          .then(res=>{
            let flag = res.data.success
            if (flag) {
              this.verificationCodeSent = true;
              this.startCountdown();
              alert("验证码已发送至您的邮箱，请查收！");
            } else {
              alert("验证码发送失败，请重试！");
            }
        })
      } catch (error) {
        console.error(error);
        alert("发送验证码时出现问题！");
      }
    },

    async verifyCode() {
      if (!this.verificationCodeSent) {
        window.alert('验证码尚未发送');
        return;
      }
      try {
       await this.axios.post('http://127.0.0.1:8000/api/verify_code', {
          email: this.email,
          verification_code: this.verificationCode
       }).then(res=>{
         console.log(res.data)
         const respCode = res.data.respCode
         if (respCode === '400031') {
           this.isVerified = false;
           // alert("验证码与邮箱不能为空");
         } else if (respCode === '400032') {
           this.isVerified = false;
           alert("验证码已过期");
         } else if (respCode === '400033') {
           this.isVerified = false;
           alert("验证码错误");
         } else if (respCode === '000007') this.isVerified = true;
         else if (respCode === '400034') {
           this.isVerified = false;
           alert("验证码不存在");
         }
       })
      } catch (error) {
        console.error(error);
        alert("验证错误！");
      }
    },

    startCountdown() {
      this.countdown = 60;
      const countdownInterval = setInterval(() => {
        if (this.countdown > 0) {
          this.countdown--;
        } else {
          clearInterval(countdownInterval);
        }
      }, 1000);
    }
  }
};
</script>

<style scoped>
.register-page {
  background: linear-gradient(to right, #4facfe, #00f2fe); /* 渐变背景 */
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
}

.card {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
  padding: 40px;
}

h1 {
  font-family: 'Arial', sans-serif;
  font-weight: bold;
  text-align: center;
  color: #2c3e50;
}

p {
  font-size: 16px;
  color: #7f8c8d;
}

.is-invalid {
  border-color: red !important;
  border-width: 2px; /* 增加边框宽度 */
  box-shadow: 0 0 5px red; /* 加阴影效果 */
}

/* 绿色框体，表示有效密码 */
.is-valid {
  border-color: green !important;
  border-width: 2px; /* 增加边框宽度 */
  box-shadow: 0 0 5px green; /* 加阴影效果 */
}

input.form-control {
  border-radius: 6px;
  padding: 8px 10px;
  font-size: 16px;
  margin-left: 10px;
  margin-bottom: 10px;
}

button.btn {
  border-radius: 6px;
  padding: 7px 10px;
  font-size: 14px;
  font-weight: bold;
  margin-top: 20px;
}

button.btn:hover {
  background-color: #007bff;
}

button.btn:focus {
  outline: none;
}

.is-invalid {
  border-color: red;
}

@media (max-width: 576px) {
  .card {
    padding: 30px;
  }
}
</style>
