<template>
  <div class="tradition-meeting-detail">
    <div class="tradition-meeting-back">
      <span class="back-btn" @click="$router.go(-1)"></span>
      <span class="base-info-title">服务器详情</span>
      <button class="normal-btn export" @click="onExport()" style="float:right" v-show="tabType=='unrepairwarning'">导出</button>
    </div>
    <ul>
      <li class="diagnosis-time-title">诊断时间</li>
      <li id="diagnosis_time">{{ inspect_time }}</li>
    </ul>
    <el-tabs v-model="tabType">
      <el-tab-pane label="硬件资源" name="hardwareresource">
        <div style="float:top;">
          <base-diagnose-item title="内存使用率">
            <res-diagnose-item :total="total" :userate="userate" title="内存"/>
          </base-diagnose-item>
        </div>
        <div>
          <base-diagnose-item title="磁盘状况">
            <div class="disk_profiles" v-for="(item, index) in diskData">
              <span style="padding-right: 550px;">{{ item.disk_name }}</span>
              <res-info-item :usednum="item.used" :totalnum="item.total" :usedpercent="Number(item.userate)" :totalday="item.age.toString()"/>
            </div>
          </base-diagnose-item>
        </div>
        <div>
          <base-diagnose-item title="CPU使用率">
            <div class="res-chart" id="cpuChart" :style="height_style"/>
          </base-diagnose-item>
        </div>
        <div>
          <base-diagnose-item title="网口吞吐量">
            <div class="res-chart_net" id="netChart" style="width: 820px; height: 410px"/>
          </base-diagnose-item>
        </div>
      </el-tab-pane>
      <el-tab-pane label="未修复告警" name="unrepairwarning">
        <div v-if="uServerWarninglList.length === 0" class="no-info-tip">
          没有告警数据！
        </div>
        <div v-if="uServerWarninglList.length > 0" style="padding-top: 10px;">
          <nms-pager-table :data="uServerWarninglList" :fields="uServerWarninglListFields" :total-page="uServerWarninglListTotalPage" :biao-zhi="cage" v-model="curPage"/>
        </div>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import api from "../../../axios";
import {ins_drawEcharts, ins_drawNetEcharts, getuServerWarninglListFields, setMyOption} from "../../../assets/js/diagnose";
import NmsPagerTable from "../../common/nms-pager-table";
import BaseDiagnoseItem from "../base-diagnose-item";
import ResDiagnoseItem from "../res-diagnose-item";
import ResInfoItem from "../res-info-item";
import {Upexcele}  from '../../../common/commonFunction'

export default {
  components: {
    NmsPagerTable,
    BaseDiagnoseItem,
    ResDiagnoseItem,
    ResInfoItem
  },
  name: "physicsdetail",
  data() {
    return {
      tabType: "hardwareresource",
      perPage: 10, // 表格每页显示数量
      curPage: 1,
      cage: 1,

      device_moid: "",
      taskid: "",
      // unrepairedwarning
      uServerWarninglList: [],
      uServerWarninglListFields: [],
      uServerWarninglListTotalPage: 1,

      deviceType: "server",

      diskData: [],
      total: 0,
      userate: 0,
      height_style: {
        height: ""
      },
      inspect_time: ""
    };
  },
  methods: {
    onExport: function() {
      api.downloadInspect({params:{taskid:this.taskid},responseType: 'blob'})
      .then((res) => {
        Upexcele(res, '巡检信息.xls')
      }).catch(error => {
        console.log(error)
      });
    },
    getResourceInfo: function () {
      this.diskData=[]
      api.getInspectServerResource(this.taskid, this.device_moid).then((res) => {
        console.log("服务器资源： "+JSON.stringify(res))
        if(res.success==1){
          // disk
          this.diskData = res.data.diskinfo
          // mem
          this.meminfo = res.data.meminfo
          this.total = Math.floor((res.data.meminfo.total / (1024 * 1024)).toFixed(2))
          this.userate = Number(res.data.meminfo.userate)
          // cpu
          var option_cpu = {
            xAxis: {
              name: '%',
              type: 'value',
              boundaryGap: false,
              min: 0,
              max: 100,
              interval: 10,
              axisLabel: {
                rotate: 90,
                textStyle: {
                  color: 'black',
                  fontSize: 13,
                  fontStyle: 'normal',
                  fontWeight: 500
                }
              },
              axisLine: {
                symbol: ['none', 'arrow'],
                symbolSize: [8, 12],
              },
              splitLine: {
                show: true,
                lineStyle: {
                  type: 'dotted'
                }
              },
            },
            yAxis: {
              minInterval: 1,
              type: 'category',
              data: [],
              axisTick: {
                show: true
              },
              axisLine: {
                symbol: ['none', 'arrow'],
                symbolSize: [8, 12],
                symbolOffset: [0, 10]
              },
            },
            grid: {
              top: 20,
              bottom: 15,
              containLabel: true
            },
            tooltip: {
              trigger: 'axis',
              axisPointer: {
                  type: 'shadow'
              }
            },
            series: [
              {
                  name: [],
                  type: 'bar',
                  data: [],
                  barWidth: 8,
                  itemStyle: {
                    normal: {
                      color: "#0f97e5",
                    }
                  }
              },
            ],
          }
          this.height_style.height == ""
          if (res.data.cpuinfo.length > 48) {
            let chartName = this.$echarts.init(document.getElementById("cpuChart"));
            this.autoHeight = 1600
            this.height_style.height == 1600 + "px"
            chartName.resize({height:this.autoHeight});
          } else if (res.data.cpuinfo.length > 32) {
            let chartName = this.$echarts.init(document.getElementById("cpuChart"));
            this.autoHeight = 950
            this.height_style.height == 950 + "px"
            chartName.resize({height:this.autoHeight});
          } else if (res.data.cpuinfo.length > 16) {
            let chartName = this.$echarts.init(document.getElementById("cpuChart"));
            this.autoHeight = 710
            this.height_style.height == 710 + "px"
            chartName.resize({height:this.autoHeight});
          } else {
            let chartName = this.$echarts.init(document.getElementById("cpuChart"));
            this.autoHeight = 410
            this.height_style.height == 410 + "px"
            chartName.resize({height:this.autoHeight});
          }
          var i = 0
          res.data.cpuinfo.forEach(item => {
            option_cpu.series[0].data.push(item)
            i = i + 1
            option_cpu.yAxis.data.push(i + "_cpu")
          })
          this.$nextTick(() => {
            setMyOption(this.$echarts, 'cpuChart', option_cpu)
          })
          // net
          var option_net = {
            calculable: true,
            legend: {
              data: ['出流量', '进流量']
            },
            xAxis: {
              name: 'Mbps',
              type: 'value',
              boundaryGap: false,
              axisLabel: {
                rotate: 90,
                textStyle: {
                  color: 'black',
                  fontSize: 13,
                  fontStyle: 'normal',
                  fontWeight: 500
                }
              },
              axisLine: {
                symbol: ['none', 'arrow'],
                symbolSize: [8, 12],
              },
              splitLine: {
                show: true,
                lineStyle: {
                  type: 'dotted'
                }
              },
            },
            yAxis: {
              minInterval: 1,
              type: 'category',
              data: [],
              axisTick: {
                show: true
              },
              axisLine: {
                symbol: ['none', 'arrow'],
                symbolSize: [8, 12],
              },
            },
            grid: {
              top: 20,
              bottom: 15,
              containLabel: true
            },
            tooltip: {
              trigger: 'axis',
              axisPointer: {
                  type: 'shadow'
              }
            },
            series: [
              {
                  name: '出流量',
                  type: 'bar',
                  data: [],
                  barWidth: 20,
                  itemStyle: {
                    normal: {
                      color: "#0f97e5",
                    }
                  }
              },
              {
                  name: '进流量',
                  type: 'bar',
                  data: [],
                  barWidth: 20,
                  itemStyle: {
                    normal: {
                      color: "#FFCC22",
                    }
                  }
              }
            ],
          }
          res.data.netcardinfo.forEach(item => {
            option_net.series[0].data.push((Number(item.sendkbps) / 1024).toFixed(3))
            option_net.series[1].data.push((Number(item.recvkbps) / 1024).toFixed(3))
            option_net.yAxis.data.push(item.name)
          })
          this.$nextTick(() => {
            setMyOption(this.$echarts, 'netChart', option_net)
          })
        }
      }).catch(error => {
        console.log(error)
      });
    }
  },
  activated: function() {
    this.tabType="hardwareresource"
    this.device_moid = this.$route.params.device_moid;
    this.taskid = this.$route.params.taskid;
    this.inspect_time = this.$route.params.inspect_time
    console.log("this.device_moid" + this.device_moid);
    console.log("this.taskid" + this.taskid);
    this.getResourceInfo()
  },
  watch: {
    tabType: function(newType, oldType) {
      if(this.tabType=="hardwareresource") {
        console.log("hardwareresource")
      }else if(this.tabType=="unrepairwarning") {
        console.log("hardwareresource")
        api.getInspectSWarning(this.taskid, this.device_moid, this.deviceType).then((res) => {
          console.log("server未修复告警反馈： "+JSON.stringify(res))
          if(res.success==1){
            this.uServerWarninglList = res.data.warning_list
            this.uServerWarninglListFields = getuServerWarninglListFields()
            this.uServerWarninglListTotalPage = Math.ceil(res.data.max_page)
          }
        }).catch(error => {
          console.log(error)
        });
      }
    },
    curPage: function (newPageNum, oldPageNum) {
      this.cage = 1
      api.getInspectSWarning(this.taskid, this.device_moid, this.deviceType, {params:{page:newPageNum}}).then((res) => {
        console.log("server未修复告警反馈： "+JSON.stringify(res))
        if(res.success==1){
          this.uServerWarninglList = res.data.warning_list
          this.uServerWarninglListFields = getuServerWarninglListFields()
          this.uServerWarninglListTotalPage = Math.ceil(res.data.max_page)
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
  width: 820px;
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
  text-align: left;
  padding-top: 13px;
}

</style>
