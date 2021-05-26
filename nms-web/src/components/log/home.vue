<template>
  <div class="log-content">
    <div class="log_tab">
      <input type="text" class="filter-text" v-model="userName" placeholder="用户名"/>
      <el-select v-model="operateType" value="" placeholder="操作类型" filterable>
        <el-option
          v-for="(item,index) in operateTypes"
          :key="index"
          :label="item.text"
          :value="item.value">
        </el-option>
      </el-select>
      <el-select v-model="operateLevel" value="" placeholder="操作等级" filterable>
        <el-option
          v-for="(item,index) in operateLevels"
          :key="index"
          :label="item.text"
          :value="item.value">
        </el-option>
      </el-select>
      <el-select v-model="timePeriodValue" value="" placeholder="最近一周" filterable>
        <el-option
          v-for="(item,index) in timePeriod"
          :key="index"
          :label="item.label"
          :value="item.value">
        </el-option>
      </el-select>
      <div style="display: inline-block; width: 16px"></div>
      <DateBox v-if="reSet" inputId="d1" v-model="startDate" style="width: 110px" format="yyyy-MM-dd" :disabled="timePeriodValue !== 'selfdefine'"></DateBox>
      <div style="display: inline-block; width: 19px">→</div>
      <DateBox v-if="reSet" inputId="d2" v-model="endDate" style="width: 110px;" format="yyyy-MM-dd" :disabled="timePeriodValue !== 'selfdefine'"></DateBox>
      <button class='search' @click="searchLog()"></button>
      <button class="normal-btn export" @click="onExport()">导出</button>
    </div>
    <div v-if="logList.length === 0" class="no-info-tip">
      <span class="PromptImg"></span>
      <span>没有日志信息！</span>
    </div>
    <div v-if="logList.length > 0" class="log-table">
      <nms-pager-table :data="logList" :fields="logFields" :total-page="logTotalPage" :biao-zhi="cage" v-model="curPage"/>
    </div>
  </div>
</template>

<script>
  import * as logJs from "../../assets/js/log";
  import {getLongTimePeriod} from "../../assets/js/common";
  import api from '../../axios';
  import NmsPagerTable from "../common/nms-pager-table";
  import qs from 'qs';
  import {FormatTime,get_time} from 'assets/js/common';
  import {Upexcele}  from '../../common/commonFunction'

  export default {
    name: "log-home",
    components: {NmsPagerTable},
    data() {
      return {
        reSet: true,
        userName: '',
        operateType: '.*',
        operateLevel: '.*',
        timePeriodValue: 'lastweek',
        operateTypes: logJs.operateTypes,
        operateLevels: logJs.operateLevels,
        timePeriod: [],
        timeRange: [],
        logList: [],
        logFields: [],
        perPage: 10, // 表格每页显示数量
        logTotalPage: 1, // 总页数
        curPage: 1, // 当前页
        cage: 1, // 搜索curPage归1标志码

        startDate: new Date(),
        endDate: new Date(),
      }
    },
    created: function () {
      this.timePeriod = getLongTimePeriod()
      this.startDate = get_time(this.timePeriodValue)
      let start_time = FormatTime(this.startDate)
      let end_time = FormatTime(this.endDate)
      api.getLogInfo({params: {
            newPageNum: 1,
            userName: this.userName,
            operateType: this.operateType,
            operateLevel: this.operateLevel,
            starttime: start_time,
            stoptime: end_time
          }
        }).then(res => {
          console.log(res);
          this.logList = res.logs;
          this.logFields = logJs.getLogsTableFields();
          this.logTotalPage = Math.ceil(res.log_total_num / this.perPage);
        })
        .catch((error) => {
          console.log(error);
        });
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
        if (get_time(newTime)!="") {
          this.startDate = get_time(newTime)
        }
      },
      curPage: function (newPageNum, oldPageNum) {
        var start_time = FormatTime(this.startDate)
        var end_time = FormatTime(this.endDate)
        if (start_time.split(" ")[0] == FormatTime(new Date()).split(" ")[0]) {
          start_time = FormatTime(new Date(new Date().toLocaleDateString()).getTime())
        }
        this.cage = 1
        api.getLogInfo({params: {
            newPageNum: newPageNum,
            userName: this.userName,
            operateType: this.operateType,
            operateLevel: this.operateLevel,
            starttime: start_time,
            stoptime: end_time
          }
        }).then(res => {
          console.log(res);
          this.logList = res.logs;
          this.logFields = logJs.getLogsTableFields();
          this.logTotalPage = Math.ceil(res.log_total_num / this.perPage);
        })
        .catch((error) => {
          console.log(error);
        })
      }
    },
    methods: {
      onExport: function () {
        var start_time = FormatTime(this.startDate)
        var end_time = FormatTime(this.endDate)
        if (start_time.split(" ")[0]==FormatTime(new Date()).split(" ")[0]) {
          start_time = FormatTime(new Date(new Date().toLocaleDateString()).getTime())
        }
        api.getLogDownLoad({params: {
          userName: this.userName,
          operateType: this.operateType,
          operateLevel: this.operateLevel,
          starttime: start_time,
          stoptime: end_time
        }, responseType: 'blob'}).then(res => {
          Upexcele(res, '操作日志信息.xls')
        }).catch(error => {
          console.log(error)
        });
      },
      searchLog: function () {
        var start_time = FormatTime(this.startDate)
        var end_time = FormatTime(this.endDate)
        if (start_time.split(" ")[0]==FormatTime(new Date()).split(" ")[0]) {
          start_time = FormatTime(new Date(new Date().toLocaleDateString()).getTime())
        }
        api.getLogInfo({params:{
            newPageNum: 1,
            userName: this.userName,
            operateType: this.operateType,
            operateLevel: this.operateLevel,
            starttime: start_time,
            stoptime: end_time
          }
        }).then(res => {
          console.log(res);
          this.logList = res.logs;
          this.logFields = logJs.getLogsTableFields();
          this.logTotalPage = Math.ceil(res.log_total_num / this.perPage);
          this.cage = 2
        })
        .catch((error) => {
          console.log(error);
        });
      }
    },
    mounted: function() {
      this.startDate = get_time(this.timePeriodValue)
    }
  }
</script>

<style scoped>
  .log-content {
    float: left;
    overflow: hidden;
    width: 100%
  }
  .log-table {
    margin-top: 10px;
  }
  .no-info-tip {
    text-align: center;
  }
  .log_tab {
    text-align: left;
  }
  .normal-btn {
    float: right;
  }
</style>
