<template>
    <div class="res-info">
      <div v-for="(item, index) in resList" :key="index">
        <span class="title">{{ item.title }}</span>
        <div class="res-info-list">
          <res-usage-detail v-for="(detail, uIndex) in item.children" :key="uIndex"
                            :title="detail.title" :total="detail.total" :used-list="detail.usedList" class="res-info-list-item"/>
        </div>
      </div>
    </div>
</template>

<script>
    import ResUsageDetail from "./res-usage-detail";

    export default {
      components: {ResUsageDetail},
      name: "res-info",
      props: {
        resList: {
          type: Array,
          required: true
        }
      }
    }
</script>

<style scoped>
  .res-info {
    text-align: left;
  }
  .title {
    font-size: 14px;
    color: #4e4e4e;
  }
  .res-info-list {
    display: flex;
    flex-wrap: wrap;
    justify-content: flex-start;
    padding-top: 20px;
  }
  .res-info-list-item {
    margin-bottom: 30px;
  }
</style>
