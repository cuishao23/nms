<template>
  <el-dialog :title="title" :visible.sync="dialogVisible" :width="width" :before-close="close" :close-on-click-modal="false">
    <hr width="100%" size="1" color="#E0E0E0">
    <div class="dlg-content" :style="{height: height}">
      <slot name="content"></slot>
    </div>
    <slot name="footer"></slot>
    <div class="nms-dlg-btns">
      <button class="normal-btn" :class="{disable: confirmType}" :disabled="confirmType" @click="confirm" v-if="confirmBtn">确定</button>
      <input class="normal-btn" type="button" value="取消" @click="cancel" v-if="closeBtn"/>
    </div>
  </el-dialog>
</template>

<script>
  export default {
    name: "nms-big-dialog",
    data () {
      return {
        dialogVisible: false
      }
    },
    methods: {
      close: function () {
        this.dialogVisible = false
        this.$emit('close')
      },
      confirm: function () {
        this.$emit('confirm')
        this.close()
      },
      cancel: function () {
        this.$emit('cancel')
        this.close()
      },
      open: function () {
        this.dialogVisible = true
      }
    },
    props: {
      title: {
        type: String,
        required: true
      },
      confirmBtn: {
        type: Boolean,
        default: function () {
          return true
        }
      },
      confirmType: {
        type: Boolean,
        default: function () {
          return false
        }
      },
      closeBtn: {
        type: Boolean,
        default: function () {
          return true
        }
      },
      width: {
        type: String,
        default: function () {
          return '560px'
        }
      },
      height: {
        type: String,
        default: function () {
          return '500px'
        }
      }
    }
  }
</script>

<style scoped>
  div > .normal-btn {
    padding-left: 5px;
    padding-right: 5px;
  }

  div.dlg-content {
    display: block;
    margin-bottom: 25px;
  }

  .normal-btn {
    width: 70px;
    height: 25px;
    text-align: center;
    margin-bottom: 25px;
  }
  .nms-dlg-btns {
    position: absolute;
    width: 100%;
    bottom: 20px;
    text-align: center;
    margin-top: 25px;
  }
</style>
