<template>
  <div>
    <div class="history-meeting">
      <div>
        <el-select v-model="tTerminalDomainMoid" placeholder="默认服务域" filterable>
          <el-option
            v-for="(item,index) in tTerminalDomainMoids"
            :key="index"
            :label="item.name"
            :value="item.moid">
          </el-option>
        </el-select>
        <el-select v-model="tUserMoid" placeholder="全部用户域" filterable>
          <el-option
            v-for="(item,index) in tUserMoids"
            :key="index"
            :label="item.name"
            :value="item.moid">
          </el-option>
        </el-select>
        <el-select v-model="MeetingType" placeholder="会议类型" filterable>
          <el-option
            v-for="(item,index) in MeetingTypes"
            :key="index"
            :label="item.name"
            :value="item.type">
          </el-option>
        </el-select>
        <el-input v-model="device_name" placeholder="请输入会议名称" class="filter-text"></el-input>
        <button class='search' @click="searchDomain()"></button>
      </div>
    </div>
    <div v-if="traditionalMeetings.length === 0" id="meetingDetailInfo" class="no-info-tip">
      <span class="PromptImg"></span>
      <span>没有搜索到满足条件的实时会议信息！</span>
    </div>
    <div v-if="traditionalMeetings.length>0">
      <nms-pager-table :data="traditionalMeetings" :fields="traditionalMeetingFields" :total-page="meetingTotalPage" :biao-zhi="cage" v-model="curPage"/>
    </div>
  </div>
</template>

<script>
  import api from "../../../axios";
  import {gettraditionalMeetingDeviceListFields, getp2pMeetingDeviceListFields, } from "../../../assets/js/meetingtype";
  import NmsPagerTable from "../../common/nms-pager-table";

  export default {
    components: {NmsPagerTable},
    name: "realtimemeetinghome",
    inject: ["reload"],
    data() {
      return {
        multiNum: 0,
        p2pNum: 0,
        tTerminalDomainMoids: [],
        tTerminalDomainMoid: '',
        tUserMoids: [],
        tUserMoid: '',
        MeetingType: '',
        sendType: 'multi',
        MeetingTypes: [
          {name: '多点会议', type: 'multi'},
          {name: '点对点会议', type: 'p2p'},
        ],
        device_name: '',
        curMoid: '',
        domainTreeData: [],
        tabType: "", // tab标签类型
        warningUesrDomains: [],
        perPage: 10, // 表格每页显示数量
        meetingTotalPage: 1, // 总页数
        curPage: 1,
        cage: 1,
        traditionalMeetings: [], // 传统会议列表
        traditionalMeetingFields: [], // 传统会议表格字段列表
      }
    },

    mounted: function () {
      // 获取下拉框域
      api.getUserDomainTree().then((res) => {
        console.log(res)
        this.tTerminalDomainMoids = []
        this.tUserMoids = []
        let userCount = 0
        let serverCount = 0
        this.warningUesrDomains = res.data
        this.warningUesrDomains.forEach(item => {
          if (item.type === "service" || item.type === "kernel") {
            this.tTerminalDomainMoids.unshift(item)
            serverCount++
          } else if (item.type === "user") {
            this.tUserMoids.unshift(item)
            userCount++
          }
        })
        if (serverCount == 0) {
          this.tTerminalDomainMoids.unshift({
            "moid": "",
            "parent_moid": "",
            "name": "无下级域",
            "type": "server"
          })
          this.tTerminalDomainMoid = ''
        } else {
          this.tTerminalDomainMoids.unshift({
            "moid": "all",
            "parent_moid": "",
            "name": "所有服务域",
            "type": "server"
          })
          this.tTerminalDomainMoid = 'all'
        }
        if (userCount == 0) {
          this.tUserMoids.unshift({
            "moid": "",
            "parent_moid": "",
            "name": "无下级域",
            "type": "user"
          })
          this.tUserMoid = ''
        } else {
          this.tUserMoids.unshift({
            "moid": "all",
            "parent_moid": "",
            "name": "所有用户域",
            "type": "user"
          })
          this.tUserMoid = 'all'
        }
        console.log(this.tUserMoid)
        // 获取多点会议列表
        api.getRealTimeMultiMeeting({params: {parentMoid: 'all', page: 1, meetingName: this.device_name}}).then(res => {
          console.log(res)
          if (res.success == 1) {
            this.traditionalMeetings = res.data
            this.traditionalMeetingFields = gettraditionalMeetingDeviceListFields(this.gotoTraditionMeetingDetail)
            this.multiNum = res.total_num
            this.meetingTotalPage = Math.ceil(res.total_num / this.perPage)
            this.cage = 2
            this.MeetingType = 'multi'
          }
        })
      })
    },
    watch: {
      // 翻页跳转
      curPage: function(newPageNum, oldPageNum) {
        if (newPageNum <= this.meetingTotalPage && newPageNum > 0) {
          if (this.sendType == 'multi') {
            api.getRealTimeMultiMeeting({params: {parentMoid: this.tUserMoid, page: newPageNum, meetingName: this.device_name}}).then(res => {
              console.log(res)
              this.cage = 1
              if (res.success == 1) {
                this.traditionalMeetings = res.data
                this.traditionalMeetingFields = gettraditionalMeetingDeviceListFields(this.gotoTraditionMeetingDetail)
                this.meetingTotalPage = Math.ceil(res.total_num / this.perPage)
              }
            })
          } else if (this.sendType == 'p2p') {
            api.getRealTimeP2pMeeting({params: {parentMoid: this.tUserMoid, page: newPageNum, meetingName: this.device_name}}).then(res => {
              console.log(res)
              this.cage = 1
              if (res.success == 1) {
                this.traditionalMeetings = res.data
                this.meetingTotalPage = Math.ceil(res.total_num / this.perPage)
                this.traditionalMeetingFields = getp2pMeetingDeviceListFields(this.gotoTraditionMeetingDetail)
              }
            })
          }
        }
      },
      // 下拉框服务域选择
      tTerminalDomainMoid: function(newDomain, oldDomain) {
        let userCount = 0
        if (newDomain == 'all') {
          this.tUserMoids = []
          this.warningUesrDomains.forEach(item => {
            if (item.type === "user") {
              this.tUserMoids.unshift(item)
              userCount++
            }
          })
          if (userCount == 0) {
            this.tUserMoids.unshift({
              "moid": "",
              "parent_moid": "",
              "name": "无下级域",
              "type": "user"
            })
            this.tUserMoid = ''
          } else {
            this.tUserMoids.unshift({
              "moid": "all",
              "parent_moid": "",
              "name": "所有用户域",
              "type": "user"
            })
            this.tUserMoid = 'all'
          }
        } else {
          let kernel = 0
          this.warningUesrDomains.forEach(domain => {
            if (domain.moid === newDomain && domain.type === 'kernel') {
              kernel = 1
            }
          })
          if (kernel == 0) {
            this.tUserMoids = []
            this.warningUesrDomains.forEach(user => {
              if (user.parent_moid === newDomain && user.type === 'user') {
                this.tUserMoids.push(user)
                userCount++
              }
            })
            if (userCount == 0) {
              this.tUserMoids.unshift({
                "moid": "",
                "parent_moid": "",
                "name": "无下级域",
                "type": "user"
              })
              this.tUserMoid = ''
            } else {
              this.tUserMoids.unshift({
                "moid": "all",
                "parent_moid": "",
                "name": "所有用户域",
                "type": "user"
              })
              this.tUserMoid = 'all'
            }
          } else {
            this.tUserMoids = []
            this.warningUesrDomains.forEach(item => {
              if (item.type === "user") {
                this.tUserMoids.unshift(item)
                userCount++
              }
            })
            if (userCount == 0) {
              this.tUserMoids.unshift({
                "moid": "",
                "parent_moid": "",
                "name": "无下级域",
                "type": "user"
              })
              this.tUserMoid = ''
            } else {
              this.tUserMoids.unshift({
                "moid": "all",
                "parent_moid": "",
                "name": "所有用户域",
                "type": "user"
              })
              this.tUserMoid = 'all'
            }
          }
        }
      }
    },
    methods: {
      // 搜索列表
      searchDomain: function () {
        this.sendType = this.MeetingType
        console.log(this.tUserMoid)
        if (this.MeetingType == 'multi') {
          if (this.tUserMoid == '') {
            this.traditionalMeetings = []
            this.multiNum = 0
            this.meetingTotalPage = Math.ceil(this.multiNum / this.perPage)
          } else {
            api.getRealTimeMultiMeeting({params: {parentMoid: this.tUserMoid, page: 1, meetingName: this.device_name}}).then(res => {
              console.log(res)
              if (res.success == 1) {
                let Data = res.data
                this.traditionalMeetings = Data
                this.multiNum = res.total_num
                this.meetingTotalPage = Math.ceil(this.multiNum / this.perPage)
              }
            })
          }
          this.traditionalMeetingFields = gettraditionalMeetingDeviceListFields(this.gotoTraditionMeetingDetail)
          this.cage = 2
          this.MeetingType = 'multi'
        } else if (this.MeetingType == 'p2p') {
          this.traditionalMeetingFields = getp2pMeetingDeviceListFields(this.gotoTraditionMeetingDetail)
          if (this.tUserMoid == '') {
            this.traditionalMeetings = []
            this.p2pNum = 0
            this.MeetingType = 'p2p'
            this.meetingTotalPage = Math.ceil(this.p2pNum / this.perPage)
            this.cage = 2
          } else {
            api.getRealTimeP2pMeeting({params: {parentMoid: this.tUserMoid, page: 1, meetingName: this.device_name}}).then(res => {
              console.log(res)
              if (res.success == 1) {
                this.p2pNum = res.total_num

                this.MeetingType = 'p2p'
                this.traditionalMeetings = res.data
                this.meetingTotalPage = Math.ceil(this.p2pNum / this.perPage)
                this.cage = 2
              }
            })
          }
        }
      },
      // 详情页面跳转
      gotoTraditionMeetingDetail: function(data) {
        if (this.sendType == 'multi') {
          let confType = data.conf_type
          if (data.conf_type == '0') {
            confType = 't_meeting'
          } else if (data.conf_type == '1') {
            confType = 'p_meeting'
          } else if (data.conf_type == '2') {
            confType = 'sfu_meeting'
          } else if (data.conf_type == '3') {
            confType = 'mix_meeting'
          } else {
            console.log(data.conf_type)
          }
          this.$router.push({
            name: "realtimemultipointmeeting",
            params: {meetingE164: data.conf_e164, multiType: confType}
          })
          this.MeetingType = 'multi'
        } else if (this.sendType == 'p2p') {
          this.$router.push({
            name: "realtimep2pmeeting",
            params: {meetingE164: data.caller_e164, calleeE164: data.callee_e164}
          })
          this.MeetingType = 'p2p'
        }
      },
    }
  }
</script>

<style scoped>
  .history-meeting {
    display: flex;
    text-align: left;
    margin-bottom: 13px;
  }

</style>
