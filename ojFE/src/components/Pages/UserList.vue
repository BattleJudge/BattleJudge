<template>


    <el-card >
        <el-row type="flex"  justify="end" style="padding-bottom: 5px">
            <el-input v-model="input" placeholder="请输入用户名" style="padding-right: 5px"></el-input>
            <el-button type="primary" icon="el-icon-search" @click="handleSearch" >搜索</el-button>
            <el-button type="primary" icon="el-icon-circle-plus-outline" @click="handleAdd">添加用户</el-button>
        </el-row>
        <el-row>
            <el-table :data="tableData" size="small"
                      height="500">
                <el-table-column prop="id" label="#" width="50px"/>
                <el-table-column prop="username" label="用户名"/>


                <el-table-column prop="nickname" label="昵称"/>
                <el-table-column prop="email" label="邮箱"/>

                <el-table-column prop="role" label="角色" :formatter="roleFormat"/>



                <el-table-column label="操作" width="400" >
                    <template slot-scope="scope">


                        <el-button
                                size="mini"
                                @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
                        <el-button
                                size="mini"
                                type="danger"
                                @click="handleDelete(scope.$index, scope.row)">删除</el-button>

                    </template>
                </el-table-column>

            </el-table>
            <el-pagination
                    @size-change="handleSizeChange"
                    @current-change="handleCurrentChange"
                    :current-page="currentpage"
                    :page-sizes="[10, 15,20, 25]"
                    :page-size="pagesize"
                    layout="total, sizes, prev, pager, next, jumper"
                    :total="totaluser"
            ></el-pagination>
        </el-row>
        <UserDialog ref="userDialog"></UserDialog>
    </el-card>


</template>

<script>
import UserDialog from "../Dialog/UserDialog"
    export default {
        name: "UserList",
        components:{UserDialog},
        data() {
            return {
                currentpage: 1,
                pagesize: 20,
                totaluser: 0,
                input:"",
                tableData: [{
                    id:1,
                    username: 'qgm123',
                    nickname: 'QGM134',
                    user_type:"Regular user",
                    email:"qiugengming123@163.com",
                }]
            }
        },
        methods: {


            roleFormat(row){
                if (row.user_type === "Regular User") {
                    return '普通用户'
                } else  {
                    return '管理员'
                }

            },
            handleEdit(index, row) {
                console.log(index+"  "+row);
                this.$refs.userDialog.openEdit(row);
            },
            handleDelete(index, row) {
                console.log(index+"  "+row);
                this.$axios({
                    method: 'delete',
                    url: '/api/admin/user/',
                    params: {
                        username : row.username
                    }
                }).then(response => {
                    if(response.data.code==0){
                        this.$message.info("删除成功");
                        this.$router.go(0);
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
            },
            handleAdd(){
                this.$refs.userDialog.openAdd();

            },
            handleSearch(){
                if(this.input.length<6){
                    this.$message.error("请输入至少6个字符的用户名")
                    return;
                }
                this.$axios({
                    method: 'get',
                    url: '/api/admin/user_info_by_username/',
                    params: {
                       username : this.input
                    }
                }).then(response => {
                    if(response.data.code==0){
                        console.log(response.data.data);
                        this.currentpage=1;
                        this.totaluser=1;
                        this.tableData=[];
                        this.tableData.push(response.data.data);
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
            getData(limit, offset) {                //获取数据
                this.$axios({
                    method: 'get',
                    url: '/api/admin/user_info/',
                    params: {
                        size: limit,
                        page: offset
                    }
                }).then(response => {
                    if(response.data.detail!=""){
                    console.log(response.data);
                     this.tableData = response.data.data;
                     this.totaluser = response.data.total;
                    }else{
                        this.$message.error(response.data.detail)
                    }

                })
                    .catch(error => {
                        this.$message.error("权限不符合，请退出重登");
                        console.log(
                            "服务器错误！" + "(" + JSON.stringify(error) + ")"
                        );
                    });
            },
        },
        mounted(){

                if(sessionStorage.getItem("role")=="user"){
                    this.Admin=false;
                }else{
                    this.Admin=true;
                }

                this.getData(this.pagesize,this.currentpage);

        }

    }
</script>

<style scoped>

</style>