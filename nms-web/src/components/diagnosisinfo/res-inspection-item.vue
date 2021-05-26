<template>
  <div>
    <div class="content memory">
      <ul style="width: 100%;text-align:left;margin-bottom: 9px;">
          <li style="margin-right: 5px;">内存</li>
          <li style="width: 90%;background-color:lightgray">
              <res-usage-line :percent="percent"/>
          </li>
      </ul>
      <ul style="width: 100%;text-align:left">
          <li style="margin-right: 5px;" id="memory_usage_rate">{{ percent + '%'}}</li>
          <li class="memory-used" id="memory_used">已使用：{{used}}GB</li>
          <li class="memory-total" id="memory_total">总数：{{total}}GB</li>
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
    name: "res-inspection-item",
    props: [
      "title",
      "used",
      "total"
    ],
    computed: {
      percent: function () {
        let used = Number(this.used)
        let total = Number(this.total)
        if (total === 0) {
          return 0
        }
        let percent = Math.round(used / total * 100)
        return percent
      }
    }
  }
</script>

<style scoped>
  .res-diagnose-item {
    display: block;
    margin-bottom: 56px;
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
  .res-diagnose-item > div {
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
    width: 15px;
    height: 15px;
    cursor: pointer;
    margin-left: 11px;
  }
  .section-title {
    font-size: 14px;
    color: #4e4e4e;
    font-weight: normal;
  }
  .content{
    width: 429px;
    font-size: 12px;
    margin-left: 100px;
    margin-bottom: 36px;
  }
  .memory li {
    display: inline-block;
    vertical-align: middle;
  }
  .memory-used,
  .memory-total {
    color: #8b8b8b;
  }
  .memory-total{
    float: right;
  }

</style>
