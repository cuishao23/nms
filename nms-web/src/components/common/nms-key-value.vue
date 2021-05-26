<template>
  <div class="nms-key-value" :style="{minWidth: width + 'px'}">
    <span class="nms-key">{{ label }}</span>
    <span class="nms-value">{{ showVal }}</span>
  </div>
</template>

<script>
  export default {
    name: "nms-key-value",
    computed: {
      showVal: function () {
        if (this.value === 'on') {
          return '开启'
        } else if (this.value === 'off') {
          return '关闭'
        } else if (this.value === 'yes') {
          return '有'
        } else if (this.value === 'no' || this.value === 'none' || this.value === 'NONE') {
          return '无'
        } else if (this.value === '') {
          return '无'
        } else if (this.value === 'online') {
          return '在线'
        } else if (this.value === 'conference') {
          return '与会'
        } else if (this.value === 'offline') {
          return '离线'
        } else if (this.value === '1' && this.label != '接收带宽' && this.label != '发送带宽' && this.label != '槽位') {
          return '开启'
        } else if (this.value === '0' && this.label != '接收带宽' && this.label != '发送带宽' && this.label != '槽位') {
          return '关闭'
        } else if (this.value === 'critical' && this.label === '告警状态') {
          return '严重'
        } else if (this.value === 'important' && this.label === '告警状态') {
          return '重要'
        } else if (this.value === 'normal' && this.label === '告警状态') {
          return '一般'
        } else if ((this.label === '内存使用率' && this.value != '') || (this.label === 'CPU使用率' && this.value != '')) {
          return this.value + '%'
        } else if (this.value == '0' && (this.label === '主芯片状态' || this.label === '编解码芯片' || this.label === '运行温度')) {
          return '正常'
        } else if (this.value == '1' && (this.label === '主芯片状态' || this.label === '编解码芯片' || this.label === '运行温度')) {
          return '异常'
        } else if (this.label === '终端运行时长') {
          var run_time = 0
          if (this.value > 0) {
            let day = parseInt(this.value / 86400)
            if (day > 0) {
              run_time = day + '天' + Math.round((this.value / 86400 - day)*24) + "小时"
            } else {
              run_time = Math.round(this.value / 3600) + "小时"
            }
          }
          return run_time
        } else {
          return this.value
        }
      }
    },
    props: {
      label: {
        type: String,
        required: true
      },
      value: {
        type: [String, Number],
        default: function () {
          return ''
        }
      },
      width: {
        type: Number,
        default: function () {
          return 306
        }
      }
    }
  }
</script>

<style scoped>
  .nms-key-value {
    font-size: 12px;
    text-align: left;
    display: flex;
    align-items: center;
  }

  .nms-key {
    width: 99px;
    color: #8b8b8b;
    display: inline-block;
  }

  .nms-value {
    color: #4e4e4e;
    width: 180px;
    display: inline-block;
    word-break: break-all;
    padding-top: 0px;
  }
</style>
