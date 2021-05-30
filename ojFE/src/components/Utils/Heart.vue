<!--心跳机制-->
<template>
  <div>
    <!--    <h1> websocket 心跳机制测试：{{data}}</h1>-->
  </div>
</template>

<script>
  import PubSub from 'pubsub-js'
    export default {
        name: 'Heart',
        data() {
            return {
                gameId: "",
                data: 0,
                lockReconnect: false,//是否真正建立连接
                timeout: 7 * 1000,//10秒一次心跳（有误差）
                // timeoutObj: null,//心跳心跳倒计时
                // serverTimeoutObj: null,//心跳倒计时
                // timeoutnum: null,//断开 重连倒计时
                websocket: null,
                tonken: true,

            }
        },

        methods: {
            initWebSocket() {

                let url = "后台链接";

                this.websocket = new WebSocket(url)
                // 连接错误
                this.websocket.onerror = this.setErrorMessage
                // 连接成功
                this.websocket.onopen = this.setOnopenMessage
                // 收到消息的回调
                this.websocket.onmessage = this.setOnmessageMessage
                // 连接关闭的回调
                this.websocket.onclose = this.setOncloseMessage
                // 监听窗口关闭事件，当窗口关闭时，主动去关闭websocket连接，防止连接还没断开就关闭窗口，server端会抛异常。
                window.onbeforeunload = this.onbeforeunload

              // this.$router.afterEach( function () {
              //   this.websocket.close()
              // })
            },


            sendQuitMessage() {              //发送退出请求
              this.closeWebSocket();
            },
          dealResult( result){
            console.log("result   "+result);
            switch (result) {
              case -2:return "编译错误";
              case -1:return "答案错误";
              case 1:return "超时";
              case 2:return "超时";
              case 3:return "内存溢出";
              case 4:return "运行时错误";
              case 5:return "系统错误";
            }
          },
            setOnmessageMessage(event) {                   //获取服务器返回的信息
                var data = JSON.parse(event.data)
              console.log(data)
              if(data.code=="0"){
                if(data.msg!="connect success"){
                  if(data.msg=="draw"){
                    PubSub.publish("Draw", data.msg);//对方放弃比赛
                  }else if(data.msg=="lose"){
                    PubSub.publish("Complete", data.data.winner_code);//对方成功提交
                  }else if(data.msg=="submit success"){
                    if(data.data.result==0){
                      PubSub.publish("Success", data.data.result);//用户提交成功
                    }else{
                      this.$message.error(this.dealResult(data.data.result));
                    }
                  }
                }else if(data.msg=="connect success"){
                  if(data.data.problem_data!=null){
                     // console.log(data.data.problem_data)
                    sessionStorage.setItem("ProblemInformation",JSON.stringify(data.data.problem_data))
                    // PubSub.publish("getProblemInformation", data.data.problem_data);
                    PubSub.publish("getCompetitor1", data.data.opponent_info.nickname);
                  }
                }
              }

            },
            setErrorMessage() {                                //发生错误，重连
              this.closeWebSocket();
                console.log("WebSocket连接发生错误" + '   状态码：' + this.websocket.readyState)
            },
            setOnopenMessage() {                               //开启心跳
                console.log("WebSocket连接成功" + '   状态码：' + this.websocket.readyState)

            },
            SendCode(data) {
              console.log(data);
                this.websocketsend(JSON.stringify(data))
            },
            setOncloseMessage() {

                clearTimeout(this.timeoutObj);
                clearTimeout(this.serverTimeoutObj);
                console.log("WebSocket连接关闭" )

            },
            onbeforeunload() {
                this.closeWebSocket();
            },
            websocketsend(messsage) {                       //websocket发送消息
                    this.websocket.send(messsage)
            },
            closeWebSocket() {                              // 关闭websocket
              if(this.websocket)
              this.websocket.close();

            },

        },
        mounted() {
            let beginTime = 0;
            let differTime = 0;

            window.onunload = function () {                   //根据时间差区别刷新和关闭
                differTime = new Date().getTime() - beginTime;
                if (differTime <= 5) {
                    this.sendQuitMessage();
                }
            }
            window.onbeforeunload = function () {
                beginTime == new Date().getTime() - beginTime;
            }
          PubSub.unsubscribe('SendCode2');
            PubSub.subscribe("SendCode2", (msg, data) => {
                this.SendCode(data);
                // PubSub.publish("UpdateRecord", "");            //更新提交记录
            });

        }
    }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
