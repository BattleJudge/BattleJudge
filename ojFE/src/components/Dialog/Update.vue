<!--更新个人信息的弹窗-->
<template>
    <div align="center">
        <el-dialog
                title="修改个人信息"
                :visible.sync="dialogRegisterVisible"
                width="450px">
            <el-form
                    @keyup.native.enter="updateClick"
                    :close-on-click-modal="false"
                    label-width="80px">

                <el-form-item label="用户头像">
                    <el-upload
                            class="avatar-uploader head_img"
                            :before-upload="beforeAvatarSuccess"
                            :show-file-list="false"
                            :on-change="imgSaveToUrl"
                            action="string"
                            :http-request="setFile"

                    >
                        <img v-if="avatar" :src="avatar">
                        <i v-else class="el-icon-plus avatar-uploader-icon"></i>
                    </el-upload>
                </el-form-item>


                <el-form-item label="用户昵称">
                    <el-input v-model="updateform.nickname"
                              autocomplete="off"
                              placeholder="不少于6个字符的用户昵称，必填"></el-input>
                </el-form-item>


                <el-form-item label="个性签名">
                    <el-input
                            v-model="updateform.motto"
                            style="height:100px;overflow-y: auto;"
                            type="textarea"
                            autocomplete="off"
                            placeholder="请填写个性签名"></el-input>
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
    import Qs from "qs"

    export default {

        name: "Update",
        data() {
            return {
                dialogRegisterVisible: false,
                event: "",

                avatar: "http://121.4.57.217:9000/static/default.png",
                updateform: {
                    nickname: "",
                    motto: "",

                }

            };
        },
        methods: {
            setFile(file) {
                this.event = file;
            },
            //读取本地文件
            imgSaveToUrl(event) {
                // 获取上传图片的本地URL，用于上传前的本地预览
                var URL = null;
                if (window.createObjectURL != undefined) {
                    // basic
                    URL = window.createObjectURL(event.raw);
                } else if (window.URL != undefined) {
                    // mozilla(firefox)
                    URL = window.URL.createObjectURL(event.raw);
                } else if (window.webkitURL != undefined) {
                    // webkit or chrome
                    URL = window.webkitURL.createObjectURL(event.raw);
                }
                // 转换后的地址为 blob:http://xxx/7bf54338-74bb-47b9-9a7f-7a7093c716b5
                this.avatar = URL;
            },
            // 限制图片大小
            beforeAvatarSuccess(file) {
                const isLt2M = file.size / 1024 / 1024 / 2;
                if (!isLt2M) {
                    this.$message.error('上传头像图片大小不能超过2MB！');
                }
                return isLt2M;
            },

            // 上传文件
            uploadFile(file) {
                //console.log(file.file);
                let formData = new window.FormData();
                formData.append('image', file.file);
                let options = {
                    url: "/api/avatar/",
                    data: formData,
                    method: 'post',
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                };
                this.$axios(options).then((res) => {
                    this.avatar = res.data.data.avatar;
                    this.dialogRegisterVisible = false;
                    this.$router.go(0);          //刷新界面

                });
            },
            updateInformation() {
                this.$axios({
                    method: 'put',
                    url: "/api/profile/",
                    data: Qs.stringify(this.updateform),

                }).then(response => {
                    console.log(response.data)
                    if (response.data.code != "0") {
                        this.$message.error("修改失败");
                        return;
                    } else {

                        //上传头像
                        if (this.event != "") {
                            this.uploadFile(this.event);
                        } else {
                            this.$message({
                                message: "修改成功！",
                                type: "success"
                            });
                            this.dialogRegisterVisible = false;
                            this.$router.go(0);          //刷新界面
                        }


                    }
                })
                    .catch(error => {
                        this.$message.error(
                            "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
                        );
                    });
            },


            open() {
                this.dialogRegisterVisible = true;
                this.event = "";

                this.avatar = sessionStorage.getItem("avatar")
                this.updateform.nickname = sessionStorage.getItem("nickname")
                this.updateform.motto = sessionStorage.getItem("motto")
            },
            updateClick() {
                if (
                    !this.updateform.nickname
                ) {
                    this.$message.error("昵称不能为空！");
                    return;
                }
                console.log(this.updateform.nickname.length)
                if (this.updateform.nickname.length < 6) {
                    this.$message.error("昵称太短！");
                    return;
                }

                //上传其他个人信息
                this.updateInformation();


            }

        }

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
