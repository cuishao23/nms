<template>
  <div class="Message">
    <el-dialog :modal="false" title="提示" :visible.sync="show" width="186px" top="80vh">
      <div class="mid">{{msg}}</div>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: "SuccessDialog",
  data() {
    return {
      show: false,
      msg: "",
      timer: null
    };
  },
  mounted() {
    Vue.prototype.$successDialog = this;
  },
  methods: {
    open(msg) {
      clearTimeout(this.timer)
      this.show = true;
      this.msg = msg;
      this.timer = setTimeout(this.close, 3000)
    },
    close(){
      this.show = false
      this.msg = ''
    }
  }
};
</script>

<style scoped>
.mid {
  text-align: center;
}
</style>
