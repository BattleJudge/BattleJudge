<!--显示某道题上个人提交记录-->
<template>
    <div>

        <div class="Contest">
            <HistoryLayout> <!-- 布局 -->
                <el-row type="flex" justify="center">
                    <div class="demo-split" style="width: 70%">
                        <div slot="left" class="demo-split-pane">
                            <SubmissionPane ref="left"></SubmissionPane>
                        </div>
                    </div>
                </el-row>
                <el-button @click="handleBack" style="margin-top: 5px"> 返 回</el-button>
            </HistoryLayout>
        </div>

    </div>
</template>
<script>


    import HistoryLayout from '../ContestComps/HistoryLayout.vue'
    import SubmissionPane from '../ContestComps/SubmissionPane.vue'


    export default {
        name: 'HistoryDetail',
        components: {
            HistoryLayout,
            SubmissionPane
        },
        data() {
            return {
                split1: 0.5, // 从中间分开

                dialogVisible: false,
                battle_id: "1",
                competitor_id: "2",
                competitor_username: "3",
                problem_id: "4",
            }
        },
        methods: {

            handleBack() {
                this.$router.replace({path: '/History'});
            },
            // SetQuestionDes() {   //获取题目的详细信息
            //     this.$axios({
            //         methods: 'get',
            //         url: "qusetion/" + this.problem_id,
            //     }).catch(error => {
            //         console.log(error)
            //         this.$message.error("题目获取失败");
            //     });
            // },
        },

        mounted() {
            // this.$refs.left.$refs.des.GetQuestionDes(sessionStorage.getItem("problemId"), sessionStorage.getItem("Id"));//获取问题详细信息
        }

    }
</script>
<style scoped>
    .demo-split {
        height: 650px;
        border: 1px solid #dcdee2;
    }

    .demo-split-pane {
        padding: 10px;
    }
</style>
