<template>
    <div>
        <div style="height: 500px" v-if="loading==true">
            <div class="Loading-container"
                 v-loading="loading"
                 element-loading-text="匹配对手中"
                 element-loading-spinner="el-icon-loading">

            </div>
            <el-button type="primary" @click="cancel">取消</el-button>
        </div>
        <div v-if="!loading" class="layout">
            <Layout> <!-- 头部（默认的还没改 -->
                <Header class="layout-head" :style="{position: 'fixed', width: '100%'}">
                    <Menu mode="horizontal" theme="dark" active-name="1">

                    </Menu>
                </Header>
                <!-- 主体 -->
                <Content class="layout-content"
                         :style="{margin: '78px 10px 0', background: '#fff', minHeight: '500px'}">
                    <slot></slot> <!-- 插入分割面板 -->
                </Content>
            </Layout>
        </div>
    </div>
</template>

<script>
    import PubSub from 'pubsub-js'

    export default {
        name: 'ContestLayout',
        data() {
            return {
                loading: true,
            }
        },
        methods: {
            cancel() {
                this.loading = false;
                PubSub.publish("cancelCompete", "");
            },
        },
        mounted() {
            // this.UpdateRecord();
            PubSub.unsubscribe('getCompetitor1');
            PubSub.subscribe("getCompetitor1", (msg, data) => {           //Heart提交时发出更新记录的消息
                console.log(msg);
                this.$message.success("匹配到的对手是" + data)
                this.loading = false;
            })

        }


    }
</script>

<style scoped>
    .layout {
        border: 1px solid #d7dde4;
        background: #f5f7f9;
        position: relative;
        border-radius: 4px;
        overflow: hidden;

    }

    .layout-head {
        z-index: 15;
    }

    .layout-logo {
        width: 100px;
        height: 30px;
        background: #5b6270;
        border-radius: 3px;
        float: left;
        position: relative;
        top: 15px;
        left: 20px;
    }

    .layout-nav {
        width: 420px;
        margin: 0 auto;
        margin-right: 20px;
    }

    .layout-content {
    }

    .Loading-container {
        border-radius: 50px;
        background-clip: padding-box;
        margin: 90px auto;
        width: 350px;
        padding: 35px 35px 15px 35px;
        background: #ffffff;
        border: 1px solid #eaeaea;
        box-shadow: 0 0 25px #cac6c6;
    }
</style>
