<template>
  <div class="versionDiv">
    <div class="sus-back">
      <span class="back-btn" @click="$router.go(-1)"></span>
      <span class="base-info-title">{{ deviceType}}</span>
      <div class="operation">
        <button class="normal-btn" @click="onUpload()">上传</button>
        <button class="normal-btn" :class="{disable: selections.length == 0}" :disabled="selections.length == 0" @click="onEdit()">编辑</button>
        <button class="normal-btn" :class="{disable: selections.length == 0}" :disabled="selections.length == 0" @click="onDelete()">删除</button>
      </div>
    </div>
    <div>
      <nms-pages-table :data="deviceList" :fields="deviceFields" :total-page="userTotalPage" v-model="selections" />
    </div>
    <nms-big-dialog title="版本上传" ref="cfgUploadDlg" @confirm="onSign()" @cancel="cancelSign()" :width="'550px'" :height="'570px'">
      <div slot="content" class="version-info" style="height:500px;width:535px;overflowY:auto">
        <!-- 设备型号 -->
        <ul class="item-list">
          <li class="first-col">设备型号</li>
          <li class="second-col" id="dev_type_li">{{ deviceType }}</li>
        </ul>

        <!-- 版本号 -->
        <ul class="item-list">
          <li class="first-col">版本号</li>
          <li class="second-col" v-show="uploadShow">
            <el-input v-model="vNum" type="text" @blur="examineVer" oninput="value=value.replace(/[^\d^\.^v^V]/g,'')" maxlength="64"></el-input>
          </li>
          <li v-show="uploadShow"><span style="color:red">*</span></li>
          <li class="second-col" v-show="editShow">{{ vNum }}</li>
        </ul>

        <!-- 升级文件 -->
        <ul class="item-list">
          <li class="first-col">升级文件</li>
          <li class="second-col" v-show="uploadShow">
            <el-input v-model="upFile" type="text" readonly="readonly" style="pointer-events:none;"></el-input>
          </li>
          <li class="second-col" v-show="editShow">{{ upFile }}</li>
          <li class="third-col" v-show="logoShow">
            <el-upload
              class="upload-demo"
              ref="upload"
              :action="UploadUrl()"
              :data="verDate"
              :on-change="handleChange"
              :on-success="upload_success"
              :on-progress="uploadVideoProcess"
              :file-list="fileList"
              :show-file-list="false"
              :auto-upload="false">
              <label class="select-file" slot="trigger" size="small" type="primary"></label>
            </el-upload>
          </li>
        </ul>
        <!-- OEM标识 -->
        <ul class="item-list">
          <li class="first-col">oem标志</li>
          <li class="second-col" v-show="uploadShow">
            <el-input v-model="oem" type="text" @blur="examineVer"></el-input>
          </li>
          <li class="second-col" v-show="editShow">{{ oem }}</li>
          <li v-show="uploadShow"><span style="color:red">*</span></li>
        </ul>

        <!-- 版本属性 -->
        <ul class="item-list">
          <li class="first-col">版本属性</li>
          <li class="second-col">
            <el-select v-model="vAttribute" @change="selectVersion(vAttribute)">
              <el-option v-for="(item,index) in vAttributes" :key="index" :label="item.text" :value="item.value" style="width:319px">
              </el-option>
            </el-select>
          </li>
        </ul>

        <!-- 用户域 -->
        <ul class="item-list with-textarea" id="user_domain_container" v-show="userDomainShow">
          <li class="first-col">用户域</li>
          <li class="second-col">
            <el-input type="textarea" v-model="userDomains" :rows="4" readonly="readonly"></el-input>
          </li>
          <li class="third-col">
            <button id="select_users" @click="userDomainUpload()"></button>
          </li>
        </ul>

        <!-- 终端号码 -->
        <ul class="item-list" id="terminal_e164_container" v-show="terminalNumShow">
          <li class="first-col">终端号码</li>
          <li class="second-col">
            <el-input v-model="TerminalNum" type="text" maxlength="13"></el-input>
          </li>
          <li class="third-col">
            <button id="add_ter_num" @click="addTerminalNum()"></button>
          </li>
        </ul>

        <!-- 终端号码显示 -->
        <ul class="without-first-col" id="ter_num_list" v-show="areShow">
          <li class="ter-num" v-for="e164 in e164List">{{e164}}
            <s @click="delOneTerNum(e164)"></s>
          </li>
        </ul>

        <!-- 版本级别 -->
        <ul class="ver-level item-list">
          <li class="first-col">版本级别</li>
          <li class="second-col">
            <el-select v-model="vLevel" value="">
              <el-option v-for="(item,index) in vLevels" :key="index" :label="item.text" :value="item.value" style="width:319px">
              </el-option>
            </el-select>
          </li>
        </ul>

        <!-- 版本描述 -->
        <ul class="item-list with-textarea">
          <li class="first-col">
            版本描述
            <br>
            <span class="note">(限300个字符)</span>
          </li>
          <li class="second-col">
            <el-input type="textarea" v-model="textareas" :rows="4" maxlength="300"></el-input>
          </li>
        </ul>
      </div>
    </nms-big-dialog>
    <nms-big-dialog title="选择用户域" :width="'429px'" :height="'450px'" ref="cfgUserUploadDlg" @confirm="determine()">
      <div slot="content" class="version-info">
        <userdomain-tree :data="domainTreeData" :node-click="nodeClick" v-model="cNodes"></userdomain-tree>
      </div>
    </nms-big-dialog>
    <nms-dialog title="提示" :width="'400px'" :height="'152px'" :close-btn="true" ref="OnWarningDialog_second">
       <div slot="content">
         <div class="tipMsg">
            <span class="PromptImg"></span>
            <span>请输入版本号</span>
         </div>
       </div>
    </nms-dialog>
    <nms-dialog title="提示" :width="'400px'" :height="'152px'" :close-btn="true" ref="OnWarningDialog_vernum">
       <div slot="content">
         <div class="tipMsg">
            <span class="PromptImg"></span>
            <span>此版本号已经重复，请重新输入！</span>
         </div>
       </div>
    </nms-dialog>
    <nms-dialog title="提示" :width="'400px'" :height="'152px'" :close-btn="true" ref="OnWarningDialog_third">
       <div slot="content">
         <div class="tipMsg">
            <span class="PromptImg"></span>
            <span>请上传版本</span>
         </div>
       </div>
    </nms-dialog>
    <nms-dialog title="提示" :width="'400px'" :height="'152px'" :close-btn="true" ref="OnWarningDialog_error">
       <div slot="content">
         <div class="tipMsg">
            <span class="PromptImg"></span>
            <span>同一oem同一终端类型已经存在同一版本类型!</span>
         </div>
       </div>
    </nms-dialog>
    <nms-dialog title="提示" :width="'400px'" :height="'152px'" :close-btn="true" ref="OnDelVerDialog" @confirm="verDelete()">
       <div slot="content">
         <div class="tipMsg">
            <span class="PromptImg"></span>
            <span>是否删除所选版本？</span>
         </div>
       </div>
    </nms-dialog>
    <msg-dialog title="提示" :width="'400px'" :height="'177px'" :close-btn="true" ref="MsgDialog" @cancel="cancel()">
       <div slot="content">
         <div class="delTipsDiv" style="padding: 40px 10px">
            <span>版本文件正在上传中，请稍后...</span>
            <span><el-progress  type="line" :percentage="percent" :stroke-width="6" style="margin-top: 5px"></el-progress></span>
            <div style="padding-top: 5px;">
              <span>文件大小: {{fileSize}}</span>
              <span style="float:right">已上传: {{this.percent}}%</span>
            </div>
         </div>
       </div>
    </msg-dialog>
    <nms-dialog title="提示" :width="'400px'" :height="'152px'" :close-btn="false" @confirm="onCancel()" ref="OnCancelDialog">
       <div slot="content">
         <div class="tipMsg">
            <span class="PromptImg"></span>
            <span>已取消上传版本！</span>
         </div>
       </div>
    </nms-dialog>
  </div>
</template>

<script>
import NmsPagesTable from "components/common/nms-pages-table";
import api from "../../axios";
import qs from 'qs';
import * as susjs from "assets/js/susmgr";
import NmsBigDialog from "components/common/nms-big-dialog";
import NmsDialog from "components/common/nms-dialog";
import MsgDialog from "components/common/msg-dialog";
import UserdomainTree from "components/common/userdomain-tree";

export default {
    name: "susdetail",
    components: {
      NmsPagesTable,
      NmsBigDialog,
      UserdomainTree,
      MsgDialog,
      NmsDialog
    },
    inject: ['reload'],
    data() {
        return {
            deviceType: "",
            sign: "", // 用去区分编辑/上传的标志符
            // 表格每页显示数量
            perPage: 10,
            userTotalPage: 1,
            deviceList: [],
            deviceFields: [],
            selections: [],

            // 表单数据
            ver_sn: "",
            vNum: "",
            oem: "kedacom",
            vAttribute: "1",
            vAttributes: susjs.vAttributes,
            vLevel: "1",
            vLevels: susjs.vLevels,
            textareas: "",
            userDomains: "",
            userMoid: [],

            userDomainShow: false,
            terminalNumShow: false,
            areShow: true,
            logoShow: false,
            uploadShow: true,
            editShow: false,

            domainTreeData: [],
            e164List: [],
            TerminalNum: "",

            cNodes: [],
            fileList: [],
            upFile: "",
            verDate: {
                device_type: '',
                soft_ver: ''
            },
            success_status: "",

            videoFlag: false,
            percent: 0,
            fileSize: '',
            detailFileNum: 0,
            // 编辑：同一oem同一终端类型已经存在同一版本类型验证标识(true:不需要验证/false:需要验证)
            tip: true
        };
    },
    activated: function() {
        this.deviceType = this.$route.params.terminal;
    },
    mounted() {
        this.deviceType = this.$route.params.terminal;
        api.getTerminalTypeVersions(this.deviceType).then(res => {
            this.deviceList = res.data;
            this.deviceFields = susjs.getTerminalTableFields();
            this.userTotalPage = Math.ceil(this.deviceList.length / this.perPage);
            this.detailFileNum = this.deviceList.length
        });
        api.getUserDomainTree().then((res) => {
          if (res.success == 1) {
            res.data.forEach(item => {
              if (item.type == "user") {
                this.domainTreeData.push(item)
              }
            });
          }
        })
    },
    watch: {
      selects: function(newValue,oldValue) {
        this.selections = newValue
      },
      // 监听文件上传成功/失败状态
      success_status: function(val) {
        if (val == 1) {
          this.verUploadTrue() // 版本文件上传成功，执行版本信息上传
        } else {
          console.log("error")
        }
      }
    },
    computed: {
      selects: function() {
        return this.$store.state.terminal_selection_list
      }
    },
    methods: {
        UploadUrl: function() {
            return this.axios.defaults.baseURL + "/nms/sus/uploadverfile/";
        },
        examineVer: function (event) {
          this.axios.post("/nms/sus/existver/", qs.stringify(
            {
              device_type: this.deviceType,
              oem_mark: this.oem,
              soft_ver: this.vNum
              }),
              {headers: {'Content-Type': 'application/x-www-form-urlencoded'}})
              // 成功返回
              .then(response => {
                  if (response.data.success == 1) {
                    this.vNum = 0
                    this.$refs.cfgUploadDlg.open()
                    this.$refs.OnWarningDialog_vernum.open()
                    // this.$refs.OnWarningDialog_error.open()
                  }
              })
              // 失败返回
              .catch(error => {
                  console.log("failed" + error);
              })
        },
        onSign: function () {
          if (this.sign === "edit") {
            this.verEdit()
          } else if (this.sign === "upload") {
            this.verUpload()
          }
        },
        cancelSign: function () {
          this.reload()
        },
      // 上传
        onUpload: function() {
          this.editShow = false
          this.uploadShow = true
          this.areShow = false
          this.userDomainShow = false
          this.terminalNumShow = false
          this.userDomains = ''
          this.sign = "upload"
          this.vNum = ''
          this.upFile = ''
          this.vLevel = '1'
          this.vAttribute = '1'
          this.textareas = ''
          this.$refs.cfgUploadDlg.open()
          this.logoShow = true
          // this.examineVer()  // 初始化校验
        },
        uploadVideoProcess(event, file, fileList) {
          this.videoFlag = true;
          if (event.percent > 97) {
            this.percent = 97
          } else {
            this.percent = Math.floor(event.percent);
          }
        },
        verUpload() {
          // 上传文件额外带的参数
          this.verDate.device_type = this.deviceType
          this.verDate.soft_ver = this.vNum
          this.verDate.oem_mark = this.oem

          if (this.vNum == "") {
            this.$refs.cfgUploadDlg.open()
            this.$refs.OnWarningDialog_second.open();
          } else if (this.upFile == "") {
            this.$refs.cfgUploadDlg.open()
            this.$refs.OnWarningDialog_third.open();
          } else if (this.userDomains.length == "" && this.e164List.length == 0 && this.vAttribute == 4) {
            this.$refs.cfgUploadDlg.open()
            this.errorDialog.open('用户域和164号码，至少要添加一个')
          } else {
            this.submitUpload()
            this.$refs.MsgDialog.open()
          }
        },
        verUploadTrue() {
          this.axios.post("/nms/sus/addverinfo/", qs.stringify(
            {
                        oem_mark: this.oem,
                        device_type: this.deviceType,
                        ver_level: this.vLevel,
                        release_attribute: this.vAttribute,
                        soft_ver: this.vNum,
                        release_notes: this.textareas,
                        file_name: this.upFile,
                        file_size: this.upFileSize,
                        grayrange_moidlist: this.userMoid.join(','),
                        grayrange_e164list: this.e164List.join(','),
              }),
              {headers: {'Content-Type': 'application/x-www-form-urlencoded'}}
            )
            // 成功返回
            .then(response => {
              if (response.data.success === 1) {
                for (this.percent = 97; this.percent < 100; this.percent++) {
                  if (this.percent == 99) {
                    this.reload() // 刷新当前页面
                  }
                }
                this.successDialog.open('上传成功')
              } else if (response.data.success === 0) {
                this.reload()
                this.errorDialog.open(response.data.message)
              }
            })
            // 失败返回
            .catch(error => {
              this.errorDialog.open('上传失败')
              console.log("failed" + error);
            })

        },

        // 编辑
        onEdit: function() {
          this.sign = "edit"
          this.editShow = true
          this.uploadShow = false
          this.logoShow = false
          this.e164List = []
          this.userDomains = ''
          this.TerminalNum = ''
          this.$refs.cfgUploadDlg.open()
          // 判断版本属性是否为灰度
          if (this.selections.release_attribute == 4) {
            this.areShow = true
            this.userDomainShow = true
            this.terminalNumShow = true
            let str = this.selections.grayrange_e164list.split(',') // e164号码列表
            for (var i = 0; i < str.length; i++) {
              if (str[i] !== '') {
                this.e164List.push(str[i])
              }
            }
          } else {
            this.userDomainShow = false
            this.terminalNumShow = false
          }
          this.vNum = this.selections.soft_ver // 版本号
          this.oem = this.selections.oem_mark // oem标识
          this.ver_sn = this.selections.ver_sn // 版本id
          this.vLevel = this.selections.ver_level.toString() // 版本级别
          this.vAttribute = this.selections.release_attribute.toString() // 版本属性
          this.textareas = this.selections.release_notes // 版本描述
          this.upFile = this.selections.file_name // 文件名
          console.log(this.selections.grayrange_moidlist)

          var moidList = this.selections.grayrange_moidlist.split(',')
          var moidUser = ''
          console.log(moidList)
          moidList.forEach(moid => {
            console.log(moid)
            this.domainTreeData.forEach(item => {
              console.log(item)
              if (item.moid == moid) {
                moidUser = moidUser + item.name + ','
              }
            })
          })
          console.log(moidUser)
          this.userMoid = this.selections.grayrange_moidlist // 用户域moid列表
          this.userDomains = moidUser
        },
        verEdit() {
          if (typeof(this.userMoid) == "object") {
            this.userMoid = this.userMoid.join(',')
          } else if (typeof(this.userMoid) == "string") {
            this.userMoid = this.userMoid
          }
          if (this.vAttribute == this.selections['release_attribute']) {
            this.tip = true
          } else {
            this.tip = false
          }
          this.axios.post("/nms/sus/editver/", qs.stringify(
            {
                      ver_sn: this.ver_sn,
                      ver_level: this.vLevel,
                      release_attribute: this.vAttribute,
                      release_notes: this.textareas,
                      grayrange_moidlist: this.userMoid,
                      grayrange_e164list: this.e164List.join(','),
                      tip: this.tip
              }),
              {headers: {'Content-Type': 'application/x-www-form-urlencoded'}}
            )
            // 成功返回
            .then(response => {
              console.log(response)
                if (response.data.success === 2) {
                    this.$refs.cfgUploadDlg.open()
                    this.$refs.OnWarningDialog_error.open()
                } else if (response.data.success === 1) {
                  this.successDialog.open('保存成功')
                  this.reload()
                } else {
                  this.errorDialog.open('保存失败')
                }
            })
            // 失败返回
            .catch(error => {
              this.errorDialog.open('保存失败')
              console.log("编辑失败：" + error);
            })
        },
        onDelete: function () {
          this.$refs.OnDelVerDialog.open();
        },
        verDelete: function () {
          this.ver_sn = this.selections.ver_sn
          this.axios.post("/nms/sus/deletever/", qs.stringify(
              {
                  ver_sn: this.ver_sn,
              }),
              {headers:{'Content-Type': 'application/x-www-form-urlencoded'}}
            )
            // 成功返回
            .then(response => {
              if (response.data.success == 1) {
                this.successDialog.open('删除成功')
                this.detailFileNum = this.detailFileNum - 1
                if (this.detailFileNum>0) {
                  this.reload()
                } else {
                  this.$router.push('/susmgrinfo/susmgr')
                }
              } else {
                this.errorDialog.open('删除失败')
              }
            })
            // 失败返回
            .catch(error => {
              this.errorDialog.open('删除失败')
              console.log("删除失败：" + error);
            })
        },
        userDomainUpload: function () {
          this.$refs.cfgUserUploadDlg.open()
        },
        addTerminalNum: function () {
          var numReg = /^[0-9]*$/
          var numRe = new RegExp(numReg)
          if (numRe.test(this.TerminalNum)) {
            if (this.TerminalNum.length >= 6) {
              if (this.e164List.length < 300) {
                var exist = 0
                this.e164List.forEach(item => {
                  if (item == this.TerminalNum) {
                    exist = 1
                  }
                })
                if (exist == 0) {
                  this.e164List.push(this.TerminalNum)
                  this.TerminalNum = ''
                } else {
                  this.errorDialog.open('添加号码已存在')
                }
              } else {
                this.errorDialog.open('号码不得超过300个')
              }
            } else {
              this.errorDialog.open('号码不得小于六位')
            }
          } else {
            this.errorDialog.open('号码必须为数字')
          }
        },
        delOneTerNum: function (e164) {
          this.e164List.splice(this.e164List.indexOf(e164), 1)
        },
        selectVersion: function (vAttribute) {
          // this.examineVer() // 校验
          if (vAttribute === "4") {
            this.userDomainShow = true
            this.terminalNumShow = true
            this.areShow = true
          } else {
            this.userDomainShow = false
            this.terminalNumShow = false
            this.areShow = false
          }
        },
        nodeClick: function (nodeData) {
          // let name = nodeData.name
          // console.log("用户域name:"+name)
        },
        determine: function () {
          this.userDomains = "" // 清空上次选择的用户域
          this.userMoid = []
          for (var j = 0; j < this.cNodes.length; j++) {
            this.userDomains = this.userDomains + this.cNodes[j].name + ";"
            this.userMoid.push(this.cNodes[j].moid)
          }
          if (this.userDomains.length > 0) {
            this.userDomains = this.userDomains.substr(0, this.userDomains.length - 1)
          }
        },
        submitUpload() {
          this.$refs.upload.submit();
        },
        handleChange(file, fileList) {
          if (fileList.length > 1) {
            fileList.shift()
          }
          this.upFile = file.name
          this.upFileSize = file.size
          if (file.size / 1024 / 1024 < 1) {
            this.fileSize = Math.floor(file.size / 1024) + "KB"
          } else {
            if (file.size / 1024 / 1024 / 1024 < 1) {
              this.fileSize = Math.floor(file.size / 1024 / 1024) + "MB"
            } else {
              this.fileSize = Math.floor(file.size / 1024 / 1024 / 1024) + "GB"
            }
          }
        },
        upload_success(response, file, fileList) {
          this.success_status = response.success
        },
        cancel(file) {
          this.$refs.upload.abort();
          this.$refs.OnCancelDialog.open()
        },
        onCancel: function() {
          this.reload()
        },
        succeccMsg: function() {
          this.$message({
            duration: 2000,
            center: true,
            message: '上传成功',
            offset: 400
          })
        },
    }
};
</script>

<style scoped>
.versionDiv {
    text-align: left;
    overflow: hidden;
}
.sus-back {
    position: relative;
    height: 33px;
    margin-bottom: 14px;
}
.operation {
    position: absolute;
    right: 0;
    top: 0;
}
  .searchDiv{
    position: relative;
    height: 33px;
    margin-bottom: 14px;
  }
  .uploadBtn {
    position: absolute;
    right: 0;
    top: 0;
  }
  .item-list {
    color: #4e4e4e;
    font-size: 0;
    margin-left: 3px;
    margin-bottom: 25px;
  }
  .item-list li {
    font-size: 12px;
    display: inline-block;
    vertical-align: middle;
  }
  .first-col {
    width: 87px;
  }
  .version-info {
    padding-left: 30px;
    padding-top: 30px;
  }
  .second-col {
    width: 319px;
    margin-right: 15px;
  }
  .second-col input[type='text'] {
    width: 319px;
  }
  .el-input {
    width: 319px;
  }
  .select-file {
    display: block;
    width: 30px;
    height: 30px;
    background: url(../../assets/image/open_file.png);
    cursor: pointer;
  }
  .without-first-col {
    margin-left: 90px;
    margin-bottom: 27px;
    font-size: 0;
  }
  #start_upload {
    margin-top: -7px;
    margin-right: 15px;
  }
  .first-col .note {
    font-size: 11px;
    color: #8b8b8b;
  }
  .with-textarea .first-col {
    vertical-align: top;
  }
  #select_users {
    display: block;
    width: 30px;
    height: 30px;
    background: url(../../assets/image/btn-select.png);
  }
  #add_ter_num {
    display: block;
    width: 30px;
    height: 30px;
    background: url(../../assets/image/add.png);
  }
  #ter_num_list {
    margin-top: -7px;
  }
  .without-first-col li {
    font-size: 12px;
    display: inline-block;
    vertical-align: middle;
  }
  .ter-num {
    margin-right: 6px;
    margin-bottom: 10px;
    font-size: 11px;
    border: 1px solid #999;
    padding: 6px 6px 6px 8px;
    color: #4e4e4e;
  }
  .ter-num s {
    position: relative;
    top: 3px;
    width: 13px;
    height: 13px;
    display: inline-block;
    margin-left: 15px;
    background: url(../../assets/image/delete.png);
    cursor: pointer;
  }
  .tipMsg {
    text-align: center;
    padding-top: 50px;
  }
  /deep/ .el-progress__text {
    font-size: 14px;
    color: #606266;
    display: inline-block;
    vertical-align: middle;
    margin-left: 10px;
    line-height: 1;
    display: none;
  }
</style>

<style>
  /* 不加scoped自定义样式*利用类下类引用解决了全局污染 */
  .second-col .el-input {
    width: 319px;
  }
</style>
