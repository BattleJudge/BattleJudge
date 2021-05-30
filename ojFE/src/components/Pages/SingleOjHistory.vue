<template>
    <div> <!-- 提交记录表格 -->
        <el-row type="flex" justify="center">
        <el-card style="width: 80%">
            <el-table :data="tableData" size="small"
                      height="500" @row-click="rowClick">

                <el-table-column prop="create_time" label="提交时间"/>

                <el-table-column prop="language" label="语言"/>
                <el-table-column prop="result" label="结果" :formatter="resultFormat"/>
                <el-table-column prop="static_info.time_cost" label="时间消耗(单位ms)"/>
                <el-table-column prop="static_info.memory_cost" label="空间消耗（单位MB）" :formatter="memory_costFormat"/>


            </el-table>

        </el-card>

        </el-row>

        <el-pagination
                @size-change="handleSizeChange"
                @current-change="handleCurrentChange"
                :current-page="currentpage"
                :page-sizes="[10, 15,20, 25]"
                :page-size="pagesize"
                layout="total, sizes, prev, pager, next, jumper"
                :total="total"
        ></el-pagination>
        <el-button type="primary" @click="handleBack" >返 回</el-button>
        <!-- 对话框，点击某条提交记录后弹出，查看提交的代码 -->
        <Modal v-model="modal1"
               title="code">
            <pre> {{text}} </pre>
        </Modal>
    </div>

</template>

<script>

    export default {
        name: 'SingleOjHistory',
        data() {
            return {
                currentpage: 1,
                pagesize: 20,
                total: 0,

                loading: false,
                modal1: false,

                text: "",
                tableData: [{
                    create_time:"2021-02-23 20:00:21",
                    result:0,
                    static_info:{
                        time_cost:3,
                        memory_cost:4,
                    },
                    code:'5',
                    language:"C++"
                }],
            }
        },

        methods: {

            memory_costFormat(row){
                if(row.result!=-2)
                return Math.round(row.static_info.memory_cost/(1024*1024))
                else return "";
            },
            resultFormat(row){
                switch (row.result) {
                    case -2:return "编译错误";
                    case -1:return "答案错误";
                    case 0: return "正确";
                    case 1:return "超时";
                    case 2:return "超时";
                    case 3:return "内存溢出";
                    case 4:return "运行时错误";
                    case 5:return "系统错误";
                }
            },
            // on-row-click有两个返回值：行内容和行号（从0开始）
            rowClick(row) {

                this.text = row.code;
                // 弹对话框显示代码
                this.modal1 = true;
            },
            handleBack(){
              this.$router.replace("/SingleOj");
            },
            getData(limit, offset) {                //获取数据
                this.$axios({
                    method: 'get',
                    url: '/api/submission_list/',
                    params: {
                        pro_id:sessionStorage.getItem("ProblemId"),
                        size: limit,
                        page: offset
                    }
                }).then(response => {
                    if(response.data.detail!=""){
                        console.log(response.data);
                        this.tableData = response.data.data;
                        this.total = response.data.total;
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

            handleSizeChange(val) {
                this.pagesize = val;
                this.currentpage=1;
                this.getData(this.pagesize, this.currentpage);
            },
            handleCurrentChange(val) {
                this.currentpage = val;
                this.getData(this.pagesize, this.currentpage);
            },

        },
        mounted() {
            this.getData(this.pagesize,this.currentpage);

        }
    }
</script>

<style>
</style>
