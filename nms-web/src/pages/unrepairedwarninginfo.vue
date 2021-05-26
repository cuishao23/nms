<template>
  <div>
    <button class="normal-btn export" @click="onExport()">导出</button>
    <el-tabs v-model="tabType">
      <el-tab-pane label="服务器告警" name="server">
        <div class="server">
          <div>
            <div>
              <el-select v-model="sServiceDomainMoid" placeholder="请选择" @change="snodeClick" filterable>
                <el-option
                  v-for="(item,index) in sServiceDomainMoids"
                  :key="index"
                  :label="item.name"
                  :value="item.moid">
                </el-option>
              </el-select>
              <el-select v-model="sPlatformDomainMoid" placeholder="请选择" filterable>
                <el-option
                  v-for="(item,index) in sPlatformDomainMoids"
                  :key="index"
                  :label="item.name"
                  :value="item.moid">
                </el-option>
              </el-select>
              <el-select v-model="sMachineRoomMoid" placeholder="请选择" filterable>
                <el-option
                  v-for="(item,index) in sMachineRoomMoids"
                  :key="index"
                  :label="item.name"
                  :value="item.moid">
                </el-option>
              </el-select>
              <el-select v-model="sDeviceType" filterable>
                <el-option
                    v-for="(item,index) in sDeviceTypes"
                    :key="index"
                    :label="item.text"
                    :value="item.value">
                </el-option>
              </el-select>
              <el-input v-model="device_name_s" placeholder="请输入设备名称、IP" class="filter-text"></el-input>
            </div>
          </div>
          <div class="warning">
            <div>
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
              <DateBox v-if="reSet" inputId="d1" v-model="startDate" style="width: 110px" format="yyyy-MM-dd" :disabled="timePeriodValue !== 'selfdefine'"></DateBox>
              <div style="display: inline-block; width: 19px">→</div>
              <DateBox v-if="reSet" inputId="d2" v-model="endDate" style="width: 110px;" format="yyyy-MM-dd" :disabled="timePeriodValue !== 'selfdefine'"></DateBox>
              <button class='search' @click="searchUrepairedWarningsS()"></button>
              <span class="clear-filter" @click="clearFilterS()">清除筛选</span>
            </div>
          </div>
        </div>
        <div v-show="unrepairedserverWarningList.length === 0 && slistFlash" class="no-info-tip">
          <span class="PromptImg"></span>
          <span>没有满足条件的统计数据！</span>
        </div>
        <div v-show="unrepairedserverWarningList.length > 0 && ser_show">
          <nms-pager-table :data="unrepairedserverWarningList" :fields="unrepairedserverWarningFields"  :total-page="serverTotalPage"  :biao-zhi="cage" v-model="curPage" ref="t_page" class="el-tabs__content"/>
        </div>
      </el-tab-pane>

      <el-tab-pane label="终端告警" name="terminal">
        <div class="server">
          <div>
            <div>
              <el-select v-model="tTerminalDomainMoid" placeholder="请选择" @change="tnodeClick" filterable>
                <el-option
                  v-for="(item,index) in tTerminalDomainMoids"
                  :key="index"
                  :label="item.name"
                  :value="item.moid">
                </el-option>
              </el-select>
              <el-select v-model="tUserMoid" placeholder="请选择" filterable>
                <el-option
                  v-for="(item,index) in tUserMoids"
                  :key="index"
                  :label="item.name"
                  :value="item.moid">
                </el-option>
              </el-select>
              <el-select v-model="tDeviceType" filterable>
                <el-option
                  v-for="(item,index) in tDeviceTypes"
                  :key="index"
                  :label="item.text"
                  :value="item.value">
                </el-option>
              </el-select>
              <el-input v-model="device_name_t" placeholder="设备名称，E164号" class="filter-text"></el-input>
            </div>
          </div>
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
              <DateBox v-if="reSet" inputId="d3" v-model="startDate" style="width: 110px" format="yyyy-MM-dd" :disabled="timePeriodValue !== 'selfdefine'"></DateBox>
              <div style="display: inline-block; width: 19px">→</div>
              <DateBox v-if="reSet" inputId="d4" v-model="endDate" style="width: 110px;" format="yyyy-MM-dd" :disabled="timePeriodValue !== 'selfdefine'"></DateBox>
              <button class='search' @click="searchUrepairedWarningsT()"/>
              <span class="clear-filter" @click="clearFilterT()">清除筛选</span>
            </div>
          </div>
        </div>
        <div v-show="unrepairedterminalWarningList.length === 0 && tlistFlash" class="no-info-tip">
          <span class="PromptImg"></span>
          <span>没有满足条件的统计数据！</span>
        </div>
        <div v-show="unrepairedterminalWarningList.length > 0 && ter_show">
          <nms-pager-table :data="unrepairedterminalWarningList" :fields="unrepairedterminalWarningFields"  :total-page="terminalTotalPage" :biao-zhi="cage" v-model="curPage"/>
        </div>
      </el-tab-pane>
      <nms-dialog title="提示" ref="export">
          <div slot="content" class="ex-po-rt">
            <span>导出失败</span>
          </div>
      </nms-dialog>
    </el-tabs>
  </div>
</template>

<script>
    import {getTimePeriod} from "assets/js/common";
    import {getUnrepairedServerWarningTblFields,getUnrepairedTerminalWarningTblFields} from 'assets/js/subwarninginfo';
    import NmsDialog from "../components/common/nms-dialog";
    import NmsPagerTable from "../components/common/nms-pager-table";
    import api from '../axios';
    import qs from 'qs';
    import {FormatTime,get_time} from 'assets/js/common';
    import {Upexcele}  from '../common/commonFunction'


    export default {
        components: {
          NmsDialog,
          NmsPagerTable
        },
        name: "unrepairedwarninginfo",
        inject: ['reload'],
        data () {
          return {
            reSet: true,
            tabType: 'server', // tab标签类型
            perPage: 10, // 表格每页显示数量
            curPage: 1,
            cage: 1,

            timePeriod: [],
            timePeriodValue: 'lastweek',
            timeRange: [],
            // server
            sServiceDomainMoid: '',
            sPlatformDomainMoid: '',
            sMachineRoomMoid: '',
            sDeviceType: 'all', // 要搜索的服务器告警设备类型
            sServiceDomainMoids: [], // 服务域类型列表
            sPlatformDomainMoids: [], // 平台域列表
            sMachineRoomMoids: [], // 机房类型列表
            s: [],
            p: [],
            m: [],
            sDeviceTypes: [{
              text: '全部设备类型',
              value: 'all'
            }], // 服务器告警设备类型列表
            serverTotalPage: 1, // 总页数
            // 未修复服务器告警列表
            unrepairedserverWarningList: [],
            unrepairedserverWarningFields: [],
            critical: true,
            important: true,
            normal: true,

            // terminal
            tTerminalDomainMoids: [],
            tTerminalDomainMoid: '',
            tUserMoids: [],
            tUserMoid: '',
            tm: [],
            tu: [],
            tDeviceTypes: [{
              text: '全部设备类型',
              value: 'all'
            }],
            tDeviceType: 'all',
            terminalTotalPage: 1, // 总页数
            // 未修复终端告警列表
            unrepairedterminalWarningList: [],
            unrepairedterminalWarningFields: [],

            device_name_s: "",
            device_name_t: "",

            t_critical: true,
            t_important: true,
            t_normal: true,

            warningUesrDomains: [],
            warningDomains: [],

            startDate: new Date(),
            endDate: new Date(),

            moid_value: "",
            moid_top: "",
            moid_troom: "",

            moid_do: "",
            moid_main: "",
            top_main: "",

            slistFlash: false,
            tlistFlash: false,

            ser_show: true,
            ter_show: true
          }
        },
        async created() {
            this.timePeriod = getTimePeriod()
            this.startDate=get_time(this.timePeriodValue)
            // phisical
            api.getServerTypeList().then((res) => {
              for (var i = 0; i < res.data.length; i++) {
                let dic = {}
                dic["text"] = res.data[i]
                dic["value"] = res.data[i]
                this.sDeviceTypes.push(dic)
              }
            })
            // terminal
            api.getTerminalTypeList().then((res) => {
              for (var i = 0; i < res.data.length; i++) {
                let dic = {}
                dic["text"] = res.data[i]
                dic["value"] = res.data[i]
                this.tDeviceTypes.push(dic)
              }
            })
            // platform
            await api.getPlatformDomainTree().then((res) => {
              this.sServiceDomainMoids = []
              this.sPlatformDomainMoids = []
              this.sMachineRoomMoids = []
              this.s=[]
              this.p=[]
              this.m=[]
              this.warningDomains=res.data
              this.warningDomains.forEach(i=>{
                if(i.type=="service" || i.type=="kernel"){
                  this.sServiceDomainMoids.push(i)
                  this.s.push(i)
                  if(i.type=="kernel"){
                    this.top_main=i.moid
                  }
                }else if(i.type=="platform"){
                  this.sPlatformDomainMoids.push(i)
                  this.p.push(i)
                }else if(i.type=="machine_room"){
                  this.sMachineRoomMoids.push(i)
                  this.m.push(i)
                }
              })
              this.sServiceDomainMoids.unshift({
                "moid": "",
                "parent_moid": "",
                "name": "所有服务域",
                "type": "server"
              })
              this.sPlatformDomainMoids.unshift({
                "moid": "",
                "parent_moid": "",
                "name": "所有平台域",
                "type": "platform"
              })
              this.sMachineRoomMoids.unshift({
                "moid": "",
                "parent_moid": "",
                "name": "所有虚拟机房",
                "type": "machine_room"
              })
              this.sServiceDomainMoid = ""
              this.sPlatformDomainMoid = ""
              this.sMachineRoomMoid = ""

              this.getServerUnrepairedWarning()
            })
            // user
            await api.getUserDomainTree().then((res) => {
              this.tTerminalDomainMoids=[]
              this.tUserMoids=[]
              this.tm=[]
              this.tu=[]
              this.warningUesrDomains = res.data
              this.warningUesrDomains.forEach(i=>{
                if(i.type=="service" || i.type=="kernel"){
                  this.tTerminalDomainMoids.push(i)
                  this.tm.push(i)
                }else if(i.type=="user"){
                  this.tUserMoids.push(i)
                  this.tu.push(i)
                }
              })
              this.tTerminalDomainMoids.unshift({
                "moid": "",
                "parent_moid": "",
                "name": "所有服务域",
                "type": "server"
              })
              this.tUserMoids.unshift({
                "moid": "",
                "parent_moid": "",
                "name": "所有用户域",
                "type": "user"
              })
              this.tTerminalDomainMoid = ""
              this.tUserMoid = ""

          })

          if (this.$route.params.warningType === 'serverWarning') {
            this.tabType = 'server'
          } else if (this.$route.params.warningType === 'terminalWarning') {
            this.tabType = 'terminal'
          }
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
            if ((newTime - this.startDate) < 0 && FormatTime(newTime).substr(0, 10) !== FormatTime(this.startDate).substr(0, 10) && newTime != null) {
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
            if(newTime!="selfdefine"){
              this.endDate=new Date()
            }
          },
          sServiceDomainMoid: function (val) {
              if(val==""){
                this.sServiceDomainMoids = []
                this.sPlatformDomainMoids = []
                this.sMachineRoomMoids = []
                this.sServiceDomainMoids = [].concat(this.s)
                this.sPlatformDomainMoids = [].concat(this.p)
                this.sMachineRoomMoids = [].concat(this.m)
                this.sServiceDomainMoids.unshift({
                    "moid": "",
                    "parent_moid": "",
                    "name": "所有服务域",
                    "type": "server"
                  })
                  this.sPlatformDomainMoids.unshift({
                    "moid": "",
                    "parent_moid": "",
                    "name": "所有平台域",
                    "type": "platform"
                  })
                  this.sMachineRoomMoids.unshift({
                    "moid": "",
                    "parent_moid": "",
                    "name": "所有虚拟机房",
                    "type": "machine_room"
                })
                this.sServiceDomainMoid = ""
                this.sPlatformDomainMoid = ""
                this.sMachineRoomMoid = ""
              }else if(val==this.top_main){
                this.sPlatformDomainMoids = []
                this.sMachineRoomMoids = []
                this.sPlatformDomainMoids = [].concat(this.p)
                this.sMachineRoomMoids = [].concat(this.m)
                this.sPlatformDomainMoids.unshift({
                    "moid": "",
                    "parent_moid": "",
                    "name": "所有平台域",
                    "type": "platform"
                })
                this.sMachineRoomMoids.unshift({
                    "moid": "",
                    "parent_moid": "",
                    "name": "所有虚拟机房",
                    "type": "machine_room"
                })
                this.sPlatformDomainMoid = ""
                this.sMachineRoomMoid = ""
              }else{
                this.sPlatformDomainMoids = []
                this.sMachineRoomMoids = []
                this.p.forEach(j=>{
                  if(val==j.parent_moid){
                    this.sPlatformDomainMoids.push(j)
                    this.m.forEach(k=>{
                      if(j.moid==k.parent_moid){
                        this.sMachineRoomMoids.push(k)
                      }
                    })
                  }
                })
                this.sPlatformDomainMoids.unshift({
                  "moid": "",
                  "parent_moid": "",
                  "name": "所有平台域",
                  "type": "platform"
                })
                this.sPlatformDomainMoid=""
                if(this.sMachineRoomMoids.length==0){
                  this.sMachineRoomMoids.unshift({
                    "moid": "",
                    "parent_moid": "",
                    "name": "无下级域",
                    "type": "machine_room"
                  })
                }else{
                  this.sMachineRoomMoids.unshift({
                    "moid": "",
                    "parent_moid": "",
                    "name": "所有虚拟机房",
                    "type": "machine_room"
                  })
                }
                this.sMachineRoomMoid=""
              }
          },
          sPlatformDomainMoid: function (val) {
              if(val==""){
                this.sPlatformDomainMoids = []
                this.sMachineRoomMoids = []
                this.sPlatformDomainMoids = [].concat(this.p)
                this.sMachineRoomMoids = [].concat(this.m)
                  this.sPlatformDomainMoids.unshift({
                    "moid": "",
                    "parent_moid": "",
                    "name": "所有平台域",
                    "type": "platform"
                  })
                  this.sMachineRoomMoids.unshift({
                    "moid": "",
                    "parent_moid": "",
                    "name": "所有虚拟机房",
                    "type": "machine_room"
                })
                this.sPlatformDomainMoid = ""
                this.sMachineRoomMoid = ""
              }else{
                this.sMachineRoomMoids = []
                this.m.forEach(i=>{
                  if(val==i.parent_moid){
                    this.sMachineRoomMoids.push(i)
                  }
                })
                if(this.sMachineRoomMoids.length==0){
                  this.sMachineRoomMoids.unshift({
                    "moid": "",
                    "parent_moid": "",
                    "name": "无下级域",
                    "type": "machine_room"
                  })
                }else{
                  this.sMachineRoomMoids.unshift({
                    "moid": "",
                    "parent_moid": "",
                    "name": "所有虚拟机房",
                    "type": "machine_room"
                  })
                }
                this.sMachineRoomMoid=""
              }
          },
          tTerminalDomainMoid: function (val) {
            if(val==""){
                this.tTerminalDomainMoids = []
                this.tUserMoids = []
                this.tTerminalDomainMoids = [].concat(this.tm)
                this.tUserMoids = [].concat(this.tu)
                this.tTerminalDomainMoids.unshift({
                  "moid": "",
                  "parent_moid": "",
                  "name": "所有服务域",
                  "type": "server"
                })
                this.tUserMoids.unshift({
                  "moid": "",
                  "parent_moid": "",
                  "name": "所有用户域",
                  "type": "user"
                })
                this.tTerminalDomainMoid = ""
                this.tUserMoid = ""
              }else if(val==this.top_main){
                this.tUserMoids = []
                this.tUserMoids = [].concat(this.tu)
                this.tUserMoids.unshift({
                  "moid": "",
                  "parent_moid": "",
                  "name": "所有用户域",
                  "type": "user"
                })
                this.tUserMoid = ""
              }else{
                this.tUserMoids=[]
                this.tu.forEach(j=>{
                  if(val==j.parent_moid){
                    this.tUserMoids.push(j)
                  }
                })
                if(this.tUserMoids.length==0){
                  this.tUserMoids.unshift({
                    "moid": "",
                    "parent_moid": "",
                    "name": "无下级域",
                    "type": "user"
                  })
                }else{
                  this.tUserMoids.unshift({
                    "moid": "",
                    "parent_moid": "",
                    "name": "所有用户域",
                    "type": "user"
                  })
                }
                this.tUserMoid=""
              }
          },
          tabType: function (val) {
            let start_time = FormatTime(this.startDate)
            let end_time = FormatTime(this.endDate)
            if (val == "server") {
              api.getLatestServerUnrepairedWarning({params:{
                  newPageNum: 1,
                  critical: this.critical,
                  important: this.important,
                  normal: this.normal,
                  deviceName: this.device_name_s,
                  deviceType: this.sDeviceType,
                  parentMoid: this.sMachineRoomMoid,
                  starttime: start_time,
                  stoptime: end_time
                }
              })
              .then((res) => {
                if(res.success==1){
                  this.unrepairedserverWarningList = res.data
                  this.unrepairedserverWarningFields = getUnrepairedServerWarningTblFields(this.editServerWarning, this.gotoPhysicalDetail)
                  this.serverTotalPage = Math.ceil(res.total_num / this.perPage)
                  this.cage = 2
                }
              })
              .catch((error) => {
                console.log(error);
              });
            } else if (val == "terminal") {
              api.getLatestTerminalUnrepairedWarning({params:{
                  newPageNum: 1,
                  critical: this.t_critical,
                  important: this.t_important,
                  normal: this.t_normal,
                  deviceName: this.device_name_t,
                  deviceType: this.tDeviceType,
                  parentMoid: this.tUserMoid,
                  starttime: start_time,
                  stoptime: end_time
                }
              })
              .then((res) => {
                if(res.success==1){
                  if (res.total_num == 0) {
                    this.tlistFlash = true
                  } else {
                    this.tlistFlash = false
                  }
                  this.unrepairedterminalWarningList = res.data
                  this.unrepairedterminalWarningFields = getUnrepairedTerminalWarningTblFields(this.editTerminalWarning, this.gotoCtrlTerminalDetail)
                  this.terminalTotalPage = Math.ceil(res.total_num / this.perPage)
                  this.cage = 2
                }
              })
              .catch((error) => {
                console.log(error);
              });
            }
          },
          curPage: function (newPageNum, oldPageNum) {
            var start_time = FormatTime(this.startDate)
            var end_time = FormatTime(this.endDate)
            // if(start_time.split(" ")[0]==FormatTime(new Date()).split(" ")[0]){
            //   start_time = FormatTime(new Date(new Date().toLocaleDateString()).getTime())
            // }
            this.cage = 1
            if (this.tabType == "server") {
              this.ser_show = false
              api.getLatestServerUnrepairedWarning({params: {
                  newPageNum: newPageNum,
                  critical: this.critical,
                  important: this.important,
                  normal: this.normal,
                  deviceName: this.device_name_s,
                  deviceType: this.sDeviceType,
                  parentMoid: this.sMachineRoomMoid,
                  starttime: start_time,
                  stoptime: end_time
                }
              })
              .then((res) => {
                if(res.success==1){
                  this.unrepairedserverWarningList = res.data
                  this.unrepairedserverWarningFields = getUnrepairedServerWarningTblFields(this.editServerWarning, this.gotoPhysicalDetail)
                  this.serverTotalPage = Math.ceil(res.total_num / this.perPage)
                  this.ser_show = true
                }
              })
              .catch((error) => {
                console.log(error);
              });
            } else if (this.tabType == "terminal") {
              this.ter_show = false
              api.getLatestTerminalUnrepairedWarning({params: {
                  newPageNum: newPageNum,
                  critical: this.t_critical,
                  important: this.t_important,
                  normal: this.t_normal,
                  deviceName: this.device_name_t,
                  deviceType: this.tDeviceType,
                  parentMoid: this.tUserMoid,
                  starttime: start_time,
                  stoptime: end_time
                }
              })
              .then((res) => {
                if(res.success==1){
                  this.unrepairedterminalWarningList = res.data
                  this.unrepairedterminalWarningFields = getUnrepairedTerminalWarningTblFields(this.editTerminalWarning, this.gotoCtrlTerminalDetail)
                  this.terminalTotalPage = Math.ceil(res.total_num / this.perPage)
                  this.ter_show = true
                }
              })
              .catch((error) => {
                console.log(error);
              });
            }
          }
        },
        methods:{
          onExport: function () {
            let start_time = FormatTime(this.startDate)
            let end_time = FormatTime(this.endDate)
            if(start_time.split(" ")[0]==FormatTime(new Date()).split(" ")[0]){
              start_time = FormatTime(new Date(new Date().toLocaleDateString()).getTime())
            }
            if (this.tabType == "server") {
              api.getWarningDownLoad({params: {
                critical: this.critical,
                important: this.important,
                normal: this.normal,
                deviceName: this.device_name_s,
                deviceType: this.sDeviceType,
                parentMoid: this.sMachineRoomMoid,
                starttime: start_time,
                stoptime: end_time,
                warningType: 'unrepaired_server_warning'
              }, responseType: 'blob'}).then(res => {
                Upexcele(res, '未修复服务器告警信息.xls')
              }).catch(error => {
                console.log(error)
                this.errorDialog.open('导出失败')
              });
            } else if (this.tabType == "terminal") {
              console.log()
              api.getWarningDownLoad({params: {
                critical: this.t_critical,
                important: this.t_important,
                normal: this.t_normal,
                deviceName: this.device_name_t,
                deviceType: this.tDeviceType,
                parentMoid: this.tUserMoid,
                starttime: start_time,
                stoptime: end_time,
                warningType: 'unrepaired_terminal_warning'
              }, responseType: 'blob'}).then(res => {
                Upexcele(res, '未修复终端告警信息.xls')
              }).catch(error => {
                console.log(error)
                this.errorDialog.open('导出失败')
              });
            }
          },
          clearFilterS: function () {
            this.device_name_s = ""
            this.timePeriodValue = "selfdefine"
            this.timeRange = []
            this.critical=true
            this.important=true
            this.normal=true
            this.startDate=null
            this.endDate=null
          },
          clearFilterT: function () {
            this.device_name_t = ""
            this.timePeriodValue = "selfdefine"
            this.timeRange = []
            this.t_critical=true
            this.t_important=true
            this.t_normal=true
            this.startDate=null
            this.endDate=null
          },
          // server
          getServerUnrepairedWarning: function () {
              let start_time = FormatTime(this.startDate)
              let end_time = FormatTime(this.endDate)
              api.getLatestServerUnrepairedWarning({params:{
                    newPageNum: 1,
                    critical: this.critical,
                    important: this.important,
                    normal: this.normal,
                    deviceName: this.device_name_s,
                    deviceType: this.sDeviceType,
                    parentMoid: this.sMachineRoomMoid,
                    starttime: start_time,
                    stoptime: end_time
                  }
                })
                .then((res) => {
                  if(res.success==1){
                    if (res.total_num == 0) {
                      this.slistFlash = true
                    } else {
                      this.slistFlash = false
                    }
                    this.unrepairedserverWarningList = res.data
                    this.unrepairedserverWarningFields = getUnrepairedServerWarningTblFields(this.editServerWarning, this.gotoPhysicalDetail)
                    this.serverTotalPage = Math.ceil(res.total_num / this.perPage)
                  }
                })
                .catch((error) => {
                  console.log(error);
                });
          },
          gotoPhysicalDetail: function(data) {
              console.log("告警"+JSON.stringify(data))
              this.$router.push({
                  name: "physicaldetail",
                  // params: {name: data.device_name,type: data.device_type,machine_room_moid: data.machine_room_moid, ip: data.device_ip, moid: data.device_moid}
                  params: {moid: data.device_moid, page: 'unrepairedwarning'}
              });
          },
          editServerWarning: function (rowData) {
            let machineRoomMoid = rowData.machine_room_moid
            let deviceMoid = rowData.device_moid
            let code = rowData.code
            api.getRepairServerWarning({params:{
                  machineRoomMoid: machineRoomMoid,
                  deviceMoid: deviceMoid,
                  code: code
                }
              })
              .then((res) => {
                if(res.success==1){
                  // this.reload()
                  this.getServerUnrepairedWarning()
                }
              })
              .catch((error) => {
                console.log(error);
              });
          },
          editTerminalWarning: function (rowData) {
            let domainMoid = rowData.domain_moid
            let deviceMoid = rowData.device_moid
            let code = rowData.code
            api.getRepairTerminalWarning({params:{
                  domainMoid: domainMoid,
                  deviceMoid: deviceMoid,
                  code: code
                }
              })
              .then((res) => {
                console.log("修复终端告警结果反馈="+JSON.stringify(res))
                if(res.success==1){
                  // this.reload()
                  this.getTerminalUnrepairedWarning()
                }
              })
              .catch((error) => {
                console.log(error);
              });
          },
          snodeClick: function() {
            var s_selected_val = this.sServiceDomainMoid
            if (s_selected_val == 'subdefault') {
              this.sPlatformDomainMoid = 'pldefault'
              this.sMachineRoomMoid = 'allroom'
            } else {
               this.sPlatformDomainMoid = 'kernel'
               this.sMachineRoomMoid ='allroom'
            }
          },
          searchUrepairedWarningsS: function () {
            var start_time = FormatTime(this.startDate)
            var end_time = FormatTime(this.endDate)
            if (this.timePeriodValue == "lasthour") {
              start_time = start_time
            } else {
              if(start_time.split(" ")[0]==FormatTime(new Date()).split(" ")[0]){
                start_time = FormatTime(new Date(new Date().toLocaleDateString()).getTime())
              }
            }
            api.getLatestServerUnrepairedWarning({params:{
                  newPageNum: 1,
                  critical: this.critical,
                  important: this.important,
                  normal: this.normal,
                  deviceName: this.device_name_s,
                  deviceType: this.sDeviceType,
                  parentMoid: this.sMachineRoomMoid,
                  starttime: start_time,
                  stoptime: end_time
                }
              })
              .then((res) => {
                if(res.success==1){
                  if (res.total_num == 0) {
                    this.slistFlash = true
                  } else {
                    this.slistFlash = false
                  }
                  this.unrepairedserverWarningList = res.data
                  this.unrepairedserverWarningFields = getUnrepairedServerWarningTblFields(this.editServerWarning, this.gotoPhysicalDetail)
                  this.serverTotalPage = Math.ceil(res.total_num / this.perPage)
                  this.cage = 2
                }
              })
              .catch( (error) => {
                console.log(error);
              });
          },
          // terminal
          getTerminalUnrepairedWarning: function () {
            let start_time = FormatTime(this.startDate)
            let end_time = FormatTime(this.endDate)
            api.getLatestTerminalUnrepairedWarning({params:{
                newPageNum: 1,
                critical: this.t_critical,
                important: this.t_important,
                normal: this.t_normal,
                deviceName: this.device_name_t,
                deviceType: this.tDeviceType,
                parentMoid: this.tUserMoid,
                starttime: start_time,
                stoptime: end_time
              }
            })
            .then((res) => {
              if(res.success==1){
                if (res.total_num == 0) {
                  this.tlistFlash = true
                } else {
                  this.tlistFlash = false
                }
                this.unrepairedterminalWarningList = res.data
                this.unrepairedterminalWarningFields = getUnrepairedTerminalWarningTblFields(this.editTerminalWarning, this.gotoCtrlTerminalDetail)
                this.terminalTotalPage = Math.ceil(res.total_num / this.perPage)
              }
            })
            .catch((error) => {
              console.log(error);
            });
          },
          gotoCtrlTerminalDetail: function(data) {
             this.$router.push({name: 'ctrlterminaldetail', params: {moid: data.device_moid, name: data.device_name, e164: data.device_e164}})
          },
          tnodeClick: function() {
            var t_selected_val = this.tTerminalDomainMoid
            if (t_selected_val == 'tdefault' || t_selected_val == 'kedacom') {
              this.tUserMoid = 'alltuser'
            }
          },
          searchUrepairedWarningsT: function () {
            var start_time = FormatTime(this.startDate)
            var end_time = FormatTime(this.endDate)
            if (this.timePeriodValue == "lasthour") {
              start_time = start_time
            } else {
              if(start_time.split(" ")[0]==FormatTime(new Date()).split(" ")[0]){
                start_time = FormatTime(new Date(new Date().toLocaleDateString()).getTime())
              }
            }
            api.getLatestTerminalUnrepairedWarning({params:{
                  newPageNum: 1,
                  critical: this.t_critical,
                  important: this.t_important,
                  normal: this.t_normal,
                  deviceName: this.device_name_t,
                  deviceType: this.tDeviceType,
                  parentMoid: this.tUserMoid,
                  starttime: start_time,
                  stoptime: end_time
                }
              })
              .then((res) => {
                if(res.success==1){
                  this.unrepairedterminalWarningList = res.data
                  this.unrepairedterminalWarningFields = getUnrepairedTerminalWarningTblFields(this.editTerminalWarning, this.gotoCtrlTerminalDetail)
                  this.terminalTotalPage = Math.ceil(res.total_num / this.perPage)
                  this.cage = 2
                }
              })
              .catch( (error) => {
                console.log(error);
              });
          },
        }
    }
</script>

<style scoped>
  .server > div:first-child > div:first-child {
    display: inline;
    float: left;
    padding-top: 12px;
  }
  .export {
    float: right;
  }

  .warning {
    clear: left;
    text-align: left;
    padding-top: 18px;
  }
  .clear-filter {
    font-size: 12px;
    color: #3e9bd0;
    cursor: pointer;
    padding-left: 5px;
  }
  .filter-text {
    width: 176px
  }
  .ex-po-rt {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    height: 100%;
  }
 .ex-po-rt input {
    margin-left: 30px;
  }
  .f-field {
    top: -2px;
  }
  .el-select {
    padding-right: 16px;
  }
  /deep/ .el-tabs__nav-scroll {
    cursor:pointer
  }
</style>
