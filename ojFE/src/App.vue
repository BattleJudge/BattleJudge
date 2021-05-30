<template>
    <div id="app">
        <!--导航栏-->
        <div v-if="$route.meta.keepAlive">
            <el-menu :default-active="$route.path"
                     mode="horizontal"
                     v-bind:router="true"
                     id="nav"
            >

                <el-menu-item index="/Information">
                    <i class="el-icon-user"></i>个人信息
                </el-menu-item>
                <el-menu-item index="/Regular/Problem/List" >
                    题目列表
                </el-menu-item>

                <el-menu-item index="/history">
                    <i class="el-icon-tickets"></i>pk历史
                </el-menu-item>

                <el-menu-item index="/Rank">
                    <i class="el-icon-star-on"></i>排名
                </el-menu-item>

                <el-menu-item index="/Problem/List" v-if=Admin>
                    <i class="el-icon-s-order"></i>题库
                </el-menu-item>



                <el-menu-item index="/Contest">
                    <i class="el-icon-c-scale-to-original"></i>PK
                </el-menu-item>


                <el-menu-item index="/User/List" v-if=Admin>
                    用户管理
                </el-menu-item>


                <el-button type="primary"
                           style="margin-top:-14px; height:80px; width: 10%;background: #ca1f1d;border: none; float: right;"
                           v-on:click="LogOutClick">Logout
                </el-button>
                <!--        <el-button type="primary"-->
                <!--                   style="margin-top:-14px; height:80px; width: 30%;background: #285eca;border: none; float: right;"-->
                <!--                   v-on:click="PkClick">PK-->
                <!--        </el-button>-->


            </el-menu>

            <router-view></router-view>

        </div>
        <!--内容界面-->
        <router-view v-if="!$route.meta.keepAlive"></router-view>


    </div>

</template>

<script>
    import PubSub from "pubsub-js"
    //
    // import Login from "./components/Pages/Login"
    // import food from "./components/Pages/Contest"

    export default {
        name: 'App',
        data() {
            return {
                Admin: false,
            }
        },

        methods: {
            PkClick() {
                this.$router.replace("/Loading");
            },
            LogOutClick() {
                this.$store.commit('LOGOUT');
                this.$router.replace("/")
            }

        },
        mounted() {

            PubSub.subscribe("Login", () => {
                if (sessionStorage.getItem("role") == "user") {
                    this.Admin = false;
                } else {
                    this.Admin = true;
                }
            })
          if (sessionStorage.getItem("role") == "user") {
            this.Admin = false;
          } else {
            this.Admin = true;
          }
        }
    }
</script>

<style>

    #app {
        font-family: 'Avenir', Helvetica, Arial, sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        text-align: center;
        color: #2c3e50;
        margin-top: 0px;
    }

    vue-particles {
        color: #dedede;
        particleOpacity: 0.7;
        particlesNumber: 1000;
        shapeType: "circle";
        particleSize: "4";
        linesColor: #dedede;

        clickMode: push;
    }

</style>
