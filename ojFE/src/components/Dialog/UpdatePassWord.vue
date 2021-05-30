<!--更新个人信息的弹窗-->
<template>
  <div align="center">
    <el-dialog
      title="修改密码"
      :visible.sync="dialogRegisterVisible"
      width="450px">
      <el-form
        @keyup.native.enter="updateClick"
        :close-on-click-modal="false"
        label-width="80px">






        <el-form-item label="旧密码">
          <el-input type="password"
                    v-model="updateform.old_password"
                    autocomplete="off"
                    placeholder="不少于6个字符的密码，必填"></el-input>
        </el-form-item>

        <el-form-item label="新密码">
          <el-input type="new_password"
                    v-model="updateform.new_password"
                    autocomplete="off"
                    placeholder="不少于6个字符的密码，必填"></el-input>
        </el-form-item>



        <div style="margin-top: 20px">
          <el-button @click="dialogRegisterVisible = false">取 消</el-button>
          <el-button type="primary"
                     @click="updateClick">确 定
          </el-button>
        </div>
      </el-form>


    </el-dialog>
  </div>
</template>

<script>

    import Qs from 'qs'
    export default {

        name: "UpdatePassWord",
        data() {
            return {
                dialogRegisterVisible: false,

                updateform: {
                  old_password: "",
                  new_password:"",
                }

            };
        },
        methods: {

            open() {
                this.dialogRegisterVisible = true;
            },
            updateClick() {
                if (
                    !this.updateform.new_password ||
                    !this.updateform.old_password

                ) {
                    this.$message.error("字段不能为空！");
                    return;
                }

                if (this.updateform.old_password.length < 6) {
                    this.$message.error("旧密码错误");
                    return;
                }
                if (this.updateform.new_password.length < 6) {
                    this.$message.error("新密码太短！");
                    return;
                }

                this.$axios({
                    method: 'post',
                    url: "/api/change_password/",
                    data: Qs.stringify(this.updateform),

                }).then(response => {
                    console.log(response.data)
                    if (response.data.code != "0") {
                        this.$message.error(response.data.msg);
                        return;
                    } else {
                        this.$message({
                            message: "修改成功！",
                            type: "success"
                        });
                        this.dialogRegisterVisible = false;
                        sessionStorage.setItem("password", this.updateform.new_password);
                        this.$router.go(0);          //刷新界面
                    }
                })
                    .catch(error => {
                        this.$message.error(
                            "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
                        );
                    });

            }

        },

    };
</script>

<style scoped>


  .item_bock {

    align-items: center;
    height: 80px;
    width: 200px;
    padding: 0px 10px 0px 20px;
    border-bottom: 1px solid #f7f7f7;
    background: #fff;
  }

  .head_p {
    height: 132px;
  }

  .head_img img {
    width: 90px;
    height: 90px;
    border-radius: 50px
  }

  .hiddenInput {
    display: none;
  }

  .avatar-uploader {
    width: 90px;
    height: 90px;
    margin: 0 auto;
    border: 1px dashed #d9d9d9;
    border-radius: 50px;
    cursor: pointer;
    position: relative;
    overflow: hidden;
  }

  .avatar-uploader .el-upload:hover {
    border-color: #409EFF;
  }

  .avatar-uploader-icon {
    font-size: 14px;
    color: #8c939d;
    width: 90px;
    height: 90px;
    line-height: 90px;
    text-align: center;
  }
</style>
