<template>
  <div id="app">
    <div class="mainHeader">
      <!--网站头部-->
      <div id="headerContiner">
        <nms-header :show="true"></nms-header>
      </div>
    </div>
    <keep-alive>
      <router-view v-if="$route.meta.keepAlive && isRouterAlive"></router-view>
    </keep-alive>
    <router-view v-if="!$route.meta.keepAlive && isRouterAlive"></router-view>
    <success-dialog ref="successDialog"></success-dialog>
    <error-dialog ref="errorDialog"></error-dialog>
    <simple-progress ref="simpleProgress"></simple-progress>
  </div>
</template>

<script>
import NmsHeader from "components/common/nms-header";
import SuccessDialog from "./common/SuccessDialog";
import ErrorDialog from "./common/ErrorDialog";
import SimpleProgress from "./common/SimpleProgress";
import Vue from "vue";
import {keepAlive} from "./common/commonFunction"

export default {
  name: "app",
  // 主界面根据告警等级显示对应告警
  globalMenuWarningLevel: [
    {
      serviceCritical: 1,
      serviceImportant: 1,
      serviceNormal: 1
    },
    {
      terminalCritical: 1,
      terminalImportant: 1,
      terminalNormal: 1
    }
  ],
  provide() {
    return {
      reload: this.reload
    };
  },
  data() {
    return {
      isRouterAlive: true,
      keepliveList: ['unrepairedwarninginfo','subwarninginfo'],
      notkeepliveList: ['physicaldetail','ctrlterminaldetail']
    };
  },
  watch: {
    $route(to, from) {
      // 如果form(离开)的页面是 keepAlive缓存的
      if (this.notkeepliveList.includes(to.name) && this.keepliveList.includes(from.name)) {
        from.meta.keepAlive = true
      }
      // 如果form(离开)的页面是 不需要keepAlive缓存的
      else if (this.keepliveList.includes(from.name) && !this.notkeepliveList.includes(to.name)) {
        from.meta.keepAlive = false
      }
    }
  },
  mounted() {
    Vue.prototype.successDialog = this.$refs.successDialog;
    Vue.prototype.errorDialog = this.$refs.errorDialog;
    Vue.prototype.simpleProgress = this.$refs.simpleProgress;
    // 抓包和抓日志页面保活
    keepAlive();
  },
  methods: {
    reload() {
      this.isRouterAlive = false;
      this.$nextTick(function() {
        this.isRouterAlive = true;
      });
    }
  },
  components: {
    NmsHeader,
    SuccessDialog,
    ErrorDialog,
    SimpleProgress
  }
};
</script>

<style>
#app {
  font-family: "Microsoft Yahei", arial;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

html {
  overflow-x: hidden;
  overflow-y: hidden;
}
.router-link-active {
  background: url(./assets/image/tab_select.png?t=5.0.0.0_1339108041) no-repeat;
  color: white !important;
  background-color: #53afe4;
  background: -webkit-gradient(
    linear,
    left bottom,
    right bottom,
    from(#2d8bc0),
    to(#53afe4)
  );
}
.el-submenu__title .router-link-active {
  color: black !important;
}

select option {
  margin-bottom: 1px;
  color: #616060;
  white-space: pre;
  line-height: 25px;
  padding: 0px 0px 0px 7px;
  cursor: pointer;
}

.clearfix:after {
  content: ".";
  display: block;
  height: 0;
  visibility: hidden;
  clear: both;
}

/*头部样式*/
.mainHeader {
  width: 100vw;
  height: 54px;
  background-color: #373d41;
  position: fixed;
  top: 0;
  left: 0;
  z-index: 100;
  overflow: hidden;
}

#headerContiner {
  height: 98px;
  margin: 0 90px 0 88px;
}

.mainHeader #logo {
  float: left;
  margin: 36px 0 0 0;
}

.mainHeader #head_cureline {
  float: left;
  margin: 39px 0 0 6px;
}

.mainHeader .fontTitle {
  margin: 38px 0 0 8px;
  float: left;
  font-size: 13px;
  font-weight: 700;
  color: #ffffff;
  max-width: 150px;
  white-space: nowrap;
  text-overflow: ellipsis;
  overflow: hidden;
}

.mainHeader .btnContainer {
  width: 24px;
  height: 24px;
  float: right;
  margin: 37px 0 0 0;
}

.mainHeader .btnContainer a#exit {
  display: inline-block;
  height: 24px;
  width: 24px;
  background: url(./assets/image/exit_all.png?t=5.0.0.0_1975907832) 96px 0;
  overflow: hidden;
  cursor: pointer;
}

.mainHeader .btnContainer a#exit:hover {
  background-position: 72px 0;
}

.mainHeader .btnContainer a#exit:active {
  background-position: 48px 0;
}

.mainHeader .userInfoContainer {
  float: right;
  width: 24px;
  height: 24px;
  margin: 37px 5px 0 0;
  text-align: center;
}

.mainHeader .userInfoContainer img {
  border-radius: 25px;
  width: 24px;
  height: 24px;
}

.mainHeader #userInfo {
  height: 12px;
  float: right;
  margin: 42px 18px 0 0;
  color: #ffffff;
  font: 12px/12px Microsoft YaHei;
}

.mainHeader #userInfo a:hover {
  color: #ffffff;
  text-decoration: none;
  cursor: pointer;
}

.mainHeader .linkContainer {
  float: right;
  height: 18px;
  margin: 41px 15px;
  display: inline-block;
  position: relative;
  font-size: 12px;
  color: #ffffff;
}

/*菜单的样式*/
.mainContainer {
  width: 100vw;
  margin-left: calc((100% - 100vw) / 2);
  position: relative;
  top: 30px;
}

.mainContainer .menuContainer {
  /* width: 275px; */
  height: calc(100% - 98px - 17px - 32px);
  float: left;
  /* position: fixed; */
  top: 115px;
  /* border-right: solid 1px #949799; */
  height: 592px;
}

.mainContainer .menuContainer ul {
  margin-right: 36px;
}

.mainContainer .menuContainer li {
  text-align: right;
  font-weight: 400;
  font-size: 14px;
  color: #4e4e4e;
  cursor: pointer;
  margin-bottom: 5px;
}

.mainContainer .menuContainer a {
  padding: 4px 4px;
}

.mainContainer .menuContainer a:hover {
  /* color: #007ac0; */
  /* font-size: 14px; */
}

.mainContainer .menuContainer li ul.level2 {
  display: none;
}

.mainContainer .menuContainer .menu_select {
  font-weight: 400;
  color: #fff;
  background-color: #53afe4;
}

.mainContainer .menuContainer .menu_select1 {
  font-weight: 700;
  color: #000000;
}

.mainContainer .menuContainer .sub_menu_select {
  font-size: 12px;
  color: #ffffff;
  background-color: #53afe4;
}

.mainContainer .menuContainer .level2 {
  padding: 6px 0 24px;
  font-size: 12px;
  margin: 0;
}

.mainContainer .menuContainer .level2 li {
  margin-bottom: 20px;
}

.mainContainer .menuContainer .level2 li a {
  padding: 3px 4px;
  font-size: 12px;
}

.mainContainer .menuContainer .level2 li a:hover {
  color: #007ac0;
  font-size: 12px;
}

/*内容的样式*/
.mainContainer .contentContainer {
  height: calc(100vh - 98px - 17px - 32px);
  margin: 0 0 0 195px;
  padding: 0 114px 1px 0;
  overflow-x: auto !important;
  /*overflow-y: auto !important;*/
}

#frame_content {
  min-width: 1000px;
}

.wrap-outer {
  margin-left: calc(100vw - 100%);
}

#depSelector {
  display: inline-block;
  color: #fff;
  float: right;
  margin-top: 12px;
}

#evnSelector {
  display: none;
  color: #fff;
}

#machineRoomSelector {
  display: inline-block;
  color: #fff;
  margin-left: 5px;
}

.aboutInfo {
  margin: 78px 180px 0 206px;
  border: 1px solid #949799;
  width: 398px;
  height: 264px;
}

#table_content {
  clear: right;
}

.servertabletitle {
  margin-top: 16px;
  height: 33px;
  /* 33 + 16 == 85 - 36 */
}

.clienttabletitle,
.basetabletitle {
  margin-top: 33px;
  height: 33px;
  /* 33 + 33 == 66 */
}

.tablelefttext {
  float: left;
  padding: 10px 0 7px 0; /* h: 10 + 16 + 7 = 33 */
  clear: right;
  font-size: 12px;
}

.tablerightbtn {
  float: right;
  padding: 0 0 10px 0; /* h: 10 + 23 = 33 */
  clear: right;
}

#uploadAddBtnserver,
#uploadAddBtnclient,
#uploadAddBtnbase,
#uploadConfData {
  display: inline-block;
  position: relative;
  height: 21px;
}

#uploadFileBtnserver,
#uploadFileBtnclient,
#uploadFileBtnbase,
#uploadConfDataFile {
  position: absolute;
  right: 0;
  top: 0;
  font-size: 100%;
  font-family: Arial;
  cursor: pointer;
  opacity: 0;
  overflow: hidden;
  height: 21px;
  width: 94px;
}

#upgradeBtnserver,
#upgradeBtnclient,
#upgradeBtnbase {
  height: 23px;
}

.systemConTitle {
  margin: 36px 0;
  font-size: 14px;
  color: #4e4e4e;
}

.systemConfItem {
  margin: 31px 0;
  font-size: 12px;
  color: #4e4e4e;
}

#synBtn {
  display: inline-block;
}

.systemConfItemText {
  display: inline-block;
  width: 55px;
}

.systemConfName {
  width: 144px;
  display: inline-block;
  vertical-align: bottom;
}

.systemConfDate {
  margin: 0 3px 0 18px;
  display: inline-block;
}

.systemConfTime {
  margin: 0 3px 0 16px;
  display: inline-block;
}

.input {
  width: 257px;
}

.backupTitle {
  font-size: 12px;
  font-weight: 700;
  color: #4e4e4e;
  margin: 35px 0 18px 0;
}

.backupItem {
  font-size: 12px;
  color: #4e4e4e;
  margin: 18px 0;
}

.backupButton {
  margin: 18px 0 35px 0;
}

/*dialog显示*/

/*artDialog-reset*/
.aui_nw,
.aui_ne,
.aui_sw,
.aui_se {
  width: 1px;
  height: 1px;
}

.aui_nw,
.aui_n,
.aui_ne,
.aui_w,
.aui_e,
.aui_sw,
.aui_s,
.aui_se {
  background: none repeat scroll 0 0 #555;
}

.w400h260 {
  width: 368px;
  height: 260px;
}

.w400h300 {
  width: 368px;
  height: 300px;
}

.w400h470 {
  width: 368px;
  height: 470px;
}

.w550 {
  width: 518px;
  height: 350px;
}

.w720 {
  width: 688px;
  height: 500px;
}

.aui_content {
  width: 100%;
  height: 100%;
}

/*对话框通用*/
.el-dialog {
  border-radius: 0px;
}

.el-dialog__headerbtn {
  line-height: 40px;
  top: 0px;
}

/*.el-dialog__body {*/
/*height: 216px;*/
/*}*/

.el-dialog__body .info {
  text-align: center;
  position: relative;
  width: 300px;
  height: 75px;
}

.el-dialog__body .btn-wrapper {
  bottom: 0;
  padding-top: 21px;
  text-align: center;
  width: 100%;
  position: relative;
  margin-bottom: 20px;
}

.el-dialog__body .mo-btn-x {
  cursor: pointer;
  display: inline-block;
  *display: inline;
  *zoom: 1;
  font-size: 12px;
  height: 23px;
  line-height: 23px;
  padding: 0 22px;
  text-align: center;
  border: 1px solid #dcdfe1;
}

.el-dialog__body .mo-btn-gray {
  /*background-color: #eff2f4;*/
  color: #5f5f5f;
  text-decoration: none;
}

.el-dialog__body {
  margin: 0 auto;
  padding: 0px 0px;
  position: relative;
  color: #4e4e4e;
  font-size: 12px;
  overflow: hidden;
}

.el-dialog__header {
  height: 40px;
  padding: 0 16px;
}

.el-dialog__title {
  height: 40px;
  line-height: 40px;
  position: relative;
  font-size: 12px;
}

.el-dialog__body .separater {
  border-top: 1px solid #ececec;
  padding: 0;
  margin: 0;
}

.el-dialog__body .w-close {
  position: absolute;
  top: 9px;
  right: -5px;
  width: 23px;
  height: 23px;
}

.el-dialog__body .w-close:hover {
  background-position: -23px 0;
}

.el-dialog__body .w-close:active {
  background-position: -46px 0;
}

.el-dialog__body .w-close.disabled {
  background-position: -69px 0;
}

.el-dialog__body .info {
  margin: 0px 34px;
}

.el-dialog__body .setting-item {
  margin-top: 20px;
  *zoom: 1;
}

.el-dialog__body .setting-item:after {
  content: "\20";
  display: block;
  height: 0;
  clear: both;
}

.el-dialog__body .setting-item label {
  display: block;
  float: left;
  width: 87px;
}

.el-dialog__body .setting-item-main {
  background: none repeat scroll 0 0 #ffffff;
  margin-left: 87px;
  position: relative;
  width: 210px;
  *margin-left: 0px;
}

.el-dialog__body .info .showInput {
  border: 0px;
  color: #4e4e4e;
  border-bottom: 1px solid #4e4e4e;
  font-size: 12px;
  width: 100%;
  height: 16px;
}

.el-dialog__body .item-msg {
  margin-top: 7px;
  margin-left: 87px;
  *margin-left: 85px;
  background: #949494;
  color: #fff;
  width: 210px;
  padding: 0 10px;
}

.el-dialog__body .item-msg .msg {
  padding-left: 16px;
}

.el-dialog__body .text-tips {
  margin-top: 2px;
}

.el-dialog__body .btn-wrapper {
  position: absolute;
  bottom: 30px;
  left: 0px;
  padding: 0;
  height: 24px;
}

.machine_content {
  position: relative;
  margin: 14px 34px 40px 34px;
  width: 620px;
  height: 336px;
  text-align: left;
}

.peri_content {
  position: relative;
  left: 30px;
  top: 20px;
  width: 260px;
  height: 280px;
  overflow-y: auto;
}

.tips_content {
  width: 420px;
  height: 260px;
}

.view_content {
  position: relative;
  left: 30px;
  top: 20px;
  width: 720px;
  height: 540px;
}

.grid_content1 {
  width: 368px;
  height: 234px;
}

.grid_content2 {
  width: 508px;
  height: 234px;
}

.grid_content3 {
  width: 688px;
  height: 234px;
}

/*弹框自定义续写*/
.Message .el-dialog__header {
  display: none !important;
}

.Message .el-dialog__body {
  width: 186px;
  height: 41px;
  line-height: 43px;
  text-align: center;
  background: #434343;
  color: #ffffff;
  font-size: 14px;
}

.machine .el-dialog__body {
  height: 454px;
}

/* 主机页手动添加 */
.addmenumachineone .el-dialog__body {
  height: 300px !important;
}

.addmenumachinetwo .el-dialog__body {
  height: 340px;
}

.addmenumachinethree .el-dialog__body {
  height: 445px;
}

/* 机框添加弹窗 */
.update_add_frame .el-dialog__body {
  height: 207px;
}

.version_upgrade_height .el-dialog__body {
  height: 260px;
}

.peri_add_frame .el-dialog__body {
  height: 268px;
}

.periadd .el-dialog__body {
  height: 360px;
}

.addip .el-dialog__body {
  height: 260px;
}

/* 表格行事件 */
/*.el-table--enable-row-hover .el-table__body tr:hover > td {*/
  /*!*background-color: u;*!*/
  /*color: white !important;*/
/*}*/

.el-table--enable-row-hover .el-table__body tr:hover > td a {
  color: white !important;
}

.el-table--enable-row-active .el-table__body tr:active > td {
  background: #000000 !important;
}

/* 表格暂无数据显示隐藏 */
.el-table__empty-block {
  display: none;
}

/* a链接 */
.optionlink {
  margin-right: 15px;
  color: #007ac0;
}

.el-radio__input.is-checked + .el-radio__label {
  color: #4e4e4e;
}

.el-radio__input.is-checked .el-radio__inner {
  border-color: #606266;
  background: #606266;
}

.el-checkbox__input.is-checked .el-checkbox__inner,
.el-checkbox__input.is-indeterminate .el-checkbox__inner {
  background-color: #606266;
  border-color: rgba(255, 255, 255, 0.5);
}

.el-checkbox__input.is-checked + .el-checkbox__label {
  color: #606266;
}
/*下拉框设计*/
.select_big .el-input {
  width: 205px;
}
.periItemSon .el-input {
  width: 260px;
}
.periItem .el-input {
  width: 260px;
}
.confLine .el-input {
  width: 96px;
}

.el-select-dropdown .popper__arrow::after {
  display: none;
}
body {
  padding-right: 0px !important;
}
.el-popover{
  min-height: 200px;
}
.no-info-tip {
  padding-top: 200px;
}
</style>
