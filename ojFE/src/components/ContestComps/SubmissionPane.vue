<template>
  <div class="LeftPane">
    <Tabs type="card">
      <TabPane label="题目描述">
        <div class="left-scroll">
          <SubmissionHistory ref="des"></SubmissionHistory> <!-- 题目描述组件 -->
        </div>
      </TabPane>
      <TabPane label="提交记录">
        <Submissions></Submissions> <!-- 提交记录组件 -->
      </TabPane>

    </Tabs>
  </div>
</template>

<script>
    import Submissions from './Submissions.vue'
    import SubmissionHistory from './SubmissionHistory.vue'


    export default {
        name: 'LeftPane',
        components: {
            Submissions,
            SubmissionHistory
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
