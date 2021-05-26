<template>
  <div class="warningContent">
    <div v-if="this.tabSel === 'subWarningCode'" class="addBtn">
      <button class="normal-btn" @click="onSubWarningCode()" v-if="!useAble">设置告警项</button>
      <button class="normal-btn" :class="{disable: useAble}" :disabled="useAble" v-if="useAble">告警保存中</button>
      <nms-big-dialog title="设置告警项" ref="setWarningDialog" @confirm="onWarningTreeSet()">
        <div slot="content">
          <warning-tree :data="warningTreeData" @sendWarningdata="sendwarningData($event)" :flash="checkFlash"/>
        </div>
      </nms-big-dialog>
    </div>
    <div v-if="this.tabSel === 'warningNotify'" class="addBtn">
      <button class="normal-btn" @click="onAddWarningNotify()">新增</button>
      <nms-dialog title="新增告警通知" ref="addWarningNotify" @confirm="OnSaveTimingTask()" :width="'544px'" :height="'512px'">
        <div class="textleft" slot="content">
          <div class="fontCommon">
            <span class="modifyCommon">通知人员</span>
            <input type="text" class="backNamePathCommon" placeholder="姓名" v-model="inputName" @blur="examineMsg"/>
            <span style="color:red">*</span>
          </div>
          <div class="fontCommon">
            <span class="modifyCommon">邮箱通知</span>
            <input type="text" class="backNamePathCommon" placeholder="邮箱" v-model="inputEmail" @blur="examineMsg"/>
          </div>
          <div class="fontCommon">
            <span class="modifyCommon">手机通知</span>
            <input type="text" class="backNamePathCommon" placeholder="手机号" v-model="inputPhone" @blur="examineMsg"/>
          </div>
          <div class="fontCommon">
            <span class="modifyCommon">微信通知</span>
            <input type="text" class="backNamePathCommon" placeholder="微信号" v-model="inputWechat" @blur="examineMsg"/>
          </div>
          <div class="fontCommon">
            <span class="specialCommon">告警项</span>
            <div class="specialPathCommon" :style="{width: 250 + 'px', height: 270 + 'px', overflowY: 'auto'}">
              <setwarning-tree :width='230' :height='250' :data="warningTreeData" @getnodes="getNodes($event)" :warningcheck="warningEditList" :checkClear="warningCheckClear"/>
            </div>
          </div>
        </div>
      </nms-dialog>
    </div>
    <el-tabs v-model="tabSel">
      <el-tab-pane label="已选告警" name="subWarningCode">
        <div v-if="serviceWarningList.length === 0 && deviceWarningList.length === 0 && mcuWarningList.length === 0 && otherWarningList.length === 0 " class="warningNotify">
          <span class="PromptImg"></span>
          <span class="warningNotifyNone">当前未选择任何告警项，点击右侧<a class="warningNotifyAdd" v-on:click="onSubWarningCode()">设置告警项</a>进行更改</span>
        </div>
        <div v-if="serviceWarningList.length > 0 || deviceWarningList.length > 0 || mcuWarningList.length > 0 || otherWarningList.length > 0 ">
          <div v-if="serviceWarningList.length > 0">
            <div class="warningLine">
              <span class="warningName">服务器告警</span>
              <span class="warningFont">已选<span class="warningNum">{{ serviceWarningNum }}</span></span>
            </div>
            <div class="warningDiv">
              <div class="warningDetail" v-for="(item,index) in serviceWarningList" :key="index">{{ item.name }}</div>
            </div>
          </div>
          <div v-if="deviceWarningList.length > 0">
            <div class="warningLine">
              <span class="warningName">终端设备告警</span>
              <span class="warningFont">已选<span class="warningNum">{{ deviceWarningNum }}</span></span>
            </div>
            <div class="warningDiv">
              <div class="warningDetail" v-for="(item,index) in deviceWarningList" :key="index">{{ item.name }}</div>
            </div>
          </div>
          <div v-if="mcuWarningList.length > 0">
            <div class="warningLine">
              <span class="warningName">MCU告警</span>
              <span class="warningFont">已选<span class="warningNum">{{ mcuWarningNum }}</span></span>
            </div>
            <div class="warningDiv">
              <div class="warningDetail" v-for="(item,index) in mcuWarningList" :key="index">{{ item.name }}</div>
            </div>
          </div>
          <div v-if="otherWarningList.length > 0">
            <div class="warningLine">
              <span class="warningName">其他告警</span>
              <span class="warningFont">已选<span class="warningNum">{{ otherWarningNum }}</span></span>
            </div>
            <div class="warningDiv">
              <div class="warningDetail" v-for="(item,index) in otherWarningList" :key="index">{{ item.name }}</div>
            </div>
          </div>
        </div>
      </el-tab-pane>
      <el-tab-pane label="告警通知" name="warningNotify">
        <div v-if="warningNotifyList.length === 0"  class="warningNotify">
          <span class="PromptImg"></span>
          <span class="warningNotifyNone">尚无告警通知规则，请先<a class="warningNotifyAdd" v-on:click="addNotify()">新增告警通知规则</a></span>
        </div>
        <div v-if="warningNotifyList.length > 0">
          <nms-pager-table v-if="NotifyReset" :data="warningNotifyList" :fields="warningNotifyFields" :total-page="userTotalPage" :perPage="perPage" :biao-zhi="cage" v-model="curPage"/>
        </div>
        <nms-dialog title="编辑告警通知" :close-btn="true" :width="'544px'" :height="'512px'" ref="warningEditDialog" @confirm="onSaveEdit()">
          <div class="textleft" slot="content">
            <div class="fontCommon">
              <span class="modifyCommon">通知人员</span>
              <span class="backNamePathCommon">{{ editLineData.name }}</span>
            </div>
            <div class="fontCommon">
              <span class="modifyCommon">邮箱通知</span>
              <input type="text" class="backNamePathCommon" placeholder="邮箱" v-model="email_line_data" @blur="examineChange"/>
            </div>
            <div class="fontCommon">
              <span class="modifyCommon">手机通知</span>
              <input type="text" class="backNamePathCommon" placeholder="手机号" v-model="phone_line_data" @blur="examineChange"/>
            </div>
            <div class="fontCommon">
              <span class="modifyCommon">微信通知</span>
              <input type="text" class="backNamePathCommon" placeholder="微信号" v-model="wechat_line_data" @blur="examineChange"/>
            </div>
            <div class="fontCommon">
              <span class="specialCommon">告警项</span>
              <div class="specialPathCommon" :style="{width: 250 + 'px', height: 270 + 'px', overflowY: 'auto'}">
                <setwarning-tree :width='230' :height='250' :data="warningTreeData" @getnodes="getNodesdetail($event)" :warningcheck="warningEditList"/>
              </div>
            </div>
          </div>
        </nms-dialog>
        <nms-dialog title="告警通知详情" :width="'720px'" :height="'560px'" :confirm-btn="false" :close-btn="true" ref="warningDetailDialog">
          <div slot="content">
            <div class="warningMassage">
              <div class="notifyIteam">
                <span class="iteamKey">通知人员</span>
                <span class="iteamValue">{{ detailLineData.name }}</span>
              </div>
              <div class="notifyIteam">
                <span class="iteamKey">邮件通知</span>
                <span class="iteamValue">{{ detailLineData.email }}</span>
              </div>
              <div class="notifyIteam">
                <span class="iteamKey">短信通知</span>
                <span class="iteamValue">{{ detailLineData.phone }}</span>
              </div>
              <div class="notifyIteam">
                <span class="iteamKey">微信通知</span>
                <span class="iteamValue">{{ detailLineData.wechat }}</span>
              </div>
            </div>
            <div v-if="serviceWarningDetail.length === 0 && deviceWarningDetail.length === 0 && mcuWarningDetail.length === 0 && otherWarningDetail.length === 0 ">
              <span style="font-size: 14px; margin-left: 10px">该人员未选择任何告警项</span>
            </div>
            <el-tabs v-model="userWarningType" class="warningTab">
              <el-tab-pane label="服务器告警" name="serviceWarning" v-if="serviceWarningDetail.length > 0">
                <div class="warningLinelist">
                  <span class="warningFontlist">已选告警项：<span class="warningNumlist">{{ serviceWarningCount }}</span></span>
                </div>
                <div class="warningDivlist">
                  <div class="warningDetaillist" v-for="(item,index) in serviceWarningDetail" :key="index">{{ item.name }}</div>
                </div>
              </el-tab-pane>
              <el-tab-pane label="终端告警" name="deviceWarning" v-if="deviceWarningDetail.length > 0">
                <div class="warningLinelist">
                  <span class="warningFontlist">已选告警项：<span class="warningNumlist">{{ deviceWarningCount }}</span></span>
                </div>
                <div class="warningDivlist">
                  <div class="warningDetaillist" v-for="(item,index) in deviceWarningDetail" :key="index">{{ item.name }}</div>
                </div>
              </el-tab-pane>
              <el-tab-pane label="MCU告警" name="mcuWarning" v-if="mcuWarningDetail.length > 0">
                <div class="warningLinelist">
                  <span class="warningFontlist">已选告警项：<span class="warningNumlist">{{ mcuWarningCount }}</span></span>
                </div>
                <div class="warningDivlist">
                  <div class="warningDetaillist" v-for="(item,index) in mcuWarningDetail" :key="index">{{ item.name }}</div>
                </div>
              </el-tab-pane>
              <el-tab-pane label="其他告警" name="otherWarning" v-if="otherWarningDetail.length > 0">
                <div class="warningLinelist">
                  <span class="warningFontlist">已选告警项：<span class="warningNumlist">{{ otherWarningCount }}</span></span>
                </div>
                <div class="warningDivlist">
                  <div class="warningDetaillist" v-for="(item,index) in otherWarningDetail" :key="index">{{ item.name }}</div>
                </div>
              </el-tab-pane>
            </el-tabs>
          </div>
        </nms-dialog>
        <nms-dialog title="提示" :width="'400px'" :height="'152px'" :close-btn="true" ref="warningDeleteDialog"
                    @confirm="OnWarningNotifyDelete()">
          <div slot="content">
            <div class="delTipsDiv">
              <span class="PromptImg"></span>
              <span>确认删除该条规则吗？</span>
            </div>
          </div>
        </nms-dialog>
      </el-tab-pane>

      <el-tab-pane label="告警过滤" name="warningFilter" style="cursor:default">
        <div class="warningFilterContent">
          <div>
            <div class="firstTitle">首页告警显示</div>
            <div class="content">
              <div class="checkWarningLevel">
                <span class="setName">服务器告警</span>
                <el-checkbox-group v-model="serviceWarningCheckList" style="float:left" @change="serviceCheckedChange">
                  <el-checkbox label="严重"></el-checkbox>
                  <el-checkbox label="重要"></el-checkbox>
                  <el-checkbox label="一般"></el-checkbox>
                </el-checkbox-group>
              </div>
              <div class="checkWarningLevel">
                <span class="setName">终端告警</span>
                <el-checkbox-group v-model="terminalWarningCheckList" style="float:left" @change="terminalCheckedChange">
                  <el-checkbox label="严重"></el-checkbox>
                  <el-checkbox label="重要"></el-checkbox>
                  <el-checkbox label="一般"></el-checkbox>
                </el-checkbox-group>
              </div>
            </div>
          </div>
          <div>
            <div class="secondTitle">
              <span>已选暂停告警({{ domainCount }})</span>
              <button class="normal-btn setBtn" @click="onStopWarningCode()">设置暂停告警</button>
              <nms-big-dialog title="设置暂停告警" :close-btn="true" @confirm="onStopwarning()" @cancel="offStopwarning()" ref="setStopWarning" width="720px" height="500px">
                <div slot="content">
                  <stopwarning-tree v-if="stopwarningReset" @reSet="resetStopWarning($event)" :confirm="stopwarningConfirm"></stopwarning-tree>
                </div>
              </nms-big-dialog>
            </div>
            <div>
              <nms-pager-table v-if="warningReset" :data="warningFilterList" :fields="warningFilterFields" :total-page="warningTotalPage" :perPage="perPage" :biao-zhi="warningcage" v-model="warningcurPage"/>
            </div>
          </div>
        </div>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
  import NmsPagerTable from "../../components/common/nms-pager-table";
  import api from '../../axios';
  import * as setJs from "../../assets/js/set";
  import NmsDialog from "../../components/common/nms-dialog";
  import NmsTransfer from "../../components/common/nms-transfer";
  import StopwarningTree from "../../components/common/stopwarning-tree";
  import WarningTree from "../../components/common/warning-tree";
  import NmsBigDialog from "../../components/common/nms-big-dialog";
  import SubwarningTree from "../../components/common/subwarning-tree";
  import StopwarningTransfer from "../../components/common/stopwarning-transfer";
  import SetwarningTree from "components/common/setwarning-tree";

  export default {
    name: "warningset",
    inject: ["reload"],
    components: {SetwarningTree, StopwarningTransfer, StopwarningTree, NmsTransfer, SubwarningTree, NmsBigDialog, WarningTree, NmsDialog, NmsPagerTable},
    data() {
      return {
        stopwarningConfirm: 0,
        stopwarningReset: true,
        useAble: false,
        serviceWarningCheckList: [],
        terminalWarningCheckList: [],
        serverWarningLevel: [],
        terminalWarningLevel: [],
        serverWarningLevelList: '',
        terminalWarningLevelList: '',
        inputEmail: '',
        inputWechat: '',
        inputPhone: '',
        inputName: '',
        warningMsg: {
          email: '',
          wechat: '',
          phone: '',
          code_list: '',
          name: '',
        },
        tabSel: "subWarningCode",
        tabSel2: "notifyPhoneEmail",
        subWarningList: [],
        warningNotifyList: [],
        warningNotifyFields: [],
        warningFilterList: [],
        warningTreeData: [],
        warningFilterFields: [{
          prop: 'name',
          label: '已选暂停告警'
        }],
        // 已选告警
        serviceWarningNum: 0,
        serviceNum: 0,
        serviceWarningList: [],
        serviceWarning: [],
        deviceWarningNum: 0,
        deviceNum: 0,
        deviceWarningList: [],
        deviceWarning: [],
        mcuWarningNum: 0,
        mcuNum: 0,
        mcuWarningList: [],
        mcuWarning: [],
        otherWarningNum: 0,
        otherNum: 0,
        otherWarningList: [],
        otherWarning: [],
        checkFlash: false,
        sendCheck: 0,
        // 告警通知
        userWarningType: '',
        sendwarningdata: [],
        NotifyReset: true,
        serviceWarningType: [],
        deviceWarningType: [],
        mcuWarningType: [],
        otherWarningType: [],
        serviceWarningDetail: [],
        deviceWarningDetail: [],
        mcuWarningDetail: [],
        otherWarningDetail: [],
        serviceWarningCount: 0,
        deviceWarningCount: 0,
        mcuWarningCount: 0,
        otherWarningCount: 0,
        phone_line_data: [],
        email_line_data: [],
        wechat_line_data: [],
        warning_line_data: [],
        warning_line: [],
        warningReset: true,
        warningCheckClear: false,
        // 表格每页显示数量
        perPage: 10,
        userTotalPage: 1, // 总页数
        curPage: 1, // 当前页
        cage: 1, // 搜索当前页归1标志符 置二归一
        deviceTotalNum: 0,
        // 暂停告警页数
        warningTotalPage: 1,
        warningcage: 1,
        warningcurPage: 1,
        warningTotalNum: 0,
        domainCount: 0,
        detailLineData: {},
        editLineData: {},
        warningDetailList: [],
        warningEditList: [],
        subwarningCode: [],
        stopwarning: {},
        stopwarningroom: [],
        Domaintree: [],
        stopwarningDomain: [],
        stopedwarningDomain: [],
        warningAllList: [],
        delSendWarning: 0,
      }
    },
    mounted: function () {
      api.getSubWarningCode().then((res) => {
        if (res.success == 1) {
          console.log(res)
          this.subwarningCode = res.subwarningcode;
          api.getWarningTree().then((res) => {
            console.log(res)
            this.warningTreeData = res.warning_trees;
            this.serviceWarningType = res.warning_trees[2].children
            this.deviceWarningType = res.warning_trees[3].children
            this.mcuWarningType = res.warning_trees[1].children
            this.otherWarningType = res.warning_trees[0].children
            console.log(this.warningTreeData)
            this.subwarningCode.forEach(item => {
              let count = 0
              if (count == 0) {
                this.warningTreeData[0].children.forEach(warn => {
                  if (warn.code === item.code) {
                    this.otherWarning.push({'name': warn.name})
                    this.otherNum++;
                    count = 1
                  }
                })
              }
              if (count == 0) {
                this.warningTreeData[1].children.forEach(warn => {
                  if (warn.code === item.code) {
                    this.mcuWarning.push({'name': warn.name})
                    this.mcuNum++;
                    count = 1
                  }
                })
              }
              if (count == 0) {
                this.warningTreeData[2].children.forEach(warn => {
                  if (warn.code === item.code) {
                    this.serviceWarning.push({'name': warn.name})
                    this.serviceNum++;
                    count = 1
                  }
                })
              }
              if (count == 0) {
                this.warningTreeData[3].children.forEach(warn => {
                  if (warn.code === item.code) {
                    this.deviceWarning.push({'name': warn.name})
                    this.deviceNum++;
                    count = 1
                  }
                })
              }
            });
            this.serviceWarningList = this.serviceWarning
            this.deviceWarningList = this.deviceWarning
            this.mcuWarningList = this.mcuWarning
            this.otherWarningList = this.otherWarning
            this.serviceWarningNum = this.serviceNum;
            this.deviceWarningNum = this.deviceNum;
            this.mcuWarningNum = this.mcuNum;
            this.otherWarningNum = this.otherNum;
          })
        }
      });
    },
    watch: {
      tabSel: function(newtab, oldtab) {
        if (newtab == 'subWarningCode') {
          api.getSubWarningCode().then((res) => {
            console.log(res)
            if (res.success == 1) {
              this.otherWarning = []
              this.otherNum = 0
              this.mcuWarning = []
              this.mcuNum = 0
              this.serviceWarning = []
              this.serviceNum = 0
              this.deviceWarning = []
              this.deviceNum = 0
              this.subwarningCode = res.subwarningcode;
              api.getWarningTree().then((res) => {
                console.log(res)
                this.warningTreeData = res.warning_trees;
                this.serviceWarningType = res.warning_trees[2].children
                this.deviceWarningType = res.warning_trees[3].children
                this.mcuWarningType = res.warning_trees[1].children
                this.otherWarningType = res.warning_trees[0].children
                this.subwarningCode.forEach(item => {
                  let count = 0
                  if (count == 0) {
                    this.warningTreeData[0].children.forEach(warn => {
                      if (warn.code === item.code) {
                        this.otherWarning.push({'name': warn.name})
                        this.otherNum++;
                        count = 1
                      }
                    })
                  }
                  if (count == 0) {
                    this.warningTreeData[1].children.forEach(warn => {
                      if (warn.code === item.code) {
                        this.mcuWarning.push({'name': warn.name})
                        this.mcuNum++;
                        count = 1
                      }
                    })
                  }
                  if (count == 0) {
                    this.warningTreeData[2].children.forEach(warn => {
                      if (warn.code === item.code) {
                        this.serviceWarning.push({'name': warn.name})
                        this.serviceNum++;
                        count = 1
                      }
                    })
                  }
                  if (count == 0) {
                    this.warningTreeData[3].children.forEach(warn => {
                      if (warn.code === item.code) {
                        this.deviceWarning.push({'name': warn.name})
                        this.deviceNum++;
                        count = 1
                      }
                    })
                  }
                });
                this.serviceWarningList = this.serviceWarning
                this.deviceWarningList = this.deviceWarning
                this.mcuWarningList = this.mcuWarning
                this.otherWarningList = this.otherWarning
                this.serviceWarningNum = this.serviceNum;
                this.deviceWarningNum = this.deviceNum;
                this.mcuWarningNum = this.mcuNum;
                this.otherWarningNum = this.otherNum;
              })
            }
          });
        } else if (newtab == 'warningNotify') {
          // 获得告警通知
          api.getWarningNotifyInfo({params: {newPageNum: 1}}).then((res) => {
            console.log(res)
            if (res.success == 1) {
              this.warningNotifyList = []
              this.warningNotifyList = res.warning_notify_list;
              this.warningNotifyFields = setJs.getWarningNotifyTableFields(this.editCallback, this.detailCallback, this.deleteCallback);
              this.userTotalPage = Math.ceil(res.TotalNum / this.perPage)
              this.deviceTotalNum = res.TotalNum
              this.cage = 2
            }
          });
        } else if (newtab == 'warningFilter') {
          // 获得暂停告警列表
          api.getStopWarningInfo({params: {newPageNum: 1}}).then((res) => {
            console.log(res)
            if (res.success == 1) {
              this.warningFilterList = []
              this.warningFilterList = res.stopWarnings;
              this.warningAllList = res.allWarnings
              this.warningTotalPage = Math.ceil(res.TotalNum / this.perPage)
              this.warningTotalNum = res.TotalNum
              this.domainCount = this.warningTotalNum;
              this.warningcage = 2
            }
          })
          api.warningLevel().then((res) => {
            console.log(res)
            if (res.status == undefined) {
              if (res.success == 1) {
                console.log(res.level);
                this.serverWarningLevel = res.level.serverlevel.split(',');
                this.terminalWarningLevel = res.level.terminallevel.split(',');
                this.serviceWarningCheckList = []
                this.terminalWarningCheckList = []
                this.serverWarningLevel.forEach(server => {
                  if (server === 'critical') {
                    this.serviceWarningCheckList.push('严重')
                  } else if (server === 'important') {
                    this.serviceWarningCheckList.push('重要')
                  } else if (server === 'normal') {
                    this.serviceWarningCheckList.push('一般')
                  }
                })
                this.terminalWarningLevel.forEach(terminal => {
                  if (terminal === 'critical') {
                    this.terminalWarningCheckList.push('严重')
                  } else if (terminal === 'important') {
                    this.terminalWarningCheckList.push('重要')
                  } else if (terminal === 'normal') {
                    this.terminalWarningCheckList.push('一般')
                  }
                })
              }
            } else if (res.error_code == 111401) {
              this.$router.push({name: 'forbidden'})
            }
          });
        }
      },
      // 翻页跳转
      curPage: function(newPageNum, oldPageNum) {
        this.cage = 1
        if (newPageNum <= this.userTotalPage && newPageNum > 0) {
          api.getWarningNotifyInfo({params: {newPageNum: newPageNum}}).then((res) => {
            console.log(res)
            if (res.success == 1) {
              this.warningNotifyList = res.warning_notify_list;
              this.warningNotifyFields = setJs.getWarningNotifyTableFields(this.editCallback, this.detailCallback, this.deleteCallback);
              this.userTotalPage = Math.ceil(res.TotalNum / this.perPage)
              this.deviceTotalNum = res.TotalNum
            }
          }).catch((error) => {
            console.log(error);
          })
        }
      },
      warningcurPage: function(newPageNum, oldPageNum) {
        this.warningcage = 1
        if (newPageNum <= this.warningTotalPage && newPageNum > 0) {
          api.getStopWarningInfo({params: {newPageNum: newPageNum}}).then((res) => {
            console.log(res)
            if (res.success == 1) {
              this.warningFilterList = res.stopWarnings;
              this.warningTotalPage = Math.ceil(res.TotalNum / this.perPage)
              this.warningTotalNum = res.TotalNum
              this.domainCount = this.warningTotalNum;
            }
          }).catch((error) => {
            console.log(error);
          })
        }
      },
    },
    methods: {
      examineMsg: function() {
        var numReg = /^[0-9]*$/
        var emailReg = /^(\w+[@][a-zA-Z0-9_]+(\.[a-zA-Z0-9_]+)+)*$/
        var wechatReg = /^([a-zA-Z0-9_-]{6,20})*$/
        var nameReg = /^[A-Za-z0-9\u4e00-\u9fa5]+$/
        var numRe = new RegExp(numReg)
        var emailRe = new RegExp(emailReg)
        var wechatRe = new RegExp(wechatReg)
        var nameRe = new RegExp(nameReg)

        if (this.inputName !== '') {
          if (this.inputName.length > 12) {
            this.errorDialog.open('请填写12字符以内内容')
            this.inputName = ''
          } else {
            if (!nameRe.test(this.inputName)) {
              this.errorDialog.open('请填写中文、数字和英文')
              this.inputName = ''
            }
          }
        }
        // } else {
        //   this.errorDialog.open('请填写中文、数字和英文')
        //   this.inputName = ''
        // }

        if (this.inputPhone !== '') {
          if (this.inputPhone.length !== 11) {
            this.errorDialog.open('请填写有效的11位手机号')
            this.inputPhone = ''
          }
        }
        if (!numRe.test(this.inputPhone)) {
          this.errorDialog.open('手机号码必须为数字')
          this.inputPhone = ''
        }

        if (this.inputEmail !== '') {
          if (!emailRe.test(this.inputEmail)) {
            this.errorDialog.open('邮箱格式不合理')
            this.inputEmail = ''
          }
        }
        if (this.inputWechat !== '') {
          if (!wechatRe.test(this.inputWechat)) {
            this.errorDialog.open('微信格式不合理（需6-20个字母、数字、下划线和减号）')
            this.inputWechat = ''
          }
        }

        // if (this.inputPhone == '' && this.inputEmail == '' && this.inputWechat == '') {
        //   this.errorDialog.open('请至少填写一种联系方式')
        // }
      },
      examineChange: function() {
        var numReg = /^[0-9]*$/
        var emailReg = /^(\w+[@][a-zA-Z0-9_]+(\.[a-zA-Z0-9_]+)+)*$/
        var wechatReg = /^([a-zA-Z0-9_-]{6,20})*$/
        var numRe = new RegExp(numReg)
        var emailRe = new RegExp(emailReg)
        var wechatRe = new RegExp(wechatReg)
        if (this.editLineData.phone != '') {
            if (!numRe.test(this.phone_line_data)) {
              this.errorDialog.open('手机号码必须为数字')
              this.phone_line_data = this.editLineData.phone
            }
        } else {
          if (this.phone_line_data != '') {
            if (!numRe.test(this.phone_line_data)) {
              this.errorDialog.open('手机号码必须为数字')
              this.phone_line_data = this.editLineData.phone
            } else {
              if (this.phone_line_data.length != 11) {
                this.errorDialog.open('请填写有效的11位手机号')
                this.phone_line_data = this.editLineData.phone
              }
            }
          }
        }

        if (this.editLineData.email != '') {
            if (!emailRe.test(this.email_line_data)) {
              this.errorDialog.open('邮箱格式不合理')
              this.email_line_data = this.editLineData.email
            }
        } else {
          if (this.email_line_data != '') {
            if (!emailRe.test(this.email_line_data)) {
              this.errorDialog.open('邮箱格式不合理')
              this.email_line_data = this.editLineData.email
            }
          }
        }
        if (this.editLineData.wechat != '') {
            if (!wechatRe.test(this.wechat_line_data)) {
              this.errorDialog.open('微信格式不合理（需6-20个字母、数字、下划线和减号）')
              this.wechat_line_data = this.editLineData.wechat
            }
        } else {
          if (this.wechat_line_data != '') {
            if (!wechatRe.test(this.wechat_line_data)) {
              this.errorDialog.open('微信格式不合理（需6-20个字母、数字、下划线和减号）')
              this.wechat_line_data = this.editLineData.wechat
            }
          }
        }
      },
      serviceCheckedChange: function(value) {
        this.serverWarningLevelList = ''
        value.forEach(level => {
          if (level === '严重') {
            this.serverWarningLevelList = this.serverWarningLevelList + 'critical' + ','
          } else if (level === '重要') {
            this.serverWarningLevelList = this.serverWarningLevelList + 'important' + ','
          } else if (level === '一般') {
            this.serverWarningLevelList = this.serverWarningLevelList + 'normal' + ','
          }
        })
        this.serverWarningLevelList = this.serverWarningLevelList.slice(0, this.serverWarningLevelList.length - 1)
        console.log(this.serverWarningLevelList)
        api.setWarningLevel({level: this.serverWarningLevelList, type: 'server'}).then(res => {
          console.log(res)
          if (res.success == 1) {
            this.successDialog.open('保存成功')
          } else {
            this.errorDialog.open('保存失败')
          }
        }).catch(error => {
          console.log(error)
        });
      },
      terminalCheckedChange: function(value) {
        this.terminalWarningLevelList = ''
        value.forEach(level => {
          if (level === '严重') {
            this.terminalWarningLevelList = this.terminalWarningLevelList + 'critical' + ','
          } else if (level === '重要') {
            this.terminalWarningLevelList = this.terminalWarningLevelList + 'important' + ','
          } else if (level === '一般') {
            this.terminalWarningLevelList = this.terminalWarningLevelList + 'normal' + ','
          }
        })
        this.terminalWarningLevelList = this.terminalWarningLevelList.slice(0, this.terminalWarningLevelList.length - 1)
        console.log(this.terminalWarningLevelList)
        api.setWarningLevel({level: this.terminalWarningLevelList, type: 'terminal'}).then(res => {
          console.log(res)
          if (res.success == 1) {
            this.successDialog.open('保存成功')
          } else {
            this.errorDialog.open('保存失败')
          }
        }).catch(error => {
          console.log(error)
        });
      },
      // 获取当前修改告警
      sendwarningData: function(data) {
        console.log(data)
        this.otherWarning = []
        this.mcuWarning = []
        this.serviceWarning = []
        this.deviceWarning = []
        this.serviceNum = 0
        this.deviceNum = 0
        this.mcuNum = 0
        this.otherNum = 0
        this.sendwarningdata = data
        data.forEach(item => {
          if (item.type == 'other') {
            console.log(typeof (item.code));
            this.otherWarning.push({'name': item.name})
            this.otherNum++;
          } else if (item.type == 'mcu') {
            this.mcuWarning.push({'name': item.name})
            this.mcuNum++;
          } else if (item.type == 'server') {
            this.serviceWarning.push({'name': item.name})
            this.serviceNum++;
          } else if (item.type == 'terminal') {
            this.deviceWarning.push({'name': item.name})
            this.deviceNum++;
          }
        })
        this.sendCheck = 1
      },
      // 确认修改告警
      onWarningTreeSet: function() {
        console.log(this.sendwarningdata)
        if (this.sendCheck === 1) {
          if (this.sendwarningdata.length > 0) {
            let codeList = []
            this.sendwarningdata.forEach(item => {
              if (item.type == 'other' || item.type == 'mcu' || item.type == 'server' || item.type == 'terminal') {
                codeList.push({code: item.code})
              }
            })
            this.useAble = true
            api.setSubWarningCode({warning_code: codeList}).then(res => {
              console.log(res)
              if (res) {
                this.useAble = false
              }
            })
            this.sendwarningdata = []
            this.serviceWarningList = this.serviceWarning
            this.deviceWarningList = this.deviceWarning
            this.mcuWarningList = this.mcuWarning
            this.otherWarningList = this.otherWarning
            this.serviceWarningNum = this.serviceNum;
            this.deviceWarningNum = this.deviceNum;
            this.mcuWarningNum = this.mcuNum;
            this.otherWarningNum = this.otherNum;
          } else {
            api.setSubWarningCode({warning_code: []}).then(res => {
                console.log(res)
            })
            this.serviceWarningList = []
            this.deviceWarningList = []
            this.mcuWarningList = []
            this.otherWarningList = []
          }
          this.sendCheck = 0
        }
      },
      // 设置已选告警项
      getNodes: function (val) {
        console.log(val);
        this.warningMsg.code_list = ''
        val.forEach((item) => {
          let count = 0
          if (count == 0) {
            this.warningTreeData[0].children.forEach(warn => {
              if (warn.code === item) {
                this.warningMsg.code_list = this.warningMsg.code_list + warn.code + ','
                count = 1
              }
            })
          }
          if (count == 0) {
            this.warningTreeData[1].children.forEach(warn => {
              if (warn.code === item) {
                this.warningMsg.code_list = this.warningMsg.code_list + warn.code + ','
                count = 1
              }
            })
          }
          if (count == 0) {
            this.warningTreeData[2].children.forEach(warn => {
              if (warn.code === item) {
                this.warningMsg.code_list = this.warningMsg.code_list + warn.code + ','
                count = 1
              }
            })
          }
          if (count == 0) {
            this.warningTreeData[3].children.forEach(warn => {
              if (warn.code === item) {
                this.warningMsg.code_list = this.warningMsg.code_list + warn.code + ','
                count = 1
              }
            })
          }
          count = 0
        })
        console.log(this.warningMsg.code_list);
      },
      resetStopWarning: function (data) {
        console.log(data)
        api.getStopWarningInfo({params: {newPageNum: 1}}).then((res) => {
          console.log(res)
          if (res.success == 1) {
            this.warningFilterList = []
            this.warningReset = false
            this.$nextTick(() => {
              this.warningReset = true
            })
            this.warningFilterList = res.stopWarnings
            this.warningTotalPage = Math.ceil(res.TotalNum / this.perPage)
            this.warningTotalNum = res.TotalNum
            this.domainCount = res.TotalNum
          }
        })
      },
      onStopwarning: function () {
        this.stopwarningConfirm = 0
        this.$nextTick(() => {
          this.stopwarningConfirm = 1
        })
      },
      offStopwarning: function () {
        this.stopwarningConfirm = 0
        this.$nextTick(() => {
          this.stopwarningConfirm = 2
        })
      },
      onStopWarningCode: function () {
        this.stopwarningReset = false
        this.$nextTick(() => {
          this.stopwarningReset = true
        })
        this.$refs.setStopWarning.open()
      },
      // 已选告警弹框
      onSubWarningCode: function () {
        this.$refs.setWarningDialog.open()
        this.checkFlash = false
        this.$nextTick(() => {
          this.checkFlash = true
        })
      },
      // 当无告警通知时添加跳转提示
      addNotify: function() {
        this.inputEmail = ''
        this.inputWechat = ''
        this.inputPhone = ''
        this.inputName = ''
        this.$refs.addWarningNotify.open()
        this.warningCheckClear = false
        this.$nextTick(() => {
          this.warningCheckClear = true
        })
      },
      onAddWarningNotify: function () {
        this.inputEmail = ''
        this.inputWechat = ''
        this.inputPhone = ''
        this.inputName = ''
        this.$refs.addWarningNotify.open()
        this.warningCheckClear = false
        this.$nextTick(() => {
          this.warningCheckClear = true
        })
      },
      editCallback: function (rowData) {
        this.$refs.warningEditDialog.open();
        this.editLineData = rowData;
        console.log(this.editLineData)
        this.warningEditList = []
        this.warningEditList = rowData.warning.split(',');
        this.phone_line_data = this.editLineData.phone;
        this.email_line_data = this.editLineData.email;
        this.wechat_line_data = this.editLineData.wechat;
      },
      getNodesdetail: function (val) {
        console.log(val)
        this.warning_line = val
        /* this.editLineData.warning = ''
        val.forEach((item) => {
          this.editLineData.warning = this.editLineData.warning + item + ','
        }) */
      },
      onSaveEdit: function () {
        this.warning_line_data = ''
        this.warning_line.forEach((item) => {
          console.log(item)
          let count = 0
          if (count == 0) {
            this.warningTreeData[0].children.forEach(warn => {
              if (warn.code === item) {
                this.warning_line_data = this.warning_line_data + warn.code + ','
                count = 1
              }
            })
          }
          if (count == 0) {
            this.warningTreeData[1].children.forEach(warn => {
              if (warn.code === item) {
                this.warning_line_data = this.warning_line_data + warn.code + ','
                count = 1
              }
            })
          }
          if (count == 0) {
            this.warningTreeData[2].children.forEach(warn => {
              if (warn.code === item) {
                this.warning_line_data = this.warning_line_data + warn.code + ','
                count = 1
              }
            })
          }
          if (count == 0) {
            this.warningTreeData[3].children.forEach(warn => {
              if (warn.code === item) {
                this.warning_line_data = this.warning_line_data + warn.code + ','
                count = 1
              }
            })
          }
          count = 0
        })
        api.editWarningNotifyInfo({
          id: this.editLineData.id,
          phone: this.phone_line_data,
          email: this.email_line_data,
          wechat: this.wechat_line_data,
          code_list: this.warning_line_data
        }).then(res => {
          if (this.phone_line_data == '' && this.email_line_data == '' && this.wechat_line_data == '') {
            this.errorDialog.open('请至少填写一种联系方式')
            this.phone_line_data = this.editLineData.phone
            this.email_line_data = this.editLineData.email
            this.wechat_line_data = this.editLineData.wechat
          } else {
            if (res.success == 1) {
              this.successDialog.open('修改成功')
            } else {
              this.errorDialog.open('修改失败')
            }
          }
          // if (res.success == 1) {
          //   this.successDialog.open('修改成功')
          // } else {
          //   this.errorDialog.open('修改失败')
          // }
          this.editLineData.phone = this.phone_line_data
          this.editLineData.email = this.email_line_data
          this.editLineData.wechat = this.wechat_line_data
          this.editLineData.warning = this.warning_line_data
        }).catch(error => {
          console.log(error)
        })
      },
      detailCallback: function (rowData) {
        this.serviceWarningDetail = []
        this.deviceWarningDetail = []
        this.mcuWarningDetail = []
        this.otherWarningDetail = []
        this.serviceWarningCount = 0;
        this.deviceWarningCount = 0;
        this.mcuWarningCount = 0;
        this.otherWarningCount = 0;

        this.$refs.warningDetailDialog.open();
        this.detailLineData = rowData;
        this.warningDetailList = rowData.warning.split(',');
        this.warningDetailList.forEach(item => {
          this.serviceWarningType.forEach(type => {
            console.log(typeof (type.code))
            if (type.code.toString() === item) {
              this.serviceWarningDetail.push({'name': type.name})
              this.serviceWarningCount++;
            }
          })
          this.deviceWarningType.forEach(type => {
            if (type.code.toString() === item) {
              console.log(type)
              this.deviceWarningDetail.push({'name': type.name})
              this.deviceWarningCount++;
            }
          })
          this.mcuWarningType.forEach(type => {
            if (type.code.toString() === item) {
              console.log(type)
              this.mcuWarningDetail.push({'name': type.name})
              this.mcuWarningCount++;
            }
          })
          this.otherWarningType.forEach(type => {
            if (type.code.toString() === item) {
              console.log(type)
              this.otherWarningDetail.push({'name': type.name})
              this.otherWarningCount++;
            }
          })
        })
        console.log(this.serviceWarningCount)
        if (this.serviceWarningCount !== 0) {
          this.userWarningType = 'serviceWarning'
        } else if (this.deviceWarningCount !== 0) {
          this.userWarningType = 'deviceWarning'
        } else if (this.mcuWarningCount !== 0) {
          this.userWarningType = 'mcuWarning'
        } else if (this.otherWarning !== 0) {
          this.userWarningType = 'otherWarning'
        }
      },
      deleteCallback: function (rowData) {
        this.$refs.warningDeleteDialog.open();
        this.detailLineData = rowData;
      },
      OnWarningNotifyDelete: function () {
        api.deleteWarningNotifyInfo({id: this.detailLineData.id}).then(res => {
          api.getWarningNotifyInfo({params: {newPageNum: 1}}).then((res) => {
            console.log(res)
            if (res.success == 1) {
              this.successDialog.open('删除成功')
              this.warningNotifyList = res.warning_notify_list;
              this.warningNotifyFields = setJs.getWarningNotifyTableFields(this.editCallback, this.detailCallback, this.deleteCallback);
              this.userTotalPage = Math.ceil(res.TotalNum / this.perPage)
              this.deviceTotalNum = res.TotalNum
              this.cage = 2
            } else {
              this.errorDialog.open('删除失败')
            }
          });
        }).catch(error => {
          console.log(error)
        })
      },
      OnSaveTimingTask: function () {
        this.warningMsg.email = this.inputEmail
        this.warningMsg.wechat = this.inputWechat
        this.warningMsg.phone = this.inputPhone
        this.warningMsg.name = this.inputName
        if (this.warningMsg.email == '' && this.warningMsg.wechat == '' && this.warningMsg.phone == '') {
          this.errorDialog.open('请至少填写一种联系方式')
        } else {
          if (this.inputName == '') {
            this.errorDialog.open('通知人员为必填项')
          } else {
            api.addWarningNotifyInfo(this.warningMsg).then(res => {
            console.log(res)
            if (res.success == 1) {
              this.successDialog.open('添加成功')
            } else { 
              this.errorDialog.open('添加失败')
            }
            this.warningMsg.phone = ''
            this.warningMsg.email = ''
            this.warningMsg.wechat = ''
            this.warningMsg.code_list = ''
            this.warningMsg.name = ''
            this.inputEmail = ''
            this.inputWechat = ''
            this.inputPhone = ''
            this.inputName = ''
            api.getWarningNotifyInfo({params: {newPageNum: 1}}).then((res) => {
              console.log(res)
              if (res.success == 1) {
                this.warningNotifyList = res.warning_notify_list;
                this.warningNotifyFields = setJs.getWarningNotifyTableFields(this.editCallback, this.detailCallback, this.deleteCallback);
                this.userTotalPage = Math.ceil(res.TotalNum / this.perPage)
                this.deviceTotalNum = res.TotalNum
                this.cage = 2
              }
            });
          }).catch(error => {
            console.log(error)
          })}};
      }
    }
  }
</script>

<style scoped>
  .warningNotify{
    height: 500px;
    text-align:center;
  }
  .warningNotifyNone {
    line-height: 400px;
  }
  .warningNotifyAdd{
    color: #007ac0;
    text-decoration: underline
  }
  .textleft {
    margin-top: 35px;
    text-align: left;
  }
  .fontCommon {
    clear: both;
    margin-top: 29px;
    font-size: 12px;
    color: #4e4e4e;
    position: relative;
    overflow: hidden;
  }
  .specialCommon {
    display: inline-block;
    width: 100px;
    height: 10px;
    vertical-align:top;
    margin-left: 72px;
    margin-top: 5px;
  }
  .modifyCommon {
    display: inline-block;
    margin-left: 72px;
    width: 100px;
    height: 10px;
  }
  .specialPathCommon{

    display: inline-block;
    width: 230px;
    height:600px;
    vertical-align:top
  }
  .backNamePathCommon {
    display: inline-block;
    width: 230px;
    height: 20px;
  }
  /deep/ .el-tabs__content{
    width: 100%;
  }
  /deep/ .el-tabs__nav-scroll{
    margin-bottom: 10px;
  }
  .warningDiv {
    display: inline-block;
    font-size: 14px;
    height: auto;
    margin-bottom: 25px;
  }
  .warningDivlist {
    display: inline-block;
    font-size: 14px;
    width: 640px;
    height: 320px;
    overflow: auto;
  }
  .warningName{
    margin-left: 10px;
  }
  .warningLine {
    background-color: #eff2f4;
    font-size: 14px;
    color: #4e4e4e;
    padding-bottom: 5px;
    padding-top: 5px;
    border-bottom: 1px solid #f5f6f7;
  }
  .warningLinelist {
    background-color: #eff2f4;
    font-size: 14px;
    width: 640px;
    height: 28px;
    color: #4e4e4e;
    padding-top: 5px;
  }
  .warningTab{
    margin-left: 40px;
  }
  .warningFont{
    font-size: 12px;
    float: right;
    margin-right: 10px;
  }
  .warningFontlist{
    margin-top: 10px;
    margin-left: 10px;
  }
  .warningNum{
    color: #000000;
    font-size: 10px;
    margin-left: 6px;
    margin-right: 2px;
  }
  .warningNumlist{
    color: #000000;
    font-size: 10px;
    margin-left: 6px;
    margin-right: 2px;
  }
  .warningDetail{
    float: left;
    width: 297px;
    height: 24px;
    padding-left: 10px;
    margin-top: 5px;
  }
  .warningDetaillist{
    float: left;
    width: 305px;
    height: 24px;
    padding-left: 10px;
    padding-top: 5px;
    margin-top: 5px;
  }
  .warningContent {
    text-align: left;
    width: 100%;
    height: 100%;
  }
  .warningContentlist {
    text-align: left;
  }
  .warningMassage {
    height: 62px;
    width: 100%;
    margin-top: 14px;
    margin-bottom: 42px;
    font-size: 14px;
    color: #8b8b8b;
  }
  .addBtn {
    float: right;
    z-index: 0;
  }
  .warningFilterContent {
    margin: 21px 0 38px 0;
    clear: both;
  }

  .firstTitle {
    font-size: 15px;
    margin-top: 29px;
  }

  .content {
    margin-top: 28px;
    display: inline-block;
  }
  .checkWarningLevel {
    margin-bottom: 28px;
    height: 20px;
  }
  .setName {
    font-size: 14px;
    width: 79px;
    float: left;
    margin-right: 20px;
  }

  .warningLevel {
    font-size: 12px;
    width: 51px;
    display: inline-block;
  }

  .secondTitle {
    font-size: 15px;
    color: #4e4e4e;
    margin-top: 31px;
    margin-bottom: 7px;
  }

  .setBtn {
    position: absolute;
    right: 0;
  }

  .warningDetailDialogDiv {
    margin: 20px 36px 42px;
  }

  .notifyIteam {
    margin-top: 17px;
    width: 341px;
    display: inline-block;
  }

  .iteamKey {
    margin-left: 34px;
    width: 95px;
    float: left;
  }

  .iteamValue {
    float: left;
    width: 212px;
  }

  .warningIteam {
    margin-top: 9px;
  }

  .delTipsDiv {
    padding: 50px;
    text-align: center;
  }
</style>
