<template>


    <el-card>
        <el-row type="flex" justify="end" style="padding-bottom: 5px">
            <el-input v-model="input" placeholder="请输入题目id" style="padding-right: 5px"></el-input>
            <el-button type="primary" icon="el-icon-search" @click="handleSearch">搜索</el-button>
           </el-row>
        <el-row>
            <el-table :data="tableData" size="small"
                      height="500">
                <el-table-column prop="id" label="#" width="50px"/>
                <el-table-column prop="title" label="题目名称">
                    <template slot-scope="scope">
                        <a @click="handleOj(scope.$index, scope.row)">{{ scope.row.title }}</a>
                    </template>
                </el-table-column>

                <el-table-column prop="time_limit" label="时间限制"/>
                <el-table-column prop="memory_limit" label="空间限制"/>
                <el-table-column prop="submission_number" label="提交数"/>
                <el-table-column prop="ac_number" label="Ac数"/>
                <el-table-column prop="ac_rate" label="Ac率"/>
                <el-table-column prop="ac" label="状态" :formatter="acStatus"/>




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
        name: "RegularProblemList",
        data() {
            return {
                currentpage: 1,
                pagesize: 20,
                totalProblem: 0,
                input: "",


                tableData:[{


                    id: 1,
                    title: "a + b problem",
                    time_limit: 1000,
                    memory_limit: 1,
                    submission_number: 105,
                    ac_number: 87,
                    ac_rate: 0.83,
                    ac: false,

                }],

            }
        },
        methods: {
            acStatus(row){
                if (!row.ac) {
                    return '未通过'
                } else  {
                    return '通过'
                }
            },
            getData(limit, offset) {                //获取数据
                this.$axios({
                    method: 'get',
                    url: '/api/problem_list/',
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
            handleOj(index, row) {
                sessionStorage.setItem("ProblemId",row.id);
                this.$router.push("/SingleOj");
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
                    url: '/api/problem_list/',
                    params: {
                        id:this.input
                    }
                }).then(response=>{
                    if(response.data.code==null){
                        console.log(response.data.data);

                        this.currentpage=1;
                        this.totalProblem=1;
                        this.tableData=response.data.data;
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