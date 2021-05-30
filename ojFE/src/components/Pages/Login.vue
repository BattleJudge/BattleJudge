<!--登录界面-->
<template>
  <div>

    <el-form :model="loginForm" :rules="rules" class="login-container" label-position="left"
             label-width="0px" v-loading="loading">

      <h3 class="login_title">Battle Judge</h3>
      <el-form-item prop="email">
        <el-input type="text" v-model="loginForm.username"
                  auto-complete="off" placeholder="邮箱或用户名"></el-input>
      </el-form-item>
      <el-form-item prop="password">
        <el-input type="password" v-model="loginForm.password"
                  auto-complete="off" placeholder="密码"></el-input>
      </el-form-item>

      <el-form-item style="width: 100%">
        <el-button type="primary" style="width: 40%;background: #505458;border: none" v-on:click="login">登录</el-button>
        <el-button type="primary" style="width: 40%;background: #505458;border: none" @click="register">注册</el-button>
      </el-form-item>

      <el-form-item>
        <el-link type="success" @click="verify">找回密码</el-link>
      </el-form-item>
      <Register ref="RegisterDialog"></Register>
      <Verify ref="VerifyDialog"></Verify>
    </el-form>


  </div>
</template>

<script src="https://unpkg.com/axios/dist/axios.min.js"></script>
<script src="https://cdn.jsdelivr.net/gh/stevenjoezhang/live2d-widget/autoload.js"></script>
<script>

    import Register from "../Dialog/Register"
    import PubSub from "pubsub-js"
    import Qs from 'qs'
    import Verify from "../Dialog/Verify"



    export default {
        name: 'Login',
        components: {Register, Verify},
        data() {
            return {
                rules: {
                    username: [{required: true, message: '邮箱不能为空', trigger: 'blur'}],
                    password: [{required: true, message: '密码不能为空', trigger: 'blur'}]
                },
                checked: true,
                loginForm: {
                    username: "",
                    password: ""
                },


            }
        },
        methods: {

            register() {
                this.$refs.RegisterDialog.open();
            },
            verify() {
                this.$refs.VerifyDialog.open();
            },
            login() {

                if (!this.loginForm.username || !this.loginForm.password) {
                    this.$message.error("字段不能为空！");
                    return;
                }
              if (this.loginForm.username.length < 6) {
                this.$message.error("用户名或邮箱太短！");
                return;
              }
              if (this.loginForm.password.length < 6) {
                this.$message.error("密码太短！");
                return;
              }

                 sessionStorage.removeItem('token')
                this.$axios({
                    method: 'post',
                    // headers: { 'content-type': 'application/x-www-form-urlencoded' },
                    url: '/api/login/',
                    data: Qs.stringify(this.loginForm)
                }).then(Response => {
                    console.log(Response.data);
                    if (Response.data.code === "10004") {
                        this.loginForm.password = ""
                        this.$message.error("登录时密码错误");
                        return
                    }

                    if (Response.data.code == 0) {
                      console.log(Response.data);
                        //store保存token
                        this.$store.commit('SET_TOKEN', Response.data.data.access)   //保存token用于拦截
                        this.$store.commit('SET_USER', this.loginForm.username)
                        sessionStorage.setItem("token", Response.data.data.access);
                        sessionStorage.setItem("refreshToken", Response.data.data.refresh);
                        sessionStorage.setItem("password", this.loginForm.password);
                         sessionStorage.setItem("userId", Response.data.data.id);       //用户Id
                        sessionStorage.setItem("avatar", Response.data.data.avatar);
                        sessionStorage.setItem("TokenTime",new Date().getTime());     //记录Token创造时间
                        if(Response.data.data.user_type=="Regular User"){
                          sessionStorage.setItem("role","user")
                        }else{
                          sessionStorage.setItem("role","Admin")
                        }
                        PubSub.publish("Login")
                        this.$router.replace({path: '/Information'});
                    }else{
                      this.$message.error(Response.data.msg)
                    }
                })
                    .catch(failResponse => {
                        console.log(failResponse)
                        this.$message.error("用户名或密码错误");
                    });
            }
        }
    }
</script>
<style>


  .login-container {
    border-radius: 15px;
    background-clip: padding-box;
    margin: 90px auto;
    width: 350px;
    padding: 35px 35px 15px 35px;
    background: #fff;
    border: 1px solid #eaeaea;
    box-shadow: 0 0 25px #cac6c6;
  }

  .login_title {
    margin: 0px auto 40px auto;
    text-align: center;
    color: #505458;
  }

</style>

