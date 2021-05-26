<template>
  <div>
    <div class="info"></div>
    <div class="content memory">
      <ul style="width: 100%;text-align:left">
          <li class="memory-total" id="memory_total">总数：{{totalnum}}GB</li>
          <li class="memory-used" id="memory_used">已使用：{{usednum}}%</li>
      </ul>
      <ul style="width: 100%;text-align:left;padding-top: 9px;">
          <li style="width: 100%;background-color:lightgray">
              <res-usage-line :percent="usedpercent"/>
          </li>
      </ul>
      <ul style="width: 100%;text-align:left; padding-top: 9px;">
          <li class="memory-total" id="memory_total">使用寿命：{{totalday}}%</li>
          <li class="memory-used" id="memory_used">使用率：{{usedpercent}}%</li>
      </ul>
    </div>
  </div>
</template>

<script>
  import ResUsageLine from "components/common/res-usage-line";

  export default {
    components: {ResUsageLine},
    data() {
      return {
      }
    },
    name: "res-info-item",
    props: {
      usednum: {
        type: String,
        required: true
      },
      totalnum: {
        type: String,
        required: true
      },
      usedpercent: {
        type: Number,
        required: true
      },
      totalday: {
        type: String,
        required: true
      }
    }
  }
</script>

<style scoped>
  .res-info-item {
    display: block;
    margin-bottom: 56px;
    float: right;
    width: 400px;
  }

  .use-total {
    font-size: 12px;
    color: #8b8b8b;
  }

  .res-info-item__tip {
    text-align: left;
  }

  .used {
    float: left;
  }

  .total {
    float: right;
  }
  .use-percent {
    display: block;
    float: right;
    color: #4e4e4e;
    font-size: 12px;
  }
  .res-info-item > div {
    margin-bottom: 5px;
  }

  h4 {
    float: left;
    font-size: 12px;
    font-weight: normal;
    color: #4e4e4e;
    margin-bottom: 9px;
  }

  .info {
    display: inline-block;
    width: 50px;
    height: 50px;
    cursor: pointer;
    background-image: url(../../assets/image/dist.png);
    margin-left: 40px;
    margin-top: 15px;
    float: left;
  }
  .total_num {
    float: right;
    font-size: 12px;
    color: #8b8b8b;
  }
  .content{
    width: 429px;
    font-size: 12px;
    margin-left: 100px;
    margin-bottom: 36px;
    padding-top: 15px;
  }
  .memory-used, .memory-total {
    color: #8b8b8b;
  }
  .memory-total {
    float: right;
  }
</style>
