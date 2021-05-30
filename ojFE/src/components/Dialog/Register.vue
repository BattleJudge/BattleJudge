<!--注册的弹窗-->
<template>
  <div>
    <el-dialog title="注册"
               :visible.sync="dialogRegisterVisible"
               :close-on-click-modal="false"
               center
               width="450px">


      <el-form :model="form"
               @keyup.native.enter="registerClick"
               label-width="70px">
        <el-form-item label="用户名">
          <el-input v-model="form.username"
                    autocomplete="off"
                    placeholder="不少于6个字符的用户名，必填"></el-input>
        </el-form-item>
        <el-form-item label="用户昵称">
          <el-input v-model="form.nickname"
                    autocomplete="off"
                    placeholder="不少于6个字符的昵称，必填"></el-input>
        </el-form-item>

        <el-form-item label="密码">
          <el-input type="password"
                    v-model="form.password"
                    autocomplete="off"
                    placeholder="不少于6个字符的密码，必填"></el-input>
        </el-form-item>


        <el-form-item label="邮箱">
          <el-input
            v-model="form.email"
            autocomplete="off"
            placeholder="请填写真实邮箱，必填"></el-input>
        </el-form-item>



      </el-form>

      <div slot="footer" style="margin-top: -25px">
        <el-button @click="dialogRegisterVisible = false">取 消</el-button>
        <el-button type="primary"
                   @click="registerClick">确 定
        </el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>

  import Qs from 'qs'
    export default {

        name: "Register",
        data() {
            return {
                dialogRegisterVisible: false,
                form: {
                    nickname:"",
                    username: "",
                    password: "",
                    email: "",
                },
            };
        },
        methods: {

            open() {
                this.dialogRegisterVisible = true;
            },
            registerClick() {
                if (
                    !this.form.username ||
                    !this.form.password ||
                    !this.form.nickname ||
                    !this.form.email
                ) {
                    this.$message.error("字段不能为空！");
                    return;
                }
                if (this.form.username.length < 6) {
                    this.$message.error("用户名太短！");
                    return;
                }
              if (this.form.nickname.length < 6) {
                this.$message.error("用户名太短！");
                return;
              }

                if (this.form.password.length < 6) {
                    this.$message.error("密码太短！");
                    return;
                }
                if (
                    this.form.username.indexOf("|") >= 0 ||
                    this.form.username.indexOf(".") >= 0 ||
                    this.form.username.indexOf("#") >= 0
                ) {
                    this.$message.error("用户名包含非法字符！");
                    return;
                }
              var regEmail = /^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/
              if (!regEmail.test(this.form.email)) {
                this.$message({
                  message: '邮箱格式不正确',
                  type: 'error'
                })
                return ;
              }

                sessionStorage.removeItem('token')

                this.$axios({
                    method: 'post',
                    url: "api/register/",
                    data: Qs.stringify(this.form)
                })
                    .then(response => {
                        console.log(response.data)

                        if (response.data.code != "0") {
                            this.$message.error(response.data.msg);
                            this.form.password = ""
                            this.form.confirm = ""
                            return
                        } else {
                            this.$message({
                                message: "注册成功！",
                                type: "success"
                            });
                        }
                        this.dialogRegisterVisible = false;
                        this.form.password = "";

                    })
                    .catch(error => {
                        this.$message.error(
                            "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
                        );
                    });

            }
        }
    };
</script>

<style scoped>


  .el-form {
    /*height: 370px;*/
    margin: 0 auto;
    /*margin-left: 100px;*/
    width: 80%;
    overflow-x: hidden;

  }

  .head_p {
    height: 100px;
  }

  .head_img img {
    width: 90px;
    height: 90px;
    border-radius: 50px
  }

  .hiddenInput {
    display: none;
  }


</style>
