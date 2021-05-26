<template>
  <div class="allCommon">
    <div class="fontCommon">
      <span class="modifyCommon">权限配置</span>
      <el-radio class="chooseCommon" v-model="permissionType" label='0'>关闭权限配置</el-radio>
      <el-radio class="chooseCommon" v-model="permissionType" label='2'>开启白名单</el-radio>
      <el-radio class="chooseCommon" v-model="permissionType" label='1'>开启黑名单</el-radio>
      <button id="btnSave" class="normal-btn" @click="OnSavePermissionType()">保存</button>
    </div>
    <div class="backCommon">
      <span class="itemCommon">权限名单配置</span>
      <el-select v-model="permissionList" placeholder="名单类型" class="permissionTypes">
        <el-option
          v-for="(item,index) in permissionLists"
          :key="index"
          :label="item.name"
          :value="item.type">
        </el-option>
      </el-select>
      <button class="normal-btn" @click="onAddDeviceList()" id="addFloat">新增</button>
      <nms-pager-table v-if="deviceReset" :data="deviceList" :fields="deviceFields" :total-page="userTotalPage" :perPage="perPage" :biao-zhi="cage" v-model="curPage"/>
      <div slot="content" v-if="deviceList.length == 0">
        <div class="delTipsDiv">
          <span class="PromptImg"></span>
          <span>尚无<span v-if="permissionList == 1">白名单</span><span v-if="permissionList == 0">黑名单</span>，
          请点击<a class="warningNotifyAdd" v-on:click="onAddDeviceList()">新增</a>进行<span v-if="permissionList == 1">白名单</span><span v-if="permissionList == 0">黑名单</span>添加</span>
        </div>
      </div>
    </div>
    <nms-big-dialog title="新增" ref="addListDialog" @confirm="setDeviceList()" :width="'460px'" :height="'480px'">
      <div slot="content" class="addDeviceDialog">
        <div class="lineDiv">
          <span class="setName">E164号</span>
          <input type="text" v-model="addDeviceE164" class="setValue" @blur="examineMsg" oninput="value=value.replace(/[\W]/g,'')"/>
        </div>
        <div class="lineDiv">
          <span class="setName">终端版本号</span>
          <input type="text" v-model="addDeviceVersion" class="setValue" @blur="examineMsg"/>
        </div>
        <div class="lineDiv">
          <span class="setName">IP地址</span>
          <el-select v-model="ipTypeList" placeholder="IP类型" @change="ipTypeClick" class="ipTypes">
            <el-option
              v-for="(item,index) in ipTypeLists"
              :key="index"
              :label="item.name"
              :value="item.type">
            </el-option>
          </el-select>
          <input v-if="ipTypeList=='oneip'" type="text" v-model="addDeviceOneIP" class="setpartValue" @blur="examineMsg"/>
          <input v-if="ipTypeList=='moreip'" type="text" v-model="addDeviceFirstIP" class="setFirstValue" @blur="examineMsg"/>
          <span v-if="ipTypeList=='moreip'" class="FloatLeft"> - </span>
          <input v-if="ipTypeList=='moreip'" type="text" v-model="addDeviceLastIP" class="setLastValue" @blur="examineMsg"/>
        </div>
        <div class="lineDiv">
          <span class="setName">终端类型</span>
          <el-radio-group v-model="DeviceType">
            <el-radio class="chooseDevice" @click.native.prevent="clickitem(1)" :label="1">硬终端</el-radio>
            <el-radio class="chooseDevice" @click.native.prevent="clickitem(0)" :label="0">软终端</el-radio>
          </el-radio-group>
        </div>
        <div class="lineDiv">
          <span class="setName">终端SN序列号</span>
          <input type="text" v-model="addDeviceSN" class="setValue" @blur="examineMsg" oninput="value=value.replace(/[\W]/g,'')"/>
        </div>
        <div class="lineDiv">
          <span class="setName">设备主型号</span>
          <el-select v-model="mainTypeList" placeholder="主型号类型" class="mainTypes" @change="mainTypeClick">
            <el-option
              v-for="(item,index) in mainTypeLists"
              :key="index"
              :label="item.name"
              :value="item.type">
            </el-option>
          </el-select>
        </div>
        <div class="lineDiv">
          <span class="setName">设备子型号</span>
          <el-select v-model="subTypeList" placeholder="子型号类型" class="mainTypes">
            <el-option
              v-for="(item,index) in subTypeLists"
              :key="index"
              :label="item.name"
              :value="item.type">
            </el-option>
          </el-select>
        </div>
      </div>
    </nms-big-dialog>
    <nms-big-dialog title="编辑" ref="editListDialog" @confirm="editDeviceList()" :width="'460px'" :height="'480px'">
      <div slot="content" class="addDeviceDialog">
        <div class="lineDiv">
          <span class="setName">E164号</span>
          <input type="text" v-model="editDeviceE164" class="setValue" @blur="examineMsg"/>
        </div>
        <div class="lineDiv">
          <span class="setName">终端版本号</span>
          <input type="text" v-model="editDeviceVersion" class="setValue" @blur="examineMsg"/>
        </div>
        <div class="lineDiv">
          <span class="setName">IP地址</span>
          <el-select v-model="ipTypeList" placeholder="IP类型" @change="ipTypeChange" class="ipTypes">
            <el-option
              v-for="(item,index) in ipTypeLists"
              :key="index"
              :label="item.name"
              :value="item.type">
            </el-option>
          </el-select>
          <input v-if="ipTypeList=='oneip'" type="text" v-model="editDeviceOneIP" class="setpartValue" @blur="examineMsg"/>
          <input v-if="ipTypeList=='moreip'" type="text" v-model="editDeviceFirstIP" class="setFirstValue" @blur="examineMsg"/>
          <span v-if="ipTypeList=='moreip'" class="FloatLeft"> - </span>
          <input v-if="ipTypeList=='moreip'" type="text" v-model="editDeviceLastIP" class="setLastValue" @blur="examineMsg"/>
        </div>
        <div class="lineDiv">
          <span class="setName">终端类型</span>
          <el-radio-group v-model="editDeviceType">
            <el-radio class="chooseDevice" @click.native.prevent="edititem(1)" :label="1">硬终端</el-radio>
            <el-radio class="chooseDevice" @click.native.prevent="edititem(0)" :label="0">软终端</el-radio>
          </el-radio-group>
        </div>
        <div class="lineDiv">
          <span class="setName">终端SN序列号</span>
          <input type="text" v-model="editDeviceSN" class="setValue" @blur="examineMsg"/>
        </div>
        <div class="lineDiv">
          <span class="setName">设备主型号</span>
          <el-select v-model="editmainTypeList" placeholder="主型号类型" class="mainTypes" @change="editMainTypeClick">
            <el-option
              v-for="(item,index) in editmainTypeLists"
              :key="index"
              :label="item.name"
              :value="item.type">
            </el-option>
          </el-select>
        </div>
        <div class="lineDiv">
          <span class="setName">设备子型号</span>
          <el-select v-model="editsubTypeList" placeholder="子型号类型" class="mainTypes">
            <el-option
              v-for="(item,index) in editsubTypeLists"
              :key="index"
              :label="item.name"
              :value="item.type">
            </el-option>
          </el-select>
        </div>
      </div>
    </nms-big-dialog>
  </div>
</template>

<script>
  import * as setJs from "../../assets/js/set"
  import NmsBigDialog from "../../components/common/nms-big-dialog";
  import NmsPagerTable from "../../components/common/nms-pager-table";
  import api from '../../axios';

  export default {
    name: "permissionset",
    components: {NmsBigDialog, NmsPagerTable},
    inject: ['reload'],
    data() {
      return {
        permissionType: '0',
        permissionList: 0,
        permissionLists: [
          {
            name: '黑名单',
            type: 0
          },
          {
            name: '白名单',
            type: 1
          }
        ],
        ipTypeList: 'oneip',
        ipTypeLists: [
          {
            name: '单个IP',
            type: 'oneip'
          },
          {
            name: 'IP段',
            type: 'moreip'
          }
        ],
        mainTypeList: '',
        mainTypeLists: [],
        subTypeList: '',
        subTypeLists: [],
        editmainTypeList: '',
        editmainTypeLists: [],
        editsubTypeList: '',
        editsubTypeLists: [],
        DeviceType: null,
        deviceList: [],
        devicedata: [],
        deviceFields: [],
        addDeviceE164: '',
        addDeviceVersion: '',
        addDeviceOneIP: '',
        addDeviceFirstIP: '',
        addDeviceLastIP: '',
        addDeviceSN: '',
        editDeviceE164: '',
        editDeviceVersion: '',
        editDeviceOneIP: '',
        editDeviceFirstIP: '',
        editDeviceLastIP: '',
        editDeviceSN: '',
        editDeviceType: null,
        DeviceTypes: 0,
        DeviceinfoList: [],
        deviceReset: true,
        editMoid: '',
        TotalNum: 0,
        userTotalPage: 0,
        perPage: 10,
        cage: 1,
        curPage: 1,
      }
    },
    mounted: function() {
      this.deviceFields = setJs.getPermissionConfigFields(this.editPermission, this.deletePermission)
      api.getDeviceTypeLimit({params: {limitType: this.permissionList, newPageNum: 1}}).then(res => {
        console.log(res)
        if (res.success == 1) {
          this.devicedata = res.data
          if (this.devicedata.length > 0) {
            this.devicedata.forEach(item => {
              if (item.terminal_type == 0) {
                item.terminal_type = '软终端'
              } else if (item.terminal_type == 1) {
                item.terminal_type = '硬终端'
              } else {
                item.terminal_type = '未知终端'
              }
            })
            this.deviceList = this.devicedata
            this.userTotalPage = Math.ceil(res.total_num / this.perPage)
            this.TotalNum = res.total_num
            this.cage = 1
          } else {
            this.deviceList = []
            this.deviceReset = false
            this.$nextTick(() => {
              this.deviceReset = true
            })
            this.userTotalPage = 1
            this.TotalNum = 0
            this.cage = 1
          }
        }
      })
      api.getDeviceTypeLimitCfg().then(res => {
        console.log(res)
        if (res.success == 1) {
          if (res.data == 0) {
            this.permissionType = '0'
          } else if (res.data == 1) {
            this.permissionType = '1'
          } else if (res.data == 2) {
            this.permissionType = '2'
          }
        }
      })
    },
    methods: {
      clickitem: function(e) {
        this.mainTypeLists = [{'name': '请选择主型号', 'type': ''}]
        this.mainTypeList = ''
        this.subTypeLists = [{'name': '请选择子型号', 'type': ''}]
        this.subTypeList = ''
        if (this.DeviceType == e && this.DeviceType !== '') {
          this.DeviceType = null
        } else {
          this.DeviceType = e
          if (this.DeviceType === 0 || this.DeviceType === 1) {
            api.getDeviceTypes().then(res => {
              console.log(res)
              if (res.success == 1) {
                this.DeviceinfoList = res.data
                let count = 0
                if (this.DeviceinfoList.length > 0) {
                  this.DeviceinfoList.forEach(item => {
                    if (item.terminal_type == this.DeviceType) {
                      count = 0
                      this.mainTypeLists.push({'name': item.name, 'type': item.name})
                      this.mainTypeLists.forEach(value => {
                        if (value.name == item.name) {
                          count++
                        }
                      })
                      if (count > 1) {
                        this.mainTypeLists.pop()
                      }
                    }
                  })
                  this.mainTypeList = this.mainTypeLists[0]['type']
                }
              }
            })
          }
        }
      },
      edititem: function(e) {
        this.editmainTypeLists = [{'name': '请选择主型号', 'type': ''}]
        this.editmainTypeList = ''
        this.editsubTypeLists = [{'name': '请选择子型号', 'type': ''}]
        this.editsubTypeList = ''
        if (this.editDeviceType == e && this.editDeviceType !== '') {
          this.editDeviceType = null
        } else {
          this.editDeviceType = e
          if (this.editDeviceType === 0 || this.editDeviceType === 1) {
            api.getDeviceTypes().then(res => {
              console.log(res)
              if (res.success == 1) {
                this.DeviceinfoList = res.data
                let count = 0
                if (this.DeviceinfoList.length > 0) {
                  this.DeviceinfoList.forEach(item => {
                    if (item.terminal_type == this.editDeviceType) {
                      count = 0
                      this.editmainTypeLists.push({'name': item.name, 'type': item.name})
                      this.editmainTypeLists.forEach(value => {
                        if (value.name == item.name) {
                          count++
                        }
                      })
                      if (count > 1) {
                        this.editmainTypeLists.pop()
                      }
                    }
                  })
                  this.editmainTypeList = this.editmainTypeLists[0]['type']
                }
              }
            })
          }
        }
      },
      examineMsg: function() {
        var ipv4Reg = /^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$/
        var ipv6Reg = /^(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))$/
        var ipv4Re = new RegExp(ipv4Reg)
        var ipv6Re = new RegExp(ipv6Reg)
        if (this.addDeviceE164 !== '') {
          if (this.addDeviceE164.length > 32) {
            this.errorDialog.open('e164号长度不得超出32字节')
            this.addDeviceE164 = ''
          }
        }
        if (this.addDeviceVersion !== '') {
          if (this.addDeviceVersion.length > 64) {
            this.errorDialog.open('版本号长度不得超出64字节')
            this.addDeviceVersion = ''
          }
        }
        if (this.addDeviceOneIP !== '' && this.ipTypeList == 'oneip') {
          if (this.addDeviceOneIP.length > 64) {
            this.errorDialog.open('IP长度不得超出64字节')
            this.addDeviceOneIP = ''
          }
          if (!ipv4Re.test(this.addDeviceOneIP) && !ipv6Re.test(this.addDeviceOneIP)) {
            this.errorDialog.open('IP格式不合理（须符合ipv4/ipv6格式）')
            this.addDeviceOneIP = ''
          }
        }
        if (this.addDeviceFirstIP !== '' && this.ipTypeList == 'moreip') {
          if (this.addDeviceFirstIP.length > 64) {
            this.errorDialog.open('IP长度不得超出64字节')
            this.addDeviceFirstIP = ''
          }
          if (!ipv4Re.test(this.addDeviceFirstIP) && !ipv6Re.test(this.addDeviceFirstIP)) {
            this.errorDialog.open('IP格式不合理（须符合ipv4/ipv6格式）')
            this.addDeviceFirstIP = ''
          }
        }
        if (this.addDeviceLastIP !== '' && this.ipTypeList == 'moreip') {
          if (this.addDeviceLastIP.length > 64) {
            this.errorDialog.open('IP长度不得超出64字节')
            this.addDeviceLastIP = ''
          }
          if (!ipv4Re.test(this.addDeviceLastIP) && !ipv6Re.test(this.addDeviceLastIP)) {
            this.errorDialog.open('IP格式不合理（须符合ipv4/ipv6格式）')
            this.addDeviceLastIP = ''
          }
        }
        if (this.addDeviceSN !== '') {
          if (this.addDeviceSN.length > 36) {
            this.errorDialog.open('SN号长度不得超出36字节')
            this.addDeviceSN = ''
          }
        }
        if (this.editDeviceE164 !== '') {
          if (this.editDeviceE164.length > 32) {
            this.errorDialog.open('e164号长度不得超出32字节')
            this.editDeviceE164 = ''
          }
        }
        if (this.editDeviceVersion !== '') {
          if (this.editDeviceVersion.length > 64) {
            this.errorDialog.open('版本号长度不得超出64字节')
            this.editDeviceVersion = ''
          }
        }
        if (this.editDeviceOneIP !== '' && this.ipTypeList == 'oneip') {
          if (this.editDeviceOneIP.length > 64) {
            this.errorDialog.open('IP长度不得超出64字节')
            this.editDeviceOneIP = ''
          }
          if (!ipv4Re.test(this.editDeviceOneIP) && !ipv6Re.test(this.editDeviceOneIP)) {
            this.errorDialog.open('IP格式不合理（须符合ipv4/ipv6格式）')
            this.editDeviceOneIP = ''
          }
        }
        if (this.editDeviceFirstIP !== '' && this.ipTypeList == 'moreip') {
          if (this.editDeviceFirstIP.length > 64) {
            this.errorDialog.open('IP长度不得超出64字节')
            this.editDeviceFirstIP = ''
          }
          if (!ipv4Re.test(this.editDeviceFirstIP) && !ipv6Re.test(this.editDeviceFirstIP)) {
            this.errorDialog.open('IP格式不合理（须符合ipv4/ipv6格式）')
            this.editDeviceFirstIP = ''
          }
        }
        if (this.editDeviceLastIP !== '' && this.ipTypeList == 'moreip') {
          if (this.editDeviceLastIP.length > 64) {
            this.errorDialog.open('IP长度不得超出64字节')
            this.editDeviceLastIP = ''
          }
          if (!ipv4Re.test(this.editDeviceLastIP) && !ipv6Re.test(this.editDeviceLastIP)) {
            this.errorDialog.open('IP格式不合理（须符合ipv4/ipv6格式）')
            this.editDeviceLastIP = ''
          }
        }
        if (this.editDeviceSN !== '') {
          if (this.editDeviceSN.length > 36) {
            this.errorDialog.open('SN号长度不得超出36字节')
            this.editDeviceSN = ''
          }
        }
      },
      mainTypeClick: function() {
        this.subTypeLists = [{'name': '请选择子型号', 'type': ''}]
        this.subTypeList = ''
        if (this.mainTypeList !== '') {
          api.getDeviceTypes().then(res => {
            console.log(res)
            if (res.success == 1) {
              this.DeviceinfoList = res.data
              let count = 0
              if (this.DeviceinfoList.length > 0) {
                this.DeviceinfoList.forEach(item => {
                  if (item.name == this.mainTypeList) {
                    count = 0
                    this.subTypeLists.push({'name': item.product_name, 'type': item.product_name})
                    this.subTypeLists.forEach(value => {
                      if (value.name == item.name) {
                        count++
                      }
                    })
                    if (count > 1) {
                      this.subTypeLists.pop()
                    }
                  }
                })
                this.subTypeList = this.subTypeLists[0]['type']
              }
            }
          })
        }
      },
      editMainTypeClick: function() {
        this.editsubTypeLists = [{'name': '请选择子型号', 'type': ''}]
        this.editsubTypeList = ''
        if (this.editmainTypeList !== '') {
          api.getDeviceTypes().then(res => {
            console.log(res)
            if (res.success == 1) {
              let count = 0
              this.DeviceinfoList = res.data
              if (this.DeviceinfoList.length > 0) {
                this.DeviceinfoList.forEach(item => {
                  if (item.name == this.editmainTypeList) {
                    count = 0
                    this.editsubTypeLists.push({'name': item.product_name, 'type': item.product_name})
                    this.editsubTypeLists.forEach(value => {
                      if (value.name == item.name) {
                        count++
                      }
                    })
                    if (count > 1) {
                      this.editsubTypeLists.pop()
                    }
                  }
                })
                this.editsubTypeList = this.editsubTypeLists[0]['type']
              }
            }
          })
        }
      },
      onAddDeviceList: function() {
        this.addDeviceE164 = ''
        this.addDeviceVersion = ''
        this.addDeviceOneIP = ''
        this.addDeviceFirstIP = ''
        this.addDeviceLastIP = ''
        this.addDeviceSN = ''
        this.ipTypeList = 'oneip'
        this.DeviceType = null
        this.mainTypeLists = [{'name': '请选择主型号', 'type': ''}]
        this.mainTypeList = ''
        this.subTypeLists = [{'name': '请选择子型号', 'type': ''}]
        this.subTypeList = ''
        this.$refs.addListDialog.open()
      },
      setDeviceList: function() {
        // if (this.addDeviceOneIP == '' && (this.addDeviceFirstIP == '' || this.addDeviceLastIP == '')) {
        //   this.errorDialog.open("IP地址不能为空！")
        // } else {
          api.addDeviceTypeLimit({
            e164: this.addDeviceE164,
            version: this.addDeviceVersion,
            ip: this.addDeviceOneIP,
            startIP: this.addDeviceFirstIP,
            endIP: this.addDeviceLastIP,
            sn: this.addDeviceSN,
            terminalType: this.DeviceType,
            mainType: this.mainTypeList,
            subType: this.subTypeList,
            limitType: this.permissionList
          }).then(res => {
            console.log(res)
            if (res.success == 1) {
              this.successDialog.open('保存成功')
            } else {
              this.errorDialog.open('保存失败')
            }
            api.getDeviceTypeLimit({params: {limitType: this.permissionList, newPageNum: 1}}).then(res => {
              console.log(res)
              if (res.success == 1) {
                this.devicedata = res.data
                this.devicedata.forEach(item => {
                  if (item.terminal_type == 0) {
                    item.terminal_type = '软终端'
                  } else if (item.terminal_type == 1) {
                    item.terminal_type = '硬终端'
                  } else {
                    item.terminal_type = '未知终端'
                  }
                })
                this.deviceList = this.devicedata
                this.userTotalPage = Math.ceil(res.total_num / this.perPage);
                this.TotalNum = res.total_num
                this.cage = 2
              }
            })
          })
        // }
      },
      ipTypeClick: function() {
        if (this.ipTypeList === 'oneip') {
          this.addDeviceFirstIP = ''
          this.addDeviceLastIP = ''
        } else if (this.ipTypeList === 'moreip') {
          this.addDeviceOneIP = ''
        }
      },
      ipTypeChange: function() {
        if (this.ipTypeList === 'oneip') {
          this.editDeviceFirstIP = ''
          this.editDeviceLastIP = ''
        } else if (this.ipTypeList === 'moreip') {
          this.editDeviceOneIP = ''
        }
      },
      OnSavePermissionType: function() {
        console.log(this.permissionType)
        api.setDeviceTypeLimitCfg({cfgValue: this.permissionType}).then(res => {
          console.log(res)
          if (res.success == 1) {
            this.successDialog.open('保存成功')
          } else {
            this.errorDialog.open('保存失败')
          }
        })
      },
      editPermission: function(data) {
        console.log(data)
        this.editDeviceE164 = data.e164
        this.editDeviceVersion = data.version
        this.editDeviceOneIP = data.ip
        this.editmainTypeLists = [{'name': '请选择主型号', 'type': ''}]
        this.editsubTypeLists = [{'name': '请选择子型号', 'type': ''}]
        this.editmainTypeList = ''
        this.editsubTypeList = ''
        if (data.ip == '') {
          this.ipTypeList = 'moreip'
        }
        this.editDeviceFirstIP = data.start_ip
        this.editDeviceLastIP = data.end_ip
        this.editDeviceSN = data.sn
        if (data.terminal_type == "硬终端") {
          this.editDeviceType = 1
        } else if (data.terminal_type == "软终端") {
          this.editDeviceType = 0
        } else if (data.terminal_type == "未知终端") {
          this.editDeviceType = null
        }
        this.editMoid = data.moid
        api.getDeviceTypes().then(res => {
          console.log(res)
          if (res.success == 1) {
            let count = 0
            this.DeviceinfoList = res.data
            if (this.DeviceinfoList.length > 0) {
              this.DeviceinfoList.forEach(item => {
                if (item.terminal_type == this.editDeviceType) {
                  count = 0
                  this.editmainTypeLists.push({'name': item.name, 'type': item.name})
                  this.editmainTypeLists.forEach(value => {
                    if (value.name == item.name) {
                      count++
                    }
                  })
                  if (count > 1) {
                    this.editmainTypeLists.pop()
                  }
                }
              })
              this.editmainTypeList = data.main_type
              this.DeviceinfoList.forEach(item => {
                if (item.name == data.main_type && item.product_name !== '') {
                  count = 0
                  this.editsubTypeLists.push({'name': item.product_name, 'type': item.product_name})
                  this.editsubTypeLists.forEach(value => {
                    if (value.name == item.name) {
                      count++
                    }
                  })
                  if (count > 1) {
                    this.editsubTypeLists.pop()
                  }
                }
              })
              this.editsubTypeList = data.sub_type
            }
          }
        })
        this.$refs.editListDialog.open()
      },
      editDeviceList: function() {
        api.setDeviceTypeLimit({
          moid: this.editMoid,
          e164: this.editDeviceE164,
          version: this.editDeviceVersion,
          ip: this.editDeviceOneIP,
          startIP: this.editDeviceFirstIP,
          endIP: this.editDeviceLastIP,
          sn: this.editDeviceSN,
          terminalType: this.editDeviceType,
          mainType: this.editmainTypeList,
          subType: this.editsubTypeList,
          limitType: this.permissionList
        }).then(res => {
          console.log(res)
          if (res.success == 1) {
            this.successDialog.open('保存成功')
          } else {
            this.errorDialog.open('保存失败')
          }
          api.getDeviceTypeLimit({params: {limitType: this.permissionList, newPageNum: 1}}).then(res => {
            console.log(res)
            if (res.success == 1) {
              this.devicedata = res.data
              this.devicedata.forEach(item => {
                if (item.terminal_type == 0) {
                  item.terminal_type = '软终端'
                } else if (item.terminal_type == 1) {
                  item.terminal_type = '硬终端'
                } else {
                  item.terminal_type = '未知终端'
                }
              })
              this.deviceList = this.devicedata
              this.userTotalPage = Math.ceil(res.total_num / this.perPage);
              this.TotalNum = res.total_num
              this.cage = 2
            }
          })
        })
      },
      deletePermission: function(data) {
        console.log(data)
        api.delDeviceTypeLimit({moid: data.moid}).then(res => {
          console.log(res)
          if (res.success == 1) {
            this.successDialog.open('删除成功')
          } else {
            this.errorDialog.open('删除失败')
          }
          api.getDeviceTypeLimit({params: {limitType: this.permissionList, newPageNum: 1}}).then(res => {
            console.log(res)
            if (res.success == 1) {
              this.devicedata = res.data
              this.reload()
              if (this.devicedata.length > 0) {
                this.devicedata.forEach(item => {
                  if (item.terminal_type == 0) {
                    item.terminal_type = '软终端'
                  } else if (item.terminal_type == 1) {
                    item.terminal_type = '硬终端'
                  } else {
                    item.terminal_type = '未知终端'
                  }
                })
                this.deviceList = this.devicedata
                this.userTotalPage = Math.ceil(res.total_num / this.perPage);
                this.TotalNum = res.total_num
                this.cage = 2
              } else {
                this.deviceList = []
                this.TotalNum = 0
                this.userTotalPage = 1
                this.cage = 2
              }
            }
          })
        })
        // this.reload()
      }
    },
    watch: {
      // 黑白名单获取
      permissionList: function(newType, oldType) {
        this.deviceList = []
        this.deviceReset = false
        this.$nextTick(() => {
          this.deviceReset = true
        })
        this.userTotalPage = 1
        console.log(newType)
        if (newType === 1 || newType === 0) {
          api.getDeviceTypeLimit({params: {limitType: newType, newPageNum: 1}}).then(res => {
            console.log(res)
            if (res.success == 1) {
              this.devicedata = res.data
              if (this.devicedata.length > 0) {
                this.devicedata.forEach(item => {
                  if (item.terminal_type == 0) {
                    item.terminal_type = '软终端'
                  } else if (item.terminal_type == 1) {
                    item.terminal_type = '硬终端'
                  } else {
                    item.terminal_type = '未知终端'
                  }
                })
                this.deviceList = this.devicedata
                this.deviceReset = false
                this.$nextTick(() => {
                  this.deviceReset = true
                })
                this.userTotalPage = Math.ceil(res.total_num / this.perPage);
                this.TotalNum = res.total_num
                this.cage = 1
              } else {
                this.deviceList = []
                this.deviceReset = false
                this.$nextTick(() => {
                  this.deviceReset = true
                })
                this.TotalNum = 0
                this.userTotalPage = 1
                this.cage = 1
              }
            }
          })
        } else {
          console.log('名单不存在该选择')
        }
      },
      // 翻页
      curPage: function(newPage, oldPage) {
        if (newPage > 0 && newPage <= this.TotalNum) {
          api.getDeviceTypeLimit({params: {limitType: this.permissionList, newPageNum: newPage}}).then(res => {
            console.log(res)
            if (res.success == 1) {
              this.devicedata = res.data
              if (this.devicedata.length > 0) {
                this.devicedata.forEach(item => {
                  if (item.terminal_type == 0) {
                    item.terminal_type = '软终端'
                  } else if (item.terminal_type == 1) {
                    item.terminal_type = '硬终端'
                  } else {
                    item.terminal_type = '未知终端'
                  }
                })
                this.deviceList = this.devicedata
                this.userTotalPage = Math.ceil(res.total_num / this.perPage);
                this.TotalNum = res.total_num
                this.cage = 1
              }
            }
          })
        }
      },
    },
  }
</script>

<style scoped>
.allCommon {
  height: 100%;
  width: 100%;
  float: left;
}
.delTipsDiv {
  padding: 200px;
  text-align: center;
}
.fontCommon {
  text-align: left;
  height: 45px;
  width: 100%;
  font-size: 14px;
  color: #4e4e4e;
  float: left;
  margin-top: 18px;
  border-bottom: 1px dotted #c0c0c0;
}
.chooseCommon {
  float: left;
  width: 124px;
  margin-top: 5px;
}
#btnSave {
  float: left;
}
.modifyCommon {
  margin-left: 17px;
  float: left;
  width: 96px;
  margin-top: 3px;
  color: #4e4e4e;
  font-weight: bold;
}
.backCommon {
  clear: both;
  height: 100px;
  width: 100%;
  color: #4e4e4e;
  float: left;
  margin-top: 26px;
  margin-left: 17px;
}
.itemCommon {
  width: 100%;
  float: left;
  color: #4e4e4e;
  font-weight: bold;
  text-align: left;
  margin-bottom: 21px;
  font-size: 14px
}
.permissionTypes {
  float: left;
  margin-bottom: 10px;
}
#addFloat {
  float: right;
  margin-bottom: 10px;
}
.addDeviceDialog{
  height: 100%;
  width: 100%;
  float: left;
}
.lineDiv {
  float: left;
  margin-top: 30px;
  margin-left: 34px;
  font-size: 14px;
}
.setName {
  color: #4e4e4e;
  float: left;
  text-align: left;
  width: 104px;
}
.setValue {
  color: #4e4e4e;
  float: left;
  text-align: left;
  width: 256px;
}
.setpartValue {
  color: #4e4e4e;
  float: left;
  text-align: left;
  width: 196px;
  margin-left: 10px;
}
.setFirstValue {
  color: #4e4e4e;
  float: left;
  text-align: left;
  width: 87px;
  margin-left: 10px;
  margin-right: 8px;
}
.setLastValue {
  color: #4e4e4e;
  float: left;
  text-align: left;
  width: 87px;
  margin-left: 8px;
}
.ipTypes {
  float: left;
  text-align: left;
  width: 50px;
}
.FloatLeft {
  float: left;
}
.chooseDevice {
  text-align: left;
  float: left;
  width: 114px;
  padding-top: 3px;
}
.ipTypes /deep/ .el-input{
  width: 50px;
}
.mainTypes {
  float: left;
  text-align: left;
  width: 256px;
}
.mainTypes /deep/ .el-input{
  width: 256px;
}
.warningNotifyAdd{
  color: #007ac0;
  text-decoration: underline
}
</style>
