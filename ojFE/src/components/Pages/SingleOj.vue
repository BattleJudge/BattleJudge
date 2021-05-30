<template>
    <div style="margin-left: 250px;margin-top: 5px"
         v-loading="loading"
         element-loading-text="提交运行中"
         element-loading-spinner="el-icon-loading">
        <el-row :gutter="21">
            <el-col :span="15">
                <el-card>
                    <div class="description" style="text-align:left ;">
                        <div class="tag">
                            {{form.title}}
                        </div>
                        <Divider/>

                        <div>
                            <div class="tag">题目描述：</div>
                            <markdown-it-vue class="md-body retract" :content="form.description"/>

                        </div>
                        <br/>
                        <div>
                            <div class="tag">输入描述：</div>
                            <div class="retract">

                                <markdown-it-vue class="md-body" :content="form.input_description"/>
                            </div>
                            <br/>
                            <div class="tag">输出描述：</div>
                            <div class="retract">
                                <markdown-it-vue class="md-body" :content="form.output_description"/>

                            </div>
                            <br/>
                        </div>
                        <div class="tag">示例：
                        </div>

                        <el-form label-width="100px"  v-for="(item, index) in form.samples" :key="index" style="width: 100%">

                            <el-row :gutter="24" style="margin-left: -10px">
                                <el-col :span="10">
                                    <el-form-item
                                            :label="'输入样例'+`${(index + 1)}`"
                                            :prop="'form.samples.' + index + '.input'"
                                    >
                                        <el-input
                                                type="textarea"
                                                rows="2"
                                                resize="none"
                                                v-model="item.input" :readOnly="true"></el-input>
                                    </el-form-item>

                                </el-col>
                                <el-col :span="1">
                                    <el-button class="ml10" type="text" size="medium"
                                               v-clipboard:copy="item.input"
                                               v-clipboard:success="onCopy"
                                               v-clipboard:error="onError">复制</el-button>
                                </el-col>
                                <el-col :span="11">
                                    <el-form-item
                                            :label="'输出样例'+ `${(index + 1)}`"
                                            :prop="'form.samples.' + index + '.output'">
                                        <el-input
                                                type="textarea"
                                                rows="2"
                                                resize="none"
                                                v-model="item.output" :readOnly="true"></el-input>

                                    </el-form-item>
                                </el-col>
                                <el-col :span="1">
                                    <el-button class="ml10" type="text" size="medium"
                                               v-clipboard:copy="item.output"
                                               v-clipboard:success="onCopy"
                                               v-clipboard:error="onError">复制</el-button>
                                </el-col>

                            </el-row>
                        </el-form>

                        <div>
                            <div class="tag">难度：</div>
                            <div class="retract">{{ form.difficulty }}</div>
                        </div>
                        <br/>
                        <div>
                            <div class="tag">提示：</div>
                            <div class="retract">{{ form.hint }}</div>
                        </div>
                        <br/>


                    </div>
                </el-card>
            </el-col>
            <el-col :span="6">
                <el-row>
                    <el-card style="text-align: start">
                        <div>
                            内存限制(单位MB)： {{form.memory_limit}}
                        </div>
                        <div>
                            时间限制（单位毫秒）： {{ form.time_limit }}
                        </div>
                        <div>
                            提交数： {{ form.submission_number }}
                        </div>
                        <div>
                            ac数： {{ form.ac_number }}
                        </div>
                        <div>
                            来源： {{ form.created_by }}
                        </div>
                    </el-card>
                </el-row>
                <el-row style="margin-top: 10px">
                    <el-card style="text-align: start">
                        <a @click="ToHistory" style="font-size: 20px">历史记录</a>
                    </el-card>
                </el-row>
                <el-row style="margin-top: 10px">
                    <el-card style="text-align: start">
                        <a @click="ToSolve" style="font-size: 20px">题解</a>
                    </el-card>
                </el-row>
                <el-row style="margin-top: 10px">
                    <el-card style="text-align: start">
                        <a @click="ToMySolve" style="font-size: 20px">写题解</a>
                    </el-card>
                </el-row>
            </el-col>
        </el-row>
        <el-row :gutter="20" style="margin-top: 10px">
            <el-col :span="15">
                <el-card>
                    <div>
                        Language: {{tag}}
                        <el-dropdown style="margin-left: 2px">
                            <Button type="primary">
                                Language<i class="el-icon-arrow-down el-icon--right"></i>
                            </Button>
                            <el-dropdown-menu slot="dropdown">
                                <el-dropdown-item @click.native="deal_language_C">C</el-dropdown-item>
                                <el-dropdown-item @click.native="deal_language_C_Plus">C++</el-dropdown-item>
                                </el-dropdown-menu>
                        </el-dropdown>
                        <Button style="margin-left: 10px" @click="reset">reset</Button>
                    </div>
                <codemirror   v-model="Send_Info.code" :options="cmdOptions" align="left" @ready="cmReady"
                            ref="codeMirror" style="margin-top: 20px ;font-size: 20px "
                             ></codemirror>
                </el-card>
            </el-col>
        </el-row>
        <el-row style="margin-top: 5px">
            <el-col :span="15">
                <el-button icon="el-icon-check" type="primary" @click="handleSubmit">提交</el-button>
                <el-button @click="handleBack">返 回</el-button>
            </el-col>
        </el-row>


    </div>

</template>

<script>
    import MarkdownItVue from 'markdown-it-vue'
    import 'markdown-it-vue/dist/markdown-it-vue.css'
    import Qs from "qs"
    import {
        codemirror
    } from 'vue-codemirror'


    require("codemirror/lib/codemirror.css");
    require("codemirror/theme/base16-light.css");
    require("codemirror/mode/clike/clike");
    require("codemirror/mode/python/python")
    require("codemirror/addon/edit/matchbrackets.js")
    export default {
        name: "SingleOj",
        components: {
            codemirror,
        MarkdownItVue,

        },
        data() {
            return {
                language_mode: 'text/x-c++src',
                cmdOptions: {
                    tabSize: 4, //tab空格数
                    mode: "text/x-c++src",      //c++
                    lineNumbers: true, //显示行号
                    theme: "base16-light", //主题
                    matchBrackets: true, //括号匹配
                },
                Send_Info: {
                    pro_id:"",
                    code: "",
                    language: "C++",
                },
                tag: "C++",

                submission_id:"",
               loading:false,
                counter:0,
                timeoutObj:"",

                form: {
                    id: "",
                    title: "",
                    description: "",
                    input_description: "",
                    output_description: "",
                    samples: [{"input": "", "output": ""}],
                    hint: "无",
                    problem_source: "",
                    time_limit: "",
                    memory_limit: "",

                    tags: [],
                    submission_number: 0,
                    ac_number:0,
                    created_by:"",
                    difficulty: "简单",
                },

            }
        },
        methods: {

            onCopy(){
                this.$message.success("复制成功")
            },
            // 复制失败
            onError(){
                alert("复制失败");
            },
            cmReady() {
                this.$refs.codeMirror.codemirror.setSize('100%', '400px')
            },
            reset() {
                this.Send_Info.code = ``;
            },

            deal_language_C() {
                this.tag = "C"
                this.Send_Info.language = "C";

            },
            deal_language_C_Plus() {
                this.tag = "C++";
                this.Send_Info.language = "C++";

            },


            ToHistory() {
                console.log("history");
                this.$router.push("/SingleOjHistory")
            },
            ToSolve() {
                this.$router.push("/SingleSolution")
            },
            ToMySolve() {
                this.$router.replace("/MySolution");
            },
            handleBack() {
                this.$router.replace("/Regular/Problem/List");
            },
            getResult(){
                let self=this;
                self.$axios({
                    method: "get",
                    url: "/api/submission/",
                    params: {submission_id:this.submission_id}
                }).then(response=>{
                    console.log(response.data);
                    if(response.data.code==0){
                        if(response.data.result==6||response.data.result==7){
                            clearTimeout(this.timeoutObj);
                            this.timeoutObj=setTimeout(self.getResult,2000);
                        }else{
                            this.loading=false;
                            if(response.data.data.result==0){
                                this.$message.success("正确")
                            }else{
                                this.$message.error(this.dealResult(response.data.data.result));
                            }
                            return ;
                        }
                    }else{
                        this.$message.error(response.data.msg);
                    }
                    }
                ).catch(error => {
                    console.log(error.data);
                });
            },
            dealResult( result){
                console.log("result   "+result);
                switch (result) {
                    case -2:return "编译错误";
                    case -1:return "答案错误";
                    case 1:return "超时";
                    case 2:return "超时";
                    case 3:return "内存溢出";
                    case 4:return "运行时错误";
                    case 5:return "系统错误";
                }
            },

            singleOj(){
                this.$axios({
                    method: "post",
                    url: "/api/submission/",
                    data:Qs.stringify(this.Send_Info)

                }).then(response => {
                    console.log(response.data);
                    if(response.data.code==0){
                        this.submission_id=response.data.data.submission_id;
                        console.log(this.submission_id);
                        setTimeout(this.getResult,2000)
                    }else{
                        this.$message.error(response.msg);
                    }
                }).catch(error => {
                    console.log(error);
                });
            },
            handleSubmit(){
                 this.loading=true;
                //this.testRecurse();
                 this.singleOj();
            },
            getData(){
                this.$axios({
                    method: "get",
                    url: "/api/problem/",
                    params:{
                        id:this.ProblemID
                    }

                }).then(response => {
                    console.log(response.data);
                    if (response.data.code == 0) {
                        this.form=response.data.data;
                    }else{
                        this.$message.error(response.data.msg)
                    }

                }).catch(error => {
                    console.log(error.data);
                });
            }
        },

        destroyed(){
            clearTimeout(this.timeoutObj);
            this.timeoutObj = '';
          console.log("销毁");
        },
        mounted() {
            // window.addEventListener('touchmove', func, { passive: false })
            // window.addEventListener('touchmove',  function (e) { console.log("hello");e.preventDefault(); }, { passive: false });
            console.log(this.$route.path);
            this.ProblemID=sessionStorage.getItem("ProblemId");
            this.Send_Info.pro_id=this.ProblemID;
            this.getData();

        }


    }
</script>

<style scoped>
    .tag {
        color: #2db7f5;
        font-size: 20px;
    }

    .description {
        margin-left: 10px;

    }

    .problem-title {
        margin-bottom: -10px;
        margin-left: 10px;
        font-size: 16px;
    }

    .retract {
        margin-left: 15px;
    }

    .example-item {
        margin-left: 15px;
        margin-right: 15px;
        background-color: #F5F7F9;
        width: auto;
    }

</style>