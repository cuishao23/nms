<template>
  <el-row type="flex" class="nms-header" justify="space-around" :gutter="1">
    <el-col :span="5" class="logo-parent">
      <div class="logo">
        <div>
          <img
            src="../../assets/image/logo1.png"
            v-if="brand==='0' || brand==='1'"
            @click="go_home()"
            style="cursor: pointer;"
          />
          <img
            src="../../assets/image/logo2.png"
            v-if="brand==='2' || brand==='3'"
            @click="go_home()"
            style="cursor: pointer;"
          />
        </div>
        <div>
          <img src="../../assets/image/header_cutline.png" />
          <span id="fontTitle" v-if="brand==='0'||brand==='1'" @click="go_home()">科达视讯云</span>
          <span id="fontTitle" v-if="brand==='2'||brand==='3'" @click="go_home()">新视通 (4G版)</span>
        </div>
      </div>
    </el-col>
    <el-col :span="5">
      <div class="grid-content bg-purple-light"></div>
    </el-col>
    <el-col :span="5" class="user-info">
      <div class="user-header">
        <img src="../../assets/image/user_header.png" />
      </div>
      <span id="userInfo">{{ user }}</span>
      <el-dropdown trigger="click" placement="bottom-end">
        <span class="el-dropdown-link nms-set" />
        <el-dropdown-menu slot="dropdown">
          <!--<el-dropdown-item><a id="modifytimezone" href="/personalsettings/zoneset/">GMT+8</a></el-dropdown-item>
          </el-dropdown-item>-->
          <el-dropdown-item>
            <a id="help" @click="help()">帮助信息</a>
          </el-dropdown-item>
          <el-dropdown-item>
            <a id="about" @click="about()">关于</a>
          </el-dropdown-item>
        </el-dropdown-menu>
      </el-dropdown>
      <a id="exit" @click="logout()"></a>
      <nms-dialog
        title="提示"
        ref="logout"
        width="300px"
        height="200px"
        :confirmBtn="true"
        :cancelBtn="true"
        @confirm="confirmLogout"
        @cancel="cancelLogout"
      >
        <div slot="content" class="tbl-dlg">
          <p class="note-content">确认退出系统?</p>
        </div>
      </nms-dialog>
      <nms-dialog
        title="关于"
        ref="about"
        width="400px"
        height="300px"
        :confirmBtn="false"
        :cancelBtn="false"
      >
        <div slot="content" class="tbl-dlg">
          <div class="about-container" v-if="brand == 0">
            <div class="about-logo">
              <img src="../../assets/image/about_kedacom.png" alt />
              <img src="../../assets/image/about_moyun.png" alt />
            </div>
            <p class="about-title">/ 网管系统</p>
            <div class="about-item-container">
              <p class="about-item">苏州科达科技股份有限公司 版权所有</p>
              <p class="about-item">Copyright © 1995-{{year}} KEDACOM. All Rights Reserved.</p>
              <div class="about-item">Version:{{version}}</div>
              <div style="margin-top: 9px;">
                <a class="about-url" href="http://www.kedacom.com">www.kedacom.com</a>
                <a class="about-url" href="http://www.movision.com">www.movision.com</a>
              </div>
            </div>
          </div>
          <div class="about-container" v-if="brand == 1">
            <div class="about-logo">
              <img src="../../assets/image/about_kedacom.png" alt />
            </div>
            <p class="about-title">/ 网管系统</p>
            <div class="about-item-container">
              <p class="about-item">苏州科达科技股份有限公司 版权所有</p>
              <p class="about-item">Copyright © 1995-{{year}} KEDACOM. All Rights Reserved.</p>
              <div class="about-item">
                Version:{{version}}
                <span style="margin-left: 20px;">
                  <a class="about-url" href="http://www.kedacom.com">www.kedacom.com</a>
                </span>
              </div>
            </div>
          </div>
          <div class="about-container" v-if="brand == 2">
            <div class="about-logo">
              <img src="../../assets/image/about_telecom.png" alt />
            </div>
            <p class="about-title">/ 网管系统</p>
            <div class="about-item-container">
              <p class="about-item">中国电信视频服务产品（上海）运营中心 版权所有</p>
              <p class="about-item">Copyright © {{year}}}. All rights reserved.</p>
              <div class="about-item">
                Version:{{version}}
                <span style="margin-left: 20px;">
                  <a class="about-url" href="http://xst.189.cn">xst.189.cn</a>
                </span>
              </div>
            </div>
          </div>
          <div class="about-container" v-if="brand == 3">
            <div class="about-logo">
              <img src="../../assets/image/about_telecom.png" alt />
            </div>
            <p class="about-title">/ 网管系统</p>
            <div class="about-item-container">
              <p class="about-item">中国电信视频服务产品（上海）运营中心 版权所有</p>
              <p class="about-item">Copyright © {{year}} All rights reserved.</p>
              <div class="about-item">
                Version:{{version}}
                <span style="margin-left: 20px;">
                  <a class="about-url" href="http://xst.189.cn">xst.189.cn</a>
                </span>
              </div>
            </div>
          </div>
          <div class="about-container" v-if="brand > 3">
            <div class="about-logo">
              <img src="../../assets/image/about_kedacom.png" alt />
            </div>
            <p class="about-title">/ 网管系统</p>
            <div class="about-item-container">
              <p class="about-item">苏州科达科技股份有限公司 版权所有</p>
              <p class="about-item">Copyright © 1995-{{year}} KEDACOM. All Rights Reserved.</p>
              <div class="about-item">
                Version:{{version}}
                <span style="margin-left: 20px;">
                  <a class="about-url" href="http://www.kedacom.com">www.kedacom.com</a>
                </span>
              </div>
            </div>
          </div>
        </div>
      </nms-dialog>
    </el-col>
  </el-row>
</template>

<script>
import ElRow from "element-ui/packages/row/src/row";
import NmsDialog from "components/common/nms-dialog";
import api from "../../axios";
import cookie from "cookie";
export default {
  components: { ElRow, NmsDialog },
  name: "nms-header",
  data() {
    return {
      brand: "",
      version: "",
      user: "",
      year: ""
    };
  },
  created: function() {
    api
      .getServerInfo()
      .then(res => {
        this.brand = res.brand;
        this.version = res.version;
        this.user = res.user;
        if (res.brand == "2") {
          document.title = "新世通(4G)-网管系统";
        } else {
          document.title = "科达视讯云-网管系统";
        }
      })
      .catch(error => {
        console.log(error);
      });
  },
  mounted: function() {
    let date = new Date();
    this.year = date.getFullYear();
  },
  methods: {
    help: function() {
      window.open('/nms/default.html')
    },
    go_home() {
      var ck = cookie.parse(document.cookie);
      console.log(ck);
      if (ck.portal) {
        document.location = ck.portal;
      }
    },
    about: function() {
      this.$refs.about.open();
    },
    logout: function() {
      this.$refs.logout.open();
    },
    confirmLogout: function() {
      this.$refs.logout.close();
      api.logout().then(res => {
        let ck = cookie.parse(document.cookie);
        if (ck.portal == undefined) {
          document.location = "/portal/login"
        }else{
          document.location = ck.portal + "/login"
        }
      });
    },
    cancelLogout: function() {
      console.log("cancel logout");
      this.$refs.logout.close();
    }
  }
};
</script>

<style scoped>
.logo-parent {
  display: flex;
  display: -webkit-flex;
  /* justify-content: center; */
}

.logo {
  display: flex;
  justify-content: center;
}

.logo div,
.logo span {
  padding: 0px 10px 0px 0px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.user-header {
  display: flex;
  align-items: center;
}

.nms-header {
  width: 100vw;
  min-width: 720px;
  height: 54px;
  background-color: #373d41;
  position: fixed;
  top: 0;
  left: 0;
  z-index: 100;
}

.nms-header #fontTitle {
  cursor: pointer;
  float: left;
  color: #fff;
  margin-left: 10px;
  font: bold 13px/13px Microsoft YaHei;
}

.nms-header #exit {
  width: 24px;
  height: 24px;
  margin: 15px 0 0 0;
  background: url("../../assets/image/exit_all.png");
}

.nms-header #exit:hover {
  background: url("../../assets/image/exit_all.png") -24px 0px;
}

.el-dropdown {
  height: 68px;
}

.popper__arrow {
  display: none;
}

.nms-set {
  display: flex;
  align-items: baseline;
  width: 24px;
  height: 24px;
  margin: 15px 10px 0 0;
  background: url("../../assets/image/set_info.png");
}

.el-dropdown-menu,
.el-dropdown-menu__item {
  background: none repeat scroll 0% 0% #fff;
  /*border: 2px solid #E5E5E5;*/
  color: #333;
}

.el-dropdown-menu__item a {
  color: #4e4e4e;
  font-size: 12px;
  text-decoration: none;
  display: block;
  height: 100%;
}

.el-dropdown-menu__item {
  line-height: 34px;
  width: 112px;
  text-align: center;
  padding: 0px 0px 0px 0px;
}

.el-dropdown-menu__item a:hover,
.el-dropdown-menu__item:hover,
.el-dropdown-menu__item:hover a {
  background: none repeat scroll 0% 0% #46aae4;
  color: #fff;
}

.nms-set:hover {
  background: url("../../assets/image/set_info.png") -24px 0px;
}

.nms-header #userInfo {
  height: 12px;
  margin: 20px 18px 0 0;
  color: #fff;
  font: 12px/12px Microsoft YaHei;
}

.user-info {
  display: flex;
  justify-content: flex-end;
}

a:link {
  cursor: pointer;
}

.tbl-dlg {
  text-align: center;
  width: 100%;
  height: 100%;
  display: -webkit-box;
  display: -ms-flexbox;
  display: flex;
  -webkit-box-pack: center;
  -ms-flex-pack: center;
  justify-content: center;
  -webkit-box-align: center;
  -ms-flex-align: center;
  align-items: center;
}
.note-content {
  font-size: 12px;
  color: #4e4e4e;
  white-space: nowrap;
  overflow: auto;
  height: 21px;
  line-height: 21px;
  background: url(../../assets/image/prompt.png) no-repeat;
  padding-left: 30px;
}

.about-container {
  text-align: left;
  position: relative;
}

.about-title {
  font-size: 14px;
  font-weight: bold;
  color: #4e4e4e;
  position: absolute;
  top: 60px;
  right: 30px;
}

.about-item-container {
  margin-top: 55px;
}

.about-item {
  margin-top: 9px;
  font-size: 12px;
  color: #4e4e4e;
}

.about-url {
  font-size: 12px;
  color: #007ac0 !important;
  text-decoration: underline !important;
  margin-right: 17px;
}
</style>
