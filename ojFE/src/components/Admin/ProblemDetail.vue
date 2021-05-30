<template>
    <div>
        <el-row type="flex" class="row-bg" justify="space-around">
            <el-card style="width: 800px">
                <div class="description" style="text-align:left ;">


                    <div class="tag" v-if="!editable">
                        {{form.title}}
                    </div>
                    <Divider/>

                    <div>
                        <div class="tag">题目描述：</div>
                        <div class="retract">
                            <markdown-it-vue class="md-body" :content="form.description"/>
                        </div>
                    </div>
                    <br/>


                    <div>
                        <div class="tag">输入描述：</div>
                        <div class="retract">
                            <markdown-it-vue class="md-body" :content="form.input_description"/>
                        </div>
                    </div>
                    <br/>


                    <div>
                        <div class="tag">输出描述：</div>
                        <div class="retract">
                            <markdown-it-vue class="md-body" :content="form.output_description"/>
                        </div>
                    </div>
                    <br/>

                    <div>
                        <div class="tag">题目来源：</div>

                        <div class="retract">{{ form.problem_source }}</div>

                    </div>
                    <br/>
                    <div>
                        <div class="tag">示例：</div>
                        <el-form label-width="100px" v-for="(item, index) in form.samples" :key="index"
                                 style="width: 100%">

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
                                                v-bind:readOnly="true"></el-input>
                                    </el-form-item>

                                </el-col>
                                <el-col :span="1">
                                    <el-button class="ml10" type="text" size="medium"
                                               v-clipboard:copy="item.input"
                                               v-clipboard:success="onCopy"
                                               v-clipboard:error="onError">复制
                                    </el-button>
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
                                                v-bind:readOnly="true"
                                        ></el-input>

                                    </el-form-item>
                                </el-col>
                                <el-col :span="1">
                                    <el-button class="ml10" type="text" size="medium"
                                               v-clipboard:copy="item.output"
                                               v-clipboard:success="onCopy"
                                               v-clipboard:error="onError">复制
                                    </el-button>
                                </el-col>

                            </el-row>
                        </el-form>


                    </div>

                    <div>
                        <div class="tag">难度：</div>
                        <div class="retract">{{ form.difficulty }}</div>

                    </div>
                    <br/>


                    <div>
                        <div class="tag">是否显示在题库：</div>

                        <el-radio-group class="retract" v-model="form.visible" onclick="return false;">
                            <el-radio :label="true">显示</el-radio>
                            <el-radio :label="false">不显示</el-radio>

                        </el-radio-group>

                    </div>
                    <br/>

                    <div>
                        <div class="tag">是否加入到pk系统：</div>
                        <el-radio-group v-model="form.in_battle_set" class="retract"
                                        onclick="return false;">
                            <el-radio :label="true">加入</el-radio>
                            <el-radio :label="false">不加入</el-radio>

                        </el-radio-group>

                    </div>
                    <br/>

                    <div>
                        <div class="tag">内存限制(单位MB)：</div>

                        <div class="retract">{{ form.memory_limit }}</div>
                    </div>
                    <br/>
                    <div>
                        <div class="tag">时间限制（单位毫秒）：</div>

                        <div class="retract">{{ form.time_limit }}</div>
                    </div>
                    <br/>
                    <div>
                        <div class="tag">提示 ：</div>

                        <div class="retract" v-if="!editable">{{ form.hint }}</div>
                    </div>
                    <br/>


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
    import MarkdownItVue from 'markdown-it-vue'
    import 'markdown-it-vue/dist/markdown-it-vue.css'

    export default {
        name: "ProblemDetail",
        components: {
            MarkdownItVue
        },
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

            onCopy() {
                this.$message.success("复制成功")
            },
            // 复制失败
            onError() {
                alert("复制失败");
            },

            handleBack() {
                console.log(this.appear)
                this.$router.replace("/Problem/List");
            },

        },
        mounted() {
            console.log(this.$route.path);

            //获取详情
            this.editable = false;
            this.form = JSON.parse(sessionStorage.getItem("ProblemInformation"))

            console.log(this.editable);


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