<template>
  <div class="description" style="text-align:left">
    <div class="problem-title">
      {{ form.id }}.{{form.title}}
    </div>
    <Divider/>

    <div>
      题目描述：
      <div class="retract">
      <markdown-it-vue  class="md-body" :content="form.description"/>
      </div>
    </div>
    <br/>

    <div>
      <div class="tag">输入描述：</div>
      <div class="retract" >
        <markdown-it-vue class="md-body" :content="form.input_description"/>
      </div>
    </div>
    <br/>


    <div>
      <div class="tag">输出描述：</div>
      <div class="retract" >
        <markdown-it-vue class="md-body" :content="form.output_description"/>
      </div>
    </div>
    <br/>

    <div>
      <el-form label-width="100px"  v-for="(item, index) in form.samples" :key="index" style="width: 100%">
        示例{{index+1}}
        <br/>
        <div class="retract">
          输入：<div style="white-space: pre-line;">{{item.input}}</div>
        <br/>
        输出：<div style="white-space: pre-line;">{{item.output}}</div>
        <br/>
        <br/>
        </div>

      </el-form>


    </div>

    <div>
      难度：<br/>
      <div class="retract">{{ form.difficulty }}</div>
    </div>
    <br/>

    <div>
      ac次数：<br/>
      <div class="retract">{{ form.ac_number }}</div>
    </div>
  </div>
</template>

<script>

  import MarkdownItVue from 'markdown-it-vue'
  import 'markdown-it-vue/dist/markdown-it-vue.css'
    export default {
        name: 'Description',
      components: {
        MarkdownItVue
      },
        data() {
            return {
              form:{
                id: 1,
                title: 'a + b problem',
                description: '1',
                input_description: '2',
                output_description: '3',
                samples: [{'input': '1 1', 'output': '2'}, {'input': '1 2', 'output': '3'}],
                hint: '无',
                problem_source: 'root',
                time_limit: 1000,
                memory_limit: 128,
                tags: "{'简单'}",
                difficulty: '中等',
                submission_number: 39,
                ac_number: 23
              },
            }
        },
        methods: {

        },
      mounted(){
          // console.log("hello description")
          // console.log(JSON.parse(sessionStorage.getItem("ProblemInformation")))
         this.form=JSON.parse(sessionStorage.getItem("ProblemInformation"));
          console.log(this.form);

      }
    }
</script>

<style scoped>
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
