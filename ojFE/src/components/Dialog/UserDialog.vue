<!--注册的弹窗-->
<template>
    <div style="text-align:left">
        <el-dialog title="用户管理"
                   :visible.sync="dialogUserVisible"
                   :close-on-click-modal="false"
                   left
                   width="450px">


            <el-form :model="form"
                     @keyup.native.enter="registerClick"

                     label-width="70px">
                <el-form-item label="用户名">
                    <el-input v-model="form.username"
                              :readonly="status ? false : 'readonly'"
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
                              :placeholder="password_hint"></el-input>
                </el-form-item>


                <el-form-item label="邮箱">
                    <el-input
                            v-model="form.email"
                            autocomplete="off"
                            placeholder="请填写真实邮箱，必填"></el-input>
                </el-form-item>
                <el-form-item>
                    角色：

                    <el-radio-group v-model="form.user_type">
                        <el-radio label="Regular User">普通用户</el-radio>
                        <el-radio label="Admin User">管理员</el-radio>

                    </el-radio-group>
                </el-form-item>


            </el-form>

            <div slot="footer" style="margin-top: -25px">
                <el-button @click="dialogUserVisible = false">取 消</el-button>
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

        name: "UserDialog",
        data() {
            return {
                dialogUserVisible: false,
                status:"true",
                password_hint:"",
                form: {
                    nickname: "",
                    username: "",
                    password: "",
                    email: "",
                    user_type: "Regular User"
                },
            };
        },
        methods: {
            init() {
                this.form.username = "";
                this.form.nickname = "";
                this.form.password = "";
                this.form.email = "";
            },
            openAdd() {
                this.init();
                this.status=true;
                this.password_hint="不少于6个字符的密码，必填"
                this.dialogUserVisible = true;
            },
            openEdit(row){
                this.init();
                this.status=false;
                this.password_hint="默认为原来的密码"
                this.form.username = row.username;
                this.form.nickname = row.nickname;

                this.form.email = row.email;
                this.form.user_type=row.user_type;



                this.dialogUserVisible = true;
            },
            UserUpdate(){
                this.$axios({
                    method: 'post',
                    url: "/api/admin/update_user_info/",
                    data: Qs.stringify(this.form)
                })
                    .then(response => {
                        if (response.data.code != "0") {
                            this.$message.error(response.data.msg);
                            return
                        } else {
                            console.log(response.data.nickname);
                            if(response.data.data.email==-1){
                                this.$message.error("邮箱重复");
                                return
                            }
                            if(response.data.data.nickname==-1){
                                this.$message.error("昵称重复");
                                return
                            }
                            this.$message({
                                message: "修改成功",
                                type: "success"
                            });
                        }
                        this.dialogRegisterVisible = false;

                        this.$router.go(0);          //刷新界面

                    })
                    .catch(error => {
                        this.$message.error(
                            "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
                        );
                    });
            },
            UserAdd(){
                this.$axios({
                    method: 'post',
                    url: "/api/admin/user/",
                    data: Qs.stringify(this.form)
                })
                    .then(response => {
                        if (response.data.code != "0") {
                            this.$message.error(response.data.msg);
                            return
                        } else {
                            console.log(response.data.nickname);
                            if(response.data.data.email==-1){
                                this.$message.error("邮箱重复");
                                return
                            }
                            if(response.data.data.nickname==-1){
                                this.$message.error("昵称重复");
                                return
                            }
                            this.$message({
                                message: "添加成功！",
                                type: "success"
                            });
                        }
                        this.dialogRegisterVisible = false;

                        this.$router.go(0);          //刷新界面

                    })
                    .catch(error => {
                        this.$message.error(
                            "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
                        );
                    });
            },
            registerClick() {
                if (
                    !this.form.username ||

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
                    this.$message.error("昵称太短！");
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
                    return;
                }
                if(this.status){
                    this.UserAdd();
                }else{
                    this.UserUpdate();
                }


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



</style>
