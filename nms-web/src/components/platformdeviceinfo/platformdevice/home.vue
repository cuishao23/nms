
<template>
  <el-tabs v-model="tabType">
    <el-tab-pane label="会议服务器" name="meetingservice" style="text-align: left; padding-top: 20px;">
      <div class="el-tabs__content">
      <div class="device-search">
        <ul>
          <li>
            <el-select v-model="fServiceDomainMoid" placeholder="请选择" filterable>
              <el-option
                v-for="(item,index) in sServiceDomainMoids"
                :key="index"
                :label="item.name"
                :value="item.moid">
              </el-option>
            </el-select>
          </li>
          <li>
            <el-select v-model="fPlatformDomainMoid" placeholder="请选择" filterable>
              <el-option
                v-for="(item,index) in sPlatformDomainMoids"
                :key="index"
                :label="item.name"
                :value="item.moid">
              </el-option>
            </el-select>
          </li>
          <li>
            <el-select v-model="fMachineRoomMoid" placeholder="请选择" filterable>
                <el-option
                v-for="(item,index) in sMachineRoomMoids"
                :key="index"
                :label="item.name"
                :value="item.moid">
              </el-option>
            </el-select>
          </li>
          <li>
            <el-select v-model="frameType" placeholder="请选择" filterable>
              <el-option v-for="(item,index) in frameTypes" :key="index" :label="item.text" :value="item.value">
              </el-option>
            </el-select>
          </li>
          <li class="device-info-input">
            <el-input v-model="frame_name" placeholder="设备名称、IP" class="filter-text"></el-input>
          </li>
          <li class="device-info-button">
            <button class='search' @click="frameEquipment()"></button>
          </li>
        </ul>
      </div>
      <div v-if="framephysical.length == 0 && slistFlash" class="no-info-tip">
        <span class="PromptImg"></span>
        <span>此平台域下没有物理服务器设备</span>
      </div>
      <div v-if="framephysical.length > 0">
        <nms-pages-table :data="framephysical" :fields="physicalFields" :total-page="frameTotalPage" v-model="curPageFrame" />
      </div>
    </div>
    </el-tab-pane>
    <el-tab-pane label="节点服务器" name="nodeservice" style="text-align: left; padding-top: 20px;">
      <div class="el-tabs__content">
      <div class="device-search">
        <ul>
          <li>
            <el-select v-model="nServiceDomainMoid" placeholder="请选择" filterable>
              <el-option
                v-for="(item,index) in sServiceDomainMoids"
                :key="index"
                :label="item.name"
                :value="item.moid">
              </el-option>
            </el-select>
          </li>
          <li>
            <el-select v-model="nPlatformDomainMoid" placeholder="请选择" filterable>
              <el-option
                v-for="(item,index) in sPlatformDomainMoids"
                :key="index"
                :label="item.name"
                :value="item.moid">
              </el-option>
            </el-select>
          </li>
          <li>
            <el-select v-model="nMachineRoomMoid" placeholder="请选择" filterable>
                <el-option
                v-for="(item,index) in sMachineRoomMoids"
                :key="index"
                :label="item.name"
                :value="item.moid">
              </el-option>
            </el-select>
          </li>
          <li>
            <el-select v-model="noframeType" placeholder="请选择" filterable>
              <el-option v-for="(item,index) in noframeTypes" :key="index" :label="item.text" :value="item.value">
              </el-option>
            </el-select>
          </li>
          <li class="device-info-input">
            <el-input v-model="noframe_name" placeholder="设备名称、IP" class="filter-text"></el-input>
          </li>
          <li class="device-info-button">
            <button class='search' @click="noframeEquipment()"></button>
          </li>
        </ul>
      </div>
      <div v-if="nodephysical.length == 0 && slistFlash" class="no-info-tip">
        此平台域下没有物理服务器设备
      </div>
      <div v-if="nodephysical.length > 0">
        <nms-pages-table :data="nodephysical" :fields="cardFields" :total-page="noframeTotalPage" v-model="curPageDevice" />
      </div>
    </div>
    </el-tab-pane>
  </el-tabs>



</template>

<script>
import ResInfo from "../../common/res-info";
import api from "../../../axios";
import {getTimePeriod} from "assets/js/common";
import NmsPagesTable from "../../common/nms-pages-table";
import {getFrameListFields, drawMeetingEcharts, getTypeListByPhysicals, getTypeListByLogicals, getPhysicalDeviceListFields, getPlatformResInfo, meetingDomainMoids} from "../../../assets/js/platformdevice";
import NmsBigDialog from "../../../components/common/nms-big-dialog";
import NmsTransfer from "../../../components/common/nms-transfer";
import { getFrameInfo, getNodeServerInfo } from '../../../axios/api';

export default {
    components: {
        NmsPagesTable,
        ResInfo,
        NmsBigDialog,
        NmsTransfer
    },
    name: "platform-device",
    data() {
        return {
            // tab标签类型
            tabType: "",
            // 表格每页显示数量
            perPage: 10,
            // 物理服务器
            physicalTotalPage: 1, // 总页数
            frameTotalPage: 1, //frame总页数
            noframeTotalPage: 1, //noframe总页数
            physicalFields: [], // 物理服务器表格字段列表
            cardFields: [], //板卡服务器表格字段列表
            framephysical: [], //机框服务器列表
            physicals: [], // 物理服务器列表
            nodephysical: [], //节点服务器列表
            physicalTypes: [], // 物理服务器类型列表
            physicalType: "all", // 要搜索的物理服务器
            frameType: "all", // 要搜索的服务器(机框)
            noframeType: "all", // 要搜索的服务器(非机框)
            frameTypes: [], //机框类型列表
            noframeTypes: [], //非机框(板卡)类型列表

            fServiceDomainMoid: '',
            fPlatformDomainMoid: '',
            fMachineRoomMoid: '',
            nServiceDomainMoid: '',
            nPlatformDomainMoid: '',
            nMachineRoomMoid: '',
            sServiceDomainMoids: [],//服务域类型列表
            sPlatformDomainMoids: [],//平台域列表
            sMachineRoomMoids:[],//机房类型列表
            warningDomains: [],
            s: [],
            p: [],
            m: [],

            // device_name: "", // 设备名称
            frame_name: "", // 设备名称(机框)
            noframe_name: "", // 设备名称(非机框)

            // 域/机房moid
            moid: "",
            // 域机房类型
            domainType: "",

            // 过滤存的临时数组
            allDefaultPhysicals: [],
            secretMachineRoom: [],
            defaultMachineRoom: [],
            hDefaultMachineRoom: [],

            top_main: "",
            slistFlash: false,
            curPagePhysical: 1,
            curPageFrame: 1,
            curPageNoframe: 1,
            curPageFrame: 1,
            curPageDevice: 1,
            filest: []
        };
    },
    methods: {
        gotoDeviceDetail: function(data) {
          console.log(data)
          this.$router.push({name: "devicedetail", params: {moid: data.machine_room_moid, frame: data.moid, name: data.name}});
        },
        getPlatformFrame: function() {
          api.getFrameInfo({params:{
              parentMoid: this.fMachineRoomMoid,
              deviceType: this.frameType,
              deviceName: this.frame_name
            }
          })
          .then((res) => {
            console.log("机框设备"+JSON.stringify(res))
            if(res.success==1){
              if (res.total_num == 0) {
                this.slistFlash = true
              } else {
                this.slistFlash = false
              }
              let phy_list = res.data
              this.filest = JSON.parse(JSON.stringify(phy_list)); // 拷贝数据
              this.physicals = res.data
              this.fram
              this.physicalFields = getFrameListFields(this.gotoDeviceDetail)
              this.frameTotalPage = Math.ceil(this.framephysical.length / this.perPage)
            }
          })
          .catch((error) => {
            console.log(error);
          });
        },
        getPlatformDevice: function() {
          api.getNodeServerInfo({params:{
              parentMoid: this.sMachineRoomMoid,
              deviceType: this.noframeType,
              deviceName: this.noframe_name
            }
          })
          .then((res) => {
            // console.log("服务器设备"+JSON.stringify(res))
            if(res.success==1){
              if (res.total_num == 0) {
                this.slistFlash = true
              } else {
                this.slistFlash = false
              }
              let phy_list = res.data
              this.filest = JSON.parse(JSON.stringify(phy_list)); // 拷贝数据
              this.physicals = res.data
              this.fram
              this.physicalFields = getFrameListFields(this.gotoPhysicalDetail)
              this.frameTotalPage = Math.ceil(this.nodephysical.length / this.perPage)
            }
          })
          .catch((error) => {
            console.log(error);
          });
        },
        frameEquipment: function() {
          api.getFrameInfo({params:{
              parentMoid: this.fMachineRoomMoid,
              deviceType: this.frameType,
              deviceName: this.frame_name
            }
          })
          .then((res) => {
            console.log(res.data)
            if(res.success==1){
              this.framephysical = res.data
              this.physicalFields = getFrameListFields(this.gotoDeviceDetail)
              this.frameTotalPage = Math.ceil(this.physicals.length / this.perPage)
            }
          })
          .catch((error) => {
            console.log(error);
          })
        },
        noframeEquipment: function() {
          api.getNodeServerInfo({params:{
              parentMoid: this.nMachineRoomMoid,
              deviceType: this.noframeType,
              deviceName: this.noframe_name,
            }
          })
          .then((res) => {
            console.log(res)
            if(res.success==1){
              this.nodephysical = res.data
              this.physicalFields = getPhysicalDeviceListFields(this.gotoPhysicalDetail)
              this.frameTotalPage = Math.ceil(this.physicals.length / this.perPage)
            }
          })
          .catch((error) => {
            console.log(error);
          })
        },
        gotoPhysicalDetail: function(data) {
            console.log("data111 "+JSON.stringify(data))
            console.log("name: " + data.name + " moid: " + data.moid + " type: " + data.type);
            this.$router.push({
                name: "physicaldetail",
                params: {moid: data.moid, page: 'home'}
            });
        },
    },
    async activated() {
        if (this.$route.params.tabTypeProp) {
          this.tabType = this.$route.params.tabTypeProp
        } else {
          this.tabType = "meetingservice"
        }
        api.getFrameInfo({params: {deviceType: this.frameType, deviceName: this.frame_name, parentMoid: this.fMachineRoomMoid}}).then((res) => {
           console.log(res)
           this.framephysical = res.data
        })
        //frame
        api.getFrameTypeList().then((res) => {
          console.log("机框设备"+JSON.stringify(res))
          this.frameTypes = [{
            text: '全部设备类型',
            value: 'all'
          }]
          if(res.data != '{}'){
            for (var i = 0; i < res.data.length; i++) {
            let dic = {}
            dic["text"] = res.data[i]
            dic["value"] = res.data[i]
            this.frameTypes.push(dic)
          }
          }
        })
        // this.tabType = "nodeservice"
        this.cardFields = getPhysicalDeviceListFields(this.gotoPhysicalDetail)
        api.getNodeServerInfo({params: {deviceType: this.noframeType, deviceName: this.noframe_name, parentMoid: this.nMachineRoomMoid}}).then((res) => {
           console.log(res.data)
           this.nodephysical = res.data
        })

        //  noframe
        api.getNoframeTypeList().then((res) => {
          console.log("服务器设备"+JSON.stringify(res))
          this.noframeTypes = [{
            text: '全部设备类型',
            value: 'all'
          }]
          if(res.data != '{}'){
            for (var i = 0; i < res.data.length; i++) {
            let dic = {}
            dic["text"] = res.data[i]
            dic["value"] = res.data[i]
            this.noframeTypes.push(dic)
          }
          }
        })
        // frame platform
        await api.getPlatformDomainTree().then((res) => {
          console.log(res)
          this.sServiceDomainMoids = []
          this.sPlatformDomainMoids = []
          this.sMachineRoomMoids = []
          this.s=[]
          this.p=[]
          this.m=[]
          this.warningDomains = res.data
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
              this.fServiceDomainMoid = ""
              this.fPlatformDomainMoid = ""
              this.fMachineRoomMoid = ""
              this.getPlatformFrame()
        })
        //noframe platform
        await api.getPlatformDomainTree().then((res) => {
          console.log(res)
          this.sServiceDomainMoids = []
          this.sPlatformDomainMoids = []
          this.sMachineRoomMoids = []
          this.s=[]
          this.p=[]
          this.m=[]
          this.warningDomains = res.data
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
              this.nServiceDomainMoid = ""
              this.nPlatformDomainMoid = ""
              this.nMachineRoomMoid = ""
              this.getPlatformDevice()
        })
    },
    watch: {
        tabType: function(newstate,oldstate){
          // console.log(this.tabType)
          if (newstate = "meetingservice") {
            this.physicalFields= getFrameListFields(this.gotoDeviceDetail)
          } else if (newstate = "nodeservice") {
            this.cardFields= getPhysicalDeviceListFields(this.gotoPhysicalDetail)
          }
        },
        curPageFrame: function(newPageNum, oldPageNum) {
          if (newPageNum == 1) {
            let alist = JSON.parse(JSON.stringify(this.filest))
            this.physicals = alist
            this.physicalFields = getFrameListFields(this.gotoDeviceDetail)
            this.frameTotalPage = Math.ceil(this.physicals.length / this.perPage)
          }
        },
        curPageNoframe: function(newPageNum, oldPageNum) {
          if (newPageNum == 1) {
            let alist = JSON.parse(JSON.stringify(this.filest))
            this.physicals = alist
            this.cardFields = getPhysicalDeviceListFields(this.gotoPhysicalDetail)
            this.noframeTotalPage = Math.ceil(this.physicals.length / this.perPage)
          }
        },
        sServiceDomainMoid: function (val) {
          console.log("val="+JSON.stringify(val))
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
              this.fServiceDomainMoid = ""
              this.fPlatformDomainMoid = ""
              this.fMachineRoomMoid = ""
              this.nServiceDomainMoid = ""
              this.nPlatformDomainMoid = ""
              this.nMachineRoomMoid = ""
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
              this.fPlatformDomainMoid = ""
              this.fMachineRoomMoid = ""
              this.nPlatformDomainMoid = ""
              this.nMachineRoomMoid = ""
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
              this.fPlatformDomainMoid=""
              this.nPlatformDomainMoid=""
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
              this.fMachineRoomMoid=""
              this.nMachineRoomMoid=""
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
              this.fPlatformDomainMoid = ""
              this.fMachineRoomMoid = ""
              this.nPlatformDomainMoid = ""
              this.nMachineRoomMoid = ""
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
              this.fMachineRoomMoid=""
              this.nMachineRoomMoid=""
            }
        }
    }
};
</script>

<style scoped>
.no-info-tip {
    text-align: center;
}

.device-search {
    display: flex;
    padding-bottom: 10px;
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

#frameToolbar {
    height: 45px;
}

#btnDelFrame {
    float: right;
    margin-top: 20px;
    margin-right: 5px;
}

input.timeInputdisable[type="button"],
button.timeInputdisable {
    color: #fff;
    cursor: default;
    background-color: #e5e5e5;
    border-width: 0px;
    padding: 6px 22px 5px 22px;
    background-image: none;
}

#btnUpdateFrame {
    float: right;
    margin-top: 20px;
    margin-right: 5px;
}

#btnAddFrame {
    float: right;
    margin-top: 20px;
    margin-right: 5px;
}
.res-chart {
  width: 750px;
  height: 650px;
}
.filter-text {
  margin-left: 14px;
}
/* .log-content {
  float: left;
} */
</style>
