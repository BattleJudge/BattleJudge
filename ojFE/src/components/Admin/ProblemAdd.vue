<template>
    <div>
        <el-row type="flex" class="row-bg" justify="space-around">
            <el-card style="width: 800px">
                <div class="description" style="text-align:left ;">


                    <div v-if="editable">
                        <div class="tag" style="float: left">
                            题目名称：
                        </div>
                        <el-input v-model=form.title :placeholder=form.title
                                  style="float: left;margin-bottom: 10px"></el-input>
                    </div>

                    <Divider/>

                    <div>
                        <div class="tag">题目描述：</div>

                        <el-input class="retract"
                                  type="textarea"
                                  rows="10"
                                  placeholder="请输入题目的描述"
                                  v-model=form.description
                                  resize="none"
                                  ></el-input>

                    </div>
                    <br/>


                    <div>
                        <div class="tag">输入描述：</div>

                        <el-input class="retract"
                                  type="textarea"
                                  rows="2"
                                  placeholder="请填写关于输入的描述"
                                  v-model=form.input_description
                                  resize="none"
                                  ></el-input>

                    </div>
                    <br/>


                    <div>
                        <div class="tag">输出描述：</div>

                        <el-input class="retract"
                                  type="textarea"
                                  rows="2"
                                  placeholder="请填写关于输出的描述"
                                  v-model=form.output_description
                                  resize="none"
                                  ></el-input>

                    </div>
                    <br/>

                    <div>
                        <div class="tag">题目来源：</div>

                       <div class="retract" >
                            <el-input v-model="form.problem_source"></el-input>
                        </div>
                    </div>
                    <br/>
                    <div>
                        <div class="tag">示例：
                            <el-button @click="addItem" type="primary" >增加</el-button>
                        </div>
                        <br/>

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
                                                v-model="item.input"
                                                v-bind:readOnly="!editable"></el-input>
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
                                                v-model="item.output"
                                                v-bind:readOnly="!editable"
                                        ></el-input>

                                    </el-form-item>
                                </el-col>
                                <el-col :span="1">
                                    <el-button class="ml10" type="text" size="medium"
                                               v-clipboard:copy="item.output"
                                               v-clipboard:success="onCopy"
                                               v-clipboard:error="onError">复制</el-button>
                                </el-col>
                                <el-col :span="1">
                                    <i class="el-icon-delete" v-if="editable" @click="deleteItem(item, index)" style="margin-top: 10px"></i>
                                </el-col>
                            </el-row>
                        </el-form>


                    </div>

                    <div>
                        <div class="tag">难度：</div>

                        <el-radio-group v-model="form.difficulty"  class="retract">
                            <el-radio label="简单">简单</el-radio>
                            <el-radio label="中等">中等</el-radio>
                            <el-radio label="困难">困难</el-radio>
                        </el-radio-group>
                    </div>
                    <br/>


                    <div>
                        <div class="tag">是否显示在题库：</div>

                        <el-radio-group v-model="form.visible"  class="retract">
                            <el-radio :label="true">显示</el-radio>
                            <el-radio :label="false">不显示</el-radio>

                        </el-radio-group>
                    </div>
                    <br/>

                    <div>
                        <div class="tag">是否加入到pk系统：</div>

                        <el-radio-group v-model="form.in_battle_set"  class="retract">
                            <el-radio :label="true">加入</el-radio>
                            <el-radio :label="false">不加入</el-radio>

                        </el-radio-group>
                    </div>
                    <br/>

                    <div>
                        <div class="tag">内存限制(单位MB)：</div>
                        <div class="retract" >
                            <el-input v-model="form.memory_limit"></el-input>
                        </div>
                    </div>
                    <br/>
                    <div>
                        <div class="tag">时间限制（单位毫秒）：</div>

                        <div class="retract" >
                            <el-input v-model="form.time_limit"></el-input>
                        </div>
                    </div>
                    <br/>
                    <div>
                        <div class="tag">提示 ：</div>
                        <div class="retract" >
                            <el-input v-model="form.hint"></el-input>
                        </div>
                    </div>
                    <br/>
                    <el-upload
                               ref="uploadInput"
                               :file-list="InputfileList"
                               :on-change="handleInputChange"
                               action="string"
                               accept=".zip"
                               :http-request="uploadInput"
                               :auto-upload="false"
                    >
                        <el-button slot="trigger" size="small" type="primary">选取测试文件</el-button>
                        <div slot="tip" class="el-upload__tip">只能上传zip文件</div>

                    </el-upload>

                </div>
            </el-card>
        </el-row>
        <el-row style="padding-top: 10px">
            <el-button icon="el-icon-back" type="primary" @click="handleBack()">返回</el-button>
            <el-button icon="el-icon-check" type="primary" v-if="editable" @click="handleSubmit()">提交</el-button>
        </el-row>
    </div>


</template>

<script>

    export default {
        name: "ProblemAdd",

        data() {
            return {
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
                    visible: true,
                    in_battle_set: true,
                    difficulty: "简单",
                },

                editable: "",
                update: true,
                Samples: [],
                testCaseFile: "",
                InputfileList: [],

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
            addItem() {
                this.form.samples.push({
                    input: '',
                    output: ''
                })
            },
            deleteItem(item, index) {
                this.form.samples.splice(index, 1)
            },

            handleInputChange(file) {
                console.log("file change")
                this.InputfileList = [];
                this.InputfileList.push(file);
            },
            // 上传文件
            uploadFile(file, id) {
                //console.log(file.file);
                let formData = new window.FormData();
                formData.append("id", id);
                formData.append('file', file.file);
                let options = {
                    url: "/api/admin/testcase/",
                    data: formData,
                    method: 'post',
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                };
                this.$axios(options).then((res) => {
                    console.log("上传文件 " + res)
                    if (res.data.code == 0) {
                        this.$message.info("上传测试文件成功");
                    } else {
                        this.$message.error("上传测试文件失败");
                    }

                });
            },


            uploadInput(file) {
                this.testCaseFile = file;
            },

            addProblem() {

                this.$axios({
                    method: "put",
                    url: "/api/admin/problem/",
                    data: JSON.stringify(this.form),
                    headers: {"Content-Type": "application/json;charset=utf-8"}
                }).then(response => {
                    console.log(response.data);
                    if (response.data.code == 0) {
                        this.$message.info("添加题目成功");
                        if (this.InputfileList.length != 0) {
                            this.$refs.uploadInput.submit();
                            this.uploadFile(this.testCaseFile, response.data.data.id)
                        }
                    }
                }).catch(error => {
                    console.log(error.data);
                });
            },
            updateProblem() {
                this.$axios({
                    method: "post",
                    url: "/api/admin/problem/",
                    data: JSON.stringify(this.form),
                    headers: {"Content-Type": "application/json;charset=utf-8"}
                }).then(response => {
                    console.log(response.data);
                    if (response.data.code == 0) {
                        this.$message.info("更新题目成功");
                        if (this.InputfileList.length != 0) {
                            this.$refs.uploadInput.submit();
                            this.uploadFile(this.testCaseFile, response.data.data.id)
                        }
                    }

                }).catch(error => {
                    console.log(error.data);
                });
            },


            handleBack() {
                console.log(this.appear)
                this.$router.replace("/Problem/List");
            },
            handleSubmit() {
                if (this.update) {
                    console.log("updateProblem")
                    this.updateProblem();
                } else {
                    console.log("addProblem")
                    this.addProblem();
                }
                console.log(this.form);
            }
        },
        mounted() {
            console.log(this.$route.path);
            if (this.$route.path.endsWith("Add")) {                   //添加
                this.update = false;
                console.log(this.form);
            } else {
                this.update = true;                            //修改
                this.form = JSON.parse(sessionStorage.getItem("ProblemInformation"))
                console.log(this.form);
            }
            this.editable = true;
        },

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