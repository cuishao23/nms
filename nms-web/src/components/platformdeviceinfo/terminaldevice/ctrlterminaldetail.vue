<template>
  <div class="ctrl-terminal-detail">
    <div class="ctrl-terminal-back">
      <span class="back-btn" @click="$router.go(-1)"></span>
      <span class="base-info-title">{{ deviceName + '终端详情'}}</span>
      <input class="normal-btn meeting-detail" type="button" value="所属会议详情" v-if="(curTypeData != null) && (curTypeData.online == 'conference')"/>
    </div>
    <div>
      <div class="terminal-info">
        <nms-key-value label="设备名称" :value="deviceName"/>
        <nms-key-value label="E164号码" :value="deviceE164"/>
        <nms-key-value label="moid" :value="deviceMoid"/>
      </div>
    </div>
    <el-tabs v-model="tabType">
      <el-tab-pane label="运行状态" name="running">
        <div v-if="typeListData.length === 0 && listDiag" class="no-info-tip">此终端没有运行状态信息</div>
        <div v-if="typeListData.length > 0" class="no-info-tip">
          <nms-pager-table :data="typeListData" :fields="typeListFieds" :pager="false" :row-click="onTypeClick"/>
        </div>
        <div v-if="curTypeData != null" class="terminal-type-detail">
          <div class="terminal-info">
            <nms-key-value label="APS IP" :value="curTypeData.aps_ip"/>
            <nms-key-value label="DNS IP" :value="curTypeData.dns"/>
            <nms-key-value label="NAT IP" :value="curTypeData.nat_ip"/>
          </div>
          <div class="terminal-info">
            <nms-key-value label="接收带宽" :value="curTypeData.recv_bandwidth"/>
            <nms-key-value label="发送带宽" :value="curTypeData.send_bandwidth"/>
            <nms-key-value label="丢包重传" :value="curTypeData.pkt_loss_resend"/>
          </div>
          <div class="terminal-info">
            <nms-key-value label="音频优先" :value="curTypeData.audio_first"/>
            <nms-key-value label="FEC" :value="curTypeData.fec"/>
            <nms-key-value label="强解/载荷" :value="curTypeData.decode_payload_auto"/>
          </div>
          <div class="terminal-info">
            <nms-key-value label="视频输出制式" :value="curTypeData.video_format"/>
            <nms-key-value label="序列号" :value="curTypeData.SN"/>
            <nms-key-value label="注册地址" :value="curTypeData.reg_addr"/>
          </div>
          <div class="terminal-info">
            <nms-key-value label="国密状态" :value="curTypeData.state_secret"/>
          </div>
        </div>
      </el-tab-pane>
      <el-tab-pane label="告警信息" name="warningInfo">
        <div class="warning">
          <div>
            <el-checkbox v-model="t_critical">严重</el-checkbox>
            <el-checkbox v-model="t_important">重要</el-checkbox>
            <el-checkbox v-model="t_normal">一般</el-checkbox>
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
            <button class='search' @click="searchUrepairedWarningsT()"/>
          </div>
        </div>
        <div v-if="ctrlUnrepairedterminalWarningList.length === 0" class="no-info-tip">
          没有满足条件的统计数据！
        </div>
        <div v-if="ctrlUnrepairedterminalWarningList.length > 0">
          <nms-pager-table :data="ctrlUnrepairedterminalWarningList" :fields="ctrlUnrepairedterminalWarningListFields"  :total-page="terminalTotalPage" :biao-zhi="cage" v-model="curPage"/>
        </div>
      </el-tab-pane>
      <el-tab-pane label="外设信息" name="peripherals">
        <div v-if="showPer">
          <span class="title-tip" v-if="cameraList.length > 0">摄像机</span>
          <div class="title-info" v-if="cameraList.length > 0">
            <nms-pager-table :data="cameraList" :fields="cameraListFields" :pager="false" :index="false"/>
          </div>
          <span class="title-tip" v-if="microphoneList.length > 0">麦克风</span>
          <div class="title-info" v-if="microphoneList.length > 0">
            <nms-pager-table :data="microphoneList" :fields="microphoneListFields" :pager="false" :index="false"/>
          </div>
          <span class="title-tip" v-if="imixList.length > 0">IMIX</span>
          <div class="title-info" v-if="imixList.length > 0">
            <nms-pager-table :data="imixList" :fields="imixListFields" :pager="false" :index="false"/>
          </div>
        </div>
        <div v-else style="text-align: left; padding-top: 10px;">
          此终端下没有查到外设信息
        </div>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
  import NmsKeyValue from "../../common/nms-key-value";
  import api from '../../../axios'
  import {getCtrlDeviceTypeListFields,getCtrlUnrepairedterminalWarningListFields,getCameraListFields,getMicrophoneListFields,getImixListFields} from "../../../assets/js/platformdevice";
  import NmsPagerTable from "../../common/nms-pager-table";
  import NmsPagesTable from "../../common/nms-pages-table";
  import {getTimePeriod} from "../../../assets/js/common";
  import {FormatTime,get_time} from '../../../assets/js/common';

  export default {
    components: {
      NmsPagerTable,
      NmsKeyValue,
      NmsPagesTable},
    name: "ctrlterminaldetail",
    data() {
      return {
        reSet: true,
        detail: null,
        // 终端详情数据
        deviceName: '',
        deviceE164: '',
        deviceMoid: '',
        // 运行状态表格数据
        type: '',
        ip: '',
        version: '',
        idVersion: '',
        newVersion: '',
        online: '',
        // 每个终端类型对应的详细数据
        mem_usage: '',
        aps_domain: '',
        aps_ip: '',

        dns: '',
        nat_ip: '',
        pkt_loss_resend: '',

        audio_first: '',
        fec: '',
        decode_payload_auto: '',

        video_format: '',
        SN: '',
        reg_addr: '',

        state_secret: '',
        // tab切换
        tabType: 'running',
        typeListFieds: [],
        typeListData: [],

        curTypeData: null,
        // 告警信息
        t_critical: true,
        t_important: true,
        t_normal: true,

        startDate: new Date(),
        endDate: new Date(),
        timePeriod: [],
        timePeriodValue: 'lastweek',

        ctrlUnrepairedterminalWarningList: [],
        ctrlUnrepairedterminalWarningListFields: [],

        terminalTotalPage: 1, // 总页数
        perPage: 10, // 表格每页显示数量
        curPage: 1,
        cage: 1,
        // 外设信息
        cameraList: [],
        cameraListFields: [],

        microphoneList: [],
        microphoneListFields: [],

        imixList: [],
        imixListFields: [],

        listDiag: false,
        showPer: true

      }
    },
    methods: {
      onTypeClick: function (rowData) {
        this.curTypeData = rowData
      },
      searchUrepairedWarningsT: function() {
        var start_time = FormatTime(this.startDate)
        var end_time = FormatTime(this.endDate)
        if (this.timePeriodValue == "lasthour") {
          start_time = start_time
        } else {
          if(start_time.split(" ")[0]==FormatTime(new Date()).split(" ")[0]){
            start_time = FormatTime(new Date(new Date().toLocaleDateString()).getTime())
          }
        }
        api.getCtrlTerminalUnrepairedWarning({params:{
            newPageNum: 1,
            critical: this.t_critical,
            important: this.t_important,
            normal: this.t_normal,
            parentMoid: this.deviceMoid,
            starttime: start_time,
            stoptime: end_time
          }
        })
        .then((res) => {
          this.ctrlUnrepairedterminalWarningList = res.data
          this.ctrlUnrepairedterminalWarningListFields = getCtrlUnrepairedterminalWarningListFields()
          this.terminalTotalPage = Math.ceil(res.total_num / this.perPage)
        })
        .catch((error) => {
          console.log(error);
        });
        }
    },
    activated() {
      this.deviceName = this.$route.params.name
      this.deviceE164 = this.$route.params.e164
      this.deviceMoid = this.$route.params.moid
      // 初始化数据
      this.typeListFieds = getCtrlDeviceTypeListFields();
      this.timePeriod = getTimePeriod();
      this.cameraListFields = getCameraListFields()
      this.microphoneListFields = getMicrophoneListFields()
      this.imixListFields = getImixListFields()
      this.typeListData = []
      this.curTypeData = null
      api.getCtrledTerminalDetail({params:{deviceMoid: this.deviceMoid}}).then(res => {
        console.log('terminal detail ==========> ' + JSON.stringify(res))
        if (JSON.stringify(res.data) == "{}" || res.success == 0) {
          this.listDiag = true
        } else {
          this.listDiag = false
          this.typeListData = res.data
          this.tabType = 'running'
          this.curTypeData = this.typeListData[0]
        }
      });
      this.startDate=get_time(this.timePeriodValue)
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
      tabType: function (val) {
        if (val == "running") {
          console.log('running')
          api.getCtrledTerminalDetail({params:{deviceMoid: this.deviceMoid}}).then(res => {
            console.log('terminal detail ==========> ' + JSON.stringify(res))
            this.typeListData = res.data
            this.tabType = 'running'
            this.typeListFieds = getCtrlDeviceTypeListFields()

            if (this.typeListData != null && this.typeListData.length > 0) {
              this.curTypeData = this.typeListData[0]
            }
          })
        } else if (val == "warningInfo") {
          console.log('warningInfo')
          let start_time = FormatTime(this.startDate)
          let end_time = FormatTime(this.endDate)
          api.getCtrlTerminalUnrepairedWarning({params:{
              newPageNum: 1,
              critical: this.t_critical,
              important: this.t_important,
              normal: this.t_normal,
              parentMoid: this.deviceMoid,
              starttime: start_time,
              stoptime: end_time
            }
          })
          .then((res) => {
            this.ctrlUnrepairedterminalWarningList = res.data
            this.ctrlUnrepairedterminalWarningListFields = getCtrlUnrepairedterminalWarningListFields()
            this.terminalTotalPage = Math.ceil(res.total_num / this.perPage)
          })
          .catch((error) => {
            console.log(error);
          });
        }else if (val == "peripherals") {
          api.getCtrledTerminalPeripherals({params:{deviceMoid: this.deviceMoid}}).then(res => {
            if (res.data.cameras.length == 0 && res.data.microphones.length == 0 && res.data.imixes == 0) {
              this.showPer = false
            } else {
              this.showPer = true
              // camera
              this.cameraList = res.data.cameras
              // microphone
              this.microphoneList = res.data.microphones
              // imix
              this.imixList = res.data.imixes
            }
          })
          .catch((error) => {
            console.log(error);
          });
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
        api.getCtrlTerminalUnrepairedWarning({params:{
            newPageNum: 1,
            critical: this.t_critical,
            important: this.t_important,
            normal: this.t_normal,
            parentMoid: this.deviceMoid,
            starttime: start_time,
            stoptime: end_time
          }
        })
        .then((res) => {
          this.ctrlUnrepairedterminalWarningList = res.data
          this.ctrlUnrepairedterminalWarningListFields = getCtrlUnrepairedterminalWarningListFields()
          this.terminalTotalPage = Math.ceil(res.total_num / this.perPage)
        })
        .catch((error) => {
          console.log(error);
        });
      },

    },
  }
</script>

<style scoped>
  .ctrl-terminal-detail {
    display: block;
  }

  .ctrl-terminal-back {
    padding-bottom: 45px;
  }
  .meeting-detail {
    float: right;
  }

  .terminal-info {
    display: flex;
    align-items: center;
    margin-bottom: 25px;
  }

  .terminal-type-detail {
    margin-top: 40px;
  }
  .no-info-tip {
    text-align: left;
    padding-top: 15px;
  }
  .chart-tab {
    padding-top: 40px
  }
  .res-chart {
    height: 450px;
    width: 900px;
  }
  .warning {
    clear: left;
    text-align: left;
  }
  .title-tip {
    float: left;
    padding-bottom: 7px;
  }
  .title-info {
    padding-bottom: 26px
  }
</style>
