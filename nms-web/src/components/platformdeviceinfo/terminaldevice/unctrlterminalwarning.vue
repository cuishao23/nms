<template>
  <div class="unctrl-terminal-warning">
    <div class="unctrl-terminal-back">
      <span class="back-btn" @click="$router.go(-1)"></span>
      <span class="base-info-title">终端告警信息</span>
    </div>
    <div class="old-terminal-fields">
      <nms-key-value label="设备IP" :value="deviceIp"/>
      <nms-key-value label="设备类型" :value="deviceType"/>
      <nms-key-value label="在线状态" :value="online"/>
      <nms-key-value label="E164号" :value="deviceE164"/>
      <nms-key-value label="版本号" :value="deviceVersion"/>
    </div>
    <div class="warning">
      <el-checkbox v-model="critical">严重</el-checkbox>
      <el-checkbox v-model="important">重要</el-checkbox>
      <el-checkbox v-model="normal">一般</el-checkbox>
      <el-select v-model="timePeriodValue" class="time" filterable>
        <el-option v-for="item in timePeriod"
                   :key="item.value"
                   :label="item.label"
                   :value="item.value"/>
      </el-select>
      <div style="display: inline-block; width: 16px"></div>
      <DateBox v-if="reSet" inputId="d1" v-model="startDate" style="width: 150px" format="yyyy-MM-dd" :disabled="timePeriodValue !== 'selfdefine'"></DateBox>
      <div style="display: inline-block; width: 19px">→</div>
      <DateBox v-if="reSet" inputId="d2" v-model="endDate" style="width: 150px;" format="yyyy-MM-dd" :disabled="timePeriodValue !== 'selfdefine'"></DateBox>
      <button class='search' @click="searchUncontroledTerminalWarnings()"></button>
    </div>
    <div class="table_show">
      <div v-if="uncontroledTerminalWarningList.length === 0" class="no-info-tip">
        没有满足条件的告警信息！
      </div>
      <div v-if="uncontroledTerminalWarningList.length > 0">
        <nms-pager-table :data="uncontroledTerminalWarningList" :fields="uncontroledTerminalWarningFields"  :total-page="uncontroledTerminalWarningTotalPage" :biao-zhi="cage" v-model="curPage"/>
      </div>
    </div>
  </div>
</template>

<script>
  import axios from 'axios';
  import api from '../../../axios';
  import NmsKeyValue from "../../common/nms-key-value";
  import {getTimePeriod} from "../../../assets/js/common";
  import {getUncontroledTerminalWarningFields} from 'assets/js/subwarninginfo';
  import NmsPagerTable from "../../../components/common/nms-pager-table";
  import {FormatTime,get_time} from 'assets/js/common';

  export default {
    components: {NmsKeyValue,NmsPagerTable},
    name: "unctrlterminalwarning",
    data() {
      return {
        reSet: true,
        deviceName: '',
        deviceIp: '',
        deviceType: '',
        deviceE164: '',
        online: '',
        deviceVersion: '',
        typeList: [],

        critical: true,
        important: true,
        normal: true,

        timePeriod: [],
        timePeriodValue: 'lastweek',
        timeRange: [],

        uncontroledTerminalWarningList: [],
        uncontroledTerminalWarningFields: [],
        uncontroledTerminalWarningTotalPage:1, // 总页数
        perPage: 10, // 表格每页显示数量
        curPage: 1, // 当前页
        cage: 1, // 搜索当前页归1标志符

        startDate: new Date(),
        endDate: new Date(),
      }
    },
    activated: function () {
      this.deviceIp = this.$route.params.ip
      this.deviceVersion = this.$route.params.version
      this.deviceName = this.$route.params.name
      this.deviceType = this.$route.params.type
      this.deviceE164 = this.$route.params.e164
      this.online = this.$route.params.online
      this.timePeriod = getTimePeriod()
      this.startDate=get_time(this.timePeriodValue)
      this.getUnconTerWarnings()
    },
    watch: {
      startDate: function(newTime, oldTime) {
        if ((this.endDate - newTime) < 0 && this.endDate !== null && FormatTime(newTime).substr(0, 10) !== FormatTime(this.endDate).substr(0, 10)) {
          this.startDate = oldTime
          this.errorDialog.open('起始时间不得超过截至时间')
          this.reSet = false
          this.$nextTick(() => {
            this.reSet = true
          })
        }
      },
      endDate: function(newTime, oldTime) {
        if ((newTime - this.startDate) < 0 && FormatTime(newTime).substr(0, 10) !== FormatTime(this.startDate).substr(0, 10)) {
          this.endDate = oldTime
          this.errorDialog.open('截至时间不得小于起始时间')
          this.reSet = false
          this.$nextTick(() => {
            this.reSet = true
          })
        }
      },
      timePeriodValue: function (newTime, oldTime) {
        if(get_time(newTime)!=""){
          this.startDate=get_time(newTime)
        }
      },
      curPage: function (newPageNum, oldPageNum) {
        var start_time = FormatTime(this.startDate)
        var end_time = FormatTime(this.endDate)
        if(start_time.split(" ")[0]==FormatTime(new Date()).split(" ")[0]){
          start_time = FormatTime(new Date(new Date().toLocaleDateString()).getTime())
        }
        this.cage = 1
        api.getUncontroledTerminalWarnings({params:{
            newPageNum: newPageNum,
            critical: this.critical,
            important: this.important,
            normal: this.normal,
            deviceIp: this.deviceIp,
            starttime: start_time,
            stoptime: end_time
          }
        }).then(res => {
          if(res.success==1){
            this.uncontroledTerminalWarningList = res.data
            this.uncontroledTerminalWarningFields = getUncontroledTerminalWarningFields()
            this.uncontroledTerminalWarningTotalPage = Math.ceil(res.total_num / this.perPage)
          }
        })
        .catch((error) => {
          console.log(error);
        })
      }
    },
    methods: {
      getUnconTerWarnings: function () {
        let start_time = FormatTime(this.startDate)
        let end_time = FormatTime(this.endDate)
        console.log("critical"+this.critical)
        console.log("important"+this.important)
        console.log("normal"+this.normal)
        console.log("deviceIp"+this.deviceIp)
        console.log("start_time"+start_time)
        console.log("end_time"+end_time)
        api.getUncontroledTerminalWarnings({params:{
              newPageNum: 1,
              critical: this.critical,
              important: this.important,
              normal: this.normal,
              deviceIp: this.deviceIp,
              starttime: start_time,
              stoptime: end_time
            }
          }).then(res => {
            if(res.success==1){
              this.uncontroledTerminalWarningList = res.data
              this.uncontroledTerminalWarningFields = getUncontroledTerminalWarningFields()
              this.uncontroledTerminalWarningTotalPage = Math.ceil(res.total_num / this.perPage)
            }
          })
          .catch( (error) => {
            console.log(error);
          });
      },
      searchUncontroledTerminalWarnings: function () {
        var start_time = FormatTime(this.startDate)
        var end_time = FormatTime(this.endDate)
        if (this.timePeriodValue == "lasthour") {
          start_time = start_time
        } else {
          if(start_time.split(" ")[0]==FormatTime(new Date()).split(" ")[0]){
            start_time = FormatTime(new Date(new Date().toLocaleDateString()).getTime())
          }
        }
        api.getUncontroledTerminalWarnings({params:{
            newPageNum: 1,
            critical: this.critical,
            important: this.important,
            normal: this.normal,
            deviceIp: this.deviceIp,
            starttime: start_time,
            stoptime: end_time
          }
        }).then(res => {
          if(res.success==1){
            this.uncontroledTerminalWarningList = res.data
            this.uncontroledTerminalWarningFields = getUncontroledTerminalWarningFields()
            this.uncontroledTerminalWarningTotalPage = Math.ceil(res.total_num / this.perPage)
            this.cage = 2
          }
        })
        .catch( (error) => {
          console.log(error);
        });
      }
    }
  }
</script>

<style scoped>
  .old-terminal-fields {
    position: relative;
    top: 20px;
    clear: left;
    display: flex;
    justify-content: start;
  }

  .warning {
    position: relative;
    top: 40px;
    text-align: left;
  }
  .no-info-tip {
    text-align: left;
    padding-top: 13px;
  }
  .table_show {
    padding-top: 50px;
  }
</style>
