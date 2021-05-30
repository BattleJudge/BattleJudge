<template>
  <div> <!-- 提交记录表格 -->
    <el-table :data="form" @cell-click="ProblemClick" size="small"
              height="500">

      <el-table-column prop="create_time" label="提交时间"></el-table-column>
      <el-table-column prop="language" label="语言"/>
      <el-table-column prop="static_info.time_cost" label="时间消耗(单位毫秒)"/>
      <el-table-column prop="static_info.memory_cost" label="内存消耗（单位B）"/>
      <el-table-column prop="result" label="结果" :formatter="resultFormat"/>



    </el-table>
    <Modal v-model="modal1"
           title="code">
      <pre> {{text}} </pre>
    </Modal>
    <el-pagination
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
            :current-page="currentpage"
            :page-sizes="[10, 15,20, 25]"
            :page-size="pagesize"
            layout="total, sizes, prev, pager, next, jumper"
            :total="total"
    ></el-pagination>
  </div>

</template>

<script>
  // import Qs from 'qs'
  export default {
        name: 'Submissions',
        data() {
            return {
              currentpage: 1,
              pagesize: 20,
              total: 0,
                loading: false,
                modal1: false,
                form:[{
                  create_time: "2021-03-07 10:04:29",
                  code: "xxx",
                  result: 0,
                  static_info: {
                    time_cost: 1,
                    memory_cost: 1564672
                  },
                  language: "C++"
                }],
                text: "",

            }
        },
        methods: {
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
            ProblemClick(row) {

                this.text = row.code;
                // 弹对话框显示代码
                this.modal1 = true;
            },

          getData(limit, offset) {     //更新提交记录
                this.$axios({
                    method: 'get',
                    url: '/api/battle_submissions/',
                  params: {
                     battle_id:sessionStorage.getItem("Id"),

                    size: limit,
                    page: offset
                  }
                }).then(response => {
                    console.log(response.data);
                    this.form = response.data.data;
                    this.total=response.data.total;

                }).catch(failResponse => {
                  console.log(failResponse+"   获取提交记录失败");
                })
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
              this.getData(this.pagesize,this.currentpage)
        }
    }
</script>

<style>
</style>
