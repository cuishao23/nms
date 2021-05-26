<template>
  <div class="parent">
    <div class="left">
      <el-menu
        class="el-menu-vertical-demo"
        ref="el_menu"
        @open="handleOpen"
        @close="handleClose"
        :collapse="isCollapse"
        :unique-opened="true"
        :default-openeds="openeds"
        :default-active="activetip"
      >
        <el-submenu index="1">
          <template slot="title">
            <router-link :to="{name:'baseinfo'}" style="background: none;" v-show="isCollapse">
              <div class="one_image" id="srunstatus"></div>
            </router-link>
            <span slot="title">
              <router-link :to="{name:'baseinfo'}">
                <div class="one_image" id="runstatus"></div>
                <span class="targetMenu">运行状态</span>
              </router-link>
            </span>
          </template>
        </el-submenu>
        <el-submenu index="2" ref="meeting_manager">
          <template slot="title">
            <router-link
              :to="{name:'realtimemeeting'}"
              style="background: none;"
              v-show="isCollapse"
              :class="{actived: openeds[0] == 2}"
            >
              <div class="one_image" id="meetinginfo"></div>
            </router-link>
            <span slot="title">
              <router-link :to="{name:'realtimemeeting'}" style="background: none;">
                <div class="one_image" id="meetinginfo"></div>
                <span class="selectMenu">会议信息</span>
              </router-link>
            </span>
            <i v-show="!isCollapse" class="el-submenu__icon-caret el-icon-caret-right"></i>
            <i
              v-if="isMeeting && isCollapse"
              class="el-submenu__icon-arrow_add el-icon-caret-right"
              @click="openTab(2)"
            ></i>
            <i
              v-else-if="!isMeeting && isCollapse"
              class="el-submenu__icon-arrow_add el-icon-caret-right"
              @click="closeTab(2)"
              style="transform: rotateZ(90deg)"
            ></i>
          </template>
          <el-menu-item index="2-1" style="padding-left: 30px;">
            <router-link :to="{name:'realtimemeeting'}">
              <div class="one_image" id="livemeetimg"></div>实时会议
            </router-link>
          </el-menu-item>
          <el-menu-item index="2-2" style="padding-left: 30px;">
            <router-link :to="{name:'historymeeting'}">
              <div class="one_image" id="historymeetimg"></div>历史会议
            </router-link>
          </el-menu-item>
        </el-submenu>
        <el-menu-item index="2-1" v-if="meeting">
          <router-link :to="{name:'realtimemeeting'}" style="background: none;">
            <div class="one_image" id="livemeetimgs"></div>
          </router-link>
        </el-menu-item>
        <el-menu-item index="2-2" v-if="meeting">
          <router-link :to="{name:'historymeeting'}" style="background: none;">
            <div class="one_image" id="historymeetimgs"></div>
          </router-link>
        </el-menu-item>
        <el-submenu index="3" ref="device_manager">
          <template slot="title">
            <router-link
              :to="{name:'platformdeviceinfo'}"
              style="background: none;"
              v-show="isCollapse"
              :class="{actived: openeds[0] == 3}"
            >
              <div class="one_image" id="equipment"></div>
            </router-link>
            <span slot="title">
              <router-link :to="{name:'platformdeviceinfo'}" style="background: none;">
                <div class="one_image" id="equipment"></div>
                <span class="selectMenu">设备管理</span>
              </router-link>
            </span>
            <i v-show="!isCollapse" class="el-submenu__icon-caret el-icon-caret-right"></i>
            <i
              v-if="isPlatform && isCollapse"
              class="el-submenu__icon-arrow_add el-icon-caret-right"
              @click="openTab(3)"
            ></i>
            <i
              v-else-if="!isPlatform && isCollapse"
              class="el-submenu__icon-arrow_add el-icon-caret-right"
              @click="closeTab(3)"
              style="transform: rotateZ(90deg)"
            ></i>
          </template>
          <el-menu-item index="3-1" style="padding-left: 30px;">
            <router-link :to="{name:'platformdeviceinfo'}">
              <div class="one_image" id="serverequipment"></div>服务器设备
            </router-link>
          </el-menu-item>
          <el-menu-item index="3-2" style="padding-left: 30px;">
            <router-link :to="{name:'terminaldeviceinfo'}">
              <div class="one_image" id="terminalequipment"></div>终端设备
            </router-link>
          </el-menu-item>
          <el-menu-item index="3-3" style="padding-left: 30px;">
            <router-link :to="{name:'inspection'}">
              <div class="one_image" id="inspection"></div>巡检功能
            </router-link>
          </el-menu-item>
        </el-submenu>
        <el-menu-item index="3-1" v-if="platform">
          <router-link :to="{name:'platformdeviceinfo'}" style="background: none;">
            <div class="one_image" id="serverequipments"></div>
          </router-link>
        </el-menu-item>
        <el-menu-item index="3-2" v-if="platform">
          <router-link :to="{name:'terminaldeviceinfo'}" style="background: none;">
            <div class="one_image" id="terminalequipments"></div>
          </router-link>
        </el-menu-item>
        <el-menu-item index="3-3" v-if="platform">
          <router-link :to="{name:'inspection'}" style="background: none;">
            <div class="one_image" id="inspections"></div>
          </router-link>
        </el-menu-item>
        <el-submenu index="4">
          <template slot="title">
            <router-link :to="{name:'diagnosisinfo'}" style="background: none;" v-show="isCollapse">
              <div class="one_image" id="diagnostics"></div>
            </router-link>
            <span slot="title">
              <router-link :to="{name:'diagnosisinfo'}">
                <div class="one_image" id="diagnostic"></div>
                <span class="targetMenu">诊断抓包</span>
              </router-link>
            </span>
          </template>
        </el-submenu>
        <el-submenu index="5" ref="device_warnning">
          <template slot="title">
            <router-link
              :to="{name:'subwarninginfo'}"
              style="background: none;"
              v-show="isCollapse"
              :class="{actived: openeds[0] == 5}"
            >
              <div class="one_image" id="equipmentwarning"></div>
            </router-link>
            <span slot="title">
              <router-link :to="{name: admin?'subwarninginfo':'unrepairedwarninginfo'}" style="background: none">
                <div class="one_image" id="equipmentwarning"></div>
                <span class="selectMenu">设备告警</span>
              </router-link>
            </span>
            <i v-show="!isCollapse" class="el-submenu__icon-caret el-icon-caret-right"></i>
            <i
              v-if="isWarning && isCollapse"
              class="el-submenu__icon-arrow_add el-icon-caret-right"
              @click="openTab(5)"
            ></i>
            <i
              v-else-if="!isWarning && isCollapse"
              class="el-submenu__icon-arrow_add el-icon-caret-right"
              @click="closeTab(5)"
              style="transform: rotateZ(90deg)"
            ></i>
          </template>
          <el-menu-item index="5-1" style="padding-left: 30px;" v-if="admin">
            <router-link :to="{name:'subwarninginfo'}">
              <div class="one_image" id="subwarning"></div>订阅告警
            </router-link>
          </el-menu-item>
          <el-menu-item index="5-2" style="padding-left: 30px;">
            <router-link :to="{name:'unrepairedwarninginfo'}">
              <div class="one_image" id="unrepairedwarning"></div>未修复告警
            </router-link>
          </el-menu-item>
          <el-menu-item index="5-3" style="padding-left: 30px;">
            <router-link :to="{name:'repairedwarninginfo'}">
              <div class="one_image" id="repairedwarning"></div>已修复告警
            </router-link>
          </el-menu-item>
        </el-submenu>
        <el-menu-item index="5-1" v-if="warning">
          <router-link :to="{name:'subwarninginfo'}" style="background: none;">
            <div class="one_image" id="subwarnings"></div>
          </router-link>
        </el-menu-item>
        <el-menu-item index="5-2" v-if="warning">
          <router-link :to="{name:'unrepairedwarninginfo'}" style="background: none;">
            <div class="one_image" id="unrepairedwarnings"></div>
          </router-link>
        </el-menu-item>
        <el-menu-item index="5-3" v-if="warning">
          <router-link :to="{name:'repairedwarninginfo'}" style="background: none;">
            <div class="one_image" id="repairedwarnings"></div>
          </router-link>
        </el-menu-item>
        <el-submenu index="6" ref="system_setting" v-if="admin">
          <template slot="title">
            <router-link
              :to="{name:'limitset'}"
              style="background: none;"
              v-show="isCollapse"
              :class="{actived: openeds[0] == 6}"
            >
              <div class="one_image" id="sysedit"></div>
            </router-link>
            <span slot="title">
              <router-link :to="{name:'limitset'}" style="background: none">
                <div class="one_image" id="sysedit"></div>
                <span class="selectMenu">系统配置</span>
              </router-link>
            </span>
            <i v-show="!isCollapse" class="el-submenu__icon-caret el-icon-caret-right"></i>
            <i
              v-if="isSetting && isCollapse"
              class="el-submenu__icon-arrow_add el-icon-caret-right"
              @click="openTab(6)"
            ></i>
            <i
              v-else-if="!isSetting && isCollapse"
              class="el-submenu__icon-arrow_add el-icon-caret-right"
              @click="closeTab(6)"
              style="transform: rotateZ(90deg)"
            ></i>
          </template>
          <el-menu-item index="6-1" style="padding-left: 30px;">
            <router-link :to="{name:'limitset'}">
              <div class="one_image" id="thresholdvalueedit"></div>阈值配置
            </router-link>
          </el-menu-item>
          <el-menu-item index="6-2" style="padding-left: 30px;">
            <router-link :to="{name:'warningset'}">
              <div class="one_image" id="warningedit"></div>告警配置
            </router-link>
          </el-menu-item>
          <el-menu-item index="6-3" style="padding-left: 30px;">
            <router-link :to="{name:'deviceset'}">
              <div class="one_image" id="equipmentedit"></div>设备配置
            </router-link>
          </el-menu-item>
          <el-menu-item index="6-4" style="padding-left: 30px;">
            <router-link :to="{name:'permissionset'}">
              <div class="one_image" id="limitedit"></div>权限配置
            </router-link>
          </el-menu-item>
        </el-submenu>
        <el-menu-item index="6-1" v-if="setting">
          <router-link :to="{name:'limitset'}" style="background: none;">
            <div class="one_image" id="thresholdvalueedits"></div>
          </router-link>
        </el-menu-item>
        <el-menu-item index="6-2" v-if="setting">
          <router-link :to="{name:'warningset'}" style="background: none;">
            <div class="one_image" id="warningedits"></div>
          </router-link>
        </el-menu-item>
        <el-menu-item index="6-3" v-if="setting">
          <router-link :to="{name:'deviceset'}" style="background: none;">
            <div class="one_image" id="equipmentedits"></div>
          </router-link>
        </el-menu-item>
        <el-menu-item index="6-4" v-if="setting">
          <router-link :to="{name:'permissionset'}" style="background: none;">
            <div class="one_image" id="limitedits"></div>
          </router-link>
        </el-menu-item>
        <el-submenu index="7" v-if="admin">
          <template slot="title">
            <router-link :to="{name:'susmgr'}" style="background: none;" v-show="isCollapse">
              <div class="one_image" id="versionmanagements"></div>
            </router-link>
            <span slot="title">
              <router-link :to="{name:'susmgr'}">
                <div class="one_image" id="versionmanagement"></div>
                <span class="targetMenu">版本管理</span>
              </router-link>
            </span>
          </template>
        </el-submenu>
        <el-submenu index="8">
          <template slot="title">
            <router-link :to="{name:'log'}" style="background: none;" v-show="isCollapse">
              <div class="one_image" id="logmanagements"></div>
            </router-link>
            <span slot="title">
              <router-link :to="{name:'log'}">
                <div class="one_image" id="logmanagement"></div>
                <span class="targetMenu">操作日志</span>
              </router-link>
            </span>
          </template>
        </el-submenu>
      </el-menu>
    </div>
    <div class="right">
      <el-radio-group v-model="isCollapse" style="margin-bottom: 0px;" @change="toggleName">
        <el-radio-button v-if="display" :label="true" text-color="#ffffff">
          <i class="el-icon-arrow-left" style="width:10px; position:absolute; left:-2px; top:14px;"></i>
        </el-radio-button>
        <el-radio-button v-else :label="false" text-color="#ffffff">
          <i
            class="el-icon-arrow-right"
            style="width:10px; position:absolute; left:-2px; top:14px;"
          ></i>
        </el-radio-button>
      </el-radio-group>
    </div>
  </div>
</template>

<script>
import api from "../../axios";

export default {
  name: "menucontainer",
  data() {
    return {
      collapse: false,
      isCollapse: false,
      openeds: [],
      activetip: "",

      meeting: false,
      platform: false,
      warning: false,
      setting: false,

      display: true,

      isMeeting: true,
      isPlatform: true,
      isWarning: true,
      isSetting: true,
      admin: false
    };
  },
  mounted() {
    api.getServerInfo().then(res => {
        this.admin = res.admin;
    });
    let router = document.location.hash.split("/")[1];
    let index = {
      baseinfo: "1",
      realtimemeeting: "2",
      historymeeting: "2",
      platformdeviceinfo: "3",
      terminaldeviceinfo: "3",
      inspection: "3",
      diagnosisinfo: "4",
      subwarninginfo: '5',
      unrepairedwarninginfo: '5',
      repairedwarninginfo: '5',
      limitset: '6',
      warningset: '6',
      deviceset: '6',
      permissionset: '6',
      susmgrinfo: '7',
      log: '8'
    }[router]
    index = index != undefined? index : '1'
    console.log('......')
    console.log(index)
    this.handleOpen(index)
  },
  methods: {
    handleOpen(key, keyPath) {
      this.openeds = [];
      this.openeds.push(key);
      if (key == "2") {
        this.isMeeting = false;
        this.isPlatform = true;
        this.isWarning = true;
        this.isSetting = true;
      } else if (key == "3") {
        this.isPlatform = false;
        this.isMeeting = true;
        this.isWarning = true;
        this.isSetting = true;
      } else if (key == "5") {
        this.isWarning = false;
        this.isPlatform = true;
        this.isMeeting = true;
        this.isSetting = true;
      } else if (key == "6") {
        this.isSetting = false;
        this.isWarning = true;
        this.isPlatform = true;
        this.isMeeting = true;
      } else {
        this.isSetting = true;
        this.isWarning = true;
        this.isPlatform = true;
        this.isMeeting = true;
      }
    },
    handleClose(key, keyPath) {
      this.openeds = [];
      if (key == "2") {
        this.isMeeting = true;
      } else if (key == "3") {
        this.isPlatform = true;
      } else if (key == "5") {
        this.isWarning = true;
      } else if (key == "6") {
        this.isSetting = true;
      }
    },
    openTab(val) {
      this.isCollapse = true;
      this.display = false;
      if (val == 2) {
        this.isMeeting = false;
        this.openeds = [];
        this.openeds.push("2");
        console.log("nihao" + this.openeds[0]);
      } else if (val == 3) {
        this.isPlatform = false;
        this.openeds = [];
        this.openeds.push("3");
      } else if (val == 5) {
        this.isWarning = false;
        this.openeds = [];
        this.openeds.push("5");
      } else if (val == 6) {
        this.isSetting = false;
        this.openeds = [];
        this.openeds.push("6");
      }
      this.commanFun();
    },
    closeTab(val) {
      console.log("closeTab" + val);
      if (val == 2) {
        this.isMeeting = true;
        this.meeting = false;
      } else if (val == 3) {
        this.isPlatform = true;
        this.platform = false;
      } else if (val == 5) {
        this.isWarning = true;
        this.warning = false;
      } else if (val == 6) {
        this.isSetting = true;
        this.setting = false;
      }
      this.openeds = [];
    },
    commanFun: function() {
      if (this.openeds[0] == "2") {
        if (this.isCollapse) {
          this.meeting = true;
          this.platform = false;
          this.warning = false;
          this.setting = false;

          this.isPlatform = true;
          this.isWarning = true;
          this.isSetting = true;
        } else {
          this.meeting = false;
        }
      } else if (this.openeds[0] == "3") {
        if (this.isCollapse) {
          this.platform = true;
          this.meeting = false;
          this.warning = false;
          this.setting = false;

          this.isMeeting = true;
          this.isWarning = true;
          this.isSetting = true;
        } else {
          this.platform = false;
        }
      } else if (this.openeds[0] == "5") {
        if (this.isCollapse) {
          this.warning = true;
          this.meeting = false;
          this.platform = false;
          this.setting = false;

          this.isMeeting = true;
          this.isPlatform = true;
          this.isSetting = true;
        } else {
          this.warning = false;
        }
      } else if (this.openeds[0] == "6") {
        if (this.isCollapse) {
          this.setting = true;
          this.meeting = false;
          this.platform = false;
          this.warning = false;

          this.isMeeting = true;
          this.isPlatform = true;
          this.isWarning = true;
        } else {
          this.setting = false;
        }
      }
    },
    toggleName: function() {
      this.display = !this.display;
      if (this.openeds[0] == "2") {
        console.log(this.isCollapse);
        if (this.isCollapse) {
          this.meeting = true;
        } else {
          this.meeting = false;
          this.activetip = "2-2";
        }
      } else if (this.openeds[0] == "3") {
        console.log("3-1");
        console.log(this.isCollapse);
        if (this.isCollapse) {
          this.platform = true;
        } else {
          this.platform = false;
          this.activetip = "3-1";
        }
      } else if (this.openeds[0] == "5") {
        console.log(this.isCollapse);
        if (this.isCollapse) {
          this.warning = true;
        } else {
          this.warning = false;
          this.activetip = "5-1";
        }
      } else if (this.openeds[0] == "6") {
        if (this.isCollapse) {
          this.setting = true;
        } else {
          this.setting = false;
          this.activetip = "6-1";
        }
      }
    }
  }
};
</script>

<style>
.el-menu-vertical-demo:not(.el-menu--collapse) {
  width: 150px;
  min-height: 400px;
}
/* .el-menu-vertical-demo{
    overflow-x: auto;
    height: calc(100vh - 98px - 17px - 32px);
  } */
.el-menu-vertical-demo::-webkit-scrollbar {
  display: none;
}
.el-submenu__icon-arrow {
  display: none;
}
.el-submenu__icon-caret {
  position: absolute;
  top: 57%;
  /* right: 130px; */
  margin-top: -7px;
  -webkit-transition: -webkit-transform 0.3s;
  transition: -webkit-transform 0.3s;
  transition: transform 0.3s;
  transition: transform 0.3s, -webkit-transform 0.3s;
  font-size: 12px;
  left: 8px;
}
.el-radio-button,
.el-radio-button__inner {
  display: inline-block;
  position: relative;
  outline: 0;
  width: 10px;
}

span.el-radio-button__inner:hover {
  color: #fff;
  background-color: #313438;
}
.el-radio-button__inner {
  line-height: 1;
  white-space: nowrap;
  background: #fff;
  border: 1px solid #dcdfe6;
  font-weight: 500;
  border-left: 0;
  color: #fff;
  -webkit-appearance: none;
  text-align: center;
  box-sizing: border-box;
  margin: 0;
  cursor: pointer;
  -webkit-transition: all 0.3s cubic-bezier(0.645, 0.045, 0.355, 1);
  transition: all 0.3s cubic-bezier(0.645, 0.045, 0.355, 1);
  padding: 12px 20px;
  font-size: 14px;
  border-radius: 0;
  padding-left: 0px;
  padding-right: 0px;
}
.parent {
  display: flex;
}
.left {
  /* width: 200px; */
  /* height: 100%; */
  padding-left: 100px;
  overflow-x: auto;
  height: calc(100vh - 98px - 17px - 40px);
  /* overflow-y:scroll */
}
.left::-webkit-scrollbar {
  display: none;
}
.right {
    display: flex;
    -webkit-box-flex: 1;
    -ms-flex: 1;
    flex: 1;
    height: 100%;
    padding-right: 12px;
    padding-top: 290px;
    border-left: 1px solid #949799;
    padding-bottom: 460px;
}
.mainContainer .menuContainer ul {
  margin-right: 0px;
}
.mainContainer .menuContainer li {
  text-align: left;
  font-weight: 400;
  font-size: 14px;
  color: #4e4e4e;
  cursor: pointer;
  margin-bottom: 0px;
}
.el-menu {
  /* border-right: solid 1px #949799; */
  list-style: none;
  position: relative;
  margin: 0;
  padding-left: 0;
}
.mainContainer .menuContainer .level2 {
  padding: 6px 0 24px;
  font-size: 12px;
  margin: 0;
}
ul.el-menu.el-menu--inline li {
  font-size: 12px;
}
.one_image {
  display: inline-block;
  margin-right: 5px;
  width: 24px;
  text-align: center;
  /* font-size: 18px; */
  vertical-align: middle;
}
/* .el-menu-item {
    padding: 0 100px;
  }
  .el-submenu {
    padding-left: 100px;
  } */

/* .level2 li a.router-link-active, .no-children .router-link-active {
    background: #53afe4;
    color: white;
  }

  .children-active {
    font-weight: 700;
    color: #000000 !important;
    background: white;
  } */
.meeting_image {
  display: none;
}
.el-submenu__icon-arrow_add {
  position: absolute;
  top: 57%;
  margin-top: -7px;
  -webkit-transition: -webkit-transform 0.3s;
  transition: -webkit-transform 0.3s;
  transition: transform 0.3s;
  transition: transform 0.3s, -webkit-transform 0.3s;
  font-size: 12px;
  left: 8px;
}
/*菜单关闭*/
.el-submenu > .el-submenu__title .el-submenu__icon-caret {
  -webkit-transform: rotateZ(0deg);
  -ms-transform: rotate(0deg);
  transform: rotateZ(0deg);
}
/*菜单展开*/
.el-submenu.is-opened > .el-submenu__title .el-submenu__icon-caret {
  -webkit-transform: rotateZ(90deg);
  -ms-transform: rotate(90deg);
  transform: rotateZ(90deg);
}
/* .router-link-active {
    background: none;
    background-color: none;
    background: none;
} */
.el-menu--vertical {
  display: none;
}
/* img{
  position:absolute;
  clip:rect(0px 50px 200px 0px)
} */
/* .image_tab {
    width: 18px;
    height: 18px;
    object-fit: none;
} */
.el-icon-arrow-left .el-icon-arrow-right {
  position: absolute;
  left: -2px;
  top: 14px;
}
.router-link-active .targetMenu {
  color: white;
}
.router-link-active .selectMenu {
  color: #1e94da;
}
li.el-submenu.is-active.is-opened span.selectMenu {
  color: #1e94da;
}
/* 运行状态 */
#runstatus {
  width: 18px;
  height: 18px;
  background: url("../../assets/image/runstatus.png") 0 0;
}
.router-link-active #runstatus {
  background: url("../../assets/image/runstatus.png") -36px 0 !important;
}
#srunstatus {
  width: 18px;
  height: 18px;
  background: url("../../assets/image/runstatus.png") 0 0;
}
.router-link-active #srunstatus {
  background: url("../../assets/image/runstatus.png") -18px 0;
}
a:hover #runstatus {
  background: url("../../assets/image/runstatus.png") -18px 0;
}

/* 会议信息 */
.el-submenu.is-active.is-opened #meetinginfo {
  background: url("../../assets/image/meetinginfo.png") -18px 0;
}
a:hover #meetinginfo {
  background: url("../../assets/image/meetinginfo.png") -18px 0;
}
#meetinginfo {
  width: 18px;
  height: 18px;
  background: url("../../assets/image/meetinginfo.png") 0 0;
}
.router-link-active #meetinginfo {
  background: url("../../assets/image/meetinginfo.png") -18px 0;
}
.actived button#meetinginfo {
  background: url("../../assets/image/meetinginfo.png") -18px 0;
}
li.el-submenu.is-active.is-opened button#meetinginfo {
  background: url("../../assets/image/meetinginfo.png") -18px 0;
}
#livemeetimg {
  width: 18px;
  height: 18px;
  background: url("../../assets/image/livemeeting.png") 0 0;
}
.router-link-active #livemeetimg {
  background: url("../../assets/image/livemeeting.png") -36px 0 !important;
}
#livemeetimgs {
  width: 18px;
  height: 18px;
  background: url("../../assets/image/livemeeting.png") 0 0;
}
.router-link-active #livemeetimgs {
  background: url("../../assets/image/livemeeting.png") -18px 0;
}
a:hover #livemeetimg {
  background: url("../../assets/image/livemeeting.png") -18px 0;
}
#historymeetimg {
  width: 18px;
  height: 18px;
  background: url("../../assets/image/historymeeting.png") 0 0;
}
.router-link-active #historymeetimg {
  background: url("../../assets/image/historymeeting.png") -36px 0 !important;
}
#historymeetimgs {
  width: 18px;
  height: 18px;
  background: url("../../assets/image/historymeeting.png") 0 0;
}
.router-link-active #historymeetimgs {
  background: url("../../assets/image/historymeeting.png") -18px 0;
}
a:hover #historymeetimg {
  background: url("../../assets/image/historymeeting.png") -18px 0;
}
/* 设备管理 */
.el-submenu.is-active.is-opened #equipment {
  background: url("../../assets/image/equipment.png") -18px 0;
}
a:hover #equipment {
  background: url("../../assets/image/equipment.png") -18px 0;
}
#equipment {
  width: 18px;
  height: 18px;
  background: url("../../assets/image/equipment.png") 0 0;
}
.router-link-active #equipment {
  background: url("../../assets/image/equipment.png") -18px 0;
}
.actived button#equipment {
  background: url("../../assets/image/equipment.png") -18px 0;
}
li.el-submenu.is-active.is-opened button#equipment {
  background: url("../../assets/image/equipment.png") -18px 0;
}
#serverequipment {
  width: 18px;
  height: 18px;
  background: url("../../assets/image/serverequipment.png") 0 0;
}
.router-link-active #serverequipment {
  background: url("../../assets/image/serverequipment.png") -36px 0 !important;
}
#serverequipments {
  width: 18px;
  height: 18px;
  background: url("../../assets/image/serverequipment.png") 0 0;
}
.router-link-active #serverequipments {
  background: url("../../assets/image/serverequipment.png") -18px 0;
}
a:hover #serverequipment {
  background: url("../../assets/image/serverequipment.png") -18px 0;
}
#terminalequipment {
  width: 18px;
  height: 18px;
  background: url("../../assets/image/terminalequipment.png") 0 0;
}
.router-link-active #terminalequipment {
  background: url("../../assets/image/terminalequipment.png") -36px 0 !important;
}
#terminalequipments {
  width: 18px;
  height: 18px;
  background: url("../../assets/image/terminalequipment.png") 0 0;
}
.router-link-active #terminalequipments {
  background: url("../../assets/image/terminalequipment.png") -18px 0;
}
a:hover #terminalequipment {
  background: url("../../assets/image/terminalequipment.png") -18px 0;
}
#inspection {
  width: 18px;
  height: 18px;
  background: url("../../assets/image/inspection.png") 0 0;
}
.router-link-active #inspection {
  background: url("../../assets/image/inspection.png") -36px 0 !important;
}
#inspections {
  width: 18px;
  height: 18px;
  background: url("../../assets/image/inspection.png") 0 0;
}
.router-link-active #inspections {
  background: url("../../assets/image/inspection.png") -18px 0;
}
a:hover #inspection {
  background: url("../../assets/image/inspection.png") -18px 0;
}
/* 诊断抓包 */
a:hover #diagnostic {
  background: url("../../assets/image/diagnostic.png") -18px 0;
}
#diagnostic {
  width: 18px;
  height: 18px;
  background: url("../../assets/image/diagnostic.png") 0 0;
}
.router-link-active #diagnostic {
  background: url("../../assets/image/diagnostic.png") -36px 0 !important;
}
#diagnostics {
  width: 18px;
  height: 18px;
  background: url("../../assets/image/diagnostic.png") 0 0;
}
.router-link-active #diagnostics {
  background: url("../../assets/image/diagnostic.png") -18px 0;
}
/* 设置告警 */
.el-submenu.is-active.is-opened #equipmentwarning {
  background: url("../../assets/image/equipmentwarning.png") -18px 0;
}
a:hover #equipmentwarning {
  background: url("../../assets/image/equipmentwarning.png") -18px 0;
}
#equipmentwarning {
  width: 18px;
  height: 18px;
  background: url("../../assets/image/equipmentwarning.png") 0 0;
}
.router-link-active #equipmentwarning {
  background: url("../../assets/image/equipmentwarning.png") -18px 0;
}
.actived button#equipmentwarning {
  background: url("../../assets/image/equipmentwarning.png") -18px 0;
}
li.el-submenu.is-active.is-opened button#equipmentwarning {
  background: url("../../assets/image/equipmentwarning.png") -18px 0;
}
#subwarning {
  width: 18px;
  height: 18px;
  background: url("../../assets/image/subwarning.png") 0 0;
}
.router-link-active #subwarning {
  background: url("../../assets/image/subwarning.png") -36px 0 !important;
}
#subwarnings {
  width: 18px;
  height: 18px;
  background: url("../../assets/image/subwarning.png") 0 0;
}
.router-link-active #subwarnings {
  background: url("../../assets/image/subwarning.png") -18px 0;
}
a:hover #subwarning {
  background: url("../../assets/image/subwarning.png") -18px 0;
}
#unrepairedwarning {
  width: 18px;
  height: 18px;
  background: url("../../assets/image/unrepairedwarning.png") 0 0;
}
.router-link-active #unrepairedwarning {
  background: url("../../assets/image/unrepairedwarning.png") -36px 0 !important;
}
#unrepairedwarnings {
  width: 18px;
  height: 18px;
  background: url("../../assets/image/unrepairedwarning.png") 0 0;
}
.router-link-active #unrepairedwarnings {
  background: url("../../assets/image/unrepairedwarning.png") -18px 0;
}
a:hover #unrepairedwarning {
  background: url("../../assets/image/unrepairedwarning.png") -18px 0;
}
#repairedwarning {
  width: 18px;
  height: 18px;
  background: url("../../assets/image/repairedwarning.png") 0 0;
}
.router-link-active #repairedwarning {
  background: url("../../assets/image/repairedwarning.png") -36px 0 !important;
}
#repairedwarnings {
  width: 18px;
  height: 18px;
  background: url("../../assets/image/repairedwarning.png") 0 0;
}
.router-link-active #repairedwarnings {
  background: url("../../assets/image/repairedwarning.png") -18px 0;
}
a:hover #repairedwarning {
  background: url("../../assets/image/repairedwarning.png") -18px 0;
}
/* 系统配置 */
.el-submenu.is-active.is-opened #sysedit {
  background: url("../../assets/image/sysedit.png") -18px 0;
}
a:hover #sysedit {
  background: url("../../assets/image/sysedit.png") -18px 0;
}
#sysedit {
  width: 18px;
  height: 18px;
  background: url("../../assets/image/sysedit.png") 0 0;
}
.router-link-active #sysedit {
  background: url("../../assets/image/sysedit.png") -18px 0;
}
.actived button#sysedit {
  background: url("../../assets/image/sysedit.png") -18px 0;
}
li.el-submenu.is-active.is-opened button#sysedit {
  background: url("../../assets/image/sysedit.png") -18px 0;
}
#thresholdvalueedit {
  width: 18px;
  height: 18px;
  background: url("../../assets/image/thresholdvalueedit.png") 0 0;
}
.router-link-active #thresholdvalueedit {
  background: url("../../assets/image/thresholdvalueedit.png") -36px 0 !important;
}
#thresholdvalueedits {
  width: 18px;
  height: 18px;
  background: url("../../assets/image/thresholdvalueedit.png") 0 0;
}
.router-link-active #thresholdvalueedits {
  background: url("../../assets/image/thresholdvalueedit.png") -18px 0;
}
a:hover #thresholdvalueedit {
  background: url("../../assets/image/thresholdvalueedit.png") -18px 0;
}
#warningedit {
  width: 18px;
  height: 18px;
  background: url("../../assets/image/warningedit.png") 0 0;
}
.router-link-active #warningedit {
  background: url("../../assets/image/warningedit.png") -36px 0 !important;
}
#warningedits {
  width: 18px;
  height: 18px;
  background: url("../../assets/image/warningedit.png") 0 0;
}
.router-link-active #warningedits {
  background: url("../../assets/image/warningedit.png") -18px 0;
}
a:hover #warningedit {
  background: url("../../assets/image/warningedit.png") -18px 0;
}
#equipmentedit {
  width: 18px;
  height: 18px;
  background: url("../../assets/image/equipmentedit.png") 0 0;
}
.router-link-active #equipmentedit {
  background: url("../../assets/image/equipmentedit.png") -36px 0 !important;
}
#equipmentedits {
  width: 18px;
  height: 18px;
  background: url("../../assets/image/equipmentedit.png") 0 0;
}
.router-link-active #equipmentedits {
  background: url("../../assets/image/equipmentedit.png") -18px 0;
}
a:hover #equipmentedit {
  background: url("../../assets/image/equipmentedit.png") -18px 0;
}
#limitedit {
  width: 18px;
  height: 18px;
  background: url("../../assets/image/limitedit.png") 0 0;
}
.router-link-active #limitedit {
  background: url("../../assets/image/limitedit.png") -36px 0 !important;
}
#limitedits {
  width: 18px;
  height: 18px;
  background: url("../../assets/image/limitedit.png") 0 0;
}
.router-link-active #limitedits {
  background: url("../../assets/image/limitedit.png") -18px 0;
}
a:hover #limitedit {
  background: url("../../assets/image/limitedit.png") -18px 0;
}
/* 版本管理 */
a:hover #versionmanagement {
  background: url("../../assets/image/versionmanagement.png") -18px 0;
}
#versionmanagement {
  width: 18px;
  height: 18px;
  background: url("../../assets/image/versionmanagement.png") 0 0;
}
.router-link-active #versionmanagement {
  background: url("../../assets/image/versionmanagement.png") -36px 0 !important;
}
#versionmanagements {
  width: 18px;
  height: 18px;
  background: url("../../assets/image/versionmanagement.png") 0 0;
}
.router-link-active #versionmanagements {
  background: url("../../assets/image/versionmanagement.png") -18px 0;
}
/* 操作日志 */
a:hover #logmanagement {
  background: url("../../assets/image/logmanagement.png") -18px 0;
}
#logmanagement {
  width: 18px;
  height: 18px;
  background: url("../../assets/image/logmanagement.png") 0 0;
}
.router-link-active #logmanagement {
  background: url("../../assets/image/logmanagement.png") -36px 0 !important;
}
#logmanagements {
  width: 18px;
  height: 18px;
  background: url("../../assets/image/logmanagement.png") 0 0;
}
.router-link-active #logmanagements {
  background: url("../../assets/image/logmanagement.png") -18px 0;
}
</style>
