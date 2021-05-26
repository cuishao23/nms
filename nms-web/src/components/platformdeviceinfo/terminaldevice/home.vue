<template>
  <el-tabs v-model="tabType">
    <el-tab-pane label="受管终端" name="controledterminal" style="text-align: left; padding-top: 20px;">
      <div>
        <div class="device-search" style="display: inline-block;">
          <ul>
            <li>
              <el-select v-model="tTerminalDomainMoid" placeholder="请选择" filterable>
                <el-option
                  v-for="(item,index) in tTerminalDomainMoids"
                  :key="index"
                  :label="item.name"
                  :value="item.moid">
                </el-option>
              </el-select>
            </li>
            <li>
              <el-select v-model="tUserMoid" placeholder="请选择" filterable>
                <el-option
                  v-for="(item,index) in tUserMoids"
                  :key="index"
                  :label="item.name"
                  :value="item.moid">
                </el-option>
              </el-select>
            </li>
            <li class="device-info-input">
              <el-input v-model="device_name" placeholder="设备名称、IP、E164号" class="filter-text" style="width:150px"></el-input>
            </li>
            <li class="device-info-button">
              <button class='search' @click="searchCtrlEquipment()"></button>
            </li>
          </ul>
        </div>
        <div class="device-search" style="float:right">
          <ul>
            <li style="padding-right: 5px">
              <button class="normal-btn" @click="onExport()">导出</button>
            </li>
            <li style="padding-right: 5px">
              <button class="normal-btn" :class="{disable: selections.length <= 0}" :disabled="selections.length <= 0" @click="restart()">重启</button>
            </li>
            <li style="padding-right: 0px;">
              <el-dropdown>
                <el-button class="normal-btn" :class="{disable: selections.length <= 0}" style="padding: 6px 10px 5px 17px;">更多<i class="el-icon-arrow-down el-icon--right"></i></el-button>
                <el-dropdown-menu slot="dropdown">
                  <el-dropdown-item><button class="normal-btns" :class="{disable: selections.length !== 1}" :disabled="selections.length !== 1" @click="onCfgVideoMode()">配置视频制式</button></el-dropdown-item>
                  <el-dropdown-item><button class="normal-btns" :class="{disable: selections.length <= 0}" :disabled="selections.length <= 0" @click="onCfgRegAddr()">配置注册地址</button></el-dropdown-item>
                  <el-dropdown-item><button class="normal-btns" :class="{disable: selections.length <= 0}" :disabled="selections.length <= 0" @click="onCfgNetwork()">配置网络参数</button></el-dropdown-item>
                </el-dropdown-menu>
              </el-dropdown>
            </li>
          </ul>
        </div>
      </div>
      <div v-if="ctrlTerminals.length === 0 && tlistFlash" class="no-info-tip">
        <span class="PromptImg"></span>
        <span>此用户域下没有终端设备</span>
      </div>
      <div v-if="ctrlTerminals.length > 0">
        <nms-pager-table :data="ctrlTerminals" :fields="ctrlFields" :total-page="ctrlTotalPages" :selection="true" v-model="curPage" :biao-zhi="cage"/>
      </div>
      <nms-dialog title="配置视频制式" ref="cfgVideoDlg" @confirm="sendConfigVideoMsg()">
        <div slot="content" class="cfg-reg-addr">
          <span>主流第一路输出制式</span>
            <el-select v-model="videoType" placeholder="请选择">
              <el-option
                  v-for="(item,index) in videoTypes"
                  :key="index"
                  :label="item.text"
                  :value="item.value">
              </el-option>
            </el-select>
        </div>
      </nms-dialog>
      <nms-dialog title="配置注册地址" ref="cfgRegAddr" @confirm="sendRegisterAdd()">
        <div slot="content" class="cfg-reg-addr">
          <span>注册平台地址</span><input v-model="deviceConfig" type="text" @blur="examineChange">
        </div>
      </nms-dialog>
      <nms-dialog title="配置网络参数" ref="cfgNetwork" width="560px" height="260px" @confirm="sendCfgNetwork()">
        <div slot="content" class="cfg-network">
          <el-row>
            <el-col :span="8"><span>丢包重传</span></el-col>
            <el-col :span="8"><el-radio v-model="pktLostResend" :label="1">开启</el-radio></el-col>
            <el-col :span="8"><el-radio v-model="pktLostResend" :label="0">关闭</el-radio></el-col>
          </el-row>
          <el-row>
            <el-col :span="8"><span>音频优先</span></el-col>
            <el-col :span="8"><el-radio v-model="audioFirst" :label="1">开启</el-radio></el-col>
            <el-col :span="8"><el-radio v-model="audioFirst" :label="0">关闭</el-radio></el-col>
          </el-row>
          <el-row>
            <el-col :span="8"><span>FEC</span></el-col>
            <el-col :span="8"><el-radio v-model="fec" :label="1">开启</el-radio></el-col>
            <el-col :span="8"><el-radio v-model="fec" :label="0">关闭</el-radio></el-col>
          </el-row>
          <el-row>
            <el-col :span="8"><span>强解/载荷自适应</span></el-col>
            <el-col :span="8"><el-radio v-model="decodePayloadAuto" :label="1">开启</el-radio></el-col>
            <el-col :span="8"><el-radio v-model="decodePayloadAuto" :label="0">关闭</el-radio></el-col>
          </el-row>
        </div>
      </nms-dialog>
      <nms-big-dialog title="提示" ref="rebootDialog" :width="'400px'" :height="'260px'" :close-btn="true" @confirm="onRestart()" @cancel="superPwd='',passwordError=false">
        <div slot="content" class="cfg-reg-addr">
          <el-input v-model="superPwd" placeholder="请输入密码" class="sup_text" type="password"></el-input>
          <div class="tip_text">
            <span v-show="!passwordError">注：你将要重启设备{{deviceIp}}。重启过程中请勿切断电源！</span>
            <span v-show="passwordError" style="color: red;">密码错误，请输入超级管理员密码</span>
          </div>
        </div>
      </nms-big-dialog>
      <nms-big-dialog title="提示" :width="'400px'" :height="'260px'" :close-btn="true" ref="recNet">
       <div slot="content">
         <div class="delTipsDiv">
            <span class="PromptImg"></span>
            <span>批量配置{{ warn_tip_name }}失败！</span>
         </div>
          <el-container style="height: 150px; padding-top: 10px;">
            <el-aside style="padding-left: 33px" width="">
              <span>失败终端</span>
            </el-aside>
            <el-main>
              <ul class="without-first-col" id="ter_num_list">
                <li class="ter-num" v-for="dev_name in deviceNames">{{dev_name}}设备</li>
              </ul>
            </el-main>
          </el-container>
         <div>
         </div>
       </div>
      </nms-big-dialog>
      <nms-big-dialog title="提示" :width="'400px'" :height="'260px'" :close-btn="false" ref="recVideo">
       <div slot="content">
         <div class="delTipsDiv" style="text-align: center; padding-top: 80px;">
            <span class="PromptImg"></span>
            <span>配置主流第一视频输出制式操作失败！</span>
            <span>请重新操作</span>
         </div>
       </div>
      </nms-big-dialog>
    </el-tab-pane>
    <el-tab-pane label="非受管终端" name="uncontroledterminal" style="text-align: left; padding-top: 20px;">
      <div>
        <div class="device-search" style="display: inline-block;">
          <ul>
            <li>
              <el-select v-model="tTerminalDomainMoid" placeholder="请选择" filterable>
                <el-option
                  v-for="(item,index) in tTerminalDomainMoids"
                  :key="index"
                  :label="item.name"
                  :value="item.moid">
                </el-option>
              </el-select>
            </li>
            <li>
              <el-select v-model="tUserMoid" placeholder="请选择" filterable>
                <el-option
                  v-for="(item,index) in tUserMoids"
                  :key="index"
                  :label="item.name"
                  :value="item.moid">
                </el-option>
              </el-select>
            </li>
            <li class="device-info-input">
              <el-input v-model="device_name_unctrl" placeholder="请输入设备IP、E164号" class="filter-text" style="width:150px"></el-input>
            </li>
            <li class="device-info-button">
              <button class='search' @click="searchUnCtrlEquipment()"></button>
            </li>
          </ul>
        </div>
      </div>
      <div v-if="unctrlTerminals.length === 0 && slistFlash" class="no-info-tip">
        <span class="PromptImg"></span>
        <span>该组下没有终端设备！</span>
      </div>
      <div v-if="unctrlTerminals.length > 0" class="unctrl-terminal">
        <nms-pager-table :data="unctrlTerminals" :fields="unctrlFields" :total-page="unctrlTotalPages" :biao-zhi="cage" v-model="curPage"/>
      </div>
    </el-tab-pane>
  </el-tabs>
</template>

<script>
  import {getUserDomainResInfo, getCtrlDeviceListFields, getUnCtrlDeviceListFields, videoTypes} from "../../../assets/js/platformdevice";
  import ResInfo from "../../common/res-info";
  import NmsPagesTable from "../../common/nms-pages-table";
  import NmsPagerTable from "../../common/nms-pager-table";
  import api from '../../../axios';
  import NmsDialog from "../../common/nms-dialog";
  import NmsBigDialog from "../../common/nms-big-dialog";
  import {onOpen, onClose} from "../../../ws/websock"
  import {Upexcele}  from '../../../common/commonFunction'
  import qs from 'qs';

  export default {
    components: {
      NmsDialog,
      ResInfo,
      NmsPagerTable,
      NmsPagesTable,
      NmsBigDialog},
    name: "terminal-device",
    data() {
      return {
        tabType: 'controledterminal',
        moid: '',

        perPage: 10, // 每页条数
        curPage: 1, // 当前页
        cage: 1,

        // 受管终端
        ctrlTerminals: [],
        ctrlTotalPages: 1,
        ctrlFields: [],
        // selections: [],
        device_name: '',
        tDeviceTypes: [],

        // 非受管终端
        unctrlTerminals: [],
        unctrlTotalPages: 1,
        unctrlFields: [],
        device_name_unctrl: '',

        // 视频模式配置
        videoType: '4K(3840x2160)_30fps',
        videoTypes: videoTypes,

        // 网络参数配置
        pktLostResend: 1,
        audioFirst: 1,
        fec: 1,
        decodePayloadAuto: 1,

        // 配置注册地址
        deviceConfig: '',

        // terminal
        tTerminalDomainMoids: [],
        tTerminalDomainMoid: '',
        tUserMoids: [],
        tUserMoid: '',
        tm: [],
        tu: [],

        warningUesrDomains: [],

        top_main: '',
        superPwd: '',
        passwordError: false,
        deviceIp: '',
        deviceMoid: '',
        deviceType: '',
        deviceNames: [],
        warn_tip_name: '',
        ws: null,
        slistFlash: false,
        tlistFlash: false,

        setData: {}
      }
    },
    created() {
        api.getTerminalTypeList().then((res) => {
          this.tDeviceTypes = [{
            text: '全部设备类型',
            value: 'all'
          }]
          for (var i = 0; i < res.data.length; i++) {
            let dic = {}
            dic["text"] = res.data[i]
            dic["value"] = res.data[i]
            this.tDeviceTypes.push(dic)
          }
        })
        api.getUserDomainTree().then((res) => {
          this.tTerminalDomainMoids = []
          this.tUserMoids = []
          this.tm = []
          this.tu = []
          this.warningUesrDomains = res.data
          this.warningUesrDomains.forEach(i => {
            if (i.type == "service" || i.type == "kernel") {
              this.tTerminalDomainMoids.push(i)
              this.tm.push(i)
              if (i.type == "kernel") {
                this.top_main = i.moid
              }
            } else if (i.type == "user") {
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
          this.getCtrTerminal()
      })
    },
    mounted() {
      this.initWebSocket()
    },
 
    methods: {
      onExport: function() {
        api.getTerminalsDownLoad({params: {deviceName: this.device_name, parentMoid: this.tUserMoid}, responseType: 'blob'}).then(res => {
          Upexcele(res, '受管终端列表信息.xls')
        }).catch(error => {
          console.log(error)
        });
      },
      examineChange: function() {
        if (this.deviceConfig !== '') {
            var ipv4Reg = /^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$/
            var ipv6Reg = /^(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))$/
            var ipv4Re = new RegExp(ipv4Reg)
            var ipv6Re = new RegExp(ipv6Reg)
            if (!ipv4Re.test(this.deviceConfig) && !ipv6Re.test(this.deviceConfig)) {
              this.errorDialog.open('地址格式不合理（须符合ipv4/ipv6格式）')
              this.deviceConfig = ''
            }
        }
      },
      gotoCtrlTerminalDetail: function(data) {
        this.$router.push({name: 'ctrlterminaldetail', params: {moid: data.moid, name: data.name, e164: data.e164}})
      },
      gotoUnctrlTerminalEdit: function (data) {
        this.$router.push({name: 'unctrlterminaledit', params: { id: data.id, ip: data.ip, name: data.name, type: data.type, moid: data.moid, e164: data.e164, version: data.version, online: parseInt(data.online) === 1 ? 'online' : 'offline' }})
      },
      gotoUnctrlTerminalWarning: function (data) {
        this.$router.push({name: 'unctrlterminalwarning', params: { ip: data.ip, version: data.version, name: data.name, type: data.type, moid: data.moid, e164: data.e164, online: parseInt(data.online) === 1 ? 'online' : 'offline' }})
      },
      onCfgVideoMode: function () {
        console.log('config video mode')
        this.$refs.cfgVideoDlg.open()
      },
      onCfgRegAddr: function () {
        console.log('config reg address')
        this.deviceConfig = ""
        this.$refs.cfgRegAddr.open()
      },
      onCfgNetwork: function () {
        console.log('config network')
        this.$refs.cfgNetwork.open()
      },
      succeccMsg: function() {
        this.$message({
          duration: 2000,
          center: true,
          message: '配置成功'
        })
      },
      sendRegisterAdd: function () {
        if (this.deviceConfig !== '') {
          this.sendRegisterAddMsg()
        } else {
          this.errorDialog.open('输入不能为空')
        }
      },
      // 配置网络参数消息
      sendCfgNetwork: function() {
        this.setData = {}
        this.setData["data"] = this.selections
        this.setData["pktLostResend"] = this.pktLostResend
        this.setData["audioFirst"] = this.audioFirst
        this.setData["fec"] = this.fec
        this.setData["decodePayloadAuto"] = this.decodePayloadAuto
        api.configTerminalNetwork(this.setData)
          // 成功返回
          .then(response => {
              console.log("配置网络参数结果反馈："+JSON.stringify(response));
              if (response.success == 0) {
                this.deviceNames = []
                for (var index in this.selections) {
                  this.deviceNames.push(this.selections[index].name)
                }
                this.warn_tip_name = "网络参数"
                console.log(this.warn_tip_name)
                this.$refs.recNet.open()
              } else if (response.success == 1) {
                this.succeccMsg()
              }
          })
        // 失败返回
        .catch(error => {
            console.log("failed" + error);
        })
      },
      // 配置注册地址消息
      sendRegisterAddMsg: function() {
        this.setData = {}
        this.setData["data"] = this.selections
        this.setData["deviceConfig"] = this.deviceConfig
        api.configTerminalRegAddr(this.setData)
          // 成功返回
          .then(response => {
              console.log("配置注册地址结果反馈：" + JSON.stringify(response));
              if (response.success == 0) {
                this.deviceNames = []
                for (var index in this.selections) {
                  this.deviceNames.push(this.selections[index].name)
                }
                this.warn_tip_name = "注册地址"
                this.$refs.recNet.open()
              } else if (response.success == 1) {
                this.succeccMsg()
              }
          })
        // 失败返回
        .catch(error => {
            console.log("failed" + error);
        })
      },
      // 配置视频制式
      sendConfigVideoMsg: function() {
        this.setData = {}
        this.setData["data"] = this.selections
        this.setData["deviceConfig"] = this.videoType
        api.configTerminalVideoFormat(this.setData)
          // 成功返回
          .then(response => {
              console.log("配置视频制式结果反馈：" + JSON.stringify(response));
              if (response.success == 0) {
                this.$refs.recVideo.open()
              } else if (response.success == 1) {
                this.succeccMsg()
              }
          })
        // 失败返回
        .catch(error => {
            console.log("failed" + error);
        })
      },
      searchUnCtrlEquipment: function() {
          api.getUncontroledTerminals({params: {parentMoid: this.tUserMoid, newPageNum: 1, deviceName: this.device_name_unctrl}}).then(res => {
            if (res.success == 1) {
              this.unctrlTerminals = res.data
              this.unctrlTotalPages = Math.ceil(res.total_num / this.perPage)
              this.unctrlFields = getUnCtrlDeviceListFields(this.gotoUnctrlTerminalEdit, this.gotoUnctrlTerminalWarning)
              this.cage = 2
            }
          })
          .catch((error) => {
            console.log(error);
          })
      },
      searchCtrlEquipment: function() {
        api.getControledTerminals({params: {
            deviceName: this.device_name,
            parentMoid: this.tUserMoid,
            page: 1
          }
        })
        .then((res) => {
          if (res.success == 1) {
            this.ctrlTerminals = res.data
            this.ctrlTotalPages = Math.ceil(res.total_num / this.perPage)
            this.ctrlFields = getCtrlDeviceListFields(this.gotoCtrlTerminalDetail)
            this.cage = 2
          }
        })
        .catch((error) => {
          console.log(error);
        });
      },
      getCtrTerminal: function() {
        api.getControledTerminals({params: {
            deviceName: this.device_name,
            parentMoid: this.tUserMoid,
            page: 1
          }
        })
        .then((res) => {
          if (res.success == 1) {
            if (res.total_num == 0) {
              this.tlistFlash = true
            } else {
              this.tlistFlash = false
            }
            this.ctrlTerminals = res.data
            this.ctrlTotalPages = Math.ceil(res.total_num / this.perPage)
            this.ctrlFields = getCtrlDeviceListFields(this.gotoCtrlTerminalDetail)
          }
        })
        .catch((error) => {
          console.log(error);
        });
      },
      restart: function () {
        this.$refs.rebootDialog.open()
      },
      onRestart() {
        let data = {
          devices: [],
          superPwd: this.superPwd
        }
        let error = false
        for (var index in this.selections) {
          let type_ter = this.selections[index].type_ter[0]
          if (type_ter) {
            data.devices.push({
              'deviceMoid': this.selections[index].moid,
              'deviceType': this.selections[index].type_ter[0]
            })
          } else {
            error = true
            break;
          }
        }
        if (error) {
          this.errorDialog.open('请选择在线终端')
        } else {
          console.log(data)
          this.sendRestart(data)
        }
      },
      // 重启操作消息
      sendRestart: function (data) {
        this.axios.post("/nms/device/rebootterminal", data)
          // 成功返回
          .then(response => {
              console.log("重启结果反馈：" + JSON.stringify(response));
              if (response.data.success == 1) {
                this.superPwd = ''
                console.log('success')
                this.passwordError = false
                this.errorDialog.open('设备重启中，预计5分钟...重启过程中，请勿切断电源！')
              } else if (response.data.success == 0) {
                if (response.data.error_code === 20400) {
                  this.passwordError = true
                  this.$refs.rebootDialog.open()
                } else {
                  this.superPwd = ''
                  this.errorDialog.open('重启失败!')
                }
              }
          })
        // 失败返回
        .catch(error => {
            console.log("failed" + error);
        })
      },
      // ws消息处理
      initWebSocket: function () {
        console.log('建立websocket连接')
        this.ws = api.getWebSocket();
        this.ws.onopen = onOpen
        this.ws.onmessage  = this.onMessage;
        this.ws.onerror = this.websocketonerror;
        this.ws.onclose = this.websocketclose;
      },
      websocketclose(evt){
        console.log(evt)
        console.log('ws断链重连')
        this.initWebSocket()
      },
      websocketonerror(evt){
        console.log(evt)
      },
      onMessage: function(evt) {
        console.log("ws消息处理 "+evt);
        console.log(evt.data);
        let data = JSON.parse(evt.data);
        let status = "";
        try {
          switch (data.eventid) {
            // begin 终端视频制式配置
            case "EV_CONFIG_1ST_VIDEO_FORMAT_NTF":
              if (data.result == 1) {
                this.simpleProgress.success();
              } else {
                this.errorDialog.open("终端视频制式配置失败");
              }
              break;
            // 终端视频制式配置 end

            // 终端注册地址配置 begin
            case "EV_CONFIG_REG_ADDR_NTF":
              if (data.result == 1) {
                this.simpleProgress.success();
              } else {
                this.errorDialog.open("终端注册地址配置失败");
              }
              break;
            // 终端注册地址配置 end

            // 终端网络配置 begin
            case "EV_CONFIG_NETWORK_NTF":
              if (data.result == 1) {
                this.simpleProgress.success();
              } else {
                this.errorDialog.open("终端注册地址配置失败");
              }
              break;
            // 终端网络配置 end
            default:
              break;
          }
        } catch (err) {
          console.warn(err);
        }
      }
    },
    computed: {
      selections: function() {
          return this.$store.state.terminal_selection_list
      }
    },
    watch: {
      tabType: function (newTab, oldTab) {
        if (newTab === 'controledterminal') {
            api.getControledTerminals({params:{
              deviceName: this.device_name,
              parentMoid: this.tUserMoid,
              page: 1
            }
          })
          .then((res) => {
            if (res.success == 1) {
              if (res.total_num == 0) {
                this.slistFlash = true
              } else {
                this.slistFlash = false
              }
              this.ctrlTerminals = res.data
              this.ctrlTotalPages = Math.ceil(res.total_num / this.perPage)
              this.ctrlFields = getCtrlDeviceListFields(this.gotoCtrlTerminalDetail)
              this.cage = 2
            }
          })
          .catch((error) => {
            console.log(error);
          });
        } else if (newTab === 'uncontroledterminal') {
          api.getUncontroledTerminals({params: {parentMoid: this.tUserMoid, newPageNum: 1, deviceName: this.device_name_unctrl}}).then(res => {
            console.log("非受管终端" + JSON.stringify(res))
            if (res.success == 1) {
              this.unctrlTerminals = res.data
              this.unctrlTotalPages = Math.ceil(res.total_num / this.perPage)
              this.unctrlFields = getUnCtrlDeviceListFields(this.gotoUnctrlTerminalEdit, this.gotoUnctrlTerminalWarning)
              this.cage = 2
            }
          })
          .catch((error) => {
            console.log(error);
          })
        }
      },
      curPage: function (newPageNum, oldPageNum) {
        if (this.tabType == 'controledterminal') {
          this.cage = 1
          api.getControledTerminals({params:{
              deviceName: this.device_name,
              parentMoid: this.tUserMoid,
              page: newPageNum
            }
          })
          .then((res) => {
            if (res.success == 1) {
              this.ctrlTerminals = res.data
              this.ctrlTotalPages = Math.ceil(res.total_num / this.perPage)
              this.ctrlFields = getCtrlDeviceListFields(this.gotoCtrlTerminalDetail)
            }
          })
          .catch((error) => {
            console.log(error);
          });
        } else if (this.tabType == 'uncontroledterminal') {
          this.cage = 1
          api.getUncontroledTerminals({params: {parentMoid: this.tUserMoid, newPageNum: newPageNum, deviceName: this.device_name_unctrl}}).then(res => {
            if (res.success == 1) {
              this.unctrlTerminals = res.data
              this.unctrlTotalPages = Math.ceil(res.total_num / this.perPage)
              this.unctrlFields = getUnCtrlDeviceListFields(this.gotoUnctrlTerminalEdit, this.gotoUnctrlTerminalWarning)
            }
          })
          .catch((error) => {
            console.log(error);
          })
        }
      },
      tTerminalDomainMoid: function (val) {
        if (val == "") {
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
          } else if (val == this.top_main) {
            this.tUserMoids = []
            this.tUserMoids = [].concat(this.tu)
            this.tUserMoids.unshift({
              "moid": "",
              "parent_moid": "",
              "name": "所有用户域",
              "type": "user"
            })
            this.tUserMoid = ""
          } else {
            this.tUserMoids = []
            this.tu.forEach(j => {
              if (val == j.parent_moid) {
                this.tUserMoids.push(j)
              }
            })
            if (this.tUserMoids.length == 0) {
              this.tUserMoids.unshift({
                "moid": "",
                "parent_moid": "",
                "name": "无下级域",
                "type": "user"
              })
            } else {
              this.tUserMoids.unshift({
                "moid": "",
                "parent_moid": "",
                "name": "所有用户域",
                "type": "user"
              })
            }
            this.tUserMoid = ""
          }
      }
    }
  }
</script>

<style scoped>
  .server > div:first-child > div:first-child {
    display: inline;
    float: left;
  }

  .device > ul{
    display: flex;
  }

  .unctrl-terminal {
    text-align: left;
  }

  .second {
    margin-right: 30px;
  }

  .el-col {
    text-align: left;
  }

  .el-row {
    margin-top: 20px;
    margin-bottom: 20px;
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

  .cfg-video {
    margin-left: 80px;
    margin-top: 60px;
    font-size: 14px;
  }

  .cfg-reg-addr input {
    margin-left: 30px;
  }

  .cfg-network {
    margin-left: 80px;
    margin-top: 60px;
  }

  .no-info-tip {
    text-align: center;
  }
  .el-filter {
    text-align: left;
  }

  .device-search {
    display: flex;
    /* padding-bottom: 10px; */
  }

  .device-search ul {
    display: flex;
  }
  .device-search li {
    padding-right: 15px;
  }
  .device-search ul .device-info-button {
    padding-left: 0px;
  }
  .device-search li .search {
  margin-left: 10px;
  }
  .normal-btns {
    font-size: 12px;
    line-height: 12px;
    /* color: #5f5f5f; */
    cursor: pointer;
    background-color: #eff2f4;
    border: 1px solid #dcdfe1;
    /* margin-right: 6px; */
    padding: 5px 21px 4px 21px;
  }
  .el-dropdown-menu__item {
    list-style: none;
    line-height: 36px;
    padding: 0 0px;
    margin: 0;
    font-size: 14px;
    color: #606266;
    cursor: pointer;
    outline: 0;
    /* height: 19px */
 }
 .el-dropdown-menu {
    position: absolute;
    top: 0;
    left: 0;
    padding: 0 0;
    margin: 5px 0;
    background-color: #fff;
    border: 1px solid #ebeef5;
    /* border-radius: 4px; */
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, .1);
 }
.el-button {
    border-radius: 0px;
}
.tip_text {
  position: absolute;
  width: 300px;
  padding-top: 20px;
}
.sup_text {
  width: 300px;
  padding-bottom: 50px;
  position: absolute;
}
.delTipsDiv {
  text-align: left;
  padding-top: 10px;
}
.el-main {
    display: block;
    -webkit-box-flex: 1;
    -ms-flex: 1;
    flex: 1;
    -ms-flex-preferred-size: auto;
    flex-basis: auto;
    box-sizing: border-box;
    padding: 0px 20px;
}
</style>
