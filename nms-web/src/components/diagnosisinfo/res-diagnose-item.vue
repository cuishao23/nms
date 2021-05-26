<template>
  <div>
    <div class="info"></div>
    <div class="content memory">
      <ul style="width: 100%;text-align:left">
          <li class="memory-total" id="memory_total">总数：{{ total }}GB</li>
          <li class="memory-used" id="memory_used">内存使用率：{{ userate }}%</li>
      </ul>
      <ul style="width: 100%;text-align:left;margin-bottom: 9px;">
          <li style="width: 100%;background-color:lightgray">
              <res-usage-line :percent="userate"/>
          </li>
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
    name: "res-diagnose-item",
    props: {
      total: {
        type: Number,
        required: true
      },
      userate: {
        type: Number,
        required: true
      },
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

  /* .info {
    width: 15px;
    height: 15px;
    cursor: pointer;
    margin-left: 11px;
  } */
  .info {
    display: inline-block;
    width: 50px;
    height: 50px;
    cursor: pointer;
    background-image: url(../../assets/image/ram.png);
    margin-left: 40px;
    margin-top: 15px;
    float: left;
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
    padding-top: 15px;
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
