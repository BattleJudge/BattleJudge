<template>
  <div class="RightPane">
    <div class="first-section">
      <div class="lan">Language: {{tag}}</div>
      <el-dropdown>
        <Button type="primary">
          Language<i class="el-icon-arrow-down el-icon--right"></i>
        </Button>
        <el-dropdown-menu slot="dropdown">
          <el-dropdown-item @click.native="deal_language_C">C</el-dropdown-item>
          <el-dropdown-item @click.native="deal_language_C_Plus">C++</el-dropdown-item>

        </el-dropdown-menu>
      </el-dropdown>
      <Button @click="reset">reset</Button>
      <Button style="background-color: #ed4014" @click="quit">quit</Button>
    </div>
    <Divider/>

    <div class="second-section"> <!-- 代码区 -->
      <codemirror v-model="Send_Info.code" :options="cmdOptions" align="left" @ready="cmReady"
                  ref="codeMirror" style="touch-action: none"></codemirror>
    </div>



    <Divider class="divider-below"/>
    <div class="three-btn">
      <Button class="btnSub" @click="subClick" type="primary">提交</Button>
    </div>

  </div>
</template>

<script>
    import {
        codemirror
    } from 'vue-codemirror'
    import PubSub from 'pubsub-js'


    require("codemirror/lib/codemirror.css");
    require("codemirror/theme/base16-light.css");
    require("codemirror/mode/clike/clike");
    require("codemirror/mode/python/python")
    require("codemirror/addon/edit/matchbrackets.js")


    export default {
        name: 'RightPane',
        components: {
            codemirror
        },
        data() {
            return {
                language_mode: 'text/x-c++src',
                cmdOptions: {
                    tabSize: 4, //tab空格数
                    mode: "text/x-c++src",      //c++
                    lineNumbers: true, //显示行号
                    theme: "base16-light", //主题
                    matchBrackets: true, //括号匹配
                },
                Send_Info: {
                    op:"submit",
                    code: "",
                    language: "C++",
                },

                iconType: "md-arrow-dropdown", // 控制台右边的icon
                testCase: '', // 获得输入的测试用例
                execResult: '/* 执行代码之后返回的结果 */', // 执行代码结果
                tag: "C++",


            }
        },
        methods: {
            deal_language_C() {
                this.tag = "C"
                this.Send_Info.language = "C";

            },
            deal_language_C_Plus() {
                this.tag = "C++";
                this.Send_Info.language = "C++";

            },


            reset() {
                this.Send_Info.code = ``;
            },
            quit() {
                PubSub.publish("quit", "");
            },
            cmReady() {
                this.$refs.codeMirror.codemirror.setSize('100%', '540px')
            },
            subClick() {
                console.log(this.Send_Info);
                PubSub.publish("SendCode1", this.Send_Info);
            },

        }
    }
</script>

<style scoped>
  .first-section {
    height: 10px;
    text-align: left;
  }

  .lan {
    margin: 5px 15px;
    font-size: 15px;
    display: inline-block;
  }

  /*.first-section button {*/
  /*	color: #5B6270;*/
  /*	background-color: #F5F7F9;*/
  /*	font-size: 17px;*/
  /*	display: inline-block;*/
  /*	position: absolute;*/
  /*	right: 30px;*/
  /*	top: 5px;*/

  /*}*/

  .second-section {
    margin-top: -18px;
    margin-bottom: -15px;
  }

  .console {
    z-index: 15;
    position: absolute;
    bottom: 50px;
    height: 220px;
    width: 100%;
    background-color: #fff;
  }

  .card {
    height: 220px;
  }

  .card-input {
    margin-top: -10px;
    height: 160px;
    width: 100%;
    border: 1px #D7DDE4 solid;
    resize: none
  }

  .card-input:focus {
    border: .5px solid darkgrey;
    outline: none;
  }

  .divider-below {
    position: absolute;
    top: 575px;
  }

  .btnRun, .btnSub {
    margin-right: 20px;
    padding: 5px;
    font-size: 16px;
    width: 120px;
  }

  .btnRun {
    position: absolute;
    right: 130px;
    bottom: 8px;
  }

  .btnSub {
    position: absolute;
    right: 0;
    bottom: 8px;
  }

  .btnConsole {
    position: absolute;
    left: 10px;
    bottom: 8px;
    width: 100px;
    font-size: 16px;
  }
</style>
