<template>
  <!-- 简单进度条 -->
  <div>
    <el-dialog
      :title="'提示'"
      :visible.sync="show"
      :width="'400px'"
      :show-close="false"
      :close-on-click-modal="false"
    >
      <hr width="100%" size="1" color="#E0E0E0" />
      <div class="progressMsg">
        <span class="msg">{{title}}</span>
        <el-progress type="line" :percentage="progress" :stroke-width="3" :show-text="false"></el-progress>
        <span class="msg">{{msg}}</span>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import MsgDialog from "../components/common/msg-dialog";
export default {
  name: "nmsProgress",
  components: { MsgDialog },
  data() {
    return {
      msg: "",
      title: "",
      show: false,
      timer: null,
      progress: 0
    };
  },
  mounted() {},
  methods: {
    open(title, msg, millisecond) {
      clearTimeout(this.timer);
      this.progress = 0;
      this.title = title;
      this.msg = msg;
      this.show = true;
      if (millisecond) {
        this.timer = setTimeout(this.progressTimer, millisecond, millisecond);
      }
    },
    success(msg) {
      this.progress = 100;
      this.msg = msg;
      setTimeout(this.close, 1000);
    },
    updatedProgress(progress) {
      if (progress > this.progress && progress <= 100) {
        this.progress = progress;
        if (this.progress == 100) {
          this.success("");
        }
      }
    },
    close() {
      clearTimeout(this.timer);
      this.show = false;
      this.msg = "";
      this.title = "";
      this.progress = 0;
    },
    progressTimer(millisecond) {
      if (this.progress < 80) {
        this.progress++;
        setTimeout(this.progressTimer, millisecond, millisecond);
      }
    }
  }
};
</script>
<style scoped>
.progressMsg {
  text-align: left;
  line-height: 30px;
  height: 220px;
  padding: 60px 20px 0 20px;
}
</style>
