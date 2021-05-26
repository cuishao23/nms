<template>
  <div class="nms-key-value" :style="{minWidth: width + 'px'}">
    <div class="nms-key">
      <slot name="key"/>
    </div>
    <div class="nms-value">
      <slot name="value"/>
    </div>
  </div>
</template>

<script>
  export default {
    name: "nms-pair",
    props: {
      width: {
        type: Number,
        default: function () {
          return 380
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
    min-width: 110px;
    color: #8b8b8b;
    display: inline-block;
    float: left;
  }

  .nms-value {
    min-width: 260px;
    color: #4e4e4e;
    display: inline-block;
    padding-top: 0px;
  }
</style>
