<template>
  <div > <!-- 提交记录表格 -->

    <ul v-for="(ele,index) in tableData" :key="ele.id" ref="index">
      <el-row type="flex" class="row-bg" justify="center">

      <el-card style="margin-top: 10px;width: 70%; text-align: start">
        <div>
        <el-row style="font-size: 15px" type="flex" class="row-bg" :gutter="20">
          <el-col :span="18">
          <pre>作者：{{ele.author}}     更新时间：{{ele.last_update_time}}</pre>
          </el-col>


          <el-col :span="2" style="margin-left: 100px">
          <a  @click="Expand(index)" style="font-size: 20px; color: #2db7f5;">{{active==index ? "收起":"展开" }}</a>
          </el-col>
        </el-row>
        </div>
        <div :style="{'height': (active==index? '': '10px')}">
          <markdown-it-vue class="md-body" :content="ele.content"/>
        </div>

      </el-card>
      </el-row>
    </ul>

    <el-pagination
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
            :current-page="currentpage"
            :page-sizes="[10, 20, 30, 1]"
            :page-size="pagesize"
            layout="total, sizes, prev, pager, next, jumper"
            :total="totalSolution"
    ></el-pagination>
    <el-button @click="handleBack">返 回</el-button>
  </div>

</template>

<script>

  import MarkdownItVue from 'markdown-it-vue'
  import 'markdown-it-vue/dist/markdown-it-vue.css'




  export default {

        name: 'SingleSolution',
    components: {
      MarkdownItVue
    },

        data() {
            return {
              active: -1,



              currentpage: 1,
              pagesize: 10,
              totalSolution: 50,

              Solution_username:"",
              Solution: "",

              modal1: false,
              loading: false,

              input:"",
              tableData: [{
                  id:1,
                author:"ti222222222m",
                content: '# your markdown content' +
                        '![gvf](http://www.aqcoder.com/gvf-project.png =x50)\n' +
                        '![ravenq](http://www.aqcoder.com/ravenq-qr.png =50x50)\n' +
                        '\n' +
                        '## GitHub Table of Contents\n' +
                        '\n' +
                        '[toc]\n' +
                        '\n' +
                        'Note: Only `h2` and `h3` are shown in toc.\n' +
                        '\n' +
                        '## alter\n' +
                        '\n' +
                        'Markup is similar to fenced code blocks. Valid container types are `success`, `info`, `warning` and `error`.'
                        ,
                last_update_time :"2017-04-09 16:15:26"
              }
              ]
            }
        },
        methods: {
          Expand(index){
            if(this.active!=index){
              this.active=index;
            }else{
              this.active=-1;
            }
          },
            // on-row-click有两个返回值：行内容和行号（从0开始）

          handleSizeChange(val) {
            this.active=-1;
            this.pagesize = val;
            this.getData(this.pagesize, this.currentpage);
          },
          handleCurrentChange(val) {
            this.active=-1;
            this.currentpage = val;
            this.getData(this.pagesize, this.currentpage);
          },
          getData(limit, offset) {                //获取数据
            this.$axios({
              method: 'get',
              url: '/api/solution_list/',
              params: {
                pro_id:sessionStorage.getItem("ProblemId"),
                size: limit,
                page: offset
              }
            }).then(response => {

              if(response.data.total>=0){
                console.log(response.data);
                this.tableData = response.data.data;
                this.totalSolution = response.data.total;
              }

            }).catch(error => {
                      this.$message.error("服务器错误，获取数据失败");
                      console.log(
                              "服务器错误！" + "(" + JSON.stringify(error) + ")"
                      );
                    });
          },
          handleBack(){
            this.$router.replace("/SingleOj")
          }

        },
        mounted() {
          this.getData(this.pagesize, this.currentpage);
        }
    }
</script>

<style>
  .head{
    font-size: 25px;
    font-weight: bolder;
  }
  .content {
    margin-left: 15px;
    font-size: 20px;
  }
</style>
