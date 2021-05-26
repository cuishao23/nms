<template>
  <el-progress :percentage="percent" :show-text="showText" :stroke-width="lineWidth" :color="color"></el-progress>
</template>

<script>
  export default {
    name: "res-usage-line",
    data () {
      return {
        showText: false,
        color: '#1E94DA',
        lineWidth: 2
      }
    },
    props: [
      "percent"
    ],
    mounted: function () {
      if (this.percent >= 65 && this.percent < 85) {
        this.color = "#E4802A"
      } else if (this.percent >= 85) {
        this.color = "#ac1000"
      }
    }
  }
</script>

<style scoped>

</style>
