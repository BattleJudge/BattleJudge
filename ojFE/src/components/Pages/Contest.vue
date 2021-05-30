<!--对局界面-->
<template>
    <div>
        <!--    退出的提示-->
        <el-dialog title="提示" :visible.sync="dialogVisible" width="30%">
            <span>{{message}}</span>
            <span slot="footer" class="dialog-footer">
                <el-button type="primary" @click="dialogVisible = false">确 定</el-button>
                <el-button @click="showCode" v-if="message.indexOf('对方成功解答') >= 0">查看对方代码</el-button>
            </span>
        </el-dialog>

        <el-dialog
                title="提示"
                :visible.sync="quitVisible"
                width="30%"
        >
            <span>{{message}}</span>
            <span slot="footer" class="dialog-footer">
                    <el-button @click="quitVisible = false">取 消</el-button>
                     <el-button type="primary" @click="quit">确 定</el-button>
               </span>
        </el-dialog>


        <!--    匹配结果的显示-->
        <Modal v-model="codeShow"
               title="code">
            <pre> {{content}} </pre>
        </Modal>


        <div class="Contest">
            <ContestLayout> <!-- 布局 -->
                <div class="demo-split"> <!-- 分割面板 -->
                    <Split v-model="split1" :min="'300px'" :max="'400px'">
                        <div slot="left" class="demo-split-pane">
                            <LeftPane ref="left"></LeftPane> <!-- 左面板 -->
                        </div>
                        <div slot="right" class="demo-split-pane">
                            <RightPane></RightPane> <!-- 右面板 -->
                        </div>
                    </Split>
                </div>
            </ContestLayout>

        </div>

        <Heart ref="Heart"></Heart>
    </div>
</template>
<script>

    import Heart from "../Utils/Heart"
    import ContestLayout from '../ContestComps/ContestLayout.vue'
    import LeftPane from '../ContestComps/LeftPane.vue'
    import RightPane from '../ContestComps/RightPane.vue'
    import PubSub from 'pubsub-js'


    export default {

        name: 'Contest',
        components: {
            Heart,
            ContestLayout,
            LeftPane,
            RightPane
        },
        data() {
            return {
                split1: 0.5, // 从中间分开
                // tag: 1,
                dialogVisible: false,         //消息提示框显示
                quitVisible: false,             //中途退出提示框
                battle_id: "",
                competitor_id: "",
                competitor_username: "",
                problem_id: "",
                message: "",
                gameId: "",
                end: 1,                 //0代表比赛结束，1代表仍然在比赛
                tag: 0,                  //0代表连接未关闭，1代表已经关闭
                codeShow: false,
                content: ""
            }
        },
        methods: {
            showCode() {
                this.codeShow = true;
                this.dialogVisible = false
            },
            heart_open() {
                console.log("heart open")
                this.$refs.Heart.initWebSocket();//调用子组件，开启心跳
            },

            quit() {                                                 //退出返回到个人信息界面
                // this.tag = 0;
                this.dialogVisible = false;
                this.$router.replace({path: '/Information'});
                // this.$router.go(0)
                if (this.tag == 0)
                    this.$refs.Heart.sendQuitMessage();
            },


        },

        // destroyed() {
        //     console.log("destroyed")
        //     if (this.tag == 1) {
        //         this.$refs.Heart.sendQuitMessage();
        //     }
        // },
        mounted() {                                  // 初始化时 订阅相应的消息

            this.heart_open();
            PubSub.unsubscribe('cancelCompete');
            PubSub.subscribe("cancelCompete", (msg, data) => {     //退出，判断比赛是否结束
                console.log(msg + "  " + data);
                this.quit();
            });

            PubSub.unsubscribe('quit');
            PubSub.subscribe("quit", (msg, data) => {     //退出，判断比赛是否结束
                if (this.end == 1) {
                    console.log(msg + "  " + data);
                    this.message = "是否要退出比赛"
                    this.quitVisible = true;
                } else {
                    this.quit();
                }
            });
            PubSub.unsubscribe('Complete');
            PubSub.subscribe("Complete", (msg, data) => {   //对方成功解答
                console.log(msg + " " + data);
                this.message = "对方成功解答，请点击quit返回";
                this.tag = 1;
                this.$refs.Heart.sendQuitMessage();
                this.content = data;
                this.end = 0;
                this.dialogVisible = true;
            });
            PubSub.unsubscribe('Draw');
            PubSub.subscribe("Draw", (msg, data) => {       //对方弃局
                console.log(msg + " " + data);
                this.message = "对方放弃对局，本场比赛为平局，请点击quit返回";
                this.tag = 1;
                this.$refs.Heart.sendQuitMessage();
                this.end = 0;
                this.dialogVisible = true;
            });
            PubSub.unsubscribe('Success');
            PubSub.subscribe("Success", (msg, data) => {    //成功运行
                console.log(msg + " " + data);

                this.$message.success("运行成功，请点击quit返回");
                this.tag = 1;
                this.$refs.Heart.sendQuitMessage();
                this.end = 0;

            })
            PubSub.unsubscribe('SendCode1');
            PubSub.subscribe("SendCode1", (msg, data) => {  //提交代码,判断比赛是否结束
                console.log(msg + " " + data);
                if (this.end == 0) {
                    this.$message.info("比赛已经结束，请点击quit返回")
                } else {
                    PubSub.publish("SendCode2", data);
                }
            });

        }

    }
</script>
<style scoped>
    .demo-split {
        height: 650px;
        border: 1px solid #dcdee2;
    }

    .demo-split-pane {
        padding: 10px;
    }
</style>
