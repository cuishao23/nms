<template>
  <div class="physical-detail">
    <div class="physical-back">
      <!-- <span class="back-btn" @click="$router.go(-1)"></span> -->
      <span class="back-btn" @click="back_page()"></span>
      <span class="base-info-title">{{ deviceName }}服务器</span>
      <button class="normal-btn" type="button" @click="shutdown()" :class="{disable: online!=='online'} " :disabled="online!=='online'">关机</button>
      <button class="normal-btn" type="button" @click="restart()" :class="{disable: online!=='online'} " :disabled="online!=='online'" >重启</button>
    </div>
    <div class="physical-fields">
      <nms-key-value label="设备名称" :value="deviceName"/>
      <nms-key-value label="设备类型" :value="deviceType"/>
      <nms-key-value label="所属平台域" :value="platformDomainName"/>
      <nms-key-value label="所属机房" :value="machineRoomName"/>
      <nms-key-value label="设备IP" :value="deviceIp"/>
      <nms-key-value label="归属机框" :value="belong_frame"/>
      <nms-key-value label="槽位" :value="belong_slot"/>
      <nms-key-value label="moid" :value="deviceMoid"/>
    </div>
    <el-tabs v-model="tabType" style="cursor:pointer" v-if="deviceIp!==''">
      <el-tab-pane label="CPU使用率" name="cpuusage">
        <div class="time-range">
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
          <button class='search' @click="searchCpu()"></button>
        </div>
        <div class="chart-tab_net">
          <div class="main-chart">
            <div class="cpu_img"><img :src=cpu_src_img></img></div>
          </div>
        </div>
      </el-tab-pane>
      <el-tab-pane label="内存使用率" name="memusage">
        <div class="time-range">
          <el-select v-model="timePeriodValue" class="time" filterable>
            <el-option v-for="item in timePeriod"
                       :key="item.value"
                       :label="item.label"
                       :value="item.value"/>
          </el-select>
          <div style="display: inline-block; width: 16px"></div>
          <DateBox v-if="reSet" inputId="d3" v-model="startDate" style="width: 150px" format="yyyy-MM-dd" :disabled="timePeriodValue !== 'selfdefine'"></DateBox>
          <div style="display: inline-block; width: 19px">→</div>
          <DateBox v-if="reSet" inputId="d4" v-model="endDate" style="width: 150px;" format="yyyy-MM-dd" :disabled="timePeriodValue !== 'selfdefine'"></DateBox>
          <button class='search' @click="searchMem()"></button>
        </div>
        <div class="chart-tab_net">
          <div class="main-chart">
            <div class="cpu_img"><img :src=mem_src_img></img></div>
          </div>
        </div>
      </el-tab-pane>
      <el-tab-pane label="网络吞吐量" name="netinout">
        <div class="time-range">
          <el-select v-model="timePeriodValue" class="time" filterable>
            <el-option v-for="item in timePeriod"
                       :key="item.value"
                       :label="item.label"
                       :value="item.value"/>
          </el-select>
          <div style="display: inline-block; width: 16px"></div>
          <DateBox v-if="reSet" inputId="d5" v-model="startDate" style="width: 150px" format="yyyy-MM-dd" :disabled="timePeriodValue !== 'selfdefine'"></DateBox>
          <div style="display: inline-block; width: 19px">→</div>
          <DateBox v-if="reSet" inputId="d6" v-model="endDate" style="width: 150px;" format="yyyy-MM-dd" :disabled="timePeriodValue !== 'selfdefine'"></DateBox>
          <button class='search' @click="searchNetCart()"></button>
        </div>
        <div class="chart-tab_net">
          <div class="main-chart">
            <div class="cpu_img"><img :src=netcard_src_one_img></img></div>
          </div>
        </div>
      </el-tab-pane>
      <el-tab-pane label="磁盘概况" name="disk">
        <div class="disk_profiles" v-for="(item, index) in diskData">
          <span style="padding-right: 410px;">{{ item.disk_name }}</span>
          <res-info-item :usednum="item.disk_used" :totalnum="item.disk_total" :usedpercent="item.disk_userate" :totalday="item.disk_age"/>
        </div>
      </el-tab-pane>
    </el-tabs>
    <nms-big-dialog title="提示" ref="rebootDialog" :width="'400px'" :height="'260px'" :close-btn="true" @confirm="onRestart()" @cancel="passwordError=false;superPwd=''">
      <div slot="content" class="cfg-reg-addr">
        <el-input v-model="superPwd" placeholder="请输入密码" class="sup_text" type="password"></el-input>
        <div class="tip_text">
          <span v-show="!passwordError">注：你将要重启设备{{deviceIp}}。重启过程中请勿切断电源！</span>
          <span v-show="passwordError" style="color: red;">密码错误，请输入超级管理员密码</span>
        </div>
      </div>
    </nms-big-dialog>
    <nms-big-dialog title="提示" ref="shutDownDialog" :width="'400px'" :height="'260px'" :close-btn="true" @confirm="onShutdown()" @cancel="passwordError=false;superPwd=''">
      <div slot="content" class="cfg-reg-addr">
        <el-input v-model="superPwd" placeholder="请输入密码" class="sup_text" type="password"></el-input>
        <div class="tip_text">
          <span v-show="!passwordError">注：你将要关闭设备{{deviceIp}}。关机过程中请勿切断电源！</span>
          <span v-show="passwordError" style="color: red;">密码错误，请输入超级管理员密码</span>
        </div>
      </div>
    </nms-big-dialog>
  </div>
</template>

<script>
  import api from '../../../axios'
  import NmsKeyValue from "../../common/nms-key-value";
  import {getTimePeriod} from "../../../assets/js/common";
  import {FormatTime,get_time} from '../../../assets/js/common';
  import ResInfoItem from "./res-info-item";
  import NmsDialog from "../../common/nms-dialog";
  import NmsBigDialog from "../../common/nms-big-dialog";
  import qs from 'qs';

  export default {
    components: {NmsKeyValue,ResInfoItem,NmsBigDialog},
    name: "physicaldetail",
    data() {
      return {
        result_null: '---',
        reSet: true,
        tabType: 'cpuusage',
        detail: null,
        deviceMoid: '',
        deviceName: '',
        deviceType: '',
        belong_frame: '',
        belong_slot: '',
        platformDomainName: '',
        machineRoomName: '',
        deviceIp: '',
        machineRoomMoid: '',
        frameMoid: '',

        critical: true,
        important: true,
        normal: true,

        timePeriod: [],
        timePeriodValue: 'lastweek',
        timeRange: [],

        startDate: new Date(),
        endDate: new Date(),

        superPwd: '',
        passwordError: false,
        cpu_src_img: "",
        mem_src_img: "",
        netcard_src_one_img: "",
        netcard_src_two_img: "",
        online: '',
        diskData: [],
        frameFlag: false,
        backpage: ''

      }
    },
    activated: function () {
      this.deviceMoid = this.$route.params.moid
      this.backpage = this.$route.params.page
      this.getPhysicalDetail(this.deviceMoid)
      this.timePeriod = getTimePeriod()
      this.tabType = 'cpuusage'
    },
    mounted:function() {
      this.startDate=get_time(this.timePeriodValue)
      let start_time = FormatTime(this.startDate)
      let end_time = FormatTime(this.endDate)
    },
    methods: {
      back_page: function() {
        console.log(this.backpage)
        if (this.backpage == 'home') {
          this.$router.push({ name: 'platformdeviceinfohome', params: {tabTypeProp:'nodeservice'}})
        } else if (this.backpage == 'device' && this.frameMoid !== '') {
          this.$router.push({name: "devicedetail", params: {moid: this.machineRoomMoid, frame: this.frameMoid, name: this.belong_frame}});
        } if (this.backpage == 'device' && this.frameMoid == '') {
          this.$router.push({name: "devicedetail", params: {moid: this.machineRoomMoid, frame: this.deviceMoid, name: this.deviceName}});
        } if (this.backpage == 'subwarning') {
          this.$router.push({name: 'subwarninginfo', params: {tabTypeProp:'server'}});
        } if (this.backpage == 'unrepairedwarning') {
          this.$router.push({name: 'unrepairedwarninginfo', params: {tabTypeProp:'server'}})
        }

      },
      getPhysicalDetail:function(val) {
        api.getPhysicalDetailInfo({params:{
            deviceMoid: val
          }
        })
        .then((res) => {
          this.online = res.data.online
          this.deviceName = res.data.name
          this.deviceType = res.data.type
          this.platformDomainName = res.data.domain_name
          this.machineRoomName = res.data.machine_room_name
          this.deviceIp = res.data.ip
          this.belong_frame = res.data.belong_frame
          this.belong_slot = res.data.belong_slot
          this.machineRoomMoid = res.data.machine_room_moid
          this.frameMoid = res.data.belong_moid
          if (this.deviceIp!=='') {
            this.timePeriod = getTimePeriod()
            this.searchCpu()
          }
          if (!this.belong_frame) {
            this.belong_frame = this.result_null
          }
          if (this.belong_slot=='') {
            this.belong_slot = this.result_null
          }
        })
        .catch((error) => {
          console.log(error);
        })
      },
      // CPU
      // CPU_RESOURCE = "resource.{machine_room_moid}.{p_server_moid}.cpu.{cpu}"
      searchCpu: function() {
        var start_time = FormatTime(this.startDate)
        var end_time = FormatTime(this.endDate)
        if (this.timePeriodValue == "lasthour") {
          start_time = start_time
        } else {
          if(start_time.split(" ")[0]==FormatTime(new Date()).split(" ")[0]){
            start_time = FormatTime(new Date(new Date().toLocaleDateString()).getTime())
          }
        }
        api.getCpuGraphiteInfo({params:{
            startTime: start_time,
            stopTime: end_time,
            machineRoomMoid: this.machineRoomMoid,
            deviceMoid: this.deviceMoid
          }
        })
        .then((res) => {
          if(res.success==1){
            this.cpu_src_img = "data:image/gif;base64,"+res.data
          }
        })
        .catch((error) => {
          console.log(error);
        })
      },
      // MEM
      // MEM_RESOURCE = "resource.{machine_room_moid}.{p_server_moid}.mem"
      searchMem: function() {
        var start_time = FormatTime(this.startDate)
        var end_time = FormatTime(this.endDate)
        if (this.timePeriodValue == "lasthour") {
          start_time = start_time
        } else {
          if(start_time.split(" ")[0]==FormatTime(new Date()).split(" ")[0]){
            start_time = FormatTime(new Date(new Date().toLocaleDateString()).getTime())
          }
        }
        api.getMemGraphiteInfo({params:{
            startTime: start_time,
            stopTime: end_time,
            machineRoomMoid: this.machineRoomMoid,
            deviceMoid: this.deviceMoid
          }
        })
        .then((res) => {
          console.log("内存使用率 "+JSON.stringify(res))
          if(res.success==1){
            this.mem_src_img = "data:image/gif;base64,"+res.data
            console.log("mem_src_img="+this.mem_src_img)
          }
        })
        .catch((error) => {
          console.log(error);
        })
      },
      // NETCARD
      // NETCARD_UP_RESOURCE = "resource.{machine_room_moid}.{p_server_moid}.netcard.{netcard_name}.up"
      // NETCARD_DOWN_RESOURCE = "resource.{machine_room_moid}.{p_server_moid}.netcard.{netcard_name}.down"
      searchNetCart: function() {
        var start_time = FormatTime(this.startDate)
        var end_time = FormatTime(this.endDate)
        if (this.timePeriodValue == "lasthour") {
          start_time = start_time
        } else {
          if(start_time.split(" ")[0]==FormatTime(new Date()).split(" ")[0]){
            start_time = FormatTime(new Date(new Date().toLocaleDateString()).getTime())
          }
        }
        api.getGraphiteChartData({params:{
            startTime: start_time,
            stopTime: end_time,
            machineRoomMoid: this.machineRoomMoid,
            deviceMoid: this.deviceMoid
          }
        })
        .then((res) => {
          if(res.success==1){
            this.netcard_src_one_img = "data:image/gif;base64,"+res.data
            console.log("netcard_src_one_img="+this.netcard_src_one_img)
          }
        })
        .catch((error) => {
          console.log(error);
        })
      },
      // DISK
      searchDisk: function() {
        this.diskData=[]
        api.getDiskInfo({params:{
            deviceMoid: this.deviceMoid,
          }
        })
        .then((res) => {
          console.log("磁盘信息"+JSON.stringify(res))
          if(res.success==1){
            for(let i=0; i<res.data.disknum; i++){
              let dic = {}
              dic["disk_name"] = res.data['disk'+(i+1)+"_name"]
              dic["disk_used"] = res.data['disk'+(i+1)+"_used"]
              dic["disk_total"] = res.data['disk'+(i+1)+"_total"]
              dic["disk_userate"] = Number(res.data['disk'+(i+1)+"_userate"])
              dic["disk_age"] = res.data['disk'+(i+1)+"_age"]
              this.diskData.push(dic)
            }
          }
        })
        .catch((error) => {
          console.log(error);
        })
      },
      restart: function () {
        this.$refs.rebootDialog.open()
      },
      onRestart() {
        this.axios.post("/nms/device/rebootserver", qs.stringify(
          {
            superPwd: this.superPwd,
            deviceMoid: this.deviceMoid,
            deviceType: this.deviceType
          }),
          {headers:{'Content-Type':'application/x-www-form-urlencoded'}})
          //成功返回
          .then(response => {
              if (response.data.success==1) {
                this.passwordError=false
                this.errorDialog.open('设备重启中，预计5分钟...重启过程中，请勿切断电源！')
              }else if (response.data.success==0) {
                if (response.data.error_code===20400){
                  this.passwordError=true
                  this.$refs.rebootDialog.open()
                }else{
                  this.superPwd = ''
                  this.errorDialog.open('重启失败')
                }
              }
          })
        //失败返回
        .catch(error => {
            this.errorDialog.open('重启失败')
        })
      },
      shutdown: function () {
        this.$refs.shutDownDialog.open()
      },
      onShutdown() {
        this.axios.post("/nms/device/shutdownserver", qs.stringify(
          {
            superPwd: this.superPwd,
            deviceMoid: this.deviceMoid,
            deviceType: this.deviceType
          }),
          {headers:{'Content-Type':'application/x-www-form-urlencoded'}})
          //成功返回
          .then(response => {
              console.log("关机结果反馈："+JSON.stringify(response));
              if (response.data.success==1) {
                this.passwordError=false
                this.errorDialog.open('设备关机中，预计5分钟...关机过程中，请勿切断电源！')
              }else if (response.data.success==0) {
                if (response.data.error_code===20400){
                  this.passwordError=true
                  this.$refs.shutDownDialog.open()
                }else{
                  this.superPwd = ''
                  this.errorDialog.open('关机失败')
                }
              }
          })
        //失败返回
        .catch(error => {
             this.errorDialog.open('关机失败')
        })
      },
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
      // 下拉框服务域选
      timePeriodValue: function (newTime, oldTime) {
        if(get_time(newTime)!=""){
          this.startDate=get_time(newTime)
        }
      },
      tabType: function(val) {
        console.log("val=="+val)
        if(val=="cpuusage"){
          this.searchCpu()
        }else if(val=="memusage") {
          this.searchMem()
        }else if(val=="netinout") {
          this.searchNetCart()
        }else if(val=="disk") {
          this.searchDisk()
        }
      }
    }
  }
</script>

<style scoped>
  .physical-detail {
    display: block;
  }

  .physical-back {
    padding-bottom: 45px;
  }

  .normal-btn {
    float: right;
    margin-left: 6px;
  }

  .physical-fields {
    clear: both;
    display: flex;
    flex-wrap: wrap;;
  }

  .physical-fields > div {
    width: 25%;
    padding-bottom: 25px;
  }

  .warning, .time-range {
    text-align: left;
    padding-top: 10px;
  }
  .time {
    margin-left: 0px;
  }
  .res-chart {
    height: 450px;
    width: 900px;
  }
  .chart-tab {
    padding-top: 40px
  }
  .res-chart_net {
    height: 300px;
    width: 600px;
    float: left;
    left: -60px;
    padding-top: 15px;
  }
  .chart-tab_net {
    text-align: left;
    padding-top: 35px
  }
  .main-chart {
    height: 400px;
    width: 700px;
    float: left;
  }
  .disk_profiles {
    width: 460px;
    padding-top: 40px;
  }
  .cfg-reg-addr {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    height: 100%;
    position: relative;
    text-align: left;
  }
  .cfg-reg-addr input {
    margin-left: 30px;
  }
  .sup_text {
    width: 300px;
    padding-bottom: 50px;
    position: absolute;
  }
  .tip_text {
    position: absolute;
    width: 300px;
    padding-top: 20px;
    pointer-events: none
  }
  div.dlg-content[data-v-a8a6c15c] {
    display: block;
    margin-bottom: 0px;
 }
 .cpu_img {
   text-align: left;
 }
</style>
