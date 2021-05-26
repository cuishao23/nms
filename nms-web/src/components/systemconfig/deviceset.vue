<template>
  <div class="text-left">
    <div class="search-line">
      <el-input v-model="device_model" placeholder="请输入设备型号" class="filter-text"></el-input>
      <el-select v-model="device_type" placeholder="全部类型" @change="typeClick" class="filter-select" filterable>
        <el-option
          v-for="(item,index) in device_types"
          :key="index"
          :label="item.name"
          :value="item.type">
        </el-option>
      </el-select>
      <button class='search' @click="searchDevice()" id="searchFloat"></button>
      <button class="normal-btn" :class="{disable: selectRow.length == 0}" :disabled="selectRow.length == 0" @click="onDeleteDeviceList()" id="deleteFloat">删除</button>
      <button class="normal-btn" @click="onAddDeviceList()" id="addFloat">新增</button>
      <nms-big-dialog title="新增" :width="'450px'" :height="'320px'" :close-btn="true" ref="addDeviceDialog" :confirmType="addConfirm" @confirm="OnSave()" @cancel="OnCancel()">
        <div slot="content" class="textleft">
          <div class="fontCommon">
            <span class="modifyCommon">设备主型号</span>
            <input type="text" class="backNamePathCommon" placeholder="限128字节" v-model="inputName" @blur="examineMsg"/>
          </div>
          <div class="fontCommon">
            <span class="modifyCommon">设备子型号</span>
            <input type="text" class="backNamePathCommon" placeholder="限128字节，不包含'/'" v-model="inputProductName" @blur="examineMsg"/>
          </div>
          <div class="fontCommon">
            <span class="modifyCommon">设备类型</span>
            <el-radio v-model="terminalType" class='radiodiv' label="1">硬件</el-radio>
            <el-radio v-model="terminalType" class='radiodiv' label="0">软件</el-radio>
            <el-radio v-model="terminalType" class='radiodiv' label="2">外设</el-radio>
          </div>
          <div class="fontCommon" v-if="terminalType!='2'">
            <span class="modifyCommon">可登陆设备</span>
            <input type="text" class="backNamePathCommon" placeholder="限50字节" v-model="inputDeviceTag" @blur="examineMsg"/>
          </div>
        </div>
      </nms-big-dialog>
      <nms-big-dialog title="提示" :width="'400px'" :height="'177px'" @confirm="deleteDeviceList()" :close-btn="true" ref="deviceEditDeleteDialog">
        <div slot="content">
          <div class="delTipsDiv">
              <span class="PromptImg"></span>
              <span>确认删除该设备？</span>
          </div>
        </div>
      </nms-big-dialog>
      <nms-big-dialog title="提示" :width="'400px'" :height="'177px'" :close-btn="true" ref="deviceEditFailDialog">
        <div slot="content">
         <div class="delTipsDiv">
            <span class="PromptImg"></span>
            <span>{{ error_msg }}</span>
         </div>
       </div>
      </nms-big-dialog>
      <nms-big-dialog title="提示" :width="'400px'" :height="'177px'" :close-btn="true" ref="deviceEditSuccessDialog">
        <div slot="content">
          <div class="delTipsDiv">
              <span class="PromptImg"></span>
              <span>保存成功</span>
          </div>
        </div>
      </nms-big-dialog>
      <nms-big-dialog title="提示" :width="'400px'" :height="'177px'" :close-btn="true" ref="deviceEditWarningDialog">
        <div slot="content">
          <div class="delTipsDiv">
              <span class="PromptImg"></span>
              <span>输入不能为空</span>
          </div>
        </div>
      </nms-big-dialog>
    </div>
    <div v-if="deviceList.length === 0" class="no-info-tip">
      <span class="PromptImg"></span>
      <span class="warningNotifyNone">当前没有设备型号，点击右侧<a class="warningNotifyAdd" v-on:click="onAddDeviceList()">新增</a>按钮进行添加</span>
    </div>
    <div class="device-list" v-if="deviceList.length > 0">
      <nms-pager-table v-if="deviceReset" :data="deviceList" :fields="deviceFields" :total-page="userTotalPage" :perPage="perPage" :biao-zhi="cage" v-model="curPage" @multiSelect='getSeletRow'/>
    </div>
  </div>
</template>

<script>
  import * as setJs from "../../assets/js/set"
  import NmsDialog from "../../components/common/nms-dialog"
  import NmsPagerTable from "../../components/common/nms-pager-table";
  import NmsBigDialog from "../../components/common/nms-big-dialog";
  import api from '../../axios';

  export default {
    name: "deviceset",
    components: {NmsBigDialog, NmsDialog, NmsPagerTable},
    data() {
      return {
        device_type: 'all',
        device_types: [{name: '所有类型', type: 'all'},
                       {name: '软件', type: '0'},
                       {name: '硬件', type: '1'},
                       {name: '外设', type: '2'}],
        device_model: '',
        // 表格每页显示数量
        deviceList: [],
        deviceFields: [],
        perPage: 10,
        curPage: 1,
        cage: 1,
        userTotalPage: 1,
        TotalNum: 0,
        domainCount: 0,
        selectRow: '',
        deviceReset: true,
        addConfirm: true,
        inputName: '',
        inputNameState: 0,
        inputProductName: '',
        inputProductNameState: 0,
        inputDeviceTag: '',
        inputDeviceTagState: 0,
        terminalType: "1",
        error_msg: '',
      }
    },
    methods: {
      typeClick: function() {

      },
      searchDevice: function() {
        console.log(this.device_type)
        console.log(this.device_model)
        api.getDeviceConfig({params: {terminal_type: this.device_type, terminal_model: this.device_model, page: 1}}).then((res) => {
          console.log(res)
          if (res.status == undefined) {
            if (res.success == 1) {
              this.deviceList = res.device
              this.TotalNum = res.TotalNum
              this.userTotalPage = Math.ceil(res.TotalNum / this.perPage);
              this.cage = 2
            }
          } else if (res.error_code == 111401) {
            this.$router.push({name: 'forbidden'})
          }
        })
        this.selectRow = ''
      },
      onDeleteDeviceList: function() {
        this.$refs.deviceEditDeleteDialog.open()
      },
      deleteDeviceList: function() {
        api.deleteDeviceConfig({
          name: this.selectRow.name,
          product_name: this.selectRow.product_name,
        }).then(res => {
          if (res.success == 1) {
            this.$message({
              duration: 2000,
              center: true,
              message: '删除成功',
              offset: 400,
            })
          } else {
            this.$message({
              duration: 2000,
              center: true,
              message: '删除失败',
              offset: 400,
            })
          }
          api.getDeviceConfig({params: {terminal_type: this.device_type, terminal_model: this.device_model, page: 1}}).then((res) => {
            console.log(res)
            if (res.success == 1) {
              this.deviceList = res.device
              this.TotalNum = res.TotalNum
              this.userTotalPage = Math.ceil(res.TotalNum / this.perPage)
              this.deviceReset = false
              this.$nextTick(() => {
                this.deviceReset = true
              })
            }
          })
          this.selectRow = ''
        }).catch(error => {
          console.log(error)
        })
      },
      onAddDeviceList: function() {
        this.inputName = ''
        this.inputProductName = ''
        this.inputDeviceTag = ''
        this.terminalType = '1'
        this.addConfirm = true
        this.$refs.addDeviceDialog.open()
      },
      getSeletRow: function(data) {
        if (this.selectRow === data) {
          this.selectRow = ''
        } else {
          this.selectRow = data
        }
      },
      examineMsg: function() {
        var nameProductReg = /^([^\/])*$/
        var nameProductRe = new RegExp(nameProductReg)
        if (this.inputName !== '') {
          if (this.inputName.length > 128) {
            this.errorDialog.open('主型号输入超出范围（限制128字节）')
            this.inputName = ''
          }
        }
        if (this.inputProductName !== '') {
          if (!nameProductRe.test(this.inputProductName)) {
            this.errorDialog.open("子型号输入格式错误（不能包含'/'）")
            this.inputProductName = ''
          } else {
            if (this.inputProductName.length > 128) {
              this.errorDialog.open('子型号输入超出范围（限制128字节）')
              this.inputProductName = ''
            }
          }
        }
        if (this.inputDeviceTag !== '') {
          if (this.inputDeviceTag.length > 50) {
            this.errorDialog.open('设备输入超出范围（限制50字节）')
            this.inputDeviceTag = ''
          }
        }
      },
      OnCancel: function() {
        this.inputDeviceTag = ''
        this.inputName = ''
        this.inputProductName = ''
        this.terminalType = '1'
        this.addConfirm = true
      },
      OnSave: function () {
        if (this.inputName !== '' && this.inputProductName !== '' && (this.inputDeviceTag !== '' || this.terminalType == '2')) {
          api.addDeviceConfig({
            name: this.inputName,
            terminal_type: this.terminalType,
            device_tag: this.inputDeviceTag,
            product_name: this.inputProductName,
          }).then(res => {
            console.log(res)
            if (res.success == 0) {
              this.error_msg = res.message
              this.$refs.deviceEditFailDialog.open();
            } else if (res.success == 1) {
              this.$message({
                duration: 2000,
                center: true,
                message: '保存成功',
                offset: 400,
              })
            }
            this.inputName = ''
            this.inputProductName = ''
            this.inputDeviceTag = ''
            this.terminalType = "1"
          })
          api.getDeviceConfig({params: {terminal_type: this.device_type, terminal_model: this.device_model, page: 1}}).then((res) => {
            console.log(res)
            if (res.success == 1) {
              this.deviceList = res.device
              this.TotalNum = res.TotalNum
              this.userTotalPage = Math.ceil(res.TotalNum / this.perPage);
              this.cage = 2
            }
          })
          this.selectRow = ''
        } else {
          this.$refs.deviceEditWarningDialog.open();
          this.inputName = ''
          this.inputProductName = ''
          this.inputDeviceTag = ''
          this.terminalType = "1"
        }
      }
    },
    watch: {
      // 翻页跳转
      curPage: function(newPageNum, oldPageNum) {
        console.log(newPageNum)
        this.cage = 1
        this.selectRow = ''
        if (newPageNum <= this.userTotalPage && newPageNum > 0) {
          api.getDeviceConfig({params: {terminal_type: this.device_type, terminal_model: this.device_model, page: newPageNum}}).then((res) => {
            console.log(res)
            if (res.status == undefined) {
              if (res.success == 1) {
                this.deviceList = res.device
                this.deviceFields = setJs.getDeviceConfigFields()
                this.TotalNum = res.TotalNum
                this.userTotalPage = Math.ceil(res.TotalNum / this.perPage);
              }
            } else if (res.error_code == 111401) {
              this.$router.push({name: 'forbidden'})
            }
          })
        }
      },
      terminalType: function (newstate, oldstart) {
        if (newstate == '2') {
          this.inputDeviceTag = ''
          this.inputDeviceTagState = 1
        } else {
          if (this.inputDeviceTag == '') {
            this.inputDeviceTagState = 0
          }
        }
        if (this.inputNameState === 1 && this.inputProductNameState === 1 && this.inputDeviceTagState === 1) {
          this.addConfirm = false
        } else {
          this.addConfirm = true
        }
      },
      inputName: function (newstate, oldstart) {
        // trim() 删除字符串前后所有空格
        if (newstate.trim().length > 0) {
          this.inputNameState = 1
        } else {
          this.inputNameState = 0
        }
        if (this.inputNameState === 1 && this.inputProductNameState === 1 && this.inputDeviceTagState === 1) {
          this.addConfirm = false
        } else {
          this.addConfirm = true
        }
      },
      inputProductName: function (newstate, oldstart) {
        if (newstate.trim().length > 0) {
          this.inputProductNameState = 1
        } else {
          this.inputProductNameState = 0
        }
        if (this.inputNameState === 1 && this.inputProductNameState === 1 && this.inputDeviceTagState === 1) {
          this.addConfirm = false
        } else {
          this.addConfirm = true
        }
      },
      inputDeviceTag: function (newstate, oldstart) {
        if (this.terminalType !== '2') {
          if (newstate.trim().length > 0) {
            this.inputDeviceTagState = 1
          } else {
            this.inputDeviceTagState = 0
          }
          if (this.inputNameState === 1 && this.inputProductNameState === 1 && this.inputDeviceTagState === 1) {
            this.addConfirm = false
          } else {
            this.addConfirm = true
          }
        }
      },
    },
    mounted: function() {
      this.deviceFields = setJs.getDeviceConfigFields()
      api.getDeviceConfig({params: {terminal_type: 'all', terminal_model: '', page: 1}}).then((res) => {
        console.log(res)
        if (res.status == undefined) {
          if (res.success == 1) {
            this.deviceList = res.device
            this.TotalNum = res.TotalNum
            this.userTotalPage = Math.ceil(res.TotalNum / this.perPage);
          }
        } else if (res.error_code == 111401) {
          this.$router.push({name: 'forbidden'})
        }
      })
      this.selectRow = ''
    },
  }
</script>

<style scoped>
.delTipsDiv {
  text-align: center;
  padding-top: 50px;
}
.search-line {
  float: left;
  width: 100%;
}
.filter-text{
  width: 120px;
  margin-right: 10px;
  float: left;
}
.filter-select{
  float: left;
}
#searchFloat{
  float: left;
}
#addFloat{
  float: right;
  margin-right: 6px;
}
#deleteFloat{
  float: right;
}
.device-list{
  float: left;
  width: 100%;
}
.fontCommon {
  clear: both;
  margin-top: 19px;
  font-size: 13px;
  color: #4e4e4e;
  position: relative;
  overflow: hidden;

}
.specialCommon {
  display: inline-block;
  width: 100px;
  height: 10px;
  vertical-align:top
}
.modifyCommon {
  display: inline-block;
  margin-top: 20px;
  margin-left: 51px;
  width: 100px;
  height: 20px;
}
.specialPathCommon{
  display: inline-block;
  width: 230px;
  height:600px;
  vertical-align:top
}
.backNamePathCommon {
  margin-top: 20px;
  display: inline-block;
  width: 230px;
  height: 20px;
}
.radiodiv {
  margin-right: 1%;
}
.textleft {
  text-align: left;
}
.warningNotifyAdd{
  color: #007ac0;
  text-decoration: underline
}
</style>
