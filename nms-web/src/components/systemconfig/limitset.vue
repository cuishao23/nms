<template>
  <div>
    <el-tabs v-model="tabSel">
      <el-tab-pane label="所有域" name="domains">
        <div class="domains-content">
          <div class="domains-content-line">
            <span class="domains-content-line-text">网管接入</span>
            <input type="text" @change="changeDomainData($event)" class="nms_domains_input" v-model="s_nms" />
            <span>个</span>
          </div>
          <div class="domains-content-line">
            <span class="domains-content-line-text">Pas接入</span>
            <input type="text" @change="changeDomainData($event)" class="pas_domains_input" v-model="s_pas"/>
            <span>个</span>
          </div>
          <div class="domains-content-line">
            <span class="domains-content-line-text">呼叫对</span>
            <input type="text" @change="changeDomainData($event)" class="callpair_domains_input" v-model="s_callpair"/>
            <span>对</span>
          </div>
          <div class="domains-content-line">
            <span class="domains-content-line-text">媒体资源使用率</span>
            <input type="text" @change="changeDomainData($event)" class="resource_domains_input" v-model="s_media_resource"/>
            <span>%</span>
          </div>
        </div>
      </el-tab-pane>
      <nms-big-dialog title="提示" :width="'400px'" :height="'177px'" :close-btn="true" ref="limitSetWarningDialog">
        <div slot="content">
          <div class="delTipsDiv">
              <span class="PromptImg"></span>
              <span>请输入合理数字</span>
          </div>
        </div>
      </nms-big-dialog>
      <el-tab-pane label="服务器" name="server">
        <div class="server-select-div">
          <el-select v-model="seviceDomain" value="" placeholder="所有服务域" filterable>
            <el-option
              v-for="(item,index) in seviceDomains"
              :key="index"
              :label="item.name"
              :value="item.moid">
            </el-option>
          </el-select>
          <el-select v-model="platformDomain" value="" placeholder="所有平台域" filterable>
            <el-option
              v-for="(item,index) in platformDomains"
              :key="index"
              :label="item.name"
              :value="item.moid">
            </el-option>
          </el-select>
          <el-select v-model="machineRoom" value="" placeholder="所有虚拟机房" filterable>
            <el-option
              v-for="(item,index) in machineRooms"
              :key="index"
              :label="item.name"
              :value="item.moid">
            </el-option>
          </el-select>
          <button class='search' @click="searchServers()" id="searchFloat"></button>
        </div>
        <div v-if="serverList.length === 0" class="no-info-tip">
          <span class="PromptImg"></span>
          <span>没有服务器信息！</span>
        </div>
        <div v-if="serverList.length > 0">
          <nms-pager-table :data="serverList" :fields="serverFields" :total-page="userTotalPage" :perPage="perPage" :biao-zhi="cage" v-model="curPage"/>
        </div>
        <nms-dialog title="阈值设置" :close-btn="true" :width="'400px'" :height="'400px'" ref="limitSetDialog"
                    @confirm="onSaveEdit()">
          <div slot="content">
            <div>
              <div class="lineDiv">
                <span class="setName">服务器名称</span>
                <span class="setValue">{{ editLineData.name }}</span>
              </div>
              <div class="lineDiv">
                <span class="setName">CPU阈值</span>
                <span class="setValue">
                  <input type="text" v-model="editLineData_cpu" @blur="examineMsg"/>
                  <span>%</span>
                </span>
              </div>
              <div class="lineDiv">
                <span class="setName">内存阈值</span>
                <span class="setValue">
                  <input type="text" v-model="editLineData_memory" @blur="examineMsg"/>
                  <span>%</span>
                </span>
              </div>
              <div class="lineDiv">
                <span class="setName">网口阈值</span>
                <span class="setValue">
                  <input type="text" v-model="editLineData_port" @blur="examineMsg"/>
                  <span>Mbps</span>
                </span>
              </div>
              <div class="lineDiv">
                <span class="setName">硬盘阈值</span>
                <span class="setValue">
                  <input type="text" v-model="editLineData_disk" @blur="examineMsg"/>
                  <span>%</span>
                </span>
              </div>
              <div class="lineDiv">
                <span class="setName">硬盘写入速度阈值</span>
                <span class="setValue">
                  <input type="text" v-model="editLineData_diskwritespeed" @blur="examineMsg"/>
                  <span>MB/s</span>
                </span>
              </div>
              <div class="lineDiv">
                <span class="setName">转发阈值</span>
                <span class="setValue">
                  <input type="text" v-model="editLineData_rateofflow" @blur="examineMsg"/>
                  <span>MB/s</span>
                </span>
              </div>
            </div>
          </div>
        </nms-dialog>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
  import api from '../../axios'
  import NmsPagerTable from "../../components/common/nms-pager-table";
  import NmsDialog from "../../components/common/nms-dialog";
  import NmsBigDialog from "components/common/nms-big-dialog";
  import * as setJs from "../../assets/js/set"

  export default {
    name: "limitset",
    components: {NmsDialog, NmsPagerTable, NmsBigDialog},
    data() {
      return {
        tabSel: "domains",
        s_pas: 0,
        s_callpair: 0,
        s_nms: 0,
        s_media_resource: 0,
        serverList: [],
        serverFields: [],

        domainDataType: '',
        domainDataValue: '',
        editLineData_cpu: '',
        editLineData_memory: '',
        editLineData_port: '',
        editLineData_disk: '',
        editLineData_diskwritespeed: '',
        editLineData_rateofflow: '',
        // 表格每页显示数量
        perPage: 10,
        userTotalPage: 1, // 总页数
        curPage: 1, // 当前页
        cage: 1, // 搜索当前页归1标志符
        TotalNum: 0,
        DomainTree: [],
        seviceDomain: 'all',
        platformDomain: 'all',
        machineRoom: 'all',
        seviceDomains: [],
        platformDomains: [],
        machineRooms: [],
        editLineData: {},
        domainData: {type: '', value: ''}
      }
    },
    mounted: function () {
      // 下拉框域信息获取
      api.getPlatformDomainTree().then((res) => {
        console.log(res)
        if (res.success == 1) {
          let serviceCount = 0
          let platformCount = 0
          let machineCount = 0
          this.DomainTree = res.data
          this.seviceDomains = []
          this.platformDomains = []
          this.machineRooms = []

          this.DomainTree.forEach(item => {
            if (item.type == "service" || item.type == "kernel") {
              this.seviceDomains.push(item)
              serviceCount++
            } else if (item.type === 'platform') {
              this.platformDomains.push(item)
              platformCount++
            } else if (item.type === 'machine_room') {
              this.machineRooms.push(item)
              machineCount++
            }
          })

          if (serviceCount == 0) {
            this.seviceDomains.unshift({
              "moid": "",
              "parent_moid": "",
              "name": "无下级域",
              "type": "server"
            })
            this.seviceDomain = ''
          } else {
            this.seviceDomains.unshift({
              "moid": "all",
              "parent_moid": "",
              "name": "所有服务域",
              "type": "server"
            })
            this.seviceDomain = 'all'
          }
          if (platformCount == 0) {
            this.platformDomains.unshift({
              "moid": "",
              "parent_moid": "",
              "name": "无下级域",
              "type": "domain"
            })
            this.platformDomain = ''
          } else {
            this.platformDomains.unshift({
              "moid": "all",
              "parent_moid": "",
              "name": "所有平台域",
              "type": "domain"
            })
            this.platformDomain = 'all'
          }
          if (machineCount == 0) {
            this.machineRooms.unshift({
              "moid": "",
              "parent_moid": "",
              "name": "无下级域",
              "type": "machine_room"
            })
            this.machineRoom = ''
          } else {
            this.machineRooms.unshift({
              "moid": "all",
              "parent_moid": "",
              "name": "所有虚拟机房",
              "type": "machine_room"
            })
            this.machineRoom = 'all'
          }
        }
      });
      // 获取所有域阈值
      api.getLimitInfo().then((res) => {
        if (res.status == undefined) {
          if (res.success == 1) {
            let limits = res.limits;
            this.s_pas = limits.s_pas;
            this.s_callpair = limits.s_callpair;
            this.s_nms = limits.s_nms;
            this.s_media_resource = limits.s_media_resource;
          } else {
            console.log(res)
          }
        } else if (res.error_code == 111401) {
          this.$router.push({name: 'forbidden'})
        }
      });
    },
    watch: {
      tabSel: function(newtab, oldtab) {
        if (newtab === 'domains') {
          api.getPlatformDomainTree().then((res) => {
            console.log(res)
            if (res.success == 1) {
              let serviceCount = 0
              let platformCount = 0
              let machineCount = 0
              this.DomainTree = res.data
              this.seviceDomains = []
              this.platformDomains = []
              this.machineRooms = []

              this.DomainTree.forEach(item => {
                if (item.type === "service" || item.type === "kernel") {
                  this.seviceDomains.push(item)
                  serviceCount++
                } else if (item.type === 'platform') {
                  this.platformDomains.push(item)
                  platformCount++
                } else if (item.type === 'machine_room') {
                  this.machineRooms.push(item)
                  machineCount++
                }
              })

              if (serviceCount === 0) {
                this.seviceDomains.unshift({
                  "moid": "",
                  "parent_moid": "",
                  "name": "无下级域",
                  "type": "server"
                })
                this.seviceDomain = ''
              } else {
                this.seviceDomains.unshift({
                  "moid": "all",
                  "parent_moid": "",
                  "name": "所有服务域",
                  "type": "server"
                })
                this.seviceDomain = 'all'
              }
              if (platformCount === 0) {
                this.platformDomains.unshift({
                  "moid": "",
                  "parent_moid": "",
                  "name": "无下级域",
                  "type": "domain"
                })
                this.platformDomain = ''
              } else {
                this.platformDomains.unshift({
                  "moid": "all",
                  "parent_moid": "",
                  "name": "所有平台域",
                  "type": "domain"
                })
                this.platformDomain = 'all'
              }
              if (machineCount === 0) {
                this.machineRooms.unshift({
                  "moid": "",
                  "parent_moid": "",
                  "name": "无下级域",
                  "type": "machine_room"
                })
                this.machineRoom = ''
              } else {
                this.machineRooms.unshift({
                  "moid": "all",
                  "parent_moid": "",
                  "name": "所有虚拟机房",
                  "type": "machine_room"
                })
                this.machineRoom = 'all'
              }
            }
          });
          // 获取所有域阈值
          api.getLimitInfo().then((res) => {
            console.log(res)
            if (res.status == undefined) {
              if (res.success == 1) {
                let limits = res.limits;
                this.s_pas = limits.s_pas;
                this.s_callpair = limits.s_callpair;
                this.s_nms = limits.s_nms;
                this.s_media_resource = limits.s_media_resource;
              }
            } else if (res.error_code == 111401) {
              this.$router.push({name: 'forbidden'})
            }
          });
        } else if (newtab == 'server') {
          // 获取服务器具体信息
          api.getServerLimitInfo({params: {newPageNum: 1, moid: 'all'}}).then((res) => {
            console.log(res)
            if (res.success == 1) {
              this.serverList = res.servers;
              this.TotalNum = res.TotalNum
              this.serverFields = setJs.getServerLimitTableFields(this.onEdit);
              this.userTotalPage = Math.ceil(res.TotalNum / this.perPage);
            }
          }).catch((error) => {
            console.log(error);
          });
        }
      },
      // 翻页跳转
      curPage: function(newPageNum, oldPageNum) {
        this.cage = 1
        if (newPageNum <= this.userTotalPage && newPageNum > 0) {
          api.getServerLimitInfo({params: {newPageNum: newPageNum, moid: this.machineRoom}}).then((res) => {
            console.log(res);
            if (res.success == 1) {
              this.serverList = res.servers;
              this.TotalNum = res.TotalNum
              this.serverFields = setJs.getServerLimitTableFields(this.onEdit);
              this.userTotalPage = Math.ceil(res.TotalNum / this.perPage);
            }
          }).catch((error) => {
            console.log(error);
          })
        }
      },
      // 下拉框服务域选择
      seviceDomain: function(newDomain, oldDomain) {
        let platformCount = 0
        let machineCount = 0
        this.platformDomains = []
        this.machineRooms = []
        if (newDomain === 'all') {
          this.DomainTree.forEach(item => {
            if (item.type === 'platform') {
              this.platformDomains.push(item)
              platformCount++
            } else if (item.type === 'machine_room') {
              this.machineRooms.push(item)
              machineCount++
            }
          })
          if (platformCount === 0) {
            this.platformDomains.unshift({
              "moid": "",
              "parent_moid": "",
              "name": "无下级域",
              "type": "domain"
            })
            this.platformDomain = ''
          } else {
            this.platformDomains.unshift({
              "moid": "all",
              "parent_moid": "",
              "name": "所有平台域",
              "type": "domain"
            })
            this.platformDomain = 'all'
          }
          if (machineCount === 0) {
            this.machineRooms.unshift({
              "moid": "",
              "parent_moid": "",
              "name": "无下级域",
              "type": "machine_room"
            })
            this.machineRoom = ''
          } else {
            this.machineRooms.unshift({
              "moid": "all",
              "parent_moid": "",
              "name": "所有虚拟机房",
              "type": "machine_room"
            })
            this.machineRoom = 'all'
          }
        } else if (newDomain == '') {
          this.platformDomains.unshift({
            "moid": "",
            "parent_moid": "",
            "name": "无下级域",
            "type": "domain"
          })
          this.platformDomain = ''
          this.machineRooms.unshift({
            "moid": "",
            "parent_moid": "",
            "name": "无下级域",
            "type": "machine_room"
          })
          this.machineRoom = ''
        } else {
          let kernel = 0
          this.DomainTree.forEach(domain => {
            if (domain.moid === newDomain && domain.type === 'kernel') {
              kernel = 1
            }
          })
          if (kernel === 0) {
            this.DomainTree.forEach(domain => {
              if (domain.parent_moid === newDomain && domain.type === 'platform' && domain.moid !== 'all' && domain.moid !== '') {
                this.platformDomains.push(domain)
                platformCount++
              }
            })
            this.platformDomains.forEach(domain => {
              this.DomainTree.forEach(room => {
                if (room.parent_moid === domain.moid && room.type === 'machine_room' && domain.moid !== 'all' && domain.moid !== '') {
                  this.machineRooms.push(room)
                  machineCount++
                }
              })
            })
            if (platformCount === 0) {
              this.platformDomains.unshift({
                "moid": "",
                "parent_moid": "",
                "name": "无下级域",
                "type": "domain"
              })
              this.platformDomain = ''
            } else {
              this.platformDomains.unshift({
                "moid": "all",
                "parent_moid": "",
                "name": "所有平台域",
                "type": "domain"
              })
              this.platformDomain = 'all'
            }
            if (machineCount === 0) {
              this.machineRooms.unshift({
                "moid": "",
                "parent_moid": "",
                "name": "无下级域",
                "type": "machine_room"
              })
              this.machineRoom = ''
            } else {
              this.machineRooms.unshift({
                "moid": "all",
                "parent_moid": "",
                "name": "所有虚拟机房",
                "type": "machine_room"
              })
              this.machineRoom = 'all'
            }
          } else if (kernel === 1) {
            this.DomainTree.forEach(item => {
              if (item.type === 'platform') {
                this.platformDomains.push(item)
                platformCount++
              } else if (item.type === 'machine_room') {
                this.machineRooms.push(item)
                machineCount++
              }
            })
            if (platformCount === 0) {
              this.platformDomains.unshift({
                "moid": "",
                "parent_moid": "",
                "name": "无下级域",
                "type": "domain"
              })
              this.platformDomain = ''
            } else {
              this.platformDomains.unshift({
                "moid": "all",
                "parent_moid": "",
                "name": "所有平台域",
                "type": "domain"
              })
              this.platformDomain = 'all'
            }
            if (machineCount === 0) {
              this.machineRooms.unshift({
                "moid": "",
                "parent_moid": "",
                "name": "无下级域",
                "type": "machine_room"
              })
              this.machineRoom = ''
            } else {
              this.machineRooms.unshift({
                "moid": "all",
                "parent_moid": "",
                "name": "所有虚拟机房",
                "type": "machine_room"
              })
              this.machineRoom = 'all'
            }
          }
        }
      },
      // 下拉框平台域选择
      platformDomain: function(newDomain, oldDomain) {
        this.machineRooms = []
        let machineCount = 0
        if (newDomain == 'all') {
          this.platformDomains.forEach(domain => {
            this.DomainTree.forEach(room => {
              if (room.parent_moid === domain.moid && room.type === 'machine_room' && domain.moid !== 'all' && domain.moid !== '') {
                this.machineRooms.push(room)
                machineCount++
              }
            })
          })
          if (machineCount == 0) {
            this.machineRooms.unshift({
              "moid": "",
              "parent_moid": "",
              "name": "无下级域",
              "type": "machine_room"
            })
            this.machineRoom = ''
          } else {
            this.machineRooms.unshift({
              "moid": "all",
              "parent_moid": "",
              "name": "所有虚拟机房",
              "type": "machine_room"
            })
            this.machineRoom = 'all'
          }
        } else if (newDomain == '') {
          this.machineRooms.unshift({
            "moid": "",
            "parent_moid": "",
            "name": "无下级域",
            "type": "machine_room"
          })
          this.machineRoom = ''
        } else {
          this.machineRooms = []
          this.DomainTree.forEach(room => {
            if (room.parent_moid === newDomain && room.type === 'machine_room') {
              this.machineRooms.push(room)
              machineCount++
            }
          })
          if (machineCount == 0) {
            this.machineRooms.unshift({
              "moid": "",
              "parent_moid": "",
              "name": "无下级域",
              "type": "machine_room"
            })
            this.machineRoom = ''
          } else {
            this.machineRooms.unshift({
              "moid": "all",
              "parent_moid": "",
              "name": "所有虚拟机房",
              "type": "machine_room"
            })
            this.machineRoom = 'all'
          }
        }
      },
    },
    methods: {
      // 搜索服务器
      searchServers: function () {
        this.cage = 2
        if (this.machineRoom != '') {
          console.log(this.machineRoom)
          api.getServerLimitInfo({params: {newPageNum: 1, moid: this.machineRoom}}).then((res) => {
            console.log(res);
            if (res.success == 1) {
              this.serverList = res.servers;
              this.TotalNum = res.TotalNum
              this.serverFields = setJs.getServerLimitTableFields(this.onEdit);
              this.userTotalPage = Math.ceil(res.TotalNum / this.perPage);
            }
          }).catch((error) => {
            console.log(error);
          });
        } else {
          this.serverList = []
          this.userTotalPage = 0
        }
      },
      // 阈值修改
      changeDomainData: function (data) {
        console.log('changedomain');
        var reg = /^[1-9]+[0-9]*]*$/;
        if ((!reg.test(data.srcElement.value)) || (data.srcElement.className == 'resource_domains_input' && data.srcElement.value > 100)) {
          console.log(data.srcElement.value);
          this.$refs.limitSetWarningDialog.open()
          api.getLimitInfo().then((res) => {
            console.log(res)
            if (res.status == undefined) {
              if (res.success == 1) {
                let limits = res.limits;
                this.s_pas = limits.s_pas;
                this.s_callpair = limits.s_callpair;
                this.s_nms = limits.s_nms;
                this.s_media_resource = limits.s_media_resource;
              }
            } else if (res.error_code == 111401) {
              this.$router.push({name: 'forbidden'})
            }
          });
        } else {
          console.log(data.srcElement.value);
          this.domainData.value = data.srcElement.value
          this.domainData.type = ''
          switch (data.srcElement.className) {
            case 'nms_domains_input':
              console.log('nms');
              this.domainData.type = 'nms'
              break;
            case 'pas_domains_input':
              console.log('pas');
              this.domainData.type = 'pas'
              break;
            case 'callpair_domains_input':
              console.log('callpair');
              this.domainData.type = 'callpair'
              break;
            case 'resource_domains_input':
              console.log('resource');
              this.domainData.type = 'resource'
              break;
            default:
              console.log('typeWarning');
              this.domainData.type = ''
              break;
          }
          if (this.domainData.type && this.domainData.value) {
            api.setLimitInfo(this.domainData).then((res) => {
              console.log(res)
              if (res.success == 1) {
                this.successDialog.open('修改成功')
              } else {
                this.errorDialog.open('修改失败')
              }
              api.getLimitInfo().then((res) => {
                console.log(res)
                if (res.status == undefined) {
                  if (res.success == 1) {
                    let limits = res.limits;
                    this.s_pas = limits.s_pas;
                    this.s_callpair = limits.s_callpair;
                    this.s_nms = limits.s_nms;
                    this.s_media_resource = limits.s_media_resource;
                  }
                } else if (res.error_code == 111401) {
                  this.$router.push({name: 'forbidden'})
                }
              });
            });
          } else {
            console.log('dataWarning');
          }
        }
      },
      examineMsg: function() {
        var numReg = /^[1-9]+[0-9]*]*$/
        var numRe = new RegExp(numReg)
        if (this.editLineData_cpu !== '') {
          if (!numRe.test(this.editLineData_cpu)) {
            this.errorDialog.open('CPU阈值必须是不为零的数')
            this.editLineData_cpu = this.editLineData.cpu
          } else if (this.editLineData_cpu > 100) {
            this.errorDialog.open('CPU阈值必须在1-100之间')
            this.editLineData_cpu = this.editLineData.cpu
          }
        } else {
          this.errorDialog.open('CPU阈值不能为空')
          this.editLineData_cpu = this.editLineData.cpu
        }
        if (this.editLineData_memory !== '') {
          if (!numRe.test(this.editLineData_memory)) {
            this.errorDialog.open('内存阈值必须是不为零的数')
            this.editLineData_memory = this.editLineData.memory
          } else if (this.editLineData_memory > 100) {
            this.errorDialog.open('内存阈值必须在1-100之间')
            this.editLineData_memory = this.editLineData.memory
          }
        } else {
          this.errorDialog.open('内存阈值不能为空')
          this.editLineData_memory = this.editLineData.memory
        }
        if (this.editLineData_disk !== '') {
          if (!numRe.test(this.editLineData_disk)) {
            this.errorDialog.open('硬盘阈值必须是不为零的数')
            this.editLineData_disk = this.editLineData.disk
          } else if (this.editLineData_disk > 100) {
            this.errorDialog.open('硬盘阈值必须在1-100之间')
            this.editLineData_disk = this.editLineData.disk
          }
        } else {
          this.errorDialog.open('硬盘阈值不能为空')
          this.editLineData_disk = this.editLineData.disk
        }
        if (this.editLineData_port !== '') {
          if (!numRe.test(this.editLineData_port)) {
            this.errorDialog.open('网口阈值必须是不为零的数')
            this.editLineData_port = this.editLineData.port
          } else if (this.editLineData_port > 9999) {
            this.errorDialog.open('网口阈值必须在1-9999之间')
            this.editLineData_port = this.editLineData.port
          }
        } else {
          this.errorDialog.open('网口阈值不能为空')
          this.editLineData_port = this.editLineData.port
        }
        if (this.editLineData_diskwritespeed !== '') {
          if (!numRe.test(this.editLineData_diskwritespeed)) {
            this.errorDialog.open('硬盘写入速度阈值必须是不为零的数')
            this.editLineData_diskwritespeed = this.editLineData.diskwritespeed
          } else if (this.editLineData_diskwritespeed > 9999) {
            this.errorDialog.open('硬盘写入速度阈值必须在1-9999之间')
            this.editLineData_diskwritespeed = this.editLineData.diskwritespeed
          }
        } else {
          this.errorDialog.open('硬盘写入速度阈值不能为空')
          this.editLineData_diskwritespeed = this.editLineData.diskwritespeed
        }
        if (this.editLineData_rateofflow !== '') {
          if (!numRe.test(this.editLineData_rateofflow)) {
            this.errorDialog.open('转发阈值必须为是不为零的数')
            this.editLineData_rateofflow = this.editLineData.rateofflow
          } else if (this.editLineData_rateofflow > 9999) {
            this.errorDialog.open('转发阈值必须在1-9999之间')
            this.editLineData_rateofflow = this.editLineData.rateofflow
          }
        } else {
          this.errorDialog.open('转发阈值不能为空')
          this.editLineData_rateofflow = this.editLineData.rateofflow
        }
      },
      onEdit: function (rowData) {
        // 存储修改前的数据
        this.editLineData = rowData;
        this.editLineData_cpu = this.editLineData.cpu
        this.editLineData_memory = this.editLineData.memory
        this.editLineData_port = this.editLineData.port
        this.editLineData_disk = this.editLineData.disk
        this.editLineData_diskwritespeed = this.editLineData.diskwritespeed
        this.editLineData_rateofflow = this.editLineData.rateofflow
        this.$refs.limitSetDialog.open()
      },
      onSaveEdit: function () {
        this.editLineData.cpu = this.editLineData_cpu
        this.editLineData.memory = this.editLineData_memory
        this.editLineData.port = this.editLineData_port
        this.editLineData.disk = this.editLineData_disk
        this.editLineData.diskwritespeed = this.editLineData_diskwritespeed
        this.editLineData.rateofflow = this.editLineData_rateofflow
        console.log(this.editLineData)
        api.setServerLimitInfo(this.editLineData).then((res) => {
          console.log(res)
          if (res.success == 1) {
            this.errorDialog.open('保存成功')
          } else {
            this.errorDialog.open('保存失败')
          }
          api.getServerLimitInfo({params: {newPageNum: 1, moid: this.machineRoom}}).then((res) => {
            console.log(res)
            if (res.success == 1) {
              this.cage = 2
              this.serverList = res.servers;
              this.TotalNum = res.TotalNum
              this.serverFields = setJs.getServerLimitTableFields(this.onEdit);
              this.userTotalPage = Math.ceil(res.TotalNum / this.perPage);
            } else {
              this.errorDialog.open('刷新失败')
            }
          })
        });
      }
    }
  }
</script>

<style scoped>
  .delTipsDiv {
    padding: 50px;
    text-align: center;
  }
  .domains-content {
    text-align: left;
    margin: 36px 0 38px 0;
  }

  .domains-content-line {
    margin-top: 28px;
  }

  .domains-content-line span {
    font-size: 12px;
    color: #4e4e4e;
    display: inline-block;
  }

  .domains-content-line-text {
    width: 110px;
  }
  .nms_domains_input {
    width: 120px;
    font-size: 12px;
    color: #616060;
    border-bottom: 1px solid #949799;
    cursor: pointer;
    padding: 0 0 2px 1px;
  }
  .pas_domains_input {
    width: 120px;
    font-size: 12px;
    color: #616060;
    border-bottom: 1px solid #949799;
    cursor: pointer;
    padding: 0 0 2px 1px;
  }
  .callpair_domains_input {
    width: 120px;
    font-size: 12px;
    color: #616060;
    border-bottom: 1px solid #949799;
    cursor: pointer;
    padding: 0 0 2px 1px;
  }
  .resource_domains_input {
    width: 120px;
    font-size: 12px;
    color: #616060;
    border-bottom: 1px solid #949799;
    cursor: pointer;
    padding: 0 0 2px 1px;
  }

  .server-select-div {
    text-align: left;
    margin-bottom: 13px;
  }

  .lineDiv {
    margin-top: 28px;
    text-align: center;
  }
  .setValue input[data-v-5cc8c685] {
      width: 70px;
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

  .setValue input {
    width: 59px;
  }
</style>
