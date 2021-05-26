<template>
  <el-progress type="circle" :percentage="percent" :color="color" show-text :width="width" :stroke-width="3"></el-progress>
</template>

<script>
  export default {
    name: "res-usage-circle",
    data () {
      return {
        color: '#1E94DA'
      }
    },
    props: {
      percent: {
        type: Number,
        required: true
      },
      width: {
        type: Number,
        default() {
          return 60
        }
      }
    },
    mounted: function () {
      if (this.percent >= 65 && this.percent < 85) {
        this.color = "#E4802A"
      } else if (this.percent >= 85) {
        this.color = "#ac1000"
      }
    },
    watch: {
      percent: function(newstate, oldstate) {
        if (this.percent >= 65 && this.percent < 85) {
          this.color = "#E4802A"
        } else if (this.percent >= 85) {
          this.color = "#ac1000"
        } else {
          this.color = "#1E94DA"
        }
      }
    }
  }
</script>

<style scoped>

</style>
