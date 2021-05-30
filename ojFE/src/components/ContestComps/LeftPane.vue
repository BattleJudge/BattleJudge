<template>
  <div class="LeftPane">
    <Tabs type="card">
      <TabPane label="题目描述">
        <div class="left-scroll">
          <Description ref="des"></Description> <!-- 题目描述组件 -->
        </div>
      </TabPane>
<!--      <TabPane label="提交记录">-->
<!--        <Submissions></Submissions> &lt;!&ndash; 提交记录组件 &ndash;&gt;-->
<!--      </TabPane>-->

    </Tabs>
  </div>
</template>

<script>
    // import Submissions from './Submissions.vue'
    import Description from './Description.vue'


    export default {
        name: 'LeftPane',
        components: {
            // Submissions,
            Description,
        },
        props: {},
        data() {
            return {}
        },
        methods: {}
    }
</script>

<style scoped>
  .left-scroll {
    height: 580px;
    overflow-y: auto;

  }
</style>
