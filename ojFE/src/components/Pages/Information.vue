<!--个人信息界面-->
<template>

  <div>


    <el-row type="flex" class="row-bg" justify="space-around">

      <el-form label-width="80px" class="InforContainer">
        <el-form-item label="用户头像">
          <div class="item_bock head_p">
            <div class="head_img">
              <img :src="form.avatar"/>
            </div>
          </div>
        </el-form-item>


        <el-form-item label="用户名">
          <el-input v-model="form.username" type="text" readonly="readonly"></el-input>
        </el-form-item>


        <el-form-item label="用户昵称">
          <el-input v-model="form.nickname" type="text" readonly="readonly"></el-input>
        </el-form-item>



        <el-form-item label="邮箱">
          <el-input v-model="form.email" type="text" readonly="readonly"></el-input>
        </el-form-item>

        <el-form-item label="个性签名">
          <el-input v-model="form.motto" type="textarea" resize="none" readonly="readonly"></el-input>
        </el-form-item>
        <el-form-item label="提交数">
          <el-input v-model="form.submission_number" type="text" readonly="readonly"></el-input>
        </el-form-item>
        <el-form-item label="ac数">
          <el-input v-model="form.accepted_number" type="text" readonly="readonly"></el-input>
        </el-form-item>

        <el-form-item style="margin-left: -80px;">
          <el-button type="primary" @click="onUpdatePassWord">修改密码</el-button>
          <el-button type="primary" @click="onSubmit">修改个人信息</el-button>
        </el-form-item>
      </el-form>

    </el-row>

    <Update ref="updateDialog"></Update>
    <UpdatePassWord ref="updatePasswordDialog"></UpdatePassWord>

  </div>
</template>

<script>
    import Update from "../Dialog/Update"
    import UpdatePassWord from "../Dialog/UpdatePassWord"
    import axios from 'axios'

    export default {

        name: "information",
        components: {Update,UpdatePassWord},
        data() {
            return {
              loading:true,
                form: {

                    username: '',
                    nickname:"",
                    motto:"",
                    avatar: "",
                    accepted_number:"",
                    submission_number:"",
                    email: "",

                }
            }
        },
        methods: {
          cancel(){
            this.loading=false;
          },
          onUpdatePassWord(){
            this.$refs.updatePasswordDialog.open();
          },
            onSubmit() {
                this.$refs.updateDialog.open();
            },
        },
        created() {

            axios({
                method: 'get',
                url: "/api/profile/",
            }).then(Response => {
                // console.log(Response.data.data);
                if (Response.data.code == 0) {
                    let data = Response.data.data;
                    this.form.nickname=data.nickname;
                    this.form.motto=data.motto;
                    this.form.username = data.username;
                    this.form.avatar = data.avatar;
                    this.form.email = data.email;
                    this.form.accepted_number=data.accepted_number;
                    this.form.submission_number=data.submission_number;

                    sessionStorage.setItem("avatar",this.form.avatar);
                    sessionStorage.setItem("nickname",this.form.nickname);
                    sessionStorage.setItem("motto",this.form.motto);

                }

            }).catch(failResponse => {
                this.$message.error(failResponse);
            });


        }

    }

</script>
<style>
  .InforContainer {
    border-radius: 15px;
    background-clip: padding-box;
    margin: 10px auto;
    width: 350px;
    padding: 20px 30px 5px 30px;
    background: #fff;
    border: 1px solid #eaeaea;
    box-shadow: 0 0 25px #a4cac5;
  }

  .el-form {
    width: 400px
  }

  .el-date-picker {
    width: 400px
  }

  .el-progress {
    margin-top: 10px
  }

  .head_p {
    height: 100px;
  }

  .head_img img {
    width: 100px;
    height: 100px;
    border-radius: 50px
  }

  .lizi {
    height: 100%;
    position: absolute;
    top: 0px;
    left: 0px;
    width: 100%;
  }

  .hiddenInput {
    display: none;
  }
</style>
