<template>
  <div class="tradition-meeting-detail">
    <div class="tradition-meeting-back">
      <span class="back-btn" @click="meetingback()"></span>
      <span class="base-info-title">{{ deviceMeetingName }}</span>
    </div>
    <div class="tradition-meeting-fields">
      <nms-key-value label="媒体格式" :value="deviceFormat"/>
      <nms-key-value label="媒体能力" :value="deviceFdis"/>
      <nms-key-value label="加密类型" :value="deviceEncryptionType"/>
      <nms-key-value label="来宾会议室" :value="deviceGuestRoom"/>
      <nms-key-value label="呼叫方式" :value="deviceCallTypec"/>
      <nms-key-value label="会议体验" :value="deviceMeetingExperience"/>
    </div>
    <div class='detail-search'>
      <el-select v-model="MeetingDetail" placeholder="会议类型" @change="DetailClick">
        <el-option
          v-for="(item,index) in MeetingDetails"
          :key="index"
          :label="item.name"
          :value="item.type">
        </el-option>
      </el-select>
      <el-input v-show = 'searchShow' v-model="device_name" placeholder="请输入名称" class="meetingtext"></el-input>
      <button v-show = 'searchShow' class='search-met' @click="searchDomain()"></button>
    </div>
    <div v-if="MeetingDetailInfos.length === 0" class = "meetingDetailInfo">此会议里没有
      <span v-if="MeetingDetail === 'SoftHardTerminal'">软硬终端！</span>
      <span v-if="MeetingDetail === 'PhoneTerminal'">电话终端！</span>
      <span v-if="MeetingDetail === 'MeetingPeripherals'">会议外设！</span>
      <span v-if="MeetingDetail === 'CascadeMeeting'">级联会议！</span>
      <span v-if="MeetingDetail === 'IPBusinessFriend'">IP和友商！</span>
      <span v-if="MeetingDetail === 'LiveStreaming'">直播！</span>
      <span v-if="MeetingDetail === 'DataCollaboration'">数据协作！</span>
    </div>
    <div v-if="MeetingDetailInfos.length>0">
      <nms-pager-table :data="MeetingDetailInfos" :fields="MeetingDetailInfoFields"  :total-page="meetingTotalPage" :biao-zhi="cage" v-model="curPage"/>
      <nms-dialog title="数据协作详情" ref="CollaborationsDlg" :width="'700px'">
        <div slot="content">
          <el-tabs v-model="datatabType">
            <el-tab-pane label="协作模式" name="mode">
              <span v-if="CollaborationDetailData.length === 0" class = "livevalue">此数据会议尚无协作详情</span>
              <nms-pager-table class="overFlow" v-if="CollaborationDetailData.length > 0" :data="CollaborationDetailData" :fields="CollaborationDetailField" :pager='false'/>
            </el-tab-pane>
            <el-tab-pane label="协作方" name="collaboration">
              <span v-if="CollaborationDetailData.length === 0" class = "livevalue">此数据会议尚无协作方</span>
              <nms-pager-table class="overFlow" v-if="CollaborationDetailData.length > 0" :data="CollaborationDetailData" :fields="CollaborationDetailField" :pager='false'/>
            </el-tab-pane>
            <el-tab-pane label="观看方" name="watch">
              <span v-if="CollaborationDetailData.length === 0" class = "livevalue">此数据会议尚无观看方</span>
              <nms-pager-table class="overFlow" v-if="CollaborationDetailData.length > 0" :data="CollaborationDetailData" :fields="CollaborationDetailField" :pager='false'/>
            </el-tab-pane>
          </el-tabs>
        </div>
      </nms-dialog>
      <nms-dialog title="直播详情" ref="LiveStreamingsDlg" :width="'700px'">
        <div slot="content">
          <span v-if="LivestreamingData.length === 0" class = "livevalue">此直播尚无观看者信息</span>
          <div v-if="LivestreamingData.length > 0">
            <span class="livevalue">最大峰值 <span class="sourse">{{ LiveMaxWatch }}</span></span>
            <span class="livetime">最大峰值时间 <span class="sourse">{{ LiveMaxTime }}</span></span>
            <nms-pager-table class="overFlow" :data="LivestreamingData" :fields="LivestreamingField " :pager='false'/>
          </div>
        </div>
      </nms-dialog>
    </div>
  </div>
</template>

<script>
  import api from '../../../axios'
  import NmsKeyValue from "../../common/nms-key-value";
  import {getPhoneTerminalFields, gethardAndSoftTerminalFields, getcascadeMeetingFields,
  getLiveStreamingFields, getonclickLiveStreamingFields, getCollaborationFields, getCollaborativeModeFields,
  getCollaboratorFields, getIPBusinessFriendFields} from "../../../assets/js/meetingtype";
  import NmsPagerTable from "../../common/nms-pager-table";
  import NmsDialog from "../../common/nms-dialog";

  export default {
    components: {
      NmsKeyValue,
      NmsPagerTable,
      NmsDialog
    },
    name: "cascademeeting",
    data() {
      return {
        datatabType: 'mode',
        searchShow: true,
        device_name: '',
        MeetingRoom: '',
        MeetingType: '',
        MeetingDetailInfos: [],
        MeetingDetailInfoFields: [],
        MeetingDetail: 'SoftHardTerminal',
        MeetingDetails: [{name: '软硬终端', type: 'SoftHardTerminal'},
                        {name: '电话终端', type: 'PhoneTerminal'},
                        {name: '级联会议', type: 'CascadeMeeting'},
                        {name: 'IP和友商', type: 'IPBusinessFriend'},
                        {name: '直播', type: 'LiveStreaming'},
                        {name: '数据协作', type: 'DataCollaboration'},
        ],
        detail: null,
        deviceMeetingName: '',
        deviceName: '',
        deviceMoid: '',
        // 多点会议详细数据
        deviceFormat: '',
        deviceFdis: '',
        deviceEncryptionType: '',
        deviceGuestRoom: '',
        deviceCallTypec: '',
        deviceMeetingExperience: '',
        dcs_moid: '',
        OperateList: ['未知', '中国电信', '中国联通', '中国移动', '有线通', '铁通', '海外', '本地', '其他'],
        // 会议各方面数据
        PrivideoData: [],
        PrivideoFields: [],
        AssvideoData: [],
        AssvideoFields: [],
        videoSource: '',
        CollaborationData: [],
        CollaborationFields: [],
        CollaborationDetailData: [],
        CollaborationDetailField: [],
        CollaborationStartTime: '',
        p2pCollaborationsData: [],
        p2pCollaborationsField: [],
        LiveMaxWatch: '',
        LiveMaxTime: '',
        LivestreamingData: [],
        LivestreamingField: [],
        cage: 1,
        perPage: 10, // 表格每页显示数量
        meetingTotalPage: 1, // 总页数
        curPage: 1,
      }
    },
    // 初始相关数据获取显示
    activated: function () {
      this.MeetingRoom = this.$route.params.meetingRoom
      console.log(this.MeetingRoom)
      // 多点会议详情界面
      this.AssvideoData = []
      this.deviceMeetingName = ''
      this.deviceFormat = ''
      this.deviceFdis = ''
      this.deviceEncryptionType = ''
      this.deviceGuestRoom = ''
      this.deviceCallTypec = ''
      this.deviceMeetingExperience = ''
      api.getHistoryMultiMeetingDetail({params: {meetingMoid: this.MeetingRoom}}).then(res => {
        console.log(res)
        if (res.success == 1) {
          this.detail = res.data
          this.deviceMeetingName = this.detail.conf_name
          this.deviceFormat = this.detail.format
          this.deviceFdis = (this.detail.resolution + '@' + this.detail.frame + 'fps' + ' ' + this.detail.bitrate)
          if (this.detail.encryption === 'aes') {
            this.deviceEncryptionType = 'AES加密'
          } else if (this.detail.encryption === 'des') {
            this.deviceEncryptionType = 'DES加密'
          } else if (this.detail.encryption === 'sm1') {
            this.deviceEncryptionType = 'SM1加密'
          } else if (this.detail.encryption === 'sm4') {
            this.deviceEncryptionType = 'SM4加密'
          } else if (this.detail.encryption === 'none') {
            this.deviceEncryptionType = '无'
          }
          this.deviceGuestRoom = this.detail.guest_mode
          if (this.detail.call_type === 'timing') {
            this.deviceCallTypec = '定时呼叫'
          } else if (this.detail.call_type === 'manual') {
            this.deviceCallTypec = '手动呼叫'
          } else {
            this.deviceCallTypec = '无'
          }
          this.deviceMeetingExperience = this.detail.experience
        }
      })
      this.device_name = ''
      this.MeetingDetail = 'SoftHardTerminal'
      this.searchShow = true
      this.MeetingDetailInfos = []
      this.MeetingDetailInfoFields = []
      api.getHistorySoftHardTerminal({params: {meetingMoid: this.MeetingRoom, page: 1, terminalName: this.device_name}}).then(res => {
        console.log(res)
        if (res.success == 1) {
          this.MeetingDetailInfos = res.data
          this.meetingTotalPage = Math.ceil(res.total_num / this.perPage)
          this.MeetingDetailInfoFields = gethardAndSoftTerminalFields(this.gotoSoftHardDetail)
          this.cage = 2
        }
      })
    },
    methods: {
      meetingback: function() {
        this.$router.push({
          name: "historymeetinghome",
        })
      },
      // 多点会议详情栏
      DetailClick: function() {
        switch (this.MeetingDetail) {
          // 软硬终端
          case 'SoftHardTerminal':
            this.device_name = ''
            this.searchShow = true
            this.MeetingDetailInfoFields = gethardAndSoftTerminalFields(this.gotoSoftHardDetail)
            api.getHistorySoftHardTerminal({params: {meetingMoid: this.MeetingRoom, page: 1, terminalName: this.device_name}}).then(res => {
              console.log(res)
              if (res.success == 1) {
                this.MeetingDetailInfos = res.data
                this.meetingTotalPage = Math.ceil(res.total_num / this.perPage)
              } else {
                this.MeetingDetailInfos = []
                this.meetingTotalPage = 1
              }
              this.cage = 2
            })
            break;
          // 电话终端
          case 'PhoneTerminal':
            this.device_name = ''
            this.searchShow = true
            this.MeetingDetailInfoFields = getPhoneTerminalFields()
            api.getHistoryPhoneTerminal({params: {meetingMoid: this.MeetingRoom, page: 1, terminalName: this.device_name}}).then(res => {
              if (res.success == 1) {
                this.MeetingDetailInfos = res.data
                this.meetingTotalPage = Math.ceil(res.total_num / this.perPage)
              } else {
                this.MeetingDetailInfos = []
                this.meetingTotalPage = 1
              }
              this.cage = 2
            })
            break;
          // 级联会议
          case 'CascadeMeeting':
            this.device_name = ''
            this.searchShow = true
            this.MeetingDetailInfoFields = getcascadeMeetingFields(this.gotoCascadeMeetingDetail)
            api.getHistoryCascadeMeeting({params: {meetingMoid: this.MeetingRoom, page: 1, meetingName: this.device_name}}).then(res => {
              console.log(res)
              if (res.success == 1) {
                this.MeetingDetailInfos = res.data
                this.meetingTotalPage = Math.ceil(res.total_num / this.perPage)
              } else {
                this.MeetingDetailInfos = []
                this.meetingTotalPage = 1
              }
              this.cage = 2
            })
            break;
          // IP和友商
          case 'IPBusinessFriend':
            this.device_name = ''
            this.searchShow = true
            this.MeetingDetailInfoFields = getIPBusinessFriendFields()
            api.getHistoryIPTerminal({params: {meetingMoid: this.MeetingRoom, page: 1, terminalName: this.device_name}}).then(res => {
              if (res.success == 1) {
                this.MeetingDetailInfos = res.data
                this.meetingTotalPage = Math.ceil(res.total_num / this.perPage)
              } else {
                this.MeetingDetailInfos = []
                this.meetingTotalPage = 1
              }
              this.cage = 2
            })
            break;
          // 直播
          case 'LiveStreaming':
            this.device_name = ''
            this.searchShow = false
            this.MeetingDetailInfoFields = getLiveStreamingFields(this.gotoLiveDetail)
            api.getHistoryLiveInfo({params: {meetingMoid: this.MeetingRoom, page: 1}}).then(res => {
              if (res.success == 1) {
                this.MeetingDetailInfos = res.data
                this.meetingTotalPage = Math.ceil(res.total_num / this.perPage)
              } else {
                this.MeetingDetailInfos = []
                this.meetingTotalPage = 1
              }
              this.cage = 2
            })
            break;
          // 数据协作
          case 'DataCollaboration':
            this.device_name = ''
            this.searchShow = false
            this.MeetingDetailInfoFields = getCollaborationFields(this.gotoCollaboration)
            api.getHistoryMeetingDcsInfo({params: {meetingMoid: this.MeetingRoom, page: 1}}).then(res => {
              if (res.success == 1) {
                this.MeetingDetailInfos = res.data
                this.meetingTotalPage = Math.ceil(res.total_num / this.perPage)
              } else {
                this.MeetingDetailInfos = []
                this.meetingTotalPage = 1
              }
              this.cage = 2
            })
            break;
          default:
            break;
        }
      },
      // 搜索
      searchDomain: function () {
        switch (this.MeetingDetail) {
          // 软硬终端
          case 'SoftHardTerminal':
            this.MeetingDetailInfoFields = gethardAndSoftTerminalFields(this.gotoSoftHardDetail)
            api.getHistorySoftHardTerminal({params: {meetingMoid: this.MeetingRoom, page: 1, terminalName: this.device_name}}).then(res => {
              console.log(res)
              if (res.success == 1) {
                this.MeetingDetailInfos = res.data
                this.meetingTotalPage = Math.ceil(res.total_num / this.perPage)
              } else {
                this.MeetingDetailInfos = []
                this.meetingTotalPage = 1
              }
              this.cage = 2
            })
            break;
          // 电话终端
          case 'PhoneTerminal':
            this.MeetingDetailInfoFields = getPhoneTerminalFields()
            api.getHistoryPhoneTerminal({params: {meetingMoid: this.MeetingRoom, page: 1, terminalName: this.device_name}}).then(res => {
              if (res.success == 1) {
                this.MeetingDetailInfos = res.data
                this.meetingTotalPage = Math.ceil(res.total_num / this.perPage)
              } else {
                this.MeetingDetailInfos = []
                this.meetingTotalPage = 1
              }
              this.cage = 2
            })
            break;
          // 级联会议
          case 'CascadeMeeting':
            this.MeetingDetailInfoFields = getcascadeMeetingFields(this.gotoCascadeMeetingDetail)
            api.getHistoryCascadeMeeting({params: {meetingMoid: this.MeetingRoom, page: 1, meetingName: this.device_name}}).then(res => {
              console.log(res)
              if (res.success == 1) {
                this.MeetingDetailInfos = res.data
                this.meetingTotalPage = Math.ceil(res.total_num / this.perPage)
              } else {
                this.MeetingDetailInfos = []
                this.meetingTotalPage = 1
              }
              this.cage = 2
            })
            break;
          // IP和友商
          case 'IPBusinessFriend':
            this.MeetingDetailInfoFields = getIPBusinessFriendFields()
            api.getHistoryIPTerminal({params: {meetingMoid: this.MeetingRoom, page: 1, terminalName: this.device_name}}).then(res => {
              if (res.success == 1) {
                this.MeetingDetailInfos = res.data
                this.meetingTotalPage = Math.ceil(res.total_num / this.perPage)
              } else {
                this.MeetingDetailInfos = []
                this.meetingTotalPage = 1
              }
              this.cage = 2
            })
            break;
          default:
            break;
        }
      },
      // 软硬终端详情
      gotoSoftHardDetail: function(data) {
        console.log(data)
        this.$router.push({name: 'msoftharddetail',
                          params: {meetingRoom: this.MeetingRoom, deviceMoid: data.moid}})
      },
      // 直播详情
      gotoLiveDetail: function(data) {
        console.log(data)
        this.LivestreamingField = getonclickLiveStreamingFields()
        this.LiveMaxWatch = data.max_user_count
        this.LiveMaxTime = data.max_user_time
        this.LivestreamingData = []
        api.getHistoryLiveUserInfo({params: {liveMoid: data.live_moid}}).then(res => {
          console.log(res)
          if (res.success == 1) {
            this.LivestreamingData = res.data
          }
        })
        this.$refs.LiveStreamingsDlg.open()
      },
      // 级联会议详情
      gotoCascadeMeetingDetail: function(data) {
        console.log(data)
        this.$router.push({name: 'multipointmeetingdetail',
                           params: {meetingRoom: data.meetingMoid}})

        // console.log(JSON.stringify(rowData));
      },
      // 协作详情
      gotoCollaboration: function(data) {
        console.log('gotoCollaboration')
        this.CollaborationDetailData = []
        console.log(data.dcs_moid)
        this.dcs_moid = data.dcs_moid
        this.datatabType = 'mode'
        api.getHistoryDcsModeChangeInfo({params: {dcsMoid: data.dcs_moid}}).then(res => {
          this.CollaborationDetailField = getCollaborativeModeFields()
          if (res.success == 1) {
            this.CollaborationDetailData = res.data
            this.meetingTotalPage = Math.ceil(this.CollaborationDetailData.length / this.perPage)
          }
        })
        this.$refs.CollaborationsDlg.open()
      },
    },
    watch: {
      // 翻页
      curPage: function (newpage, oldpage) {
        this.cage = 1
        if (newpage > 0 && newpage <= this.meetingTotalPage) {
          switch (this.MeetingDetail) {
            // 软硬终端
            case 'SoftHardTerminal':
              this.MeetingDetailInfoFields = gethardAndSoftTerminalFields(this.gotoSoftHardDetail)
              api.getHistorySoftHardTerminal({params: {meetingMoid: this.MeetingRoom, page: newpage, terminalName: this.device_name}}).then(res => {
                console.log(res)
                if (res.success == 1) {
                  this.MeetingDetailInfos = res.data
                  this.meetingTotalPage = Math.ceil(res.total_num / this.perPage)
                } else {
                  this.MeetingDetailInfos = []
                  this.meetingTotalPage = 1
                }
              })
              break;
            // 电话终端
            case 'PhoneTerminal':
              this.MeetingDetailInfoFields = getPhoneTerminalFields()
              api.getHistoryPhoneTerminal({params: {meetingMoid: this.MeetingRoom, page: newpage, terminalName: this.device_name}}).then(res => {
                if (res.success == 1) {
                  this.MeetingDetailInfos = res.data
                  this.meetingTotalPage = Math.ceil(res.total_num / this.perPage)
                } else {
                  this.MeetingDetailInfos = []
                  this.meetingTotalPage = 1
                }
              })
              break;
            // 级联会议
            case 'CascadeMeeting':
              this.MeetingDetailInfoFields = getcascadeMeetingFields(this.gotoCascadeMeetingDetail)
              api.getHistoryCascadeMeeting({params: {meetingMoid: this.MeetingRoom, page: newpage, meetingName: this.device_name}}).then(res => {
                console.log(res)
                if (res.success == 1) {
                  this.MeetingDetailInfos = res.data
                  this.meetingTotalPage = Math.ceil(res.totala_num / this.perPage)
                } else {
                  this.MeetingDetailInfos = []
                  this.meetingTotalPage = 1
                }
              })
              break;
            // IP和友商
            case 'IPBusinessFriend':
              this.MeetingDetailInfoFields = getIPBusinessFriendFields()
              api.getHistoryIPTerminal({params: {meetingMoid: this.MeetingRoom, page: newpage, terminalName: this.device_name}}).then(res => {
                if (res.success == 1) {
                  this.MeetingDetailInfos = res.data
                  this.meetingTotalPage = Math.ceil(res.total_num / this.perPage)
                } else {
                  this.MeetingDetailInfos = []
                  this.meetingTotalPage = 1
                }
              })
              break;
            // 直播
            case 'LiveStreaming':
              this.MeetingDetailInfoFields = getLiveStreamingFields(this.gotoLiveDetail)
              api.getHistoryLiveInfo({params: {meetingMoid: this.MeetingRoom, page: newpage}}).then(res => {
                if (res.success == 1) {
                  this.MeetingDetailInfos = res.data
                  this.meetingTotalPage = Math.ceil(res.total_num / this.perPage)
                } else {
                  this.MeetingDetailInfos = []
                  this.meetingTotalPage = 1
                }
              })
              break;
            // 数据协作
            case 'DataCollaboration':
              this.MeetingDetailInfoFields = getCollaborationFields(this.gotoCollaboration)
              api.getHistoryMeetingDcsInfo({params: {meetingMoid: this.MeetingRoom, page: newpage}}).then(res => {
                if (res.success == 1) {
                  this.MeetingDetailInfos = res.data
                  this.meetingTotalPage = Math.ceil(res.total_num / this.perPage)
                } else {
                  this.MeetingDetailInfos = []
                  this.meetingTotalPage = 1
                }
              })
              break;
            default:
              break;
          }
        }
      },
      // 监听多点会议协作详情
      datatabType: function (newTab, oldTab) {
        if (newTab === '' || this.MeetingRoom === '') {
          return;
        }
        if (newTab === 'mode') {
          // 协作模式
          console.log(newTab)
          this.CollaborationDetailData = []
          api.getHistoryDcsModeChangeInfo({params: {dcsMoid: this.dcs_moid}}).then(res => {
            console.log(res)
            this.CollaborationDetailField = getCollaborativeModeFields()
            if (res.success == 1) {
              this.CollaborationDetailData = res.data
              this.meetingTotalPage = Math.ceil(this.CollaborationDetailData.length / this.perPage)
              this.cage = 2
            }
          })
        }
        if (newTab === 'collaboration') {
          // 协作方
          console.log(newTab)
          this.CollaborationDetailData = []
          api.getHistoryDcsMeetingTerminal({params: {dcsMoid: this.dcs_moid}}).then(res => {
            this.CollaborationDetailField = getCollaboratorFields()
            if (res.success == 1) {
              this.CollaborationDetailData = res.Collaborator
              this.meetingTotalPage = Math.ceil(this.CollaborationDetailData.length / this.perPage)
              this.cage = 2
            }
          })
        }
        if (newTab === 'watch') {
          // 观看方
          console.log(newTab)
          this.CollaborationDetailData = []
          api.getHistoryDcsMeetingTerminal({params: {dcsMoid: this.dcs_moid}}).then(res => {
            this.CollaborationDetailField = getCollaboratorFields()
            if (res.success == 1) {
              this.CollaborationDetailData = res.Viewer
              this.meetingTotalPage = Math.ceil(this.CollaborationDetailData.length / this.perPage)
              this.cage = 2
            }
          })
        }
      },
    },
  }
</script>

<style scoped>
  .overFlow{
    height: 240px;
    overflow:auto;
  }
  .meetingDetailInfo{
    float: left;
  }
  .tradition-meeting-detail {
    display: block;
  }
  .tradition-meeting-back {
    padding-bottom: 45px;
  }
  .normal-btn {
    float: right;
  }
  .meetingtext{
    margin-left: 6px;
  }
  .detail-search {
    margin-top: 15px;
    padding-right: 2px;
    flex-wrap: wrap;
    display: flex;
    text-align: left;
    margin-bottom: 13px;
  }

  .tradition-meeting-fields {
    margin-top: 24px;
    clear: both;
    display: flex;
    flex-wrap: wrap;
    border-bottom: 1px dotted #c0c0c0;
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
  .livestreaming{
    text-align: left;
  }

  .tmeeting-search {
    padding-bottom:7px;
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
 .video{
   float: left;
   font-size: 13px;
   padding-bottom:7px;
   padding-top:20px;
 }
 .videoif{
   float: left;
   font-size: 11px;
   color: #8b8b8b;
   padding-bottom:7px;
   padding-top:20px;
   padding-left:200px;
 }
  .livevalue{
   float: left;
   color: #8b8b8b;
   font-size: 13px;
   padding-bottom:10px;
   padding-top:10px;
 }
  .livetime{
   float: left;
   font-size: 13px;
   color: #8b8b8b;
   padding-bottom:10px;
   padding-top:10px;
   padding-left:100px;
 }
 .sourse{
   padding-left:15px;
   color: #4e4e4e;
 }
 .peripheral{
   float: left;
 }
 .cascading{
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

  .setValue input{
    width: 59px;
  }
  .in_line{
    display: inline;
    float: left;
  }
</style>
