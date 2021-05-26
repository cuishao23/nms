<template>
  <el-tabs v-model="tabType" style="cursor:pointer">
    <el-tab-pane label="诊断功能" name="diagnose" style="cursor:default">
      <div class="diagnose">
        <div class="diagnose-select">
          <span class="grab-tab">诊断对象</span>
          <el-select v-model="diagnoseObject" placeholder="诊断对象" class="grab-select" filterable>
            <el-option
              v-for="(item,index) in diagnoseObjects"
              :key="index"
              :label="item.text"
              :value="item.value"
            ></el-option>
          </el-select>
          <el-select
            v-model="sPlatformDomainMoid"
            placeholder="请选择"
            class="grab-select"
            v-show="machine"
            filterable
          >
            <el-option
              v-for="(item,index) in sPlatformDomainMoids"
              :key="index"
              :label="item.name"
              :value="item.moid"
            ></el-option>
          </el-select>
          <el-select
            v-model="sMachineRoomMoid"
            placeholder="请选择"
            class="grab-select"
            v-show="machine"
            filterable
          >
            <el-option
              v-for="(item,index) in sMachineRoomMoids"
              :key="index"
              :label="item.name"
              :value="item.moid"
            ></el-option>
          </el-select>
          <el-select v-model="ddeviceName" placeholder="请选择设备" class="grab-select" v-show="machine" filterable>
            <el-option
              v-for="(item,index) in ddeviceNames"
              :key="index"
              :label="item.text"
              :value="item.value"
            ></el-option>
          </el-select>
          <el-select
            v-model="tTerminalDomainMoid"
            placeholder="请选择"
            @change="tnodeClick"
            class="grab-select"
            v-show="user"
            filterable
          >
            <el-option
              v-for="(item,index) in tTerminalDomainMoids"
              :key="index"
              :label="item.name"
              :value="item.moid"
            ></el-option>
          </el-select>
          <el-select v-model="tUserMoid" placeholder="请选择" class="grab-select" v-show="user" filterable>
            <el-option
              v-for="(item,index) in tUserMoids"
              :key="index"
              :label="item.name"
              :value="item.moid"
            ></el-option>
          </el-select>
          <el-select v-model="dsdeviceName" placeholder="请选择设备" filterable class="grab-select" v-show="user" filterable>
            <el-option
              v-for="(item,index) in dsdeviceNames"
              :key="index"
              :label="item.text"
              :value="item.value"
            ></el-option>
          </el-select>
          <el-select v-model="tDeviceType" class="grab-select" filterable v-show="user" filterable>
            <el-option
              v-for="(item,index) in tDeviceTypes"
              :key="index"
              :label="item.text"
              :value="item.value"
            ></el-option>
          </el-select>
          <button class="normal-btn" @click="onStartDiagnose()" id="diagnosisFloat">诊断</button>
        </div>
        <div class="diagnose-time">
          <span class="grab-tab">诊断时间</span>
          <span class="grab-tab">{{diagnoseTime}}</span>
        </div>
        <div v-show="machine && !null_tip">
          <div style="float:top;">
            <base-diagnose-item title="内存使用率">
              <res-diagnose-item :total="total" :userate="userate" title="内存" />
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
            <base-diagnose-item title="CPU使用率" :style="height_style">
              <div class="res-chart" id="cpuChart"/>
            </base-diagnose-item>
          </div>
          <div>
            <base-diagnose-item title="网口吞吐量">
              <div class="res-chart_net" id="netChart" style="width: 820px; height: 410px"/>
            </base-diagnose-item>
          </div>
        </div>
        <div v-show="machine && null_tip" style="padding-top: 200px;">
          <span class="PromptImg"></span>
          <span>尚无诊断结果，请选择设备进行诊断</span>
        </div>
        <div v-show="user && !terminal_tip">
          <div class="terminal-type-detail">
            <div class="terminal-info">
              <nms-key-value label="终端名称" :value="terName" />
              <nms-key-value label="内存使用率" :value="memoryUsage" />
              <nms-key-value label="CPU使用率" :value="cpuRate" />
            </div>
            <div class="terminal-info">
              <nms-key-value label="终端状态" :value="terState" />
              <nms-key-value label="注册协议" :value="gvrp" />
              <nms-key-value label="所属域" :value="belongDomain" />
            </div>
            <div class="terminal-info">
              <nms-key-value label="主芯片状态" :value="chipStatus" />
              <nms-key-value label="编解码芯片" :value="codecChip" />
              <nms-key-value label="运行温度" :value="runningTemperature" />
            </div>
            <div class="terminal-info">
              <nms-key-value label="告警状态" :value="warningStatue" />
              <nms-key-value label="终端运行时长" :value="TerRunningTime" />
              <nms-key-value label="终端型号" :value="terType" />
            </div>
            <div class="terminal-info">
              <nms-key-value label="终端版本" :value="terVersion" />
              <nms-key-value label="终端序列号" :value="terSn" />
            </div>
          </div>
          <div>
            <div v-if="peripherals.length>0">
              <div class="in_line">
                <span class="setName">外设状态</span>
              </div>
              <nms-pages-table :data="peripherals" :fields="peripheralFields" :pager="false"/>
            </div>
            <div v-if="privideos.length>0">
              <div class="in_line">
                <span class="setName">第一路主视频</span>
              </div>
              <nms-pages-table :data="privideos" :fields="privideosFields" :pager="false" :index="false"/>
            </div>
            <div v-if="privideos.length>0">
              <div class="in_line">
                <span class="setName">第一路辅视频</span>
              </div>
              <nms-pages-table :data="assvideos" :fields="assvideosFields" :pager="false" :index="false"/>
            </div>
          </div>
        </div>
        <div v-show="user && terminal_tip" style="padding-top: 200px;">
          <span class="PromptImg"></span>
          <span>尚无诊断结果，请选择设备进行诊断</span>
        </div>
      </div>
    </el-tab-pane>
    <el-tab-pane label="抓包功能" name="grabbag" style="cursor:default">
      <div class="grab">
        <div class="grab-search">
          <span class="grab-tab">抓包对象</span>
          <el-select v-model="grabObject" placeholder="对象类型" class="grab-select" filterable>
            <el-option
              v-for="(item,index) in grabObjects"
              :key="index"
              :label="item.text"
              :value="item.value"
            ></el-option>
          </el-select>
          <el-select
            v-model="gplatformDomain"
            placeholder="全部平台域"
            class="grab-select"
            v-show="gmachine"
            filterable
          >
            <el-option
              v-for="(item,index) in gplatformDomains"
              :key="index"
              :label="item.name"
              :value="item.moid"
            ></el-option>
          </el-select>
          <el-select
            v-model="gmachineRoom"
            placeholder="默认机房"
            class="grab-select"
            v-show="gmachine"
            filterable
          >
            <el-option
              v-for="(item,index) in gmachineRooms"
              :key="index"
              :label="item.name"
              :value="item.moid"
            ></el-option>
          </el-select>
          <el-select v-model="serverName" placeholder="请选择设备" class="grab-select" v-show="gmachine" filterable>
            <el-option
              v-for="(item,index) in serverNames"
              :key="index"
              :label="item.text"
              :value="item.value"
            ></el-option>
          </el-select>
          <el-select v-model="devicePort" placeholder="请选择网口" class="grab-select" v-show="gmachine" filterable>
            <el-option
              v-for="(item,index) in devicePorts"
              :key="index"
              :label="item.text"
              :value="item.value"
            ></el-option>
          </el-select>
          <el-select
            v-model="gTerminalDomainMoid"
            placeholder="请选择"
            @change="tnodeClick"
            class="grab-select"
            v-show="guser"
            filterable
          >
            <el-option
              v-for="(item,index) in gTerminalDomainMoids"
              :key="index"
              :label="item.name"
              :value="item.moid"
            ></el-option>
          </el-select>
          <el-select v-model="gUserMoid" placeholder="请选择" class="grab-select" v-show="guser" filterable>
            <el-option
              v-for="(item,index) in gUserMoids"
              :key="index"
              :label="item.name"
              :value="item.moid"
            ></el-option>
          </el-select>
          <el-select v-model="gdeviceName" placeholder="请选择设备" class="grab-select" filterable v-show="guser">
            <el-option
              v-for="(item,index) in gdeviceNames"
              :key="index"
              :label="item.text"
              :value="item.value"
            ></el-option>
          </el-select>
          <el-select v-model="gtdeviceType" placeholder="请选择类型" class="grab-select" v-show="guser" filterable>
            <el-option
              v-for="(item,index) in gtdeviceTypes"
              :key="index"
              :label="item.text"
              :value="item.value"
            ></el-option>
          </el-select>
          <el-select v-model="gdevicePort" placeholder="请选择网口" class="grab-select" v-show="guser" filterable>
            <el-option
              v-for="(item,index) in gdevicePorts"
              :key="index"
              :label="item.text"
              :value="item.value"
            ></el-option>
          </el-select>
          <button class="add-btn" @click="onAddDeviceList()" />
        </div>
        <div class="grab-msg">
          <span class="msg">抓包对象列表</span>
          <span class="msg">
            开始时间
            <span class="obj">{{ grab_start_time }}</span>
          </span>
          <span class="msg">
            抓包状态
            <span class="obj">{{ grab_state===1?'正在抓包':'' }}</span>
          </span>
          <button
            class="normal-btn"
            :class="{disable: grabObjectList.length == 0}"
            :disabled="grabObjectList.length == 0"
            @click="onStartGrabList()"
            id="grabStartFloat"
          >{{ grab_state===0? '开始抓包':'停止抓包' }}</button>
          <nms-dialog
            title="提示"
            :width="'400px'"
            :height="'152px'"
            :close-btn="true"
            ref="startGrabDialog"
            @confirm="OnGrabStart()"
          >
            <div slot="content">
              <div class="delTipsDiv">
                <span class="PromptImg"></span>
                <span>{{grab_state===0 ? '确认开始抓包?':'确认停止抓包?'}}</span>
              </div>
            </div>
          </nms-dialog>
        </div>
        <div class="grab-list" :style="{'pointer-events': grab_state == 1 ? 'none' : ''}">
          <dia-pages-table
            v-if="deviceReset"
            :selection="true"
            :data="grabObjectList"
            :fields="grabObjectFields"
            :pager="false"
            v-model="multiSelect"
            :disable-flag="grab_state"
          />
          <div slot="content" v-if="grabObjectList.length == 0">
            <div class="delTipsDiv">
              <span class="PromptImg"></span>
              <span>尚无抓包内容，请先添加设备进行抓包</span>
            </div>
          </div>
          <nms-dialog
            title="提示"
            :width="'400px'"
            :height="'152px'"
            :close-btn="true"
            ref="grabDeleteDialog"
            @confirm="OnGrabDeviceDelete()"
          >
            <div slot="content">
              <div class="delTipsDiv">
                <span class="PromptImg"></span>
                <span>确认删除该抓包对象？</span>
              </div>
            </div>
          </nms-dialog>
          <nms-dialog
            title="编辑"
            :width="'400px'"
            :height="'152px'"
            :close-btn="true"
            ref="grabeEditDialog"
            @confirm="OnGrabDeviceEdit()"
          >
            <div class="textleft" slot="content">
              <div class="fontCommon">
                <span class="modifyCommon">抓包对象</span>
                <span class="backNamePathCommon">{{ detailLineData.device_name }}</span>
              </div>
              <div class="fontCommon">
                <span class="modifyCommon">抓包类型</span>
                <span
                  v-if="detailLineData.device_category=='server'"
                  class="backNamePathCommon"
                >{{ detailLineData.device_type }}</span>
                <input
                  v-else-if="detailLineData.device_category=='terminal'"
                  type="text"
                  class="backNamePathCommon"
                  placeholder
                  v-model="obj_type"
                />
              </div>
              <div class="fontCommon">
                <span class="modifyCommon" style="float: left;">抓包网口</span>
                <el-select v-model="obj_netcard" placeholder="请选择网口" class="grab-select" v-show="detailLineData.device_category=='server'">
                  <el-option
                    v-for="(item,index) in devicePorts"
                    :key="index"
                    :label="item.text"
                    :value="item.value"
                  ></el-option>
                </el-select>
                <el-select v-model="gdevicePort" placeholder="请选择网口" class="grab-select" v-show="detailLineData.device_category=='terminal'">
                  <el-option
                    v-for="(item,index) in gdevicePorts"
                    :key="index"
                    :label="item.text"
                    :value="item.value"
                  ></el-option>
                </el-select>
              </div>
            </div>
          </nms-dialog>
        </div>
        <div class="grab-msg">
          <span class="msg">抓包文件列表</span>
          <button
            class="normal-btn"
            :class="{disable: selections.length == 0}"
            :disabled="selections.length == 0"
            @click="onDeleteFileList()"
            id="grabDeleteFloat"
          >删除文件</button>
          <nms-dialog
            title="提示"
            :width="'400px'"
            :height="'152px'"
            :close-btn="true"
            ref="grabFileDeleteDialog"
            @confirm="OnGrabFileDelete()"
          >
            <div slot="content">
              <div class="delTipsDiv">
                <span class="PromptImg"></span>
                <span>确认删除所选抓包文件？</span>
              </div>
            </div>
          </nms-dialog>
        </div>
        <div class="grab-list-last">
          <nms-pager-table
            v-if="fileReset"
            :selection="true"
            :data="grabFileList"
            :fields="grabFileFields"
            @multiSelect="getSeletRow"
            :perPage="5"
            :total-page="grapTotalPage"
            :biao-zhi="cage"
            v-model="curPage"
          />
          <div slot="content" v-if="grabFileList.length == 0">
            <div class="delTipsDiv">
              <span class="PromptImg"></span>
              <span>尚无抓包文件内容，抓包成功后可查看</span>
            </div>
          </div>
        </div>
      </div>
    </el-tab-pane>
    <el-tab-pane label="日志获取" name="getlog" style="cursor:default">
      <div class="log">
        <div class="grab-search">
          <span class="grab-tab">日志对象</span>
          <el-select v-model="logObject" placeholder="诊断对象" class="grab-select" filterable>
            <el-option
              v-for="(item,index) in logObjects"
              :key="index"
              :label="item.text"
              :value="item.value"
            ></el-option>
          </el-select>
          <el-select
            v-model="lTerminalDomainMoid"
            placeholder="请选择"
            @change="tnodeClick"
            class="grab-select"
            v-show="luser"
            filterable
          >
            <el-option
              v-for="(item,index) in lTerminalDomainMoids"
              :key="index"
              :label="item.name"
              :value="item.moid"
            ></el-option>
          </el-select>
          <el-select v-model="lUserMoid" placeholder="请选择" class="grab-select" v-show="luser" filterable>
            <el-option
              v-for="(item,index) in lUserMoids"
              :key="index"
              :label="item.name"
              :value="item.moid"
            ></el-option>
          </el-select>
          <el-select v-model="ldeviceName" placeholder="请选择设备" class="grab-select" filterable v-show="luser">
            <el-option
              v-for="(item,index) in ldeviceNames"
              :key="index"
              :label="item.text"
              :value="item.value"
            ></el-option>
          </el-select>
          <el-select v-model="ldeviceType" placeholder="请选择类型" class="grab-select" filterable v-show="luser">
            <el-option
              v-for="(item,index) in ldeviceTypes"
              :key="index"
              :label="item.text"
              :value="item.value"
            ></el-option>
          </el-select>
          <button
            class="normal-btn"
            style="float:left"
            @click="downloadTerLog()"
            v-show="luser"
            id="diagnosisFloat"
          >下载日志</button>
          <el-select
            v-model="lPlatformDomainMoid"
            placeholder="请选择"
            class="grab-select"
            v-show="lmachine"
            filterable
          >
            <el-option
              v-for="(item,index) in lPlatformDomainMoids"
              :key="index"
              :label="item.name"
              :value="item.moid"
            ></el-option>
          </el-select>
          <el-select
            v-model="lMachineRoomMoid"
            placeholder="请选择"
            class="grab-select"
            v-show="lmachine"
            filterable
          >
            <el-option
              v-for="(item,index) in lMachineRoomMoids"
              :key="index"
              :label="item.name"
              :value="item.moid"
            ></el-option>
          </el-select>
          <el-select
            v-model="lphysicalName"
            placeholder="请选择"
            class="grab-select"
            v-show="lmachine"
            filterable
          >
            <el-option
              v-for="(item,index) in lphysicalNames"
              :key="index"
              :label="item.text"
              :value="item.value"
            ></el-option>
          </el-select>
          <el-select v-model="logicalName" placeholder="请选择" class="grab-select" filterable v-show="lmachine">
            <el-option
              v-for="(item,index) in logicalNames"
              :key="index"
              :label="item.text"
              :value="item.value"
            ></el-option>
          </el-select>
          <button class="search" id="logSearchFloat" @click="searchServerLog()" v-show="lmachine"></button>
        </div>
        <div class="grab-msg" v-show="lmachine">
          <span class="msg">日志对象列表</span>
          <button
            class="normal-btn"
            id="logDownFloat"
            :class="{disable: logFileList.length == 0}"
            :disabled="logFileList.length == 0"
            @click="downloadSerLog()"
            v-show="lmachine"
          >下载</button>
        </div>
        <div class="log-list" v-show="lmachine" v-if="logFileList.length > 0">
          <nms-pages-table
            :selection="true"
            :data="logFileList"
            :fields="logFileFields"
            :total-page="logTotalPage"
            :biao-zhi="cage"
            v-model="curPageLog"
          />
        </div>
        <div slot="content" v-if="logFileList.length == 0">
          <div class="delTipsDiv">
            <span class="PromptImg"></span>
            <span>尚无日志数据项</span>
          </div>
        </div>
      </div>
    </el-tab-pane>
  </el-tabs>
</template>

<script>
import api from "../../../axios";
import mapState from "vuex";
import NmsPagerTable from "../../common/nms-pager-table";
import NmsPagesTable from "../../common/nms-pages-table";
import DiaPagesTable from "../../common/dia-pages-table";
import NmsDialog from "../../common/nms-dialog";
import BaseDiagnoseItem from "../base-diagnose-item";
import ResDiagnoseItem from "../res-diagnose-item";
import ResInfoItem from "../res-info-item";
import NmsKeyValue from "../../common/nms-key-value";
import {onOpen, onClose} from "../../../ws/websock";
import {Upexcele}  from '../../../common/commonFunction';
import {FormatTime, TERMINAL_RES, TERMINAL_VIDEO_FORMAT, TERMINAL_AUDIO_FORMAT} from '../../../assets/js/common';
import {
  drawMeetingEcharts,
  getTypeListByPhysicals,
  getTypeListByLogicals,
  getPhysicalDeviceListFields,
  getLogicalDeviceListFields,
  getPlatformResInfo,
  meetingDomainMoids
} from "../../../assets/js/platformdevice";
import {
  drawEcharts,
  drawNetEcharts,
  getLogFileFields,
  tServiceDomainMoids,
  getGrabFileFields,
  getGrabObjectFields,
  gettServiceDomainMoids,
  getsServiceDomainMoids,
  sVirtualMachines,
  getTerminalDiagnosticsFields,
  getMeetingFields,
  getServerFields,
  setMyOption,
  getPeripheralFields,
  getPrivideosFields,
  getAssvideosFields
} from "../../../assets/js/diagnose";
export default {
  components: {
    NmsPagesTable,
    NmsPagerTable,
    DiaPagesTable,
    NmsDialog,
    BaseDiagnoseItem,
    ResDiagnoseItem,
    ResInfoItem,
    NmsKeyValue
  },
  name: "diagnosisdevice",
  inject: ["reload"],
  data() {
    return {
      diagnoseObject: "server",
      diagnoseObjects: [
        { value: "server", text: "服务器" },
        { value: "terminal", text: "终端" }
      ],
      device_name: "",

      DomainTree: [],
      grabObject: "server",
      grabObjects: [
        { value: "server", text: "服务器" },
        { value: "terminal", text: "终端" }
      ],
      logObject: "server",
      logObjects: [
        { value: "server", text: "服务器" },
        { value: "terminal", text: "终端" }
      ],
      seviceDomains: [],
      seviceDomain: "",
      platformDomains: [],
      platformDomain: "",
      machineRooms: [],
      machineRoom: "",
      // deviceTypes: [],
      // deviceType: '',
      devicePorts: [],
      devicePort: "any",
      tabType: "diagnose",
      diagnosisTotalPage: 1, // 总页数

      grabObjectList: [],
      grabObjectFields: [],
      grabFileList: [],
      grabFileFields: [],
      grab_start_time: "",
      // grab_state: 0: 未开始抓包, 1: 正在抓包
      grab_state: 0,
      detailLineData: {},
      obj_type: "",
      old_obj_type: "",
      obj_netcard: "",
      old_obj_netcard: "",
      selectRow: "",
      deviceTotalNum: 0, // 设备总数
      fileTotalNum: 0, // 文件总数
      grapTotalPage: 1, // 总页数
      curPage: 1, // 当前页
      cage: 1, // 搜索当前页归1标志符 置二归一
      perPage: 5, // 表格每页显示数量
      deviceReset: true,
      fileReset: true,
      // log
      logFileList: [],
      logFileFields: getLogFileFields(),

      // 诊断抓包
      machine: true,
      user: false,
      diagnoseTime: "",
      diaDomains: [],
      sPlatformDomainMoid: "",
      sPlatformDomainMoids: [],
      sMachineRoomMoid: "",
      sMachineRoomMoids: [],
      diskData: [],
      total: 0,
      userate: 0,
      ddeviceName: "",
      ddeviceNames: [],
      dserInfo: [],
      dterDeviceMoid: "",
      type_ser: "",
      dserDeviceMoid: "",

      tTerminalDomainMoid: "",
      tTerminalDomainMoids: [],
      tUserMoid: "",
      tUserMoids: "",
      tDeviceType: "",
      tDeviceTypes: [],
      top_main: "",
      tm: [],
      tu: [],
      dsdeviceName: "",
      dsdeviceNames: [],
      dterInfo: [],
      dterTypeList: [],

      terName: "",
      memoryUsage: "",
      cpuRate: "",
      terState: "",
      gvrp: "",
      belongDomain: "",
      chipStatus: "",
      codecChip: "",
      runningTemperature: "",
      warningStatue: "",
      TerRunningTime: "",
      terType: "",
      terVersion: "",
      terSn: "",

      peripherals: [],
      peripheralFields: getPeripheralFields(),
      privideos: [],
      privideosFields: getPrivideosFields(),
      assvideos: [],
      assvideosFields: getAssvideosFields(),

      // 抓包功能
      gmachine: true,
      guser: false,
      gplatformDomain: "",
      gplatformDomains: [],
      gmachineRoom: "",
      gmachineRooms: [],
      p: [],
      m: [],
      serverName: "",
      serverNames: [],
      serverInfo: [],
      gserDeviceMoid: "",
      gsDeviceType: "",
      gsDeviceTypes: [],

      gTerminalDomainMoid: "",
      gTerminalDomainMoids: [],
      gUserMoid: "",
      gUserMoids: [],
      gdeviceName: "",
      gdeviceNames: [],
      gtdeviceType: "",
      gtdeviceTypes: [],
      gdevicePort: "any",
      gdevicePorts: [],
      terInfo: [],
      gterDeviceMoid: "",

      dev_moid: "",
      dev_type: "",
      dev_category: "",
      dev_card: "",
      fileID: "",

      multiSelect: [],
      file_name: "",
      // 日志获取
      logDir: "",

      lPlatformDomainMoid: "",
      lPlatformDomainMoids: [],
      lMachineRoomMoid: "",
      lMachineRoomMoids: [],
      lphysicalName: "",
      lphysicalNames: [],
      lphysicalType: "",
      lphysicalTypes: [],
      logicalName: "",
      logicalNames: [],
      logicalLists: [],
      logicalMoid: "",

      lTerminalDomainMoid: "",
      lTerminalDomainMoids: [],
      lUserMoid: "",
      lUserMoids: [],
      ldeviceName: "",
      ldeviceNames: [],
      ldeviceType: "",
      ldeviceTypes: [],
      lTerDevMoid: "",
      lTerInfo: [],

      logTotalPage: 1,
      logPerPage: 10,
      logSerInfo: [],
      logSerDeviceMoid: "",
      rowselections: [],
      lmachine: true,
      luser: false,
      ws: null,
      curPageLog: 1,

      null_tip: true,
      terminal_tip: true,
      logFileName: "",

      height_style: {
        height: ""
      },
      filest: [],
      tem_list: []
    };
  },
  created() {
    // diagnose server name
    this.ddeviceNames = [
      {
        text: "请选择设备",
        value: ""
      }
    ];
    // phisical device type
    api.getPhysicalTypeList().then(res => {
      console.log("服务器设备" + JSON.stringify(res));
      this.lphysicalTypes = [
        {
          text: "请选择设备类型",
          value: ""
        }
      ];
      this.gsDeviceTypes = [
        {
          text: "请选择设备类型",
          value: ""
        }
      ];
      if (res.data != "{}") {
        for (var i = 0; i < res.data.length; i++) {
          let dic = {};
          dic["text"] = res.data[i];
          dic["value"] = res.data[i];
          this.lphysicalTypes.push(dic);
          this.gsDeviceTypes.push(dic);
        }
      }
    });
    // phisical name
    this.serverNames = [
      {
        text: "请选择设备",
        value: ""
      }
    ];
    // phisical internet accesss
    this.devicePorts = [
      {
        text: "全部网口",
        value: "any"
      }
    ];
    // d ter names
    this.dsdeviceNames = [
      {
        text: "请选择设备",
        value: ""
      }
    ];
    // terminal names
    this.gdeviceNames = [
      {
        text: "请选择设备",
        value: ""
      }
    ];
    // terminal types
    this.deviceTypes = [
      {
        text: "请选择类型",
        value: ""
      }
    ];
    // terminal internet accesss
    this.gdevicePorts = [
      {
        text: "全部网口",
        value: "any"
      }
    ];
    // log phisical name
    this.lphysicalNames = [
      {
        text: "请选择设备",
        value: ""
      }
    ];
    // log phisical type
    // log terminal name
    this.ldeviceNames = [
      {
        text: "请选择设备",
        value: ""
      }
    ];
    this.logicalNames = [
      {
        text: "请选择业务模块",
        value: ""
      }
    ];
    // log terminal type
    // phisical machine room
    api.getPlatformDomainTree().then(res => {
      this.sPlatformDomainMoids = [];
      this.gplatformDomains = [];
      this.lPlatformDomainMoids = [];
      this.sMachineRoomMoids = [];
      this.gmachineRooms = [];
      this.lMachineRoomMoids = [];
      this.p = [];
      this.m = [];
      this.diaDomains = res.data;
      this.diaDomains.forEach(i => {
        if (i.type == "platform") {
          this.sPlatformDomainMoids.push(i);
          this.gplatformDomains.push(i);
          this.lPlatformDomainMoids.push(i);
          this.p.push(i);
        } else if (i.type == "machine_room") {
          this.sMachineRoomMoids.push(i);
          this.gmachineRooms.push(i);
          this.lMachineRoomMoids.push(i);
          this.m.push(i);
        }
      });
      // diagnose
      this.sPlatformDomainMoids.unshift({
        moid: "",
        parent_moid: "",
        name: "所有平台域",
        type: "platform"
      });
      this.sMachineRoomMoids.unshift({
        moid: "",
        parent_moid: "",
        name: "所有虚拟机房",
        type: "machine_room"
      });
      this.sPlatformDomainMoid = "";
      this.sMachineRoomMoid = "";
      // capture package
      this.gplatformDomains.unshift({
        moid: "",
        parent_moid: "",
        name: "所有平台域",
        type: "platform"
      });
      this.gmachineRooms.unshift({
        moid: "",
        parent_moid: "",
        name: "所有虚拟机房",
        type: "machine_room"
      });
      this.gplatformDomain = "";
      this.gmachineRoom = "";
      // log
      this.lPlatformDomainMoids.unshift({
        moid: "",
        parent_moid: "",
        name: "所有平台域",
        type: "platform"
      });
      this.lMachineRoomMoids.unshift({
        moid: "",
        parent_moid: "",
        name: "所有虚拟机房",
        type: "machine_room"
      });
      this.lPlatformDomainMoid = "";
      this.lMachineRoomMoid = "";
    });
    this.getDiaDeviceName();
    // terminal device type
    this.tDeviceTypes = [
      {
        text: "请选择设备类型",
        value: ""
      }
    ];
    this.ldeviceTypes = [
      {
        text: "请选择设备类型",
        value: ""
      }
    ];
    this.gtdeviceTypes = [
      {
        text: "请选择设备类型",
        value: ""
      }
    ];
    // terminal user
    api.getUserDomainTree().then(res => {
      this.tTerminalDomainMoids = [];
      this.gTerminalDomainMoids = [];
      this.lTerminalDomainMoids = [];
      this.tUserMoids = [];
      this.gUserMoids = [];
      this.lUserMoids = [];
      this.tm = [];
      this.tu = [];
      this.warningUesrDomains = res.data;
      this.warningUesrDomains.forEach(i => {
        if (i.type == "service" || i.type == "kernel") {
          this.tTerminalDomainMoids.push(i);
          this.gTerminalDomainMoids.push(i);
          this.lTerminalDomainMoids.push(i);
          this.tm.push(i);
          if (i.type == "kernel") {
            this.top_main = i.moid;
          }
        } else if (i.type == "user") {
          this.tUserMoids.push(i);
          this.gUserMoids.push(i);
          this.lUserMoids.push(i);
          this.tu.push(i);
        }
      });
      // diagnose
      this.tTerminalDomainMoids.unshift({
        moid: "",
        parent_moid: "",
        name: "所有服务域",
        type: "server"
      });
      this.tUserMoids.unshift({
        moid: "",
        parent_moid: "",
        name: "所有用户域",
        type: "user"
      });
      this.tTerminalDomainMoid = "";
      this.tUserMoid = "";
      // capture package
      this.gTerminalDomainMoids.unshift({
        moid: "",
        parent_moid: "",
        name: "所有服务域",
        type: "server"
      });
      this.gUserMoids.unshift({
        moid: "",
        parent_moid: "",
        name: "所有用户域",
        type: "user"
      });
      this.gTerminalDomainMoid = "";
      this.gUserMoid = "";
      // log get
      this.lTerminalDomainMoids.unshift({
        moid: "",
        parent_moid: "",
        name: "所有服务域",
        type: "server"
      });
      this.lUserMoids.unshift({
        moid: "",
        parent_moid: "",
        name: "所有用户域",
        type: "user"
      });
      this.lTerminalDomainMoid = "";
      this.lUserMoid = "";
    });
  },
  mounted: function() {
    this.initWebSocket()
  },
  computed: {
    selections: function() {
      return this.$store.state.terminal_selection_list
    }
  },
  methods: {
    // 诊断
    getDiaDeviceName: function() {
      this.ddeviceName = "";
      this.ddeviceNames = [];
      this.ddeviceNames = [
        {
          text: "请选择设备",
          value: ""
        }
      ];
      api
        .getOnlineServer({ params: { parentMoid: this.sMachineRoomMoid } })
        .then(res => {
          console.log("诊断服务器设备名结果反馈" + JSON.stringify(res));
          if (res.data != "{}" && res.success == 1) {
            this.dserInfo = res.data;
            for (var i = 0; i < res.data.length; i++) {
              let dic = {};
              dic["text"] = res.data[i]["name"];
              dic["value"] = res.data[i]["name"];
              this.ddeviceNames.push(dic);
            }
          }
        });
    },
    getDiaTerDevName: function() {
      this.dsdeviceName = "";
      this.dsdeviceNames.splice(1, this.dsdeviceNames.length - 1);
      this.tDeviceType = "";
      this.tDeviceTypes.splice(1, this.tDeviceTypes.length - 1);
      api
        .getOnlineTerminal({ params: { parentMoid: this.tUserMoid } })
        .then(res => {
          console.log("终端诊断参数列表" + JSON.stringify(res));
          if (res.data != "[]") {
            this.dterInfo = res.data;
            for (var i = 0; i < res.data.length; i++) {
              let dic_name = {};
              dic_name["text"] = res.data[i]["name"];
              dic_name["value"] = res.data[i]["name"];
              this.dsdeviceNames.push(dic_name);
            }
          }
        });
    },
    // 当前添加的抓包对象
    getAddGInfo: function() {
      api.getCaptureDevice().then(res => {
        if (res.success == 1) {
          this.grabObjectList = res.data;
          this.deviceTotalNum = res.total_num;
          this.grabObjectFields = getGrabObjectFields(
            this.grabEdit,
            this.grabDelete
          );
        }
      });
    },
    getGDevSerName: function() {
      this.serverName = "";
      this.serverNames = [];
      this.serverNames = [
        {
          text: "请选择设备",
          value: ""
        }
      ];
      api
        .getOnlineServer({ params: { parentMoid: this.gmachineRoom } })
        .then(res => {
          console.log("服务器设备名、网口" + JSON.stringify(res));
          if (res.data != "{}") {
            this.serverInfo = res.data;
            for (var i = 0; i < res.data.length; i++) {
              let dic = {};
              dic["text"] = res.data[i]["name"];
              dic["value"] = res.data[i]["name"];
              this.serverNames.push(dic);
            }
          }
        });
    },
    getGTerName: function() {
      this.gdeviceName = "";
      this.gdeviceNames.splice(1, this.gdeviceNames.length - 1);
      this.gtdeviceType = "";
      this.gtdeviceTypes.splice(1, this.gtdeviceTypes.length - 1);
      api
        .getOnlineTerminal({ params: { parentMoid: this.gUserMoid } })
        .then(res => {
          console.log("终端抓包参数列表" + JSON.stringify(res));
          if (res.data != "[]") {
            this.terInfo = res.data;
            for (var i = 0; i < res.data.length; i++) {
              let dic_name = {};
              dic_name["text"] = res.data[i]["name"];
              dic_name["value"] = res.data[i]["name"];
              this.gdeviceNames.push(dic_name);
            }
          }
        });
    },
    // 日志
    getLTerName: function() {
      this.ldeviceName = "";
      this.ldeviceNames.splice(1, this.ldeviceNames.length - 1);
      api
        .getOnlineTerminal({ params: { parentMoid: this.lUserMoid } })
        .then(res => {
          if (res.data != "[]") {
            this.lTerInfo = res.data;
            for (var i = 0; i < res.data.length; i++) {
              let dic_name = {};
              dic_name["text"] = res.data[i]["name"];
              dic_name["value"] = res.data[i]["name"];
              this.ldeviceNames.push(dic_name);
            }
          }
        });
    },
    getLSerName: function() {
      this.lphysicalName = "";
      this.lphysicalNames.splice(1, this.lphysicalNames.length - 1);
      api
        .getOnlineServer({ params: { parentMoid: this.lMachineRoomMoid } })
        .then(res => {
          console.log("lMachineRoomMoid=" + JSON.stringify(res));
          if (res.data != "{}" && res.success == 1) {
            this.logSerInfo = res.data;
            for (var i = 0; i < res.data.length; i++) {
              let dic = {};
              dic["text"] = res.data[i]["name"];
              dic["value"] = res.data[i]["name"];
              this.lphysicalNames.push(dic);
            }
          }
        });
    },
    onStartDiagnose: function() {
      if (this.dsdeviceName == "" && this.diagnoseObject == "terminal") {
        this.errorDialog.open("请选择一个设备!")
      } else if (this.ddeviceName == "" && this.diagnoseObject == "server") {
        this.errorDialog.open("请选择一个设备!")
      } else if (this.tDeviceType == "" && this.diagnoseObject == "terminal") {
        this.errorDialog.open("请选择一个类型!")
      } else {
        // 开始诊断时间
        this.diagnoseTime = ""
        this.diagnoseTime = FormatTime(new Date());
        if (this.diagnoseObject == "server") {
          api
            .diagnoseServer({
              params: {
                deviceMoid: this.dserDeviceMoid,
              }
            })
            .then(res => {
              console.log("服务器诊断反馈结果" + JSON.stringify(res));
              if(res.success==1){
                this.null_tip = false
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
              } else {
                this.null_tip = true
              }
            });
        } else if (this.diagnoseObject == "terminal") {
          api
            .diagnoseTerminal({
              deviceMoid: this.dterDeviceMoid,
              deviceType: this.tDeviceType
            })
            .then(res => {
              console.log("终端诊断反馈结果" + JSON.stringify(res));
              this.terminal_tip = false
              if (res.error_code == 20500) {

                this.errorDialog.open("诊断失败，（手机端不支持诊断或者终端内部错误）！")
                this.memoryUsage = "",
                this.cpuRate = "",
                this.terType = "",
                this.chipStatus = "",
                this.runningTemperature = "",
                this.gvrp = "",
                this.TerRunningTime = "",
                this.codecChip = "",
                this.terName = "",
                this.terState = "",
                this.belongDomain = "",
                this.terVersion = "",
                this.terSn = "",
                this.warningStatue = "",
                this.peripherals = [],
                this.privideos = [],
                this.assvideos = []
              } else {
                this.termianl_tip = true
              }
            });
        }
      }
    },
    // terminal
    tnodeClick: function() {
      var t_selected_val = this.tServiceDomainMoid;
      if (
        t_selected_val === "allservicedomains" ||
        t_selected_val === "kedacom"
      ) {
        this.tUserDomainMoid = "alluserdomains";
      }
    },
    gotoServerDiagnosisDetail: function(data) {
      console.log(" moid: " + data.moid);
      this.$router.push({
        name: "serverdiagnosisdetail",
        params: { moid: data.moid, name: data.name }
      });
    },
    gotoDiagnoseDetail: function(data) {
      console.log(" moid: " + data.moid);
      this.$router.push({
        name: "diagnosedetail",
        params: { moid: data.moid }
      });
    },
    // 添加抓包设备
    onAddDeviceList: function() {
      if (this.serverName == "" && this.grabObject == "server") {
        this.errorDialog.open("请选择一个设备!")
      } else if (this.gdeviceName == "" && this.grabObject == "terminal") {
        this.errorDialog.open("请选择一个设备!")
      } else if (this.gtdeviceType == "" && this.grabObject == "terminal") {
        this.errorDialog.open("请选择一个类型!")
      } else {
        if (this.grab_state === 1) {
          this.errorDialog.open("请先结束抓包");
        } else if (this.deviceTotalNum >= 5) {
          this.errorDialog.open("抓包对象已满5条，请先删除后重试");
        } else {
          if (this.grabObject == "server") {
            var deviceCategory = this.grabObject;
            var deviceMoid = this.gserDeviceMoid;
            var netcard = this.devicePort;
            var deviceType = this.gsDeviceType;
          } else if (this.grabObject == "terminal") {
            var deviceCategory = this.grabObject;
            var deviceMoid = this.gterDeviceMoid;
            var netcard = this.gdevicePort;
            var deviceType = this.gtdeviceType;
          }
          console.log("deviceCategory=" + this.grabObject);
          console.log("deviceMoid=" + this.gserDeviceMoid);
          console.log("netcard=" + this.devicePort);
          console.log("deviceType=" + this.gsDeviceType);
          api
            .addCaptureDevice({
              deviceCategory: deviceCategory,
              deviceMoid: deviceMoid,
              netcard: netcard,
              deviceType: deviceType
            })
            .then(res => {
              console.log("添加抓包设备反馈=" + JSON.stringify(res));
              if (res.success == 1) {
                api.getCaptureDevice().then(res => {
                  if (res.success == 1) {
                    this.grabObjectList = res.data;
                    this.deviceTotalNum = res.total_num;
                    this.grabObjectFields = getGrabObjectFields(
                      this.grabEdit,
                      this.grabDelete
                    );
                  }
                });
              } else if (res.success == 2) {
                this.errorDialog.open("抓包对象重复!")
              } else {
                this.errorDialog.open("添加抓包设备!")
              }
            });
        }
      }
    },
    // 跳转编辑设备弹框
    grabEdit: function(rowData) {
      console.log("rowData=" + JSON.stringify(rowData));
      this.devicePorts.splice(1, this.devicePorts.length - 1);
      for (var i = 0; i < this.serverInfo.length; i++) {
        if (this.serverInfo[i]["name"] == rowData.device_name) {
          if (this.serverInfo[i]["netcards"] != "{}") {
            for (var j = 0; j < this.serverInfo[i]["netcards"].length; j++) {
              let dicp = {};
              dicp["text"] = this.serverInfo[i]["netcards"][j];
              dicp["value"] = this.serverInfo[i]["netcards"][j];
              this.devicePorts.push(dicp);
            }
          }
        }
      }
      this.obj_type = rowData.device_type;
      this.obj_netcard = rowData.netcard;
      if (rowData.device_category == "server") {
        this.devicePort = this.obj_netcard
      } else {
        this.gdevicePort = this.obj_netcard
      }
      this.detailLineData = rowData;
      this.$refs.grabeEditDialog.open();
    },
    // 编辑设备函数
    OnGrabDeviceEdit: function() {
      console.log("obj_type=" + this.obj_type);
      console.log("obj_netcard=" + this.obj_netcard);
      api
        .setCaptureDevice({
          deviceID: this.detailLineData.id,
          deviceType: this.obj_type,
          netcard: this.obj_netcard
        })
        .then(res => {
          api.getCaptureDevice().then(res => {
            this.grabObjectList = res.data;
            this.deviceTotalNum = res.total_num;
            this.grabObjectFields = getGrabObjectFields(
              this.grabEdit,
              this.grabDelete
            );
          });
          console.log(res);
        })
        .catch(error => {
          console.log(error);
        });
    },
    // 跳转删除设备弹框
    grabDelete: function(rowData) {
      this.detailLineData = rowData;
      this.$refs.grabDeleteDialog.open();
    },
    // 删除设备函数
    OnGrabDeviceDelete: function() {
      api
        .deleteCaptureDevice({ deviceID: this.detailLineData.id })
        .then(res => {
          api.getCaptureDevice().then(res => {
            this.grabObjectList = res.data;
            this.deviceTotalNum = res.total_num;
            this.grabObjectFields = getGrabObjectFields(
              this.grabEdit,
              this.grabDelete
            );
            this.deviceReset = false;
            this.$nextTick(() => {
              this.deviceReset = true;
            });
          });
        })
        .catch(error => {
          console.log(error);
        });
    },
    // 跳转开始抓包弹框
    onStartGrabList: function() {
      if (this.multiSelect.length > 0) {
        if ((this.fileTotalNum + this.multiSelect.length) > 15) {
          this.errorDialog.open("抓包文件已满15条，请先删除后重试");
          return;
        } else {
          this.$refs.startGrabDialog.open()
        }
      } else {
        this.errorDialog.open("请先选择抓包对象!");
      }
    },
    // 开始抓包函数
    OnGrabStart: function() {
      if (this.grab_state === 0) {
        console.log("当前添加的抓包对象列表" + JSON.stringify(this.multiSelect));
        for (let i = 0; i < this.multiSelect.length; i++) {
          this.dev_moid = this.multiSelect[i].device_moid;
          this.dev_type = this.multiSelect[i].device_type;
          this.dev_category = this.multiSelect[i].device_category;
          this.dev_card = this.multiSelect[i].netcard;
          this.startCaught();
        }
      } else if (this.grab_state === 1) {
        for (let i = 0; i < this.multiSelect.length; i++) {
          this.dev_moid = this.multiSelect[i].device_moid;
          this.dev_type = this.multiSelect[i].device_type;
          this.dev_category = this.multiSelect[i].device_category;
          this.endCaught();
        }
      }
    },
    startCaught: function() {
      api
        .startCaptureDevice({
          deviceMoid: this.dev_moid,
          deviceType: this.dev_type,
          deviceCategory: this.dev_category,
          netcard: this.dev_card
        })
        .then(res => {
          console.log("开始抓包结果反馈 " + JSON.stringify(res));
          if (res.success === 1) {
            this.grab_start_time = FormatTime(new Date());
            this.grab_state = 1;
          } else {
            this.updateCaptureStatus(this.dev_moid, "开始抓包消息发送失败");
            this.grab_start_time = "";
            this.grab_state = 0;
          }
        });
    },
    endCaught: function() {
      api
        .stopCaptureDevice({
          deviceMoid: this.dev_moid,
          deviceType: this.dev_type,
          deviceCategory: this.dev_category,
        })
        .then(res => {
          console.log("结束抓包结果反馈 " + JSON.stringify(res));
          if (res.success === 1) {
            this.grab_state = 0;
            this.successDialog.open("抓包成功");
            this.grab_start_time = ""
          } else {
            this.grab_state = 1;
            this.updateCaptureStatus(this.dev_moid, "停止抓包消息发送失败");
            this.grab_start_time = ""
          }
        });
    },
    // 文件选择函数
    getSeletRow: function(data) {
      if (this.selectRow === data) {
        this.selectRow = "";
      } else {
        this.selectRow = data;
      }
    },
    getCaptureFileInfo: function() {
      api.getCaptureFile({ params: { newPageNum: 1 } }).then(res => {
        console.log("获取抓包文件信息结果反馈： " + JSON.stringify(res));
        if (res.success == 1) {
          this.grabFileList = res.data;
          this.grapTotalPage = Math.ceil(res.total_num / this.perPage);
          if (this.grapTotalPage == 0) {
            this.grapTotalPage = 1
          }
          this.fileTotalNum = res.total_num;
          this.grabFileFields = getGrabFileFields(this.grabdownload);
          this.fileReset = false;
          this.$nextTick(() => {
            this.fileReset = true;
          });
        }
      });
    },
    // 跳转删除文件弹框
    onDeleteFileList: function() {
      this.$refs.grabFileDeleteDialog.open();
    },
    // 删除文件函数
    OnGrabFileDelete: function() {
      for (let i = 0; i < this.selections.length; i++) {
        this.fileID = this.selections[i].id;
        this.deleteGrabFileInfo();
      }
    },
    deleteGrabFileInfo: function() {
      api
        .deleteCaptureFile({ fileID: this.fileID })
        .then(res => {
          if (res.success == 1) {
            api.getCaptureFile({ params: { newPageNum: 1 } }).then(res => {
              this.grabFileList = res.data;
              this.grapTotalPage = Math.ceil(res.total_num / this.perPage);
              if (this.grapTotalPage == 0) {
                this.grapTotalPage = 1
              }
              this.fileTotalNum = res.total_num;
              this.grabFileFields = getGrabFileFields(this.grabdownload);
              this.selectRow = "";
              this.cage = 2;
              this.fileReset = false;
              this.$nextTick(() => {
                this.fileReset = true;
              });
            });
          }
        })
        .catch(error => {
          console.log(error);
        });
    },
    // 抓包文件下载
    grabdownload: function(rowData) {
      this.file_name = rowData.file_name;
      api.getDownloadCaptureFile( rowData.device_moid, this.file_name)
    },
    // 日志文件下载
    downloadLogFun: function (devid) {
      if (this.logFileName !== "") {
        this.logFileName = this.logFileName.split("/").pop()
      }
      this.simpleProgress.success()
      api.getDownloadCaptureFile(devid, this.logFileName)
    },
    // 日志获取
    searchServerLog: function() {
      this.tem_list = []
      if (this.lphysicalName == "") {
        this.errorDialog.open("请选选择一个设备!")
      } else if (this.logicalName == "") {
        this.errorDialog.open("请先选择一个业务模块!")
      } else {
        api
          .getCaptureLog({
            deviceMoid: this.logSerDeviceMoid,
            deviceType: this.lphysicalType,
            logType: this.logicalName
          })
          .then(res => {
            console.log("日志获取结果反馈" + JSON.stringify(res));
            if (res.success === 1) {
              this.logDir = res.logDir
              this.simpleProgress.open("正在获取日志列表，请稍后...", "", 500);
            } else {
              this.errorDialog.open("获取日志信息失败");
            }
          })
          .catch(error => {
            console.log(error);
          });
      }
    },
    downloadTerLog: function() {
      // 终端日志下载
      if (this.ldeviceName == "") {
        this.errorDialog.open("请选择一个设备!")
      } else if (this.ldeviceType == "") {
        this.errorDialog.open("请选择一个类型!")
      } else {
        api
          .getDownloadCaptureLog({
            deviceMoid: this.lTerDevMoid,
            deviceType: this.ldeviceType,
            deviceCategory: "terminal"
          })
          .then(res => {
            console.log("下载终端抓包日志结果反馈" + JSON.stringify(res));
            if (res.success == 1) {
              this.simpleProgress.open("正在下载日志文件，请等待...", "", 500);
            } else {
              this.errorDialog.open("日志文件下载失败");
            }
          })
          .catch(error => {
            console.log(error);
          });
      }
    },
    downloadSerLog: function() {
      var temFilrLists= []
      var temFilrList = ""
      this.selections.forEach(item => {
        temFilrList = item.dir+item.name
        temFilrLists.push(temFilrList)
      })
      api
        .getDownloadCaptureLog({
          deviceMoid: this.logSerDeviceMoid,
          deviceType: this.lphysicalType,
          fileList: temFilrLists,
          deviceCategory: "server"
        })
        .then(res => {
          console.log("下载服务器抓包日志结果反馈" + JSON.stringify(res));
          if (res.success == 1) {
            this.simpleProgress.open("正在下载日志文件，请等待...", "", 500);
          } else {
            this.errorDialog.open("日志文件下载失败");
          }
        })
        .catch(error => {
          console.log(error);
        });
    },
    updateCaptureStatus(device_moid, status) {
      for (let i = 0; i < this.grabObjectList.length; i++) {
        if (this.grabObjectList[i]["device_moid"] === device_moid) {
          let info = this.grabObjectList[i];
          info.status = status;
          this.grabObjectList.splice(i, 1, info);
        }
      }
    },
    // ws消息处理
    initWebSocket: function () {
      this.ws = api.getWebSocket();
      this.ws.onopen = onOpen
      this.ws.onmessage  = this.onMessage;
      this.ws.onerror = this.websocketonerror;
      this.ws.onclose = this.websocketclose;
    },
    websocketclose(evt){
      console.log(evt)
      console.log('ws 断链重连')
      this.initWebSocket()
    },
    websocketonerror(evt){
      console.log(evt)
    },
    onMessage(evt) {
      console.log("ws消息处理 "+evt);
      console.log(evt.data);
      let data = JSON.parse(evt.data);
      let status = "";
      try {
        switch (data.eventid) {
          // begin 抓包消息
          case "EV_PACKETCAPTURE_START_ACK":
            // 抓包开始成功
            this.updateCaptureStatus(data.devid, "正在抓包");
            break;
          case "EV_PACKETCAPTURE_START_NACK":
            // 抓包开始失败
            this.updateCaptureStatus(data.devid, "抓包失败");
            break;
          case "EV_PACKETCAPTURE_STOP_ACK":
            // 抓包停止成功
            this.updateCaptureStatus(data.devid, "抓包成功，请等待文件上传");
            break;
          case "EV_PACKETCAPTURE_STOP_NACK":
            // 抓包停止失败
            this.updateCaptureStatus(data.devid, "抓包失败");
            break;
          case "EV_PACKETCAPTURE_UPLOAD_PROGRESS_NTF":
            // 抓包进度
            if (data.progress < 0) {
              status = "文件上传失败";
            } else if (data.progress == 100) {
              status = "文件上传成功";
              this.getCaptureFileInfo();
            } else {
              status = "文件上传进度" + data.progress + "%";
            }
            this.updateCaptureStatus(data.devid, status);
            break;
          // 抓包消息 end

          // 日志消息 begin
          case "EV_GETLOG_LIST_ACK":
            // 日志列表成功
            this.simpleProgress.success();
            this.tem_list = this.tem_list.concat(data.file_list)
            if (data.file_count <= this.tem_list.length) {
              this.tem_list.sort(function(a,b){
                return Date.parse(b.ctime) - Date.parse(a.ctime); // 时间倒序
              });
              this.filest = JSON.parse(JSON.stringify(this.tem_list)); // 拷贝数据
              this.logFileList = this.tem_list;
              this.logTotalPage = Math.ceil(this.logFileList.length / this.logPerPage);
            }
            break;
          case "EV_GETLOG_NACK":
            if (data.reasoncode == 2) {
              this.simpleProgress.close();
              this.errorDialog.open("日志上传失败，文件服务器错误");
              // 日志列表失败
            } else if (data.reasoncode == -1) {
              this.simpleProgress.close();
              this.errorDialog.open("日志上传失败");
            }
            break;
          case "EV_GETLOG_ACK":
            // 日志下载地址
            this.logFileName = data.url
            break;
          case "EV_LOG_UPLOAD_PROGRESS_NTF":
            // 日志上传进度
            if (data.reasoncode < 0) {
              this.simpleProgress.close();
              this.errorDialog.open("上传日志文件失败");
            } else {
              if (data.progress == 100) {
                this.logFileName = data.url
                this.downloadLogFun(data.devid)
              }
            }
            break;
          // 日志消息 end

          // 终端诊断消息 begin
          case "EV_PFMINFO_MSG":
            // 清空上次残留数据
            this.memoryUsage = "",
            this.cpuRate = "",
            this.terType = "",
            this.chipStatus = "",
            this.runningTemperature = "",
            this.gvrp = "",
            this.TerRunningTime = "",
            this.codecChip = "",
            this.terName = "",
            this.terState = "",
            this.belongDomain = "",
            this.terVersion = "",
            this.terSn = "",
            this.warningStatue = "",
            this.peripherals = [],
            this.privideos = [],
            this.assvideos = []
            // 终端性能消息成功
            this.simpleProgress.success();
            this.memoryUsage = data.pfm_info.mem_userate,
            this.cpuRate = data.pfm_info.cpu_userate,
            this.terType = data.devtype,
            this.chipStatus = data.pfm_info.master_chip_status,
            this.runningTemperature = data.pfm_info.temperature_status,
            this.gvrp = data.pfm_info.reg_protocol,
            this.TerRunningTime = data.pfm_info.run_time,
            this.codecChip = data.pfm_info.code_chip,
            // 剩余终端性能信息
            api.getTerminalPerformance({params:{
                deviceMoid: data.devid,
                devType: data.devtype
              }
            })
            .then((res) => {
              if (res.success == 1) {
                this.terName = res.data.name,
                this.terState = res.data.online_state,
                this.belongDomain = res.data.domain_name,
                this.terVersion = res.data.version,
                this.terSn = res.data.SN,
                this.warningStatue = res.data.warning_status
              }
            })
            .catch((error) => {
              console.log(error);
            });
            // 外设状态
            if (data.pfm_info.peripherals) {
              this.peripherals = data.pfm_info.peripherals
            } else {
              this.peripherals = []
            }
            // 第一路主视频
            let privideos_list = []
            let privideoSend = {}
            let privideoRecv = {}
            if (data.pfm_info.hasOwnProperty("privideo_send")) {
              if (data.pfm_info.privideo_send.length > 0) {
                // 主视频上行
                privideoSend = data.pfm_info.privideo_send[0]
                for (let key in privideoSend) {
                  if (key == "video_up_bitrate") {
                    privideoSend["video_up_down_bitrate"] = privideoSend[key]
                    delete privideoSend[key]
                  } else if (key == "format") {
                    if (privideoSend[key] == null) {
                      privideoSend["video_format"] = privideoSend[key]
                    } else {
                      privideoSend["video_format"] = TERMINAL_VIDEO_FORMAT[privideoSend[key]]
                    }
                    delete privideoSend[key]
                  } else if (key == "enc_start") {
                    privideoSend["video_codec_start"] = privideoSend[key]
                    delete privideoSend[key]
                  } else if (key == "hw_enc_status") {
                    privideoSend["hw_codec_status"] = privideoSend[key]
                    delete privideoSend[key]
                  } else if (key == "res" && privideoSend[key] !== null) {
                    privideoSend["res"] = TERMINAL_RES[privideoSend[key]]
                  }
                }
                privideoSend["up"] = "上行"
              }
            }
            // 音频上行
            if (data.pfm_info.hasOwnProperty("audio_send")) {
              if (data.pfm_info.audio_send.length > 0) {
                if (data.pfm_info.audio_send[0]["format"] == null) {
                  privideoSend["audio_format"] = data.pfm_info.audio_send[0]["format"]
                } else {
                  privideoSend["audio_format"] = TERMINAL_AUDIO_FORMAT[data.pfm_info.audio_send[0]["format"]]
                }
                privideoSend["audio_pkts_lose"] = data.pfm_info.audio_send[0]["audio_pkts_lose"]
                privideoSend["audio_pkts_loserate"] = data.pfm_info.audio_send[0]["audio_pkts_loserate"]
                privideoSend["audio_up_down_bitrate"] = data.pfm_info.audio_send[0]["audio_up_bitrate"]
                privideoSend["audio_codec_start"] = data.pfm_info.audio_send[0]["enc_start"]
              }
            }
            if (JSON.stringify(privideoSend) !== '{}') {
              privideos_list.push(privideoSend)
            }

            if (data.pfm_info.hasOwnProperty("privideo_recv")) {
              if (data.pfm_info.privideo_recv.length > 0) {
                // 主视频下行
                privideoRecv = data.pfm_info.privideo_recv[0]
                for (let key in privideoRecv) {
                  if (key == "video_down_bitrate") {
                    privideoRecv["video_up_down_bitrate"] = privideoRecv[key]
                    delete privideoRecv[key]
                  } else if (key == "format") {
                    if (privideoRecv[key] == null) {
                      privideoRecv["video_format"] = privideoRecv[key]
                    } else {
                      privideoRecv["video_format"] = TERMINAL_VIDEO_FORMAT[privideoRecv[key]]
                    }
                    delete privideoRecv[key]
                  } else if (key == "dec_start") {
                    privideoRecv["video_codec_start"] = privideoRecv[key]
                    delete privideoRecv[key]
                  } else if (key == "hw_dec_status") {
                    privideoRecv["hw_codec_status"] = privideoRecv[key]
                    delete privideoRecv[key]
                  } else if (key == "res" && privideoRecv[key] !== null) {
                    privideoRecv["res"] = TERMINAL_RES[privideoRecv[key]]
                  }
                }
                privideoRecv["up"] = "下行"
              }
            }
            // 音频下行
            if (data.pfm_info.hasOwnProperty("audio_recv")) {
              if (data.pfm_info.audio_recv.length > 0) {
                if (data.pfm_info.audio_recv[0]["format"] == null) {
                  privideoRecv["audio_format"] = data.pfm_info.audio_recv[0]["format"]
                } else {
                  privideoRecv["audio_format"] = TERMINAL_AUDIO_FORMAT[data.pfm_info.audio_recv[0]["format"]]
                }
                privideoRecv["audio_pkts_lose"] = data.pfm_info.audio_recv[0]["audio_pkts_lose"]
                privideoRecv["audio_pkts_loserate"] = data.pfm_info.audio_recv[0]["audio_pkts_loserate"]
                privideoRecv["audio_up_down_bitrate"] = data.pfm_info.audio_recv[0]["audio_down_bitrate"]
                privideoRecv["audio_codec_start"] = data.pfm_info.audio_recv[0]["dec_start"]
              }
            }
            if (JSON.stringify(privideoRecv) !== '{}') {
              privideos_list.push(privideoRecv)
            }
            this.privideos = privideos_list
            console.log("privideos="+JSON.stringify(this.privideos))

            // 第一路辅视频
            let assvideos_list = []
            let assvideoSend = {}
            let assvideoRecv = {}
            if (data.pfm_info.hasOwnProperty("assvideo_send")) {
              if (data.pfm_info.assvideo_send.length > 0) {
                // 辅视频上行
                assvideoSend = data.pfm_info.assvideo_send[0]
                for (let key in assvideoSend) {
                  if (key == "video_up_bitrate") {
                    assvideoSend["video_up_down_bitrate"] = assvideoSend[key]
                    delete assvideoSend[key]
                  } else if (key == "format") {
                    if (assvideoSend[key] == null) {
                      assvideoSend["video_format"] = assvideoSend[key]
                    } else {
                      assvideoSend["video_format"] = TERMINAL_VIDEO_FORMAT[assvideoSend[key]]
                    }
                    delete assvideoSend[key]
                  } else if (key == "enc_start") {
                    assvideoSend["video_codec_start"] = assvideoSend[key]
                    delete assvideoSend[key]
                  } else if (key == "hw_enc_status") {
                    assvideoSend["hw_codec_status"] = assvideoSend[key]
                    delete assvideoSend[key]
                  } else if (key == "res" && assvideoSend[key] !== null) {
                    assvideoSend["res"] = TERMINAL_RES[assvideoSend[key]]
                  }
                }
                assvideoSend["up"] = "上行"
              }
            }
            if (JSON.stringify(assvideoSend) !== '{}') {
              assvideos_list.push(assvideoSend)
            }

            if (data.pfm_info.hasOwnProperty("assvideo_recv")) {
              if (data.pfm_info.assvideo_recv.length > 0) {
                // 辅视频下行
                assvideoRecv = data.pfm_info.assvideo_recv[0]
                for (let key in assvideoRecv) {
                  if (key == "video_down_bitrate") {
                    assvideoRecv["video_up_down_bitrate"] = assvideoRecv[key]
                    delete assvideoRecv[key]
                  } else if (key == "format") {
                    if (assvideoRecv[key] == null) {
                      assvideoRecv["video_format"] = assvideoRecv[key]
                    } else {
                      assvideoRecv["video_format"] = TERMINAL_VIDEO_FORMAT[assvideoRecv[key]]
                    }
                    delete assvideoRecv[key]
                  } else if (key == "dec_start") {
                    assvideoRecv["video_codec_start"] = assvideoRecv[key]
                    delete assvideoRecv[key]
                  } else if (key == "hw_dec_status") {
                    assvideoRecv["hw_codec_status"] = assvideoRecv[key]
                    delete assvideoRecv[key]
                  } else if (key == "res" && assvideoRecv[key] !== null) {
                    assvideoRecv["res"] = TERMINAL_RES[assvideoSend[key]]
                  }
                }
                assvideoRecv["up"] = "下行"
              }
            }
            if (JSON.stringify(assvideoRecv) !== '{}') {
              assvideos_list.push(assvideoRecv)
            }
            this.assvideos = assvideos_list
            console.log("assvideos="+JSON.stringify(this.assvideos))
            break;
          case "EV_PFMINFO_NACK":
            // 终端性能消息失败回复
            this.simpleProgress.close();
            this.errorDialog.open("终端诊断失败");
            break;
          // 终端诊断消息 end
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
      return this.$store.state.grabfile_selection_list;
    }
  },
  watch: {
    sPlatformDomainMoid: function(val) {
      if (val == "") {
        this.sPlatformDomainMoids = [];
        this.sMachineRoomMoids = [];
        this.sPlatformDomainMoids = [].concat(this.p);
        this.sMachineRoomMoids = [].concat(this.m);
        this.sPlatformDomainMoids.unshift({
          moid: "",
          parent_moid: "",
          name: "所有平台域",
          type: "platform"
        });
        this.sMachineRoomMoids.unshift({
          moid: "",
          parent_moid: "",
          name: "所有虚拟机房",
          type: "machine_room"
        });
        this.sPlatformDomainMoid = "";
        this.sMachineRoomMoid = "";
      } else {
        this.sMachineRoomMoids = [];
        this.m.forEach(j => {
          if (val == j.parent_moid) {
            this.sMachineRoomMoids.push(j);
          }
        });
        if (this.sMachineRoomMoids.length == 0) {
          this.sMachineRoomMoids.unshift({
            moid: "",
            parent_moid: "",
            name: "无下级域",
            type: "machine_room"
          });
        } else {
          this.sMachineRoomMoids.unshift({
            moid: "",
            parent_moid: "",
            name: "所有虚拟机房",
            type: "machine_room"
          });
        }
        this.sMachineRoomMoid = "";
      }
    },
    sMachineRoomMoid: function(newMachine, oldMachine) {
      this.ddeviceName = "";
      this.ddeviceNames.splice(1, this.ddeviceNames.length - 1);
      api.getOnlineServer({ params: { parentMoid: newMachine } }).then(res => {
        console.log("诊断服务器设备名结果反馈" + JSON.stringify(res));
        if (res.data != "{}" && res.success == 1) {
          this.dserInfo = res.data;
          for (var i = 0; i < res.data.length; i++) {
            let dic = {};
            dic["text"] = res.data[i]["name"];
            dic["value"] = res.data[i]["name"];
            this.ddeviceNames.push(dic);
          }
        }
      });
    },
    ddeviceName: function(newName, oldName) {
      for (var i = 0; i < this.dserInfo.length; i++) {
        if (this.dserInfo[i]["name"] == newName) {
          this.dserDeviceMoid = this.dserInfo[i]["moid"];
          this.type_ser = this.dserInfo[i]["type_ser"];
        }
      }
    },
    tTerminalDomainMoid: function(val) {
      if (val == "") {
        this.tTerminalDomainMoids = [];
        this.tUserMoids = [];
        this.tTerminalDomainMoids = [].concat(this.tm);
        this.tUserMoids = [].concat(this.tu);
        this.tTerminalDomainMoids.unshift({
          moid: "",
          parent_moid: "",
          name: "所有服务域",
          type: "server"
        });
        this.tUserMoids.unshift({
          moid: "",
          parent_moid: "",
          name: "所有用户域",
          type: "user"
        });
        this.tTerminalDomainMoid = "";
        this.tUserMoid = "";
      } else if (val == this.top_main) {
        this.tUserMoids = [];
        this.tUserMoids = [].concat(this.tu);
        this.tUserMoids.unshift({
          moid: "",
          parent_moid: "",
          name: "所有用户域",
          type: "user"
        });
        this.tUserMoid = "";
      } else {
        this.tUserMoids = [];
        this.tu.forEach(j => {
          if (val == j.parent_moid) {
            this.tUserMoids.push(j);
          }
        });
        if (this.tUserMoids.length == 0) {
          this.tUserMoids.unshift({
            moid: "",
            parent_moid: "",
            name: "无下级域",
            type: "user"
          });
        } else {
          this.tUserMoids.unshift({
            moid: "",
            parent_moid: "",
            name: "所有用户域",
            type: "user"
          });
        }
        this.tUserMoid = "";
      }
    },
    tUserMoid: function(newMoid, oldMoid) {
      this.dsdeviceName = "";
      this.dsdeviceNames.splice(1, this.dsdeviceNames.length - 1);
      api.getOnlineTerminal({ params: { parentMoid: newMoid } }).then(res => {
        console.log("终端诊断参数列表" + JSON.stringify(res));
        if (res.data != "[]") {
          this.dterInfo = res.data;
          for (var i = 0; i < res.data.length; i++) {
            let dic_name = {};
            dic_name["text"] = res.data[i]["name"];
            dic_name["value"] = res.data[i]["name"];
            this.dsdeviceNames.push(dic_name);
          }
        }
      });
    },
    dsdeviceName: function(newName, oldName) {
      this.tDeviceType = "";
      this.tDeviceTypes.splice(1, this.tDeviceTypes.length - 1);
      for (var i = 0; i < this.dterInfo.length; i++) {
        if (this.dterInfo[i]["name"] == newName) {
          this.dterDeviceMoid = this.dterInfo[i]["moid"];
          if (this.dterInfo[i]["type"].length > 0) {
            for (let j = 0; j < this.dterInfo[i]["type"].length; j++) {
              let dic = {};
              dic["text"] = this.dterInfo[i]["type"][j];
              dic["value"] = this.dterInfo[i]["type"][j];
              this.tDeviceTypes.push(dic);
            }
          }
        }
      }
    },
    gTerminalDomainMoid: function(val) {
      if (val == "") {
        this.gTerminalDomainMoids = [];
        this.gUserMoids = [];
        this.gTerminalDomainMoids = [].concat(this.tm);
        this.gUserMoids = [].concat(this.tu);
        this.gTerminalDomainMoids.unshift({
          moid: "",
          parent_moid: "",
          name: "所有服务域",
          type: "server"
        });
        this.gUserMoids.unshift({
          moid: "",
          parent_moid: "",
          name: "所有用户域",
          type: "user"
        });
        this.gTerminalDomainMoid = "";
        this.gUserMoid = "";
      } else if (val == this.top_main) {
        this.gUserMoids = [];
        this.gUserMoids = [].concat(this.tu);
        this.gUserMoids.unshift({
          moid: "",
          parent_moid: "",
          name: "所有用户域",
          type: "user"
        });
        this.gUserMoid = "";
      } else {
        this.gUserMoids = [];
        this.tu.forEach(j => {
          if (val == j.parent_moid) {
            this.gUserMoids.push(j);
          }
        });
        if (this.gUserMoids.length == 0) {
          this.gUserMoids.unshift({
            moid: "",
            parent_moid: "",
            name: "无下级域",
            type: "user"
          });
        } else {
          this.gUserMoids.unshift({
            moid: "",
            parent_moid: "",
            name: "所有用户域",
            type: "user"
          });
        }
        this.gUserMoid = "";
      }
    },
    lTerminalDomainMoid: function(val) {
      if (val == "") {
        this.lTerminalDomainMoids = [];
        this.lUserMoids = [];
        this.lTerminalDomainMoids = [].concat(this.tm);
        this.lUserMoids = [].concat(this.tu);
        this.lTerminalDomainMoids.unshift({
          moid: "",
          parent_moid: "",
          name: "所有服务域",
          type: "server"
        });
        this.lUserMoids.unshift({
          moid: "",
          parent_moid: "",
          name: "所有用户域",
          type: "user"
        });
        this.lTerminalDomainMoid = "";
        this.gUserMoid = "";
      } else if (val == this.top_main) {
        this.lUserMoids = [];
        this.lUserMoids = [].concat(this.tu);
        this.lUserMoids.unshift({
          moid: "",
          parent_moid: "",
          name: "所有用户域",
          type: "user"
        });
        this.lUserMoid = "";
      } else {
        this.lUserMoids = [];
        this.tu.forEach(j => {
          if (val == j.parent_moid) {
            this.lUserMoids.push(j);
          }
        });
        if (this.lUserMoids.length == 0) {
          this.lUserMoids.unshift({
            moid: "",
            parent_moid: "",
            name: "无下级域",
            type: "user"
          });
        } else {
          this.lUserMoids.unshift({
            moid: "",
            parent_moid: "",
            name: "所有用户域",
            type: "user"
          });
        }
        this.lUserMoid = "";
      }
    },
    gplatformDomain: function(val) {
      if (val == "") {
        this.gplatformDomains = [];
        this.gmachineRooms = [];
        this.gplatformDomains = [].concat(this.p);
        this.gmachineRooms = [].concat(this.m);
        this.gplatformDomains.unshift({
          moid: "",
          parent_moid: "",
          name: "所有平台域",
          type: "platform"
        });
        this.gmachineRooms.unshift({
          moid: "",
          parent_moid: "",
          name: "所有虚拟机房",
          type: "machine_room"
        });
        this.gplatformDomain = "";
        this.gmachineRoom = "";
      } else {
        this.gmachineRooms = [];
        this.m.forEach(j => {
          if (val == j.parent_moid) {
            this.gmachineRooms.push(j);
          }
        });
        if (this.gmachineRooms.length == 0) {
          this.gmachineRooms.unshift({
            moid: "",
            parent_moid: "",
            name: "无下级域",
            type: "machine_room"
          });
        } else {
          this.gmachineRooms.unshift({
            moid: "",
            parent_moid: "",
            name: "所有虚拟机房",
            type: "machine_room"
          });
        }
        this.gmachineRoom = "";
      }
    },
    lPlatformDomainMoid: function(val) {
      if (val == "") {
        this.lPlatformDomainMoids = [];
        this.lMachineRoomMoids = [];
        this.lPlatformDomainMoids = [].concat(this.p);
        this.lMachineRoomMoids = [].concat(this.m);
        this.lPlatformDomainMoids.unshift({
          moid: "",
          parent_moid: "",
          name: "所有平台域",
          type: "platform"
        });
        this.lMachineRoomMoids.unshift({
          moid: "",
          parent_moid: "",
          name: "所有虚拟机房",
          type: "machine_room"
        });
        this.lPlatformDomainMoid = "";
        this.lMachineRoomMoid = "";
      } else {
        this.lMachineRoomMoids = [];
        this.m.forEach(j => {
          if (val == j.parent_moid) {
            this.lMachineRoomMoids.push(j);
          }
        });
        if (this.lMachineRoomMoids.length == 0) {
          this.lMachineRoomMoids.unshift({
            moid: "",
            parent_moid: "",
            name: "无下级域",
            type: "machine_room"
          });
        } else {
          this.lMachineRoomMoids.unshift({
            moid: "",
            parent_moid: "",
            name: "所有虚拟机房",
            type: "machine_room"
          });
        }
        this.lMachineRoomMoid = "";
      }
    },
    diagnoseObject: function(newType, oldType) {
      if (newType == "server") {
        this.machine = true;
        this.user = false;
        this.getDiaDeviceName();
      } else if (newType == "terminal") {
        this.user = true;
        this.machine = false;
        this.getDiaTerDevName();
      }
    },
    grabObject: function(newType, oldType) {
      if (newType == "server") {
        this.gmachine = true;
        this.guser = false;
        this.getGDevSerName();
      } else if (newType == "terminal") {
        this.guser = true;
        this.gmachine = false;
        this.getGTerName();
      }
    },
    logObject: function(newType, oldType) {
      this.ldeviceType == ""
      if (newType == "server") {
        this.lmachine = true;
        this.luser = false;
        // this.getDiaDeviceName()
      } else if (newType == "terminal") {
        this.luser = true;
        this.lmachine = false;
        // this.getDiaTerDevName()
      }
    },
    // 翻页跳转
    curPage: function(newPageNum, oldPageNum) {
      this.cage = 1;
      if (newPageNum <= this.grapTotalPage && newPageNum > 0) {
        api
          .getCaptureFile({ params: { newPageNum: newPageNum } })
          .then(res => {
            this.grabFileList = res.data;
            this.grapTotalPage = Math.ceil(res.total_num / this.perPage);
            this.grabFileFields = getGrabFileFields(this.grabdownload);
            this.fileTotalNum = res.total_num;
          })
          .catch(error => {
            console.log(error);
          });
      }
    },
    curPageLog: function(newPageNum, oldPageNum) {
      if (newPageNum == 1) {
        let alist = JSON.parse(JSON.stringify(this.filest))
        this.logFileList = alist;
        this.logTotalPage = Math.ceil(this.logFileList.length / this.logPerPage);
      }
    },
    // 诊断抓包tab栏切换刷新
    tabType: function(newTab, oldTab) {
      if (newTab === "diagnose") {
        // 诊断功能
        this.getDiaDeviceName();
      } else if (newTab === "grabbag") {
        // 抓包功能
        this.getGDevSerName();
        this.getAddGInfo();
        this.getCaptureFileInfo();
      } else if (newTab === "getlog") {
        // 日志获取
        this.getLTerName();
        this.getLSerName();
        this.logicalNames = ""
        this.logicalNames = []
      }
    },
    gmachineRoom: function(newMachine, oldMachine) {
      this.serverName = "";
      this.serverNames.splice(1, this.serverNames.length - 1);
      api.getOnlineServer({ params: { parentMoid: newMachine } }).then(res => {
        console.log("服务器设备名、网口" + JSON.stringify(res));
        if (res.data != "{}") {
          this.serverInfo = res.data;
          for (var i = 0; i < res.data.length; i++) {
            let dic = {};
            dic["text"] = res.data[i]["name"];
            dic["value"] = res.data[i]["name"];
            this.serverNames.push(dic);
          }
        }
      });
    },
    serverName: function(newName, oldName) {
      this.devicePort = "any";
      this.devicePorts.splice(1, this.devicePorts.length - 1);
      for (var i = 0; i < this.serverInfo.length; i++) {
        if (this.serverInfo[i]["name"] == newName) {
          this.gserDeviceMoid = this.serverInfo[i]["moid"];
          this.gsDeviceType = this.serverInfo[i]["type_ser"];
          if (this.serverInfo[i]["netcards"] != "{}") {
            for (var j = 0; j < this.serverInfo[i]["netcards"].length; j++) {
              let dicp = {};
              dicp["text"] = this.serverInfo[i]["netcards"][j];
              dicp["value"] = this.serverInfo[i]["netcards"][j];
              this.devicePorts.push(dicp);
            }
          }
        }
      }
      console.log("网口=" + this.devicePorts);
    },
    gUserMoid: function(newMoid, oldMoid) {
      this.gdeviceName = "";
      this.gdeviceNames.splice(1, this.gdeviceNames.length - 1);
      api.getOnlineTerminal({ params: { parentMoid: newMoid } }).then(res => {
        console.log("终端抓包参数列表" + JSON.stringify(res));
        if (res.data != "[]") {
          this.terInfo = res.data;
          for (var i = 0; i < res.data.length; i++) {
            let dic_name = {};
            dic_name["text"] = res.data[i]["name"];
            dic_name["value"] = res.data[i]["name"];
            this.gdeviceNames.push(dic_name);
          }
        }
      });
    },
    gdeviceName: function(newName, oldName) {
      this.gtdeviceType = "";
      this.gtdeviceTypes.splice(1, this.gtdeviceTypes.length - 1);
      for (var i = 0; i < this.terInfo.length; i++) {
        if (this.terInfo[i]["name"] == newName) {
          this.gterDeviceMoid = this.terInfo[i]["moid"];
          if (this.terInfo[i]["type"].length > 0) {
            this.dterTypeList = this.terInfo[i]["type"];
            for (var k = 0; k < this.terInfo[i]["type"].length; k++) {
              let dic_type = {};
              dic_type["text"] = this.terInfo[i]["type"][k];
              dic_type["value"] = this.terInfo[i]["type"][k];
              this.gtdeviceTypes.push(dic_type);
            }
          }
        }
      }
    },
    gtdeviceType: function(newType, oldType) {
      this.gdevicePort = "any";
      this.gdevicePorts.splice(1, this.gdevicePorts.length - 1);
      for (var i = 0; i < this.terInfo.length; i++) {
        for (let j = 0; j < this.dterTypeList.length; j++) {
          if (this.dterTypeList[j] == newType) {
            var key_type = newType.replace(/ /g, "~");
            if (this.terInfo[i]["netcards"][key_type].length > 0) {
              for (
                var k = 0;
                k < this.terInfo[i]["netcards"][key_type].length;
                k++
              ) {
                let dic_type = {};
                dic_type["text"] = this.terInfo[i]["netcards"][key_type][i][
                  "netcards"
                ][k];
                dic_type["value"] = this.terInfo[i]["netcards"][key_type][i][
                  "netcards"
                ][k];
                this.gdevicePorts.push(dic_type);
              }
            }
          }
        }
      }
    },
    // log
    lMachineRoomMoid: function(newMachine, oldMachine) {
      this.lphysicalName = "";
      this.lphysicalNames.splice(1, this.lphysicalNames.length - 1);
      api.getOnlineServer({ params: { parentMoid: newMachine } }).then(res => {
        console.log("lMachineRoomMoid=" + JSON.stringify(res));
        if (res.data != "{}" && res.success == 1) {
          this.logSerInfo = res.data;
          for (var i = 0; i < res.data.length; i++) {
            let dic = {};
            dic["text"] = res.data[i]["name"];
            dic["value"] = res.data[i]["name"];
            this.lphysicalNames.push(dic);
          }
        }
      });
    },
    lphysicalName: function(newName, oldName) {
      this.logicalName = ""
      this.logicalNames = [
        {
          text: "请选择业务模块",
          value: ""
        }
      ]
      this.ldeviceName = "";
      this.ldeviceNames.splice(1, this.ldeviceNames.length - 1);
      for (var i = 0; i < this.logSerInfo.length; i++) {
        if (this.logSerInfo[i]["name"] == newName) {
          this.logSerDeviceMoid = this.logSerInfo[i]["moid"];
          this.lphysicalType = this.logSerInfo[i]["type_ser"];
          api
            .getLogicalList({ params: { pServerMoid: this.logSerDeviceMoid } })
            .then(res => {
              console.log("get_logical_server_list=" + JSON.stringify(res));
              if (res.data != "{}" && res.success == 1) {
                this.logicalLists = res.data;
                for (let j = 0; j < this.logicalLists.length; j++) {
                  if (this.logicalLists[j]["type"] != "") {
                    let dic = {};
                    dic["text"] = this.logicalLists[j]["type"];
                    dic["value"] = this.logicalLists[j]["type"];
                    this.logicalNames.push(dic);
                  }
                }
              }
            });
        }
      }
    },
    logicalName: function(newName, oldName) {
      for (let i = 0; i < this.logicalLists.length; i++) {
        if (this.logicalLists[i]["type"] == newName) {
          this.logicalMoid = this.logicalLists[i]["moid"];
        }
      }
    },
    lUserMoid: function(newMoid, oldMoid) {
      this.ldeviceName = "";
      this.ldeviceNames.splice(1, this.ldeviceNames.length - 1);
      api.getOnlineTerminal({ params: { parentMoid: newMoid } }).then(res => {
        if (res.data != "[]") {
          this.lTerInfo = res.data;
          for (var i = 0; i < res.data.length; i++) {
            let dic_name = {};
            dic_name["text"] = res.data[i]["name"];
            dic_name["value"] = res.data[i]["name"];
            this.ldeviceNames.push(dic_name);
          }
        }
      });
    },
    ldeviceName: function(newName, oldName) {
      this.ldeviceType = "";
      this.ldeviceTypes.splice(1, this.ldeviceTypes.length - 1);
      for (var i = 0; i < this.lTerInfo.length; i++) {
        if (this.lTerInfo[i]["name"] == newName) {
          this.lTerDevMoid = this.lTerInfo[i]["moid"];
          if (this.lTerInfo[i]["type"].length > 0) {
            for (let j = 0; j < this.lTerInfo[i]["type"].length; j++) {
              let dic = {};
              dic["text"] = this.lTerInfo[i]["type"][j];
              dic["value"] = this.lTerInfo[i]["type"][j];
              this.ldeviceTypes.push(dic);
            }
          }
        }
      }
    }
  }
};
</script>

<style scoped>
.server,
.terminal,
.meeting {
  display: flex;
  justify-content: space-between;
  padding-bottom: 10px;
}
.diagnose {
  float: left;
  width: 100%;
  height: 100%;
}
.diagnose-select {
  margin-top: 10px;
  display: flex;
  height: 40px;
  width: 100%;
}
.diagnose-time {
  display: flex;
  margin-top: 15px;
  height: 40px;
  width: 100%;
  border-bottom: 1px dotted #c0c0c0;
}
.grab {
  float: left;
  width: 100%;
  height: 100%;
}
.grab-search {
  margin-top: 10px;
  display: flex;
  height: 40px;
  width: 100%;
  border-bottom: 1px dotted #c0c0c0;
}
.log {
  float: left;
  width: 100%;
  height: 100%;
}
.log-search {
  float: left;
  height: 30px;
  width: 100%;
  margin-top: 10px;
  display: flex;
}
.grab-select {
  padding-right: 15px;
  float: left;
}
.filter-text {
  margin-bottom: 15px;
  width: 15%;
}
.grab-msg {
  font: 14px "Microsoft Yahei", arial;
  margin-top: 10px;
  margin-bottom: 10px;
  float: left;
  height: 24px;
  width: 100%;
}
#grabStartFloat {
  float: right;
}
#diagnosisFloat {
  margin-left: 15px;
  height: 24px;
  float: left;
}
#grabDeleteFloat {
  float: right;
}
#logSearchFloat {
  float: left;
}
#logDownFloat {
  float: right;
}
.msg {
  float: left;
  text-align: left;
  width: 25%;
  margin-right: 10px;
}
.obj {
  margin-left: 15px;
}
.select {
  color: #fff;
  background-image: url(../../../assets/image/tab_select.png);
  background-size: cover;
}
.grab-tab {
  font: 14px "Microsoft Yahei", arial;
  margin-right: 15px;
  margin-top: 3px;
}
.grab-list {
  height: 260px;
  border-bottom: 1px dotted #c0c0c0;
}
.grab-list-last {
  height: 260px;
}

.delTipsDiv {
  padding: 50px;
  text-align: center;
}
.fontCommon {
  clear: both;
  margin-top: 25px;
  font-size: 12px;
  color: #4e4e4e;
  position: relative;
  overflow: hidden;
}
.backNamePathCommon {
  display: inline-block;
  width: 150px;
  height: 20px;
}
.modifyCommon {
  display: inline-block;
  margin-left: 10%;
  width: 100px;
  height: 10px;
}
.res-chart {
  /* height: 410px; */
  width: 820px;
  margin-left: 100px;
}
.res-chart_net {
  height: 690px;
  margin-left: 100px;
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
.terminal-type-detail {
  margin-top: 40px;
}
.terminal-info {
  display: flex;
  align-items: center;
  margin-bottom: 25px;
}
.in_line {
  display: inline;
  float: left;
  padding-top: 15px;
  padding-bottom: 10px;
}
.setName {
  font-size: 12px;
  color: #4e4e4e;
  display: inline-block;
  text-align: left;
  width: 110px;
}
.log-title {
  float: left;
  padding-right: 31px;
}
</style>
