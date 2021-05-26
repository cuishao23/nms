<template>
  <div class="tradition-meeting-detail">
    <div class="tradition-meeting-back">
      <span class="back-btn" @click="meetingback()"></span>
      <span class="base-info-title">与会终端详情</span>
    </div>
    <div class="tradition-meeting-fields">
      <nms-key-value label="设备名称" :value="deviceName"/>
      <nms-key-value label="设备IP" :value="deviceIP"/>
      <nms-key-value label="E164号码" :value="deviceE164"/>
      <nms-key-value label="设备类型" :value="deviceType"/>
      <nms-key-value label="呼叫码率" :value="deviceBitrate"/>
      <nms-key-value label="加密类型" :value="deviceEncryption"/>
      <nms-key-value label="设备型号" :value="deviceTypecode"/>
      <nms-key-value label="软件版本" :value="deviceVersion"/>
      <nms-key-value label="码流篡改" :value="deviceTamper"/>
      <nms-key-value label="静音状态" :value="deviceMute"/>
      <nms-key-value label="哑音状态" :value="deviceDumbness"/>
      <nms-key-value label="NAT地址" :value="deviceNet"/>
      <nms-key-value label="运营商" :value="deviceOperate"/>
    </div>
    <el-tabs v-model="tabType">
      <el-tab-pane label="视频源" name="mainvideo">
        <span class="video">第一路主视频</span>
        <span class="videoif">有无视频源 <span class="sourse">{{ videoSource }}</span></span>
        <nms-pager-table v-if="reset" :data="PrivideoData" :fields="PrivideoFields" :pager='false'/>
        <span class="video">第一路辅视频</span>
        <nms-pager-table v-if="reset" :data="AssvideoData" :fields="AssvideoFields" :pager='false'/>
      </el-tab-pane>
      <el-tab-pane label="参会概况" name="meetingstate">
        <nms-pager-table v-if="reset" :data="MeetingState" :fields="MeetingStateFields" :pager='false'/>
      </el-tab-pane>
      <el-tab-pane label="入离会统计" name="joinmeeting">
        <nms-pager-table v-if="reset" :data="MeetingLeaveData" :fields="MeetingLeaveFields" :pager='false'/>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>
leave
<script>
  import api from '../../../axios'
  import NmsKeyValue from "../../common/nms-key-value";
  import {getmainVideoFields, getInOutMeetingFields, getMeetingStateFields} from "../../../assets/js/meetingtype";
  import NmsPagerTable from "../../common/nms-pager-table";
  import {FormatTime} from '../../../assets/js/common';

  export default {
    components: {
      NmsKeyValue,
      NmsPagerTable
      },
    name: "softharddetail",
    data() {
      return {
        reset: true,
        tabType: 'mainvideo',
        detail: null,
        deviceName: '',
        deviceIP: '',
        deviceE164: '',
        deviceType: '',
        deviceBitrate: '',
        deviceEncryption: '',
        deviceTypecode: '',
        deviceVersion: '',
        deviceTamper: '',
        deviceMute: '',
        deviceDumbness: '',
        deviceNet: '',
        deviceOperate: '',

        PrivideoData: [],
        PrivideoFields: [],
        AssvideoData: [],
        AssvideoFields: [],
        MeetingState: [],
        MeetingStateFields: [],
        MeetingLeaveData: [],
        MeetingLeaveFields: [],
        videoSource: '未知',
        terminalE164: '',
        terminalMoid: '',
        meetingE164: '',
        MultiType: '',
        perPage: 10, // 表格每页显示数量
        meetingTotalPage: 1, // 总页数
        curPage: 1,
        cage: 1,
        mainvideos: [], // 主视频列表
        mainVideoFields: [], // 主视频字段列表
        OperateList: ['未知', '中国电信', '中国联通', '中国移动', '有线通', '铁通', '海外', '本地', '其他'],
        inoutmeetings: [], // 入会离会详情列表
        inOutMeetingFields: []// 入会离会详情表格字段列表
      }
    },
    activated: function () {
      this.terminalE164 = this.$route.params.terminalE164
      this.meetingE164 = this.$route.params.meetingE164
      this.MultiType = this.$route.params.multiType
      console.log(this.terminalE164)
      this.tabType = 'mainvideo'
      this.deviceName = ''
      this.deviceIP = ''
      this.deviceE164 = ''
      this.deviceType = ''
      this.deviceBitrate = ''
      this.deviceEncryption = ''
      this.deviceTypecode = ''
      this.deviceVersion = ''
      this.deviceTamper = ''
      this.deviceMute = ''
      this.deviceDumbness = ''
      this.deviceNet = ''
      this.deviceOperate = ''
      this.AssvideoData = []
      this.PrivideoFields = getmainVideoFields()
      this.AssvideoFields = getmainVideoFields()
      api.getRealTimeTerminalDetail({params: {terminalE164: this.terminalE164}}).then(res => {
        console.log(res)
        if (res.success == 1) {
          this.detail = res.data
          this.deviceName = this.detail.name
          this.deviceIP = this.detail.mt_ip
          this.deviceE164 = this.detail.e164
          this.deviceType = this.detail.mt_type_category
          this.deviceBitrate = this.detail.conf_bitrate
          this.deviceEncryption = this.detail.encryption
          this.deviceTypecode = this.detail.mt_type
          this.deviceVersion = this.detail.version
          this.deviceTamper = this.detail.tamper
          this.deviceMute = this.detail.mute
          this.deviceDumbness = this.detail.dumbness
          this.deviceNet = this.detail.nat_ip
          this.terminalMoid = this.detail.moid
          if (this.detail.operator == '') {
            this.deviceOperate = '无'
          } else if (this.OperateList[parseInt(this.detail.operator)]) {
            this.deviceOperate = this.OperateList[parseInt(this.detail.operator)]
          } else {
            this.deviceOperate = this.OperateList[0]
          }
          console.log(this.deviceE164)
          api.getRealTimeTerminalVideoDetail({params: {terminalE164: this.deviceE164}}).then(res => {
            console.log(res)
            if (res.success == 1) {
              if (res.PrivideoData.length > 0) {
                let priData = []
                let priUpPower = ''
                let priDownPower = ''
                if ((res.PrivideoData[0]['send_video_res'] == '' && res.PrivideoData[0]['send_video_framerate'] == '' && res.PrivideoData[0]['send_video_bitrate'] == '') || (res.PrivideoData[0]['send_video_res'] == undefined && res.PrivideoData[0]['send_video_framerate'] == undefined && res.PrivideoData[0]['send_video_bitrate'] == undefined)) {
                  priUpPower = ''
                } else {
                  priUpPower = (res.PrivideoData[0]['send_video_res'] + '@' + res.PrivideoData[0]['send_video_framerate'] + ' ' + res.PrivideoData[0]['send_video_bitrate'])
                }
                if ((res.PrivideoData[0]['recv_video_res'] == '' && res.PrivideoData[0]['recv_video_framerate'] == '' && res.PrivideoData[0]['recv_video_bitrate'] == '') || (res.PrivideoData[0]['recv_video_res'] == undefined && res.PrivideoData[0]['recv_video_framerate'] == undefined && res.PrivideoData[0]['recv_video_bitrate'] == undefined)) {
                  priDownPower = ''
                } else {
                  priDownPower = (res.PrivideoData[0]['recv_video_res'] + '@' + res.PrivideoData[0]['recv_video_framerate'] + ' ' + res.PrivideoData[0]['recv_video_bitrate'])
                }
                priData.push({'updown': '上行',
                  'video_format': res.PrivideoData[0]['send_video_format'],
                  'video_power': priUpPower,
                  'video_lostrate': res.PrivideoData[0]['send_video_pkts_loserate'],
                  'audio_format': res.PrivideoData[0]['send_audio_format'],
                  'audio_lostrate': res.PrivideoData[0]['send_audio_pkts_loserate'],
                })
                priData.push({'updown': '下行',
                  'video_format': res.PrivideoData[0]['recv_video_format'],
                  'video_power': priDownPower,
                  'video_lostrate': res.PrivideoData[0]['recv_video_pkts_loserate'],
                  'audio_format': res.PrivideoData[0]['recv_audio_format'],
                  'audio_lostrate': res.PrivideoData[0]['recv_audio_pkts_loserate'],
                })
                this.PrivideoData = priData
                if (res.PrivideoData[0]['send_video_resource_exist'] == '1') {
                  this.videoSource = '有'
                } else if (res.PrivideoData[0]['send_video_resource_exist'] == '0') {
                  this.videoSource = '无'
                } else {
                  this.videoSource = '未知'
                }
              } else {
                this.PrivideoData = []
                this.videoSource = '无'
              }
              if (res.AssvideoData.length > 0) {
                let assData = []
                let assUpPower = ''
                let assDownPower = ''
                if ((res.AssvideoData[0]['send_video_res'] == '' && res.AssvideoData[0]['send_framerate'] == '' && res.AssvideoData[0]['send_bitrate'] == '') || (res.AssvideoData[0]['send_video_res'] == undefined && res.AssvideoData[0]['send_framerate'] == undefined && res.AssvideoData[0]['send_bitrate'] == undefined)) {
                  assUpPower = ''
                } else {
                  assUpPower = (res.AssvideoData[0]['send_video_res'] + '@' + res.AssvideoData[0]['send_framerate'] + ' ' + res.AssvideoData[0]['send_bitrate'])
                }
                if ((res.AssvideoData[0]['recv_video_res'] == '' && res.AssvideoData[0]['recv_framerate'] == '' && res.AssvideoData[0]['recv_bitrate'] == '') || (res.AssvideoData[0]['recv_video_res'] == undefined && res.AssvideoData[0]['recv_framerate'] == undefined && res.AssvideoData[0]['recv_bitrate'] == undefined)) {
                  assDownPower = ''
                } else {
                  assDownPower = (res.AssvideoData[0]['recv_video_res'] + '@' + res.AssvideoData[0]['recv_framerate'] + ' ' + res.AssvideoData[0]['recv_bitrate'])
                }
                assData.push({'updown': '上行',
                  'video_format': res.AssvideoData[0]['send_format'],
                  'video_power': assUpPower,
                  'video_lostrate': res.AssvideoData[0]['send_pkts_loserate']
                })
                assData.push({'updown': '下行',
                  'video_format': res.AssvideoData[0]['recv_format'],
                  'video_power': assDownPower,
                  'video_lostrate': res.AssvideoData[0]['recv_pkts_loserate'],
                })
                this.AssvideoData = assData
              } else {
                this.AssvideoData = []
              }
            }
            this.reset = false
            this.$nextTick(() => {
              this.reset = true
            })
          })
        }
      })
    },
    methods: {
      meetingback: function() {
        this.$router.push({
          name: "realtimemultipointmeeting",
          params: {meetingE164: this.meetingE164, multiType: this.MultiType}
        })
      }
    },
    watch: {
      tabType: function (newTab, oldTab) {
        if (newTab === 'mainvideo') {
           // 视频源
          this.AssvideoData = []
          this.PrivideoFields = getmainVideoFields()
          this.AssvideoFields = getmainVideoFields()
          console.log(this.deviceE164)
          api.getRealTimeTerminalVideoDetail({params: {terminalE164: this.deviceE164}}).then(res => {
            console.log(res)
            if (res.success == 1) {
              if (res.PrivideoData.length > 0) {
                let priData = []
                let priUpPower = ''
                let priDownPower = ''
                if ((res.PrivideoData[0]['send_video_res'] == '' && res.PrivideoData[0]['send_video_framerate'] == '' && res.PrivideoData[0]['send_video_bitrate'] == '') || (res.PrivideoData[0]['send_video_res'] == undefined && res.PrivideoData[0]['send_video_framerate'] == undefined && res.PrivideoData[0]['send_video_bitrate'] == undefined)) {
                  priUpPower = ''
                } else {
                  priUpPower = (res.PrivideoData[0]['send_video_res'] + '@' + res.PrivideoData[0]['send_video_framerate'] + ' ' + res.PrivideoData[0]['send_video_bitrate'])
                }
                if ((res.PrivideoData[0]['recv_video_res'] == '' && res.PrivideoData[0]['recv_video_framerate'] == '' && res.PrivideoData[0]['recv_video_bitrate'] == '') || (res.PrivideoData[0]['recv_video_res'] == undefined && res.PrivideoData[0]['recv_video_framerate'] == undefined && res.PrivideoData[0]['recv_video_bitrate'] == undefined)) {
                  priDownPower = ''
                } else {
                  priDownPower = (res.PrivideoData[0]['recv_video_res'] + '@' + res.PrivideoData[0]['recv_video_framerate'] + ' ' + res.PrivideoData[0]['recv_video_bitrate'])
                }
                priData.push({'updown': '上行',
                  'video_format': res.PrivideoData[0]['send_video_format'],
                  'video_power': priUpPower,
                  'video_lostrate': res.PrivideoData[0]['send_video_pkts_loserate'],
                  'audio_format': res.PrivideoData[0]['send_audio_format'],
                  'audio_lostrate': res.PrivideoData[0]['send_audio_pkts_loserate'],
                })
                priData.push({'updown': '下行',
                  'video_format': res.PrivideoData[0]['recv_video_format'],
                  'video_power': priDownPower,
                  'video_lostrate': res.PrivideoData[0]['recv_video_pkts_loserate'],
                  'audio_format': res.PrivideoData[0]['recv_audio_format'],
                  'audio_lostrate': res.PrivideoData[0]['recv_audio_pkts_loserate'],
                })
                this.PrivideoData = priData
                if (res.PrivideoData[0]['send_video_resource_exist'] == '1') {
                  this.videoSource = '有'
                } else if (res.PrivideoData[0]['send_video_resource_exist'] == '0') {
                  this.videoSource = '无'
                } else {
                  this.videoSource = '未知'
                }
              } else {
                this.PrivideoData = []
                this.videoSource = '无'
              }
              if (res.AssvideoData.length > 0) {
                let assData = []
                let assUpPower = ''
                let assDownPower = ''
                if ((res.AssvideoData[0]['send_video_res'] == '' && res.AssvideoData[0]['send_framerate'] == '' && res.AssvideoData[0]['send_bitrate'] == '') || (res.AssvideoData[0]['send_video_res'] == undefined && res.AssvideoData[0]['send_framerate'] == undefined && res.AssvideoData[0]['send_bitrate'] == undefined)) {
                  assUpPower = ''
                } else {
                  assUpPower = (res.AssvideoData[0]['send_video_res'] + '@' + res.AssvideoData[0]['send_framerate'] + ' ' + res.AssvideoData[0]['send_bitrate'])
                }
                if ((res.AssvideoData[0]['recv_video_res'] == '' && res.AssvideoData[0]['recv_framerate'] == '' && res.AssvideoData[0]['recv_bitrate'] == '') || (res.AssvideoData[0]['recv_video_res'] == undefined && res.AssvideoData[0]['recv_framerate'] == undefined && res.AssvideoData[0]['recv_bitrate'] == undefined)) {
                  assDownPower = ''
                } else {
                  assDownPower = (res.AssvideoData[0]['recv_video_res'] + '@' + res.AssvideoData[0]['recv_framerate'] + ' ' + res.AssvideoData[0]['recv_bitrate'])
                }
                assData.push({'updown': '上行',
                  'video_format': res.AssvideoData[0]['send_format'],
                  'video_power': assUpPower,
                  'video_lostrate': res.AssvideoData[0]['send_pkts_loserate'],
                })
                assData.push({'updown': '下行',
                  'video_format': res.AssvideoData[0]['recv_format'],
                  'video_power': assDownPower,
                  'video_lostrate': res.AssvideoData[0]['recv_pkts_loserate'],
                })
                this.AssvideoData = assData
              } else {
                this.AssvideoData = []
              }
            }
            this.reset = false
            this.$nextTick(() => {
              this.reset = true
            })
          })
        }// TerminalMeetingLeaveReason
        if (newTab === 'meetingstate') {
           // 参会概况
          this.MeetingStateFields = getMeetingStateFields()
          api.getRealTimeTerminalMeetingScore({params: {terminalMoid: this.terminalMoid, meetingE164: this.meetingE164}}).then(res => {
            if (res.success == 1) {
              if (res.data.length > 0) {
                for (var i = 0; i < res.data.length; i++) {
                  if (res.data[i]["time"] != '') {
                    res.data[i]["time"] = FormatTime(res.data[i]["time"])
                  }
                }
                this.MeetingState = res.data
                this.cage = 2
              } else {
                this.MeetingState = []
                this.reset = false
                this.$nextTick(() => {
                  this.reset = true
                })
              }
            }
          })
        }
        if (newTab === 'joinmeeting') {
           // 入离会详情
          this.MeetingLeaveFields = getInOutMeetingFields()
          api.getRealTimeTerminalLeaveReason({params: {terminalMoid: this.terminalMoid, meetingE164: this.meetingE164}}).then(res => {
            console.log(res)
            if (res.success == 1) {
              if (res.data.length > 0) {
                this.MeetingLeaveData = res.data
                this.cage = 2
              } else {
                this.MeetingLeaveData = []
                this.reset = false
                this.$nextTick(() => {
                  this.reset = true
                })
              }
            }
          })
        }
      }
    }
  }
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
  .video{
   float: left;
   font-size: 13px;
   padding-bottom:7px;
   padding-top:10px;
 }
  .videoif{
   float: left;
   font-size: 11px;
   color: #8b8b8b;
   padding-bottom:7px;
   padding-top:10px;
   padding-left:200px;
  }
  .sourse{
   padding-left:15px;
   color: #4e4e4e;
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

  .warning, .time-range {
    text-align: left;
  }

  .meetingContent {
    text-align: left;
  }

  .tmeeting-search {
    padding-bottom:7px;
  }
 .auxiliaryvideo{
   float: left;
 }
</style>
