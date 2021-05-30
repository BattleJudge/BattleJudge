<!--历史界面-->
<template>
  <div>
    <el-card v-loading="loading">
      <el-row>
        <el-table :data="tableData" @cell-click="ProblemClick" size="small" :cell-style="ratingcolor" border
                  height="500">

          <el-table-column prop="pro_id" label="Problem Id"></el-table-column>
          <el-table-column prop="player1_nickname" label="Player1 Nickname"/>
          <el-table-column prop="player2_nickname" label="Player2 Nickname"/>
          <el-table-column prop="create_time" label="Create Time"/>
          <el-table-column prop="result" label="Winner">
            <template slot-scope="scope1">
              <div v-if="scope1.row.result!='drawn game'">
              {{ scope1.row.result }}
              </div>
              <div v-if="scope1.row.result=='drawn game'">
                平局
              </div>

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
          :total="totaluser"
        ></el-pagination>
      </el-row>
    </el-card>

  </div>
</template>

<script>


    export default {
        name: "History",

        data() {
            return {
                currentpage: 1,
                pagesize: 10,
                totaluser: 100,
                tableData: [{
                  id:"1",
                  result: "testuser2",
                  pro_id: 1,
                  create_time: "2021-03-07 10:04:23",
                  player1_nickname: "testuser1",
                  player2_nickname: "testuser2"

                }],
                loading: true
            };
        },
        methods: {
            ratingcolor({row}) {          //根据结果显示不同的样式

              if (row.result == sessionStorage.getItem("nickname"))
                return "background:#DFFFDF;font-weight: bold;";
              else if (row.result != sessionStorage.getItem("nickname")&&row.result!="drawn game")
                return 'background:#FFD9EC;font-weight: bold;';

            },
            ProblemClick(row) {//转至详细界面，显示该题目个人提交详情
              sessionStorage.setItem("Id", row.id);
              sessionStorage.setItem("pro_Id", row.pro_id);

                this.$router.push({path: '/HistoryDetail'});
            },

            getData(limit, offset) {                //获取数据
                this.$axios({
                    method: 'get',
                    url: '/api/battle_record/',
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
                this.currentpage=1;
                this.getData(this.pagesize, this.currentpage);
            },
            handleCurrentChange(val) {
                this.currentpage = val;
                this.getData(this.pagesize, this.currentpage);
            }
        },
        created() {
          // this.loading=false;
          this.getData(this.pagesize, this.currentpage);
        }
    };
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .el-carousel__item:nth-child(2n) {
    background-color: #afd1f1;
  }

  .el-carousel__item:nth-child(2n + 1) {
    background-color: #a7f5ff;
  }

  .image {
    width: 130px;
    height: 130px;
    display: block;
  }
</style>
