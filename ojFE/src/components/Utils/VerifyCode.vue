<!--验证码模块-->
<template>
  <div>
    <el-row style="text-align: center;">
      <el-col>
        <el-input placeholder="验证码" v-model="form.verify" style="width: 150px;"/>

        <el-button type="button" :disabled="disabled" @click="sendcode">{{btntxt}}</el-button>
      </el-col>
    </el-row>
  </div>
</template>
<script>
    export default {
        name: "VerifyCode",
        props: ['username'],      //type区分为1是找回密码验证码，0是注册验证码
        data() {
            return {
                disabled: false,
                time: 0,
                btntxt: "获取验证码",
                form: {
                    verify: ""
                }
            }
        },
        methods: {
            sendcode() {

                if (this.username == '') {
                    alert("请输入用户名");
                } else {
                    this.time = 60;
                    this.disabled = true;
                    this.query();
                    this.timer();
                }
            },
            query() {
              sessionStorage.removeItem("token");
              console.log(this.username)

                    this.$axios({
                        method: 'get',
                        url: '/api/reset_pwd_token/',
                        params: {
                            username: this.username,
                        }
                    }).then(Response => {
                        console.log(Response.data);
                        if (Response.data.code != 0) {
                            this.$message.error(Response.data.msg)
                            this.time = 0;
                            return
                        }else{
                          this.$message.info("密码已发至注册的邮箱")
                        }
                    }).catch(failResponse => {
                        this.$message.error(failResponse.assign);
                    });

            },
            timer() {
                if (this.time > 0) {
                    this.time--;
                    this.btntxt = this.time + "s后重新获取";
                    setTimeout(this.timer, 1000);
                } else {
                    this.time = 0;
                    this.btntxt = "获取验证码";
                     this.disabled = false;
                }
            },
        }
    }
</script>
