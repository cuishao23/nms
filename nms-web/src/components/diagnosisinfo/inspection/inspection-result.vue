<template>
  <div class="tradition-meeting-detail">
    <div class="tradition-meeting-back">
      <span class="back-btn" @click="$router.go(-1)"></span>
      <span class="base-info-title">巡检详情</span>
      <div style="float:right;">
        <button id="exportResult" class="normal-btn" @click="deleteInspectResult()">删除</button>
        <button id="exportResult" class="normal-btn" @click="exportInspectResult()">导出</button>
      </div>
    </div>
    <ul style="display: flex">
      <span class="grab-tab">巡检时间</span>
      <li id="diagnosis_time" v-if="inspectTimes.length>0">
        <el-select v-model="inspectTime" placeholder="请选择" class="select-time">
          <el-option
            v-for="(item,index) in inspectTimes"
            :key="index"
            :label="item.start_time"
            :value="item.id">
          </el-option>
        </el-select>
      </li>
    </ul>
    <el-tabs v-model="tabType" style="cursor:pointer">
      <div style="padding-bottom: 19px; font-size: 12px; text-align:left;padding-top: 24px;">
        <span class="itemName" style="color: #8b8b8b;">域</span>
        <span id="inspectDomainInfo" class="itemValue" style="padding-top: 0px;" v-if="checked_l == 1&&tabType === 'license'">{{ license_domain }}</span>
        <span id="inspectDomainInfo" class="itemValue" style="padding-top: 0px;" v-if="checked_so == 1&&tabType === 'resource'">{{ resource_domain }}</span>
        <span id="inspectDomainInfo" class="itemValue" style="padding-top: 0px;" v-if="checked_st == 1&&tabType === 'server'">{{ server_domain }}</span>
        <span id="inspectDomainInfo" class="itemValue" style="padding-top: 0px;" v-if="checked_t == 1&&tabType === 'terminal'">{{ terminal_domain }}</span>
      </div>
      <el-tab-pane label="License文件" name="license" style="cursor:default">
        <div v-if="licenseList.length === 0||checked_l == 0" class="no-info-tip">
          没有巡检数据！
        </div>
        <div v-if="licenseList.length > 0&&checked_l == 1">
          <nms-pager-table :data="licenseList" :fields="licenseFields" :total-page="inspectionTotalPage" :biao-zhi="cage" v-model="curPage"/>
        </div>
      </el-tab-pane>
      <el-tab-pane label="会议资源" name="resource" style="cursor:default">
        <div class="chart-circle">
          <div class="circle-block">
            <res-usage-circle :percent="APsPercent" :width='85'/>
          </div>
          <div class="circle-info">
            <div class="circle-title">
              <h4>接入端口资源</h4>
              <el-popover
                placement="right-start"
                title=""
                width="200"
                trigger="click">
                <div class="circle-info-detail">
                  <div class="circle-title">
                    <span>接入端口</span>
                  </div>
                  <div class="circle-detail">
                    <span class="circle-detail-block">已使用：<span>{{ APStarted }}</span></span>
                    <span class="circle-detail-block">剩余可使用：<span>{{ APUsable }}</span></span>
                  </div>
                </div>
                <div class="circle-info-detail">
                  <div class="circle-title">
                    <span>国密接入端口</span>
                  </div>
                  <div class="circle-detail">
                    <span class="circle-detail-block">已使用：<span>{{ GAPStarted }}</span></span>
                    <span class="circle-detail-block">剩余可使用：<span>{{ GAPUsable }}</span></span>
                  </div>
                </div>
                <el-button slot="reference" icon="el-icon-info" circle></el-button>
              </el-popover>
            </div>
            <div class="circle-detail">
              <span class="circle-detail-block">已使用：<span>{{ APsStarted }}</span></span>
              <span class="circle-detail-block">剩余可使用：<span>{{ APsUsable }}</span></span>
            </div>
          </div>
        </div>
        <div class="chart-circle">
          <div class="circle-block">
            <res-usage-circle :percent="MPsPercent" :width='85'/>
          </div>
          <div class="circle-info">
            <div class="circle-title">
              <h4>媒体端口资源</h4>
              <el-popover
                placement="right-start"
                title=""
                width="200"
                trigger="click">
                <div class="circle-info-detail">
                  <div class="circle-title">
                    <span>H264媒体端口</span>
                  </div>
                  <div class="circle-detail">
                    <span class="circle-detail-block">已使用：<span>{{ MPStarted }}</span></span>
                    <span class="circle-detail-block">剩余可使用：<span>{{ MPUsable }}</span></span>
                  </div>
                </div>
                <div class="circle-info-detail">
                  <div class="circle-title">
                    <span>H265媒体端口</span>
                  </div>
                  <div class="circle-detail">
                    <span class="circle-detail-block">已使用：<span>{{ HMPStarted }}</span></span>
                    <span class="circle-detail-block">剩余可使用：<span>{{ HMPUsable }}</span></span>
                  </div>
                </div>
                <div class="circle-info-detail">
                  <div class="circle-title">
                    <span>国密H264媒体端口</span>
                  </div>
                  <div class="circle-detail">
                    <span class="circle-detail-block">已使用：<span>{{ GMPStarted }}</span></span>
                    <span class="circle-detail-block">剩余可使用：<span>{{ GMPUsable }}</span></span>
                  </div>
                </div>
                <div class="circle-info-detail">
                  <div class="circle-title">
                    <span>国密H265媒体端口</span>
                  </div>
                  <div class="circle-detail">
                    <span class="circle-detail-block">已使用：<span>{{ GHMPStarted }}</span></span>
                    <span class="circle-detail-block">剩余可使用：<span>{{ GHMPUsable }}</span></span>
                  </div>
                </div>
                <el-button slot="reference" icon="el-icon-info" circle></el-button>
              </el-popover>
            </div>
            <div class="circle-detail">
              <span class="circle-detail-block">已使用：<span>{{ MPsStarted }}</span></span>
              <span class="circle-detail-block">剩余可使用：<span>{{ MPsUsable }}</span></span>
            </div>
          </div>
        </div>
        <div class="chart-circle">
          <div class="circle-block">
            <res-usage-circle :percent="STerPercent" :width='85'/>
          </div>
          <div class="circle-info">
            <div class="circle-title">
              <h4>软终端资源</h4>
              <el-popover
                placement="right-start"
                title=""
                width="200"
                trigger="click">
                <div class="circle-info-detail">
                  <div class="circle-title">
                    <span>放号资源信息</span>
                  </div>
                  <div class="circle-detail">
                    <span class="circle-detail-block">在线数：<span>{{ STerOnline }}</span></span>
                    <span class="circle-detail-block">放号数：<span>{{ STerStarted }}</span></span>
                  </div>
                </div>
                <el-button slot="reference" icon="el-icon-info" circle></el-button>
              </el-popover>
            </div>
            <div class="circle-detail">
              <span class="circle-detail-block">放号数：<span>{{ STerStarted }}</span></span>
              <span class="circle-detail-block">授权资源总数：<span>{{ STerTotal }}</span></span>
            </div>
          </div>
        </div>
        <div class="chart-circle">
          <div class="circle-block">
            <res-usage-circle :percent="LMPercent" :width='85'/>
          </div>
          <div class="circle-info">
            <div class="circle-title">
              <h4>直播会议</h4>
              <el-popover
                placement="right-start"
                title=""
                width="200"
                trigger="click">
                <div class="circle-info-detail">
                  <div class="circle-title">
                    <span>HTML5直播资源</span>
                  </div>
                  <div class="circle-detail">
                    <span class="circle-detail-block">已使用：<span>{{ HLSStarted }}</span></span>
                    <span class="circle-detail-block">剩余可使用：<span>{{ HLSUsable }}</span></span>
                  </div>
                </div>
                <div class="circle-info-detail">
                  <div class="circle-title">
                    <span>ASF直播资源</span>
                  </div>
                  <div class="circle-detail">
                    <span class="circle-detail-block">已使用：<span>{{ ASFStarted }}</span></span>
                    <span class="circle-detail-block">剩余可使用：<span>{{ ASFUsable }}</span></span>
                  </div>
                </div>
                <el-button slot="reference" icon="el-icon-info" circle></el-button>
              </el-popover>
            </div>
            <div class="circle-detail">
              <span class="circle-detail-block">已使用：<span>{{ LMStarted }}</span></span>
              <span class="circle-detail-block">剩余可使用：<span>{{ LMUsable }}</span></span>
            </div>
          </div>
        </div>
        <div class="chart-circle">
          <div class="circle-block">
            <res-usage-circle :percent="VRPercent" :width='85'/>
          </div>
          <div class="circle-info">
            <div class="circle-title">
              <span>录像室</span>
            </div>
            <div class="circle-detail">
              <span class="circle-detail-block">已使用：<span>{{ VRStarted }}</span></span>
              <span class="circle-detail-block">剩余可使用：<span>{{ VRUsable }}</span></span>
            </div>
          </div>
        </div>
        <div class="chart-circle" v-show="lv_show">
          <div class="circle-block">
            <res-usage-circle :percent="ViewersPercent" :width='85'/>
          </div>
          <div class="circle-info">
            <div class="circle-title">
              <span>直播观看人数</span>
            </div>
            <div class="circle-detail">
              <span class="circle-detail-block">正在观看人数：<span>{{ ViewersStarted }}</span></span>
              <span class="circle-detail-block">剩余可观看人数：<span>{{ ViewersUsable }}</span></span>
            </div>
          </div>
        </div>
        <div class="chart-circle">
          <div class="circle-block">
            <res-usage-circle :percent="CRPercent" :width='85'/>
          </div>
          <div class="circle-info">
            <div class="circle-title">
              <span>协作资源</span>
            </div>
            <div class="circle-detail">
              <span class="circle-detail-block">已使用：<span>{{ CRStarted }}</span></span>
              <span class="circle-detail-block">剩余可使用：<span>{{ CRPUsable }}</span></span>
            </div>
          </div>
        </div>
      </el-tab-pane>
      <el-tab-pane label="服务器状态" name="server" style="cursor:default">
        <div v-if="serverList.length === 0||checked_st == 0" class="no-info-tip">
          没有巡检数据！
        </div>
        <div v-if="serverList.length > 0&&checked_st == 1">
          <nms-pager-table :data="serverList" :fields="serverFields" :total-page="inspectionTotalPage" :biao-zhi="cage" v-model="curPage"/>
        </div>
      </el-tab-pane>
      <el-tab-pane label="终端状态" name="terminal" style="cursor:default">
        <div v-if="terminalList.length === 0||checked_t==0" class="no-info-tip">
          没有巡检数据！
        </div>
        <div v-if="terminalList.length > 0&&checked_t==1">
          <nms-pager-table :data="terminalList" :fields="terminalListFields" :total-page="inspectionTotalPage" :biao-zhi="cage" v-model="curPage"/>
        </div>
      </el-tab-pane>
      <nms-big-dialog title="删除巡检项" :width="'400px'" :height="'260px'" :close-btn="true" ref="deleteInspectDialog" @confirm="OnSave()" @cancel="OnCancel()">
        <div slot="content" style="padding-top: 27px">
          <div class="textleft">
            <el-checkbox v-model="checkAll" @change="handleCheckAllChange">全选</el-checkbox>
            <el-checkbox-group v-model="checkedInspectTimes" @change="handleCheckedCitiesChange">
              <el-checkbox v-for="childInspectTime in childInspectTimes" :label="childInspectTime" :key="childInspectTime" style="display:block;">{{childInspectTime}}</el-checkbox>
            </el-checkbox-group>
          </div>
        </div>
    </nms-big-dialog>
    </el-tabs>
  </div>
</template>

<script>
  import api from "../../../axios";
  import NmsPagerTable from "../../common/nms-pager-table";
  import {getLicenseFields,getServerFields,getTerminalFields,getInspectionResInfo,getInspectTaskListFields,getHours,getMinutes,getSeconds} from "../../../assets/js/diagnose";
  import ResInfo from "../../common/res-info";
  import {DateTime,KeepTwoNum} from "../../../assets/js/common";
  import {Upexcele}  from '../../../common/commonFunction';
  import NmsBigDialog from "../../common/nms-big-dialog";
  import ResUsageCircle from "../../common/res-usage-circle";
  export default {
    components:{NmsPagerTable,ResInfo,NmsBigDialog,ResUsageCircle},
    name: "inspection-result",
    inject: ['reload'],
    data() {
      return {
        tabType: "license",
        curPage: 1,
        cage: 1,
        inspectionTotalPage: 1, //总页数
        sinspectionTotalPage:1,//总页数

        datetime: "", //实时时间

        checked_l: 0,
        checked_so: 0,
        checked_st: 0,
        checked_t: 0,

        license_domain: "", //License文件域
        resource_domain: "", //服务器资源
        server_domain: "", //服务器状态
        terminal_domain: "", //终端状态

        licenses: [],
        licenseFields: [],
        physicss: [],
        physicsFields: [],
        logics: [],
        logicFields: [],
        terminals: [],
        terminalFields: [],

        physicsdatas: [],
        paramsData: {},
        taskid: "",
        inspectTime: "",
        inspectTimes: [],

        //License文件
        licenseList: [],
        licenseFields: [],

        //会议资源
        resData: [],
        resList: [],

        //服务器状态
        serverList: [],
        serverFields: [],

        //终端状态
        terminalList: [],
        terminalListFields: [],

        childInspectTimes: [],
        checkAll: true,
        checkedInspectTimes: [],

        taskid_list: [],
        // 会议资源使用量
        APsPercent: 0,
        APsStarted: 0,
        APsUsable: 0,
        APStarted: 0,
        APUsable: 0,
        GAPStarted: 0,
        GAPUsable: 0,

        MPsPercent: 0,
        MPsStarted: 0,
        MPsUsable: 0,
        MPStarted: 0,
        MPUsable: 0,
        HMPStarted: 0,
        HMPUsable: 0,
        GMPStarted: 0,
        GMPUsable: 0,
        GHMPStarted: 0,
        GHMPUsable: 0,

        STerPercent: 0,
        STerStarted: 0,
        STerTotal: 0,
        STerOnline: 0,

        LMPercent: 0,
        LMStarted: 0,
        LMUsable: 0,
        HLSStarted: 0,
        HLSUsable: 0,
        ASFStarted: 0,
        ASFUsable: 0,

        VRPercent: 0,
        VRStarted: 0,
        VRUsable: 0,

        ViewersPercent: 0,
        ViewersStarted: 0,
        ViewersUsable: 0,

        CRPercent: 0,
        CRStarted: 0,
        CRPUsable: 0,

        lv_show : false,
      }
    },
    activated: function () {
      this.paramsData = this.$route.params
      console.log("paramsData="+JSON.stringify(this.paramsData))
      if(this.paramsData.license==1){
        this.license_domain = this.paramsData.inspect_range.license.platform_domain_name
      }
      if(this.paramsData.resource==1){
        this.resource_domain = this.paramsData.inspect_range.resource.platform_domain_name+"-"+this.paramsData.inspect_range.resource.virtual_machine_room_name
      }
      if(this.paramsData.server==1){
        this.server_domain = this.paramsData.inspect_range.server.platform_domain_name+"-"+this.paramsData.inspect_range.server.virtual_machine_room_name
      }
      if(this.paramsData.terminal==1){
        this.terminal_domain = this.paramsData.inspect_range.terminal.user_domain_name
      }
      this.taskid = this.paramsData.id
      this.checked_l=this.paramsData.license
      this.checked_so=this.paramsData.resource
      this.checked_st=this.paramsData.server
      this.checked_t=this.paramsData.terminal
      this.getChildrenInspectTask()
    },
    mounted: function () {

    },
    methods: {
      // 巡检子任务
      getChildrenInspectTask: function () {
        // 清除上次巡检子任务及子任务巡检数据
        this.inspectTimes = []
        this.inspectTime = ""
        this.licenseList = []
        this.resData = []
        this.resList = []
        this.serverList = []
        this.terminalList = []
        // 会议资源
        this.APsStarted = 0
        this.APsUsable = 0
        this.APStarted = 0
        this.APUsable = 0
        this.GAPStarted = 0
        this.GAPUsable = 0

        this.MPsStarted = 0
        this.MPsUsable = 0
        this.MPStarted = 0
        this.MPUsable = 0
        this.HMPStarted = 0
        this.HMPUsable = 0
        this.GMPStarted = 0
        this.GMPUsable = 0
        this.GHMPStarted = 0
        this.GHMPUsable = 0

        this.STerStarted = 0
        this.STerTotal = 0
        this.STerOnline = 0
        // 查询巡检子任务
        api.getInspectTask(this.taskid).then((res) => {
          console.log("巡检子任务结果反馈="+JSON.stringify(res))
          if(res.success==1){
            if (res.data.length > 0) {
              this.inspectTimes=res.data
              this.inspectTime=res.data[0].id
              this.getLicense()
            }
          }
        }).catch(error => {
          console.log(error)
        });
      },
      // License文件
      getLicense() {
        api.getInspectLicense(this.inspectTime).then((res) => {
          console.log("license信息： "+JSON.stringify(res))
          if(res.success==1){
            this.licenseList = res.data.license_list
            this.licenseFields = getLicenseFields()
            this.inspectionTotalPage = Math.ceil(res.data.max_page)
          }
        }).catch(error => {
          console.log(error)
        });
      },
      // 会议资源
      getResource() {
        api.getInspectResource(this.inspectTime).then((res) => {
          if (res.success == 1) {
            // AP接入端口
            this.APsStarted = KeepTwoNum(res.data.APsStarted)
            this.APsUsable = KeepTwoNum(res.data.APsUsable)
            this.APStarted = KeepTwoNum(res.data.APStarted)
            this.APUsable = KeepTwoNum(res.data.APUsable)
            this.GAPStarted = KeepTwoNum(res.data.GAPStarted)
            this.GAPUsable = KeepTwoNum(res.data.GAPUsable)
            // MP媒体端口
            this.MPsStarted = KeepTwoNum(res.data.MPsStarted)
            this.MPsUsable = KeepTwoNum(res.data.MPsUsable)
            this.MPStarted = KeepTwoNum(res.data.MPStarted)
            this.MPUsable = KeepTwoNum(res.data.MPUsable)
            this.HMPStarted = KeepTwoNum(res.data.HMPStarted)
            this.HMPUsable = KeepTwoNum(res.data.HMPUsable)
            this.GMPStarted = KeepTwoNum(res.data.GMPStarted)
            this.GMPUsable = KeepTwoNum(res.data.GMPUsable)
            this.GHMPStarted = KeepTwoNum(res.data.GHMPStarted)
            this.GHMPUsable = KeepTwoNum(res.data.GHMPUsable)
            // 软终端
            this.STerStarted = res.data.STerStarted
            this.STerTotal = res.data.STerTotal
            this.STerOnline = res.data.STerOnline
            // 直播会议
            this.LMStarted = res.data.LMStarted
            this.LMUsable = res.data.LMUsable
            this.HLSStarted = res.data.HLSStarted
            this.HLSUsable = res.data.HLSUsable
            this.ASFStarted = res.data.ASFStarted
            this.ASFUsable = res.data.ASFUsable
            // 录像室
            this.VRStarted = res.data.VRStarted
            this.VRUsable = res.data.VRUsable
            // 直播人数
            this.ViewersStarted = res.data.ViewersStarted
            this.ViewersUsable = res.data.ViewersUsable
            if (this.ViewersUsable > 0) {
              this.lv_show = true
            } else {
              this.lv_show = false
            }
            // 协作资源
            this.CRStarted = res.data.CRStarted
            this.CRPUsable = res.data.CRPUsable
            if (this.APsStarted == 0) {
              this.APsPercent = 0
            } else {
              this.APsPercent = parseInt(parseFloat(100 * this.APsStarted / (this.APsUsable + this.APsStarted)).toFixed(0))
            }
            if (this.MPsStarted == 0) {
              this.MPsPercent = 0
            } else {
              this.MPsPercent = parseInt(parseFloat(100 * this.MPsStarted / (this.MPsUsable + this.MPsStarted)).toFixed(0))
            }
            if (this.STerStarted == 0) {
              this.STerPercent = 0
            } else {
              this.STerPercent = parseInt(parseFloat(100 * this.STerStarted / (this.STerTotal)).toFixed(0))
            }
            if (this.LMStarted == 0) {
              this.LMPercent = 0
            } else {
              this.LMPercent = parseInt(parseFloat(100 * this.LMStarted / (this.LMUsable + this.LMStarted)).toFixed(0))
            }
            if (this.VRStarted == 0) {
              this.VRPercent = 0
            } else {
              this.VRPercent = parseInt(parseFloat(100 * this.VRStarted / (this.VRUsable + this.VRStarted)).toFixed(0))
            }
            if (this.ViewersStarted == 0) {
              this.ViewersPercent = 0
            } else {
              this.ViewersPercent = parseInt(parseFloat(100 * this.ViewersStarted / (this.ViewersUsable + this.ViewersStarted)).toFixed(0))
            }
            if (this.CRStarted == 0) {
              this.CRPercent = 0
            } else {
              this.CRPercent = parseInt(parseFloat(100 * this.CRStarted / (this.CRPUsable + this.CRStarted)).toFixed(0))
            }
          }
        }).catch(error => {
          console.log(error)
        });
      },
      // 服务器状态
      getServer() {
        api.getInspectServer(this.inspectTime).then((res) => {
          console.log("server信息： "+JSON.stringify(res))
          if(res.success==1){
            this.serverList = res.data.server_list
            this.serverFields = getServerFields(this.serDetail)
            this.inspectionTotalPage = Math.ceil(res.data.max_page)
          }
        }).catch(error => {
          console.log(error)
        });
      },
      serDetail: function(data) {
        this.$router.push({name: 'physicsdetail', params: {device_moid: data.device_moid,taskid: data.taskid}})
      },
      // 终端状态
      getTerminal() {
        api.getInspectTerminal(this.inspectTime).then((res) => {
          console.log("terminal信息： "+JSON.stringify(res))
          if(res.success==1){
            this.terminalList = res.data.terminal_list
            this.terminalListFields = getTerminalFields(this.terDetail)
            this.inspectionTotalPage = Math.ceil(res.data.max_page)
          }
        }).catch(error => {
          console.log(error)
        });
      },
      terDetail: function(data) {
        this.$router.push({name: 'terminaldetail', params: {device_moid: data.device_moid,taskid: data.taskid}})
      },
      // 删除
      deleteInspectResult: function () {
        this.childInspectTimes = []
        this.checkedInspectTimes = []
        this.checkAll = true
        if (this.inspectTimes.length > 0) {
          this.inspectTimes.forEach(i=>{
            this.childInspectTimes.push(i.start_time)
            this.checkedInspectTimes = this.childInspectTimes
          })
        }
        this.$refs.deleteInspectDialog.open()
      },
      handleCheckAllChange(val) {
        this.checkedInspectTimes = val ? this.childInspectTimes : [];
      },
      handleCheckedCitiesChange(value) {
        let checkedCount = value.length;
        this.checkAll = checkedCount === this.childInspectTimes.length;
      },
      OnSave: function () {
        console.log("this.checkedInspectTimes="+this.checkedInspectTimes)
        this.taskid_list = []
        this.inspectTimes.forEach(i=>{
          this.checkedInspectTimes.forEach(j=>{
            if (j == i.start_time) {
              this.taskid_list.push(i.id)
            }
          })
        })
        console.log("this.taskid_list="+this.taskid_list)
        api.delInspectChildTask(this.taskid_list).then((res) => {
          console.log("删除巡检子任务反馈信息： "+JSON.stringify(res))
          if (res.success == 1) {
            this.getChildrenInspectTask()
            this.reload()
          }
        }).catch(error => {
          console.log(error)
        });
      },
      OnCancel: function () {
        this.checkedInspectTimes = this.childInspectTimes
        this.checkAll = true
      },
      // 导出
      exportInspectResult: function () {
        api.downloadInspect({params:{taskid:this.taskid},responseType: 'blob'})
        .then((res) => {
          Upexcele(res, '巡检信息.xls')
        }).catch(error => {
          console.log(error)
        });
      },
      gotoPhysicsDetail: function (data) {
        console.log('gotoPhysicsDetail')
        this.$router.push({name: 'physicsdetail', params: { name: data.name,moid: data.moid}})
      },
    },
    watch: {
      inspectTime: function (newTaskId, oldTaskId) {
        this.tabType = 'license'
        this.inspectTime = newTaskId
        this.getLicense()
      },
      tabType: function (newTab, oldTab) {
        if (newTab === 'license') {
          this.getLicense()
        } else if (newTab === 'resource') {
          this.getResource()
        } else if (newTab === 'server') {
          this.getServer()
        } else if (newTab === 'terminal') {
          this.getTerminal()
        }
      },
      curPage: function (newPageNum, oldPageNum) {
        this.cage = 1
        if (this.tabType == "server") {
          api.getInspectServer(this.inspectTime,{params:{page:newPageNum}}).then((res) => {
            console.log("server信息： "+JSON.stringify(res))
            if(res.success==1){
              this.serverList = res.data.server_list
              this.serverFields = getServerFields(this.serDetail)
              this.serverTotalPage = Math.ceil(res.data.max_page)
            }
          }).catch(error => {
            console.log(error)
          });
        } else if (this.tabType == "terminal") {
          api.getInspectTerminal(this.inspectTime,{params:{page:newPageNum}}).then((res) => {
            console.log("terminal信息： "+JSON.stringify(res))
            if(res.success==1){
              this.terminalList = res.data.terminal_list
              this.terminalListFields = getTerminalFields(this.terDetail)
              this.terminalListTotalPage = Math.ceil(res.data.max_page)
            }
          }).catch(error => {
            console.log(error)
          });
        } else if (this.tabType == "license") {
          api.getInspectLicense(this.inspectTime,{params:{page:newPageNum}}).then((res) => {
            console.log("license信息： "+JSON.stringify(res))
            if(res.success==1){
              this.licenseList = res.data.license_list
              this.licenseFields = getLicenseFields()
              this.licenseTotalPage = Math.ceil(res.data.max_page)
            }
          }).catch(error => {
            console.log(error)
          });
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
ul {
  text-align: left;
  padding-bottom: 28px;
}
li {
    font-size: 12px;
    vertical-align: middle;
}
.grab-tab {
    font-size: 12px;
    padding-top: 6px;
    color: rgb(139, 139, 139);
    padding-right: 50px
}
.itemName {
    float: left;
    width: 79px;
}
.itemValue {
  color: #4e4e4e;
  display: inline-block;
}
.no-info-tip {
  float: left;
}
.el-checkbox + .el-checkbox {
    margin-left: 0px;
}
.textleft {
  text-align: left;
  padding: 0 0 0 62px;
  overflow-x: auto;
  max-height: 160px;
}
.el-checkbox {
  padding-bottom: 18px;
}
.el-checkbox__label {
  padding-left: 17px;
}
div.dlg-content[data-v-a8a6c15c] {
  padding-top: 28px;
}
.chart-circle{
  float: left;
  margin-top: 56px;
  width: 200px;
  height: 120px;
  margin-right: 106px;
}
.circle-block{
  width: 100px;
  height: 120px;
  float: left;
}
.circle-info{
  width: 100px;
  height: 120px;
  float: left;
}
.circle-title{
  padding-top: 11px;
  padding-bottom: 8px;
  font-size: 13px;
  width: 100%;
  text-align: left;
  color: #000000;
  margin-left: 12px;
}
h4 {
  float: left;
  font-size: 13px;
  font-weight: normal;
}
.el-button.is-circle {
    border-radius: 50%;
    padding: 0 4px;
}
.el-button {
    display: inline-block;
    line-height: 1;
    white-space: nowrap;
    cursor: pointer;
    background: #fff;
    border: 0px solid #dcdfe6;
    color: #606266;
    -webkit-appearance: none;
    text-align: center;
    -webkit-box-sizing: border-box;
    box-sizing: border-box;
    outline: 0;
    margin: 0;
    -webkit-transition: .1s;
    transition: .1s;
    font-weight: 500;
    padding: 0px 0px;
    font-size: 14px;
    border-radius: 4px;
}
.el-button:focus, .el-button:hover {
    color: #409eff;
    border-color: #c6e2ff;
    background-color: #ecf5ff;
}
.el-popover {
    padding: 8px;
}
.circle-detail{
  width: 140%;
  text-align: left;
  font-size: 11px;
  color: #8e8e8e;
  margin-left: 12px;
}
.circle-detail-block{
  padding-top: 6px;
  display: block;
}
.resource-list {
  float: left;
  width: 100%;
}
</style>
