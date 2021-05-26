<template>
  <div>
    <div class="info"></div>
    <div style="display: inline-block; width: 10px"></div>
    <div class="res-info-item">
      <div class="res-info-item__tip">
        <span class="use-total">
            <span>已使用：</span>
            <span>{{usednum + 'GB'}}</span>
        </span>
        <span class="total_num">
            <span>总数：</span>
            <span>{{totalnum + 'GB'}}</span>
        </span>
      </div>
      <res-usage-line :percent="usedpercent"/>
      <div class="use-total">
          <span class="used">
            <span>已使用：</span>
            <span>{{usedpercent + '%'}}</span>
          </span>
          <span class="total">
            <span v-if="totalday">使用寿命：{{totalday}}%</span>
          </span>
      </div>
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
    height: 60px;
    cursor: pointer;
    background-image: url(../../../assets/image/dist.png);
    /* margin-left: 11px; */
    float: left;
  }
  .total_num {
    float: right;
    font-size: 12px;
    color: #8b8b8b;
  }
</style>
