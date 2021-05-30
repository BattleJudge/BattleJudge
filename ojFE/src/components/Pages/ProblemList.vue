<template>


    <el-card>
        <el-row type="flex" justify="end" style="padding-bottom: 5px">
            <el-input v-model="input" placeholder="请输入题目id" style="padding-right: 5px"></el-input>
            <el-button type="primary" icon="el-icon-search" @click="handleSearch">搜索</el-button>
            <el-button type="primary" icon="el-icon-circle-plus-outline" @click="handleAdd" >添加题目</el-button>
        </el-row>
        <el-row>
            <el-table :data="tableData" size="small"
                      height="500">
                <el-table-column prop="id" label="#" width="50px"/>
                <el-table-column prop="title" label="题目名称"/>

                <el-table-column prop="time_limit" label="时间限制"/>
                <el-table-column prop="memory_limit" label="空间限制"/>


                <el-table-column label="操作" width="400" >
                    <template slot-scope="scope">

                        <el-button
                                size="mini"
                                @click="handleDetail(scope.$index, scope.row)">详情
                        </el-button>
                        <el-button
                                size="mini"
                                @click="handleEdit(scope.$index, scope.row)">编辑
                        </el-button>

                    </template>
                </el-table-column>


            </el-table>
            <el-pagination
                    @size-change="handleSizeChange"
                    @current-change="handleCurrentChange"
                    :current-page="currentpage"
                    :page-sizes="[10, 20, 30, 50]"
                    :page-size="pagesize"
                    layout="total, sizes, prev, pager, next, jumper"
                    :total="totalProblem"
            ></el-pagination>
        </el-row>
    </el-card>


</template>

<script>

    export default {
        name: "ProblemList",
        data() {
            return {
                currentpage: 1,
                pagesize: 20,
                totalProblem: 0,
                input: "",


                tableData:[{
                    id: 1,
                    title: "a + b problem",
                    description: "输入两个整数a和b，输出他们的和",
                    input_description: "两个正整数$1 \\le a \\le 100, 1 \\le b \\le 100$",
                    output_description: "$a + b$",
                    samples: [{"input": "1 1", "output": "2"}, {"input": "1 2", "output": "3"}],
                    hint: "无",
                    problem_source: "source",
                    time_limit: 1000,
                    memory_limit: 1,

                    tags: ["简单"],
                    visible: "True",
                    in_battle_set: "True",
                    difficulty: "简单",
                }],
                // tableData: [{
                //     id: 1,
                //     Title: '水仙花数',
                //     acRate: '20%',
                //     acStatus: "已解决",
                //     limitTime: 120,
                //     limitMemory: 1000
                //
                //
                // }]
            }
        },
        methods: {

            getData(limit, offset) {                //获取数据
                this.$axios({
                    method: 'get',
                    url: '/api/admin/problem_list/',
                    params: {
                        size: limit,
                        page: offset
                    }
                }).then(response => {
                    if(response.data.detail!=""){
                        console.log(response.data);
                        this.tableData = response.data.data;
                        this.totalProblem = response.data.total;
                    }else{
                        this.$message.error(response.data.detail)
                    }

                })
                    .catch(error => {

                        this.$message.error("服务器错误，获取数据失败");
                        console.log(
                            "服务器错误！" + "(" + JSON.stringify(error) + ")"
                        );
                    });
            },

            handleEdit(index, row) {
                console.log(index + "edit");
                sessionStorage.setItem("ProblemInformation",JSON.stringify(row));
                this.$router.push("/Admin/Problem/Update");
            },

            handleAdd() {
                this.$router.push("/Admin/Problem/Add");
            },
            handleDetail(index, row) {
                console.log(index + "detail");
                sessionStorage.setItem("ProblemInformation",JSON.stringify(row));
                this.$router.push("/Admin/Problem/Detail");
            },
            handleSizeChange(val) {
                this.pagesize = val;
                this.getData(this.pagesize, this.currentpage);
            },
            handleCurrentChange(val) {
                this.currentpage = val;
                this.getData(this.pagesize, this.currentpage);
            },
            handleSearch(){
                this.$axios({
                    method: 'get',
                    url: '/api/admin/problem/',
                    params: {
                        id:this.input
                    }
                }).then(response=>{
                    if(response.data.code==0){
                        console.log(response.data.data);

                        this.currentpage=1;
                        this.totalProblem=1;
                        this.tableData=[];
                        this.tableData.push(response.data.data);
                    }else{
                        this.$message.error(response.data.msg);
                    }

                }).catch(error=>{
                    console.log(error)
                })
            }
        },
        mounted() {
            this.getData(this.pagesize, this.currentpage);

        }

    }
</script>

<style scoped>

</style>