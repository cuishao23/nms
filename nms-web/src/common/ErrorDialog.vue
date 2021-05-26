<template>
  <el-dialog
    :title="'提示'"
    :visible.sync="show"
    :width="'400px'"
    :show-close="false"
    :close-on-click-modal="false"
  >
    <hr width="100%" size="1" color="#E0E0E0" />
    <div class="dlg-content">
      <div class="msg">
        <span id="PromptImg" class="PromptImg"></span>
        <span>{{msg}}</span>
        <div v-for="(info, index) in listMsg" :key="index">{{info}}</div>
      </div>
    </div>
    <slot name="footer"></slot>
    <div class="nms-dlg-btns">
      <input class="normal-btn" type="button" value="确定" @click="close" />
    </div>
  </el-dialog>
</template>

<script>
export default {
  name: "ErrorDialog",
  data() {
    return {
      msg: "",
      listMsg: [],
      show: false
    };
  },
  methods: {
    open(msg, listMsg) {
      this.msg = msg;
      if (listMsg) {
        this.listMsg = listMsg;
      }
      this.show = true;
    },
    close: function() {
      this.show = false;
      this.msg = "";
      this.listMsg = [];
    }
  }
};
</script>

<style scoped>
div > .normal-btn {
  padding-left: 5px;
  padding-right: 5px;
}

.dlg-content {
  min-height: 152px;
  text-align: center;
}

.normal-btn {
  width: 70px;
  height: 25px;
  text-align: center;
}
.nms-dlg-btns {
  /* padding: 20px 0 30px 0; */
  padding-bottom: 30px
}

#PromptImg {
  /*position: absolute;
  top: 79px;
  left: 50px;*/
}

.msg {
  padding: 68px 50px 0 69px;
  text-align: center;
  word-break: break-all;
  width: 100%;
}
</style>
