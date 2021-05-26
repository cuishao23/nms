<template>
  <div class="settings-container">
    <div class="settings">
      <div class="save-area">
        <button class="normal-btn">保存</button>
        <button class="normal-btn" @click="OnCancelSetting()">取消</button>
      </div>
      <el-tabs v-model="settingType" class="tabs">
        <el-tab-pane label="个人信息" name="personalinfo">
          <div class="cfg-pane">
            <div>
              <span>账号</span>
              <span>{{account}}</span>
            </div>
            <div>
              <span>姓名</span>
              <input type="text" v-model="userName">
            </div>
            <div>
              <span>邮箱</span>
              <input type="text">
            </div>
            <div>
              <span>手机</span>
              <input type="text">
            </div>
            <div>
              <span>座机</span>
              <div class="tel">
                <input type="text">
                <span>-</span>
                <input type="text">
                <span>-</span>
                <input type="text">
              </div>
            </div>
          </div>
        </el-tab-pane>
        <el-tab-pane label="修改密码" name="changepwd">
          <div class="cfg-pane">
            <div>
              <span>当前密码</span>
              <input type="text">
            </div>
            <div>
              <span>新 密 码</span>
              <input type="text">
            </div>
            <div>
              <span>确认密码</span>
              <input type="text">
            </div>
          </div>
        </el-tab-pane>
        <el-tab-pane label="时区" name="zoneset">
          <div class="zones">
            <el-radio v-for="zone in timeZoneList" v-model="timeZone" :label="zone.value" :key="zone.value" class="zone-item">{{zone.title}}</el-radio>
          </div>
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>

<script>
  import {getTimeZoneList} from 'assets/js/timezones'

  export default {
    name: "personalsettings",
    data() {
      return {
        settingType: 'personalinfo',
        account: 'administrator',
        userName: 'administrator',
        timeZoneList: [],
        timeZone: ''
      }
    },
    mounted: function () {
      console.log('mounted')
      this.settingType = this.$route.params.type
      console.log('type: ' + this.settingType)
      this.timeZoneList = getTimeZoneList()
    },
    methods: {
      OnCancelSetting: function () {
        this.$router.push('/baseinfo')
      }
    },
    watch: {
      
    }
  }
</script>

<style scoped>
  .save-area {
    display: inline;
    float: right;
    position: relative;
    /*z-index: 2;*/
  }
  .settings-container {
    text-align: center;
    position: relative;
    top: 60px;
  }
  .tabs {
    float: left;
  }
  .settings {
    width: 1024px;
    margin: auto;
  }
  .el-tabs {
    width: auto;
  }

  .cfg-pane {
    text-align: left;
  }

  .cfg-pane div {
    margin-top: 22px;
    margin-bottom: 27px;
  }

  span {
    font-size: 12px;
    color: #4e4e4e;
  }

  div span:first-child {
    width: 60px;
    display: inline-block;
  }

  div input {
    width: 250px;
  }

  div.tel {
    display: inline;
  }

  div.tel input {
    width: 74px;
  }

  .zones {
    display: block;
    text-align: left;
    overflow-y: scroll;
    width: 800px;
    height: 600px;
  }

  .zone-item {
    width: 500px;
    font-size: 12px;
    color: #4e4e4e;
    margin-top: 15px;
  }

  .el-radio + .el-radio {
    margin-left: 0px;
  }
</style>
