<template>
    <div>
        <el-row type="flex" justify="space-around" style="margin-top: 10px" >
            <el-col :span="10">
                <el-input type="textarea" v-model="content" rows="27" resize="none" style="font-size: 20px" />
            </el-col>
            <el-col :span="10" style="text-align: start ;margin-left: 10px">
                <el-card style="height: 800px">
                    <div style="height: 780px; overflow-y: auto;">
                        <markdown-it-vue  :content="content"/>
                    </div>
                </el-card>
            </el-col>
        </el-row>
        <el-row>
            <el-button type="primary" @click="handleSubmit">提 交</el-button>
            <el-button @click="handleBack">返 回</el-button>
        </el-row>

    </div>
</template>

<script>
    import MarkdownItVue from 'markdown-it-vue'
    import 'markdown-it-vue/dist/markdown-it-vue.css'
    import Qs from "qs"
    export default {
        name: "MySolution",
        components: {
            MarkdownItVue
        },
        data() {
            return {
                content: '# your markdown content'
            }
        },
        methods:{
            handleSubmit(){
                if(this.content.length==0){
                    this.$message.error("题解信息不能为空");
                }else{
                    this.$axios({
                        method: 'put',
                        url: '/api/solution/',
                        data: Qs.stringify({
                            pro_id:sessionStorage.getItem("ProblemId"),
                            content: this.content
                        })
                    }).then(response => {
                        if(response.data.code==0){
                          this.$message.success("添加成功");
                        }else{
                            this.$message.error(response.data.msg);
                        }
                    })
                        .catch(error => {

                            this.$message.error("服务器错误，获取数据失败");
                            console.log(
                                "服务器错误！" + "(" + JSON.stringify(error) + ")"
                            );
                        });
                }
            },
            handleBack(){
                this.$router.replace("/SingleOj")
            }
        }
    }
</script>