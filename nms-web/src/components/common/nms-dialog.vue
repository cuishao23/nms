<template>
  <el-dialog :title="title" :visible.sync="dialogVisible" :width="width" :before-close="handleClose" :append-to-body="true" :close-on-click-modal="false">
    <hr width="100%" size="1" color="#E0E0E0">
    <div class="dlg-content" :style="{height: height}">
      <slot name="content"></slot>
    </div>
    <slot name="footer"></slot>
    <div class="nms-dlg-btns">
      <input class="normal-btn" type="button" value="确定" @click="confirm" v-if="confirmBtn"/>
      <input class="normal-btn" type="button" value="关闭" @click="cancel" v-if="closeBtn"/>
      <input class="normal-btn" type="button" value="取消" @click="cancel" v-if="cancelBtn"/>
    </div>
  </el-dialog>
</template>

<script>
  export default {
    name: "nms-dialog",
    data () {
      return {
        dialogVisible: false
      }
    },
    methods: {
      handleClose: function () {
        this.close()
        this.$emit('close')
      },
      close: function () {
        console.log('close dialog')
        this.dialogVisible = false
      },
      confirm: function () {
        this.close()
        this.$emit('confirm')
      },
      cancel: function () {
        this.close()
        this.$emit('cancel')
      },
      open: function () {
        console.log('open dialog')
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
      closeBtn: {
        type: Boolean,
        default: function () {
          return false
        }
      },
      cancelBtn: {
        type: Boolean,
        default: function () {
          return false
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
          return '300px'
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
    /* margin-bottom: 25px; */
  }

  .normal-btn {
    width: 70px;
    height: 25px;
    text-align: center;
  }
  .nms-dlg-btns {
    /* position: absolute;
    width: 100%;
    bottom: 20px;
    margin-top: 25px; */
    text-align: center;
    padding-bottom: 30px;
  }
</style>
