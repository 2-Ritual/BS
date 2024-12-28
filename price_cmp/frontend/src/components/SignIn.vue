<template>
  <div class="sign-in-page">
    <div class="container d-flex flex-column">
      <div class="row no-gutters text-center align-items-center justify-content-center min-vh-100">
        <div class="col-12 col-md-6 col-lg-5 col-xl-4">
          <div class="card shadow-lg p-4 rounded">
            <h1 class="font-weight-bold text-primary mb-4">用户登录</h1>
            <div class="mb-4">
              <div class="form-group mb-3">
                <label for="username" class="sr-only">账号</label>
                <input
                  type="text"
                  class="form-control form-control-lg"
                  id="username"
                  placeholder="请输入账号"
                  v-model="username"
                  :class="{'is-invalid': username && username.length < 3}"
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
                  :class="{'is-invalid': password && password.length < 6}"
                />
              </div>
              <!-- 将按钮放入一个 Flex 容器中 -->
              <div class="button-container d-flex justify-content-center">
                <button
                  class="btn btn-primary btn-lg text-uppercase font-weight-semibold"
                  type="submit"
                  @click="login"
                >
                  登录
                </button>
                <button
                  class="btn btn-secondary btn-lg text-uppercase font-weight-semibold"
                  type="button"
                  @click="register"
                >
                  注册
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
export default {
  name: 'SignInPage',
  data() {
    return {
      username: '',
      password: '',
    };
  },
  methods: {
    async login() {
      if (this.username.length > 0 && this.password.length > 0) {
        const hashedPassword = await this.hashPassword(this.password);
        const data = {
          username: this.username,
          password: hashedPassword
        };

        this.axios
          .post('http://127.0.0.1:8000/api/authenticate_user', data, {
            headers: {
              'Content-Type': 'application/json'
            }
          })
          .then((res) => {
            // console.log(res.data);
            let respCode = res.data.respCode;
            if (respCode === '000000') {
              sessionStorage.setItem('username', this.username);
              this.$router.push({
                path: '/home',
              });
            } else if (respCode === '400002') {
              window.alert('账号不存在');
              this.username = '';
              this.password = '';
            } else {
              window.alert('密码错误');
              this.username = '';
              this.password = '';
            }
          })
          .catch(() => {
            window.alert('账号获取失败');
            this.username = '';
            this.password = '';
          });
      } else {
        window.alert('请输入账号或密码');
      }
    },
    register() {
      this.$router.push('/register');
    },
    async hashPassword(password) {
      const encoder = new TextEncoder();
      const data = encoder.encode(password);
      const hashBuffer = await crypto.subtle.digest('SHA-256', data);
      const hashArray = Array.from(new Uint8Array(hashBuffer));
      return hashArray.map(byte => byte.toString(16).padStart(2, '0')).join('');
    },
  },
};
</script>

<style scoped>
.sign-in-page {
  background: linear-gradient(to right, #4facfe, #00f2fe);
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
  margin: 10px;
  flex: 1;
  width: auto;
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

.button-container {
  display: flex;
  justify-content: center;
  gap: 20px;
  width: 100%;
}
</style>

