<!--排名界面-->
<template>
  <el-card v-loading="loading">
    <el-row>
      <el-table :data="tableData" size="small" >
        <el-table-column prop="rank" label="排名"></el-table-column>
        <el-table-column prop="nickname" label="用户昵称"></el-table-column>
        <el-table-column prop="battle_score" label="分数"></el-table-column>
        <el-table-column prop="battle_win" label="胜利场次"></el-table-column>
        <el-table-column prop="battle_lose" label="失败场次"></el-table-column>
        <el-table-column prop="rate" label="胜利率"></el-table-column>
      </el-table>
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="currentpage"
        :page-sizes="[5,10, 20, 30, 50]"
        :page-size="pagesize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="totaluser"
      ></el-pagination>
    </el-row>
  </el-card>
</template>

<script>
    export default {
        name: "Rank",
        data() {
            return {
                currentpage: 1,
                pagesize: 10,
                totaluser: 0,
                tableData: [
                  {
                    nickname: "rootroot",
                    battle_score: 1500,
                    battle_win: 0,
                    battle_lose: 0,
                    rank: 1,
                    rate: 0.0
                  }
                ],


                loading: true,
            };
        },
        methods: {

            getData(limit, offset) {


                this.$axios
                this.$axios({
                    method: 'get',
                    url: '/api/rank/',
                    params: {
                        size: limit,
                        page: offset
                    }
                }).then(response => {
                    console.log(response.data);
                    this.tableData = response.data.data;
                    this.totaluser = response.data.total;
                    this.loading = false;
                })
                    .catch(error => {
                      this.loading = false;
                      this.$message.error("服务器错误，获取数据失败");
                      console.log(
                            "服务器错误！" + "(" + JSON.stringify(error) + ")"
                        );
                    });
            },
            handleSizeChange(val) {
                this.pagesize = val;
                this.getData(this.pagesize, this.currentpage);
            },
            handleCurrentChange(val) {
                this.currentpage = val;
                this.getData(this.pagesize, this.currentpage);
            }
        },
        created() {
          this.getData(this.pagesize, this.currentpage);
        }
    };
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>

</style>
