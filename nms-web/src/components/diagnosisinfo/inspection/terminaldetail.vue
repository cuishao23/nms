<template>
  <div class="tradition-meeting-detail">
    <div class="tradition-meeting-back">
      <span class="back-btn" @click="$router.go(-1)"></span>
      <span class="base-info-title">终端详情</span>
      <button class="normal-btn export" @click="onExport()" style="float:right">导出</button>
    </div>
    <span class="warning_tip">未修复告警</span>
    <div v-if="uTerminalWarninglList.length === 0" class="no-info-tip">
      没有告警数据！
    </div>
    <div v-if="uTerminalWarninglList.length > 0" style="padding-top: 10px;">
      <nms-pager-table :data="uTerminalWarninglList" :fields="uTerminalWarninglListFields" :total-page="uTerminalWarninglListTotalPage" :biao-zhi="cage" v-model="curPage"/>
    </div>
  </div>
</template>

<script>
import api from "../../../axios";
import {getuTermminalWarninglListFields} from "../../../assets/js/diagnose";
import NmsPagerTable from "../../common/nms-pager-table";
import {Upexcele}  from '../../../common/commonFunction'

export default {
  components: {
    NmsPagerTable,
  },
  name: "terminaldetail",
  data() {
    return {
      perPage: 10, // 表格每页显示数量
      curPage: 1,
      cage: 1,

      device_moid: "",
      taskid: "",
      // unrepairedwarning
      uTerminalWarninglList: [],
      uTerminalWarninglListFields: [],
      uTerminalWarninglListTotalPage: 1,

      deviceType: "terminal",
      tatalNum: "",

    };
  },
  methods: {
    getInfo: function() {
      api.getInspectTWarning(this.taskid, this.device_moid, this.deviceType).then((res) => {
          console.log("terminal未修复告警反馈： "+JSON.stringify(res))
          if(res.success==1){
            this.uTerminalWarninglList = res.data.warning_list
            this.uTerminalWarninglListFields = getuTermminalWarninglListFields()
            this.uTerminalWarninglListTotalPage = Math.ceil(res.data.max_page)
          }
        }).catch(error => {
          console.log(error)
        });
    },
    onExport: function() {
      api.downloadInspect({params:{taskid:this.taskid},responseType: 'blob'})
      .then((res) => {
        Upexcele(res, '巡检信息.xls')
      }).catch(error => {
        console.log(error)
      });
    }
  },
  activated: function() {
    this.device_moid = this.$route.params.device_moid;
    this.taskid = this.$route.params.taskid;
    console.log("this.device_moid" + this.device_moid);
    console.log("this.taskid" + this.taskid);
    this.getInfo()
  },
  watch: {
    curPage: function (newPageNum, oldPageNum) {
      this.cage = 1
      api.getInspectTWarning(this.taskid, this.device_moid, this.deviceType, {params:{page:newPageNum}}).then((res) => {
        console.log("terminal未修复告警反馈： "+JSON.stringify(res))
        if(res.success==1){
          this.uTerminalWarninglList = res.data.warning_list
          this.uTerminalWarninglListFields = getuTermminalWarninglListFields()
          this.uTerminalWarninglListTotalPage = Math.ceil(res.data.max_page)
        }
      }).catch(error => {
        console.log(error)
      });
    }
  }
};
</script>

<style scoped>
.tradition-meeting-detail {
  display: block;
}

.tradition-meeting-back {
  padding-bottom: 45px;
}

.normal-btn {
  float: right;
}

.tradition-meeting-fields {
  clear: both;
  display: flex;
  flex-wrap: wrap;
}

.tradition-meeting-fields > div {
  width: 25%;
  padding-bottom: 25px;
}

.warning,
.time-range {
  text-align: left;
}

.meetingContent {
  text-align: left;
}
.livestreaming {
  text-align: left;
}

.tmeeting-search {
  padding-bottom: 7px;
}

/*搜索图标*/
.search-met {
  width: 30px;
  height: 30px;
  background: url("../../../assets/image/search1.png") 0 0;
  cursor: pointer;
  margin-left: 21px;
  vertical-align: bottom;
  position: relative;
  /*bottom: -2px;*/
}
.phone {
  float: left;
}
.peripheral {
  float: left;
}
.cascading {
  float: left;
}
.lineDiv {
  margin-top: 28px;
}

.setName {
  font-size: 12px;
  color: #4e4e4e;
  display: inline-block;
  text-align: left;
  width: 110px;
}

.setValue {
  font-size: 12px;
  color: #4e4e4e;
  display: inline-block;
  text-align: left;
  width: 110px;
}

.setValue input {
  width: 59px;
}
ul {
  text-align: left;
  padding-bottom: 10px;
}
li {
  font-size: 12px;
  display: inline-block;
  vertical-align: middle;
  margin-right: 19px;
}
.in_line {
  display: inline;
  float: left;
}
.setName {
  font-size: 12px;
  color: #4e4e4e;
  display: inline-block;
  text-align: left;
  width: 110px;
}
.td-title {
  width: 80px;
  color: #8b8b8b;
  padding-bottom: 16px;
  vertical-align: top;
  font-size: 12px;
  text-align: left;
}
.td-content {
  width: 166px;
  color: #4e4e4e;
  padding-bottom: 16px;
  vertical-align: top;
  font-size: 12px;
  text-align: left;
}
#conf_type {
  display: inline-block;
  font-size: 12px;
  width: 74px;
}
#conf_detail {
  color: #3e9bd0;
  border-bottom: 1px solid #3e9bd0;
}

button.timeInputdisable {
  color: #fff;
  cursor: default;
  background-color: #e5e5e5;
  border-width: 0px;
  padding: 6px 22px 5px 22px;
}

button.timeInputdisable:hover {
  background-color: #e5e5e5;
  background-image: none;
}
.res-chart {
  height: 950px;
  margin-left: 100px;
}
.res-chart_net {
  height: 690px;
  margin-left: 100px;
}
.packet-loss-rate-wrap {
    position: relative;
    font-size: 12px;
}
.packet-loss-rate-wrap li {
    display: inline-block;
}
.packet-loss-rate-wrap>li:nth-child(2) {
    position: absolute;
    left: calc(80px + 166px);
}
#capture_package_content {
    margin-top: 30px;
}

#capture_package_content ul{
    margin-bottom: 25px;
    font-size: 0;
}

#capture_package_content li{
    /* display: inline-block; */
    vertical-align: bottom;
    font-size: 12px;
}

#capture_package_content li:first-child{
    width: 80px;
    color: #8b8b8b;
}
#start_capture,
#stop_capture {
    margin-left: 40px;
}
.diagnosis-time-title {
    color: #8b8b8b;
}
.no-info-tip {
  padding-top: 13px;
}
.warning_tip {
  float: left;
  padding-bottom: 10px;
}
</style>
