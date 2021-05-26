<template>
  <div class="res-usage-detail" :style="{width: width + 'px'}">
    <res-usage-circle :percent="percent" class="percent-chart"/>
    <dl class="res-usage-detail-info">
      <dt>{{ title }}</dt>
      <dd v-for="(item, index) in usedList" :key="index">
        {{ item.text + ':'}}
        <span>{{item.used}}</span>
      </dd>
      <dd>
        可用资源：
        <span>{{ total }}</span>
      </dd>
    </dl>
  </div>
</template>

<script>
  import ResUsageCircle from "./res-usage-circle";

  export default {
    components: {ResUsageCircle},
    name: "res-usage-detail",
    data() {
      return {}
    },
    props: {
      title: {
        type: String,
        required: true
      },
      total: {
        type: Number,
        required: true
      },
      usedList: {
        type: Array,
        required: true
      },
      width: {
        default: function () {
          return 224;
        }
      }
    },
    computed: {
      percent: function () {
        let used = 0;
        for (let i = 0; i < this.usedList.length; i++) {
          used += this.usedList[i].used;
        }
        if (used === 0) {
          return 0;
        } else {
          return Math.round(used / (this.total + used) * 100);
        }
      }
    }
  }
</script>

<style scoped>
  .res-usage-detail {
    display: flex;
    justify-content: flex-start;
  }

  .percent-chart {
    margin-top: 0px;
  }

  dt {
    color: #4e4e4e;
    font-family: "Microsoft YaHei";
    font-size: 14px;
    line-height: 14px;
    margin-bottom: 7px;
    max-width: 152px;
  }

  dd {
    font-size: 12px;
    line-height: 14px;
    color: #8b8b8b;
    margin-bottom: 3px;
  }

  .res-usage-detail-info {
    margin-left: 10px;
    text-align: left;
  }
</style>
