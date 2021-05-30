<!--找回密码的弹窗-->
<template>
  <div>
    <el-dialog title="重置密码"
               :visible.sync="dialogRegisterVisible"
               width="450px"
               center>
      <el-form :model="form"
               @keyup.native.enter="registerClick"
               label-width="60px">

        <el-form-item label="用户名" style="margin-bottom: 10px; text-align: center">
          <el-input
            v-model="form.username"
            autocomplete="off"
            placeholder="请填写用户名"></el-input>
        </el-form-item>

        <el-form-item label="新密码" style="text-align: center;">
          <el-input type="password"
                    v-model="form.new_password"
                    autocomplete="off"
                    placeholder="不少于6个字符的密码，必填"></el-input>
        </el-form-item>


        <VerifyCode ref="Code" :username="form.username"></VerifyCode>

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
    import VerifyCode from "../Utils/VerifyCode"
    import Qs from 'qs'

    export default {
        props: ['form.username'],
        name: "Verify",
        components: {VerifyCode},
        data() {
            return {
                dialogRegisterVisible: false,
                form: {
                    new_password: "",
                    username: "",
                    token: "",
                },
            };
        },
        methods: {


            open() {
                this.dialogRegisterVisible = true;
            },
            registerClick() {
                this.form.token = this.$refs.Code.form.verify;
                console.log(this.form.username+"  "+this.form.new_password+"  "+this.form.token)
                if (
                    !this.form.username ||
                    !this.form.new_password ||
                    !this.form.token
                ) {
                    this.$message.error("字段不能为空！");
                    return;
                }


                if (this.form.new_password.length < 6) {
                    this.$message.error("密码太短！");
                    return;
                }


                sessionStorage.removeItem('token')
                this.$axios({
                    method: 'post',
                    url: '/api/reset_pwd/',
                    data: Qs.stringify(this.form),

                }).then(Response => {
                    console.log(Response.data)
                    if (Response.data.code !="0") {
                        this.$message.error(Response.data.msg);
                        return
                    }else{
                      this.$message.info("重置成功");
                      this.dialogRegisterVisible = false;
                    }


                }).catch(error => {
                    this.$message.error("验证出差错（" + error + "）");
                    this.form.new_password = "";
                    this.$refs.Code.time = 0;
                });
            }
        }
    };
</script>


<style>

  .el-input {
    max-width: 300px;
  }

  .verify_dialog, .verify_dialog * {
    margin: 0 auto;
  }

  .verify_dialog {
    width: 60%;
  }




</style>

