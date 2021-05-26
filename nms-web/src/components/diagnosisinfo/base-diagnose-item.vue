<template>
  <div class="base-diagnose-item" :style="{height: itemHeight + 'px', width: width + 'px'}">
    <h3 class="common-title">{{ title }}</h3>
    <slot></slot>
    <hr class="line">
  </div>
</template>

<script>
  export default {
    name: "base-diagnose-item",
    props: {
      title: String,
      itemHeight: String,
      width: {
        default: function () {
          return 680
        }
      },
      height: {
        default: function () {
          return 300
        }
      }
    }
  }
</script>

<style scoped>
  .base-diagnose-item {
    /*margin-right: 81px;*/
    margin-top: 45px;
  }
  .common-title {
    font-size: 14px;
    font-weight: bold;
    color: #4e4e4e;
    margin-bottom: 5px;
    text-align: left;
  }

  .line {
    border: 0;
    border-bottom: 1px dotted #dadada;
    margin-bottom: 28px;
    width: 1462px
  }
</style>
