<template>
  <div>
     <div class="tradition-meeting-back">
        <span class="back-btn" @click="$router.go(-1)"></span>
        <span class="base-info-title">添加定时巡检</span>
        <button id="btnCancel" class="normal-btn" @click="OnCancelAddTimingTask()">取消</button>
        <button id="btnSave" class="normal-btn" @click="OnSaveTimingTask()">保存</button>
     </div>

     <div class="inspect-time-container">
          <div class="add-inspection-title">巡检时间</div>
          <ul>
              <li class="add-inspection-time">
                <el-date-picker
                  v-model="value"
                  type="datetime"
                  placeholder="选择日期"
                  style="padding-left: 30px;">
                </el-date-picker>
              </li>
          </ul>

          <div style="float:left;padding-top:4px;">
            <el-checkbox v-model="critical" @change="recyclecheck()">重复</el-checkbox>
          </div>
          <ul class="inspect-time-show-container" v-if="value1.length > 0 && critical===true">
              <li><p id="inspect-time-show">每周的{{ moncheck }}{{ tuecheck }}{{ wedcheck }}{{ thucheck }}{{ fricheck }}{{ satcheck }}{{ suncheck }}进行,直到{{ value1 }}</p></li>
              <li><a href="#" @click="editCheck()">编辑</a></li>
          </ul>
     </div>
     <div id="inspectcontent" class="inspect-item-container">
        <div class="add-inspection-title">巡检项</div>
        <table style="border-collapse: collapse;border-spacing: 0;">
          <tr>
            <td><el-checkbox v-model="checked_l"  true-label="license" false-label=''>License文件</el-checkbox></td>
            <td>
               <el-select v-model="sServiceDomainMoid_l" placeholder="请选择" @change="snodeClick">
                  <el-option
                    v-for="(item,index) in sServiceDomainMoids_l"
                    :key="index"
                    :label="item.text"
                    :value="item.text">
                  </el-option>
                </el-select>
            </td>
            <td>
               <el-select v-model="sPlatformDomainMoid_l" placeholder="请选择" @change="snodeClick">
                  <el-option
                    v-for="(item,index) in sPlatformDomainMoids_l"
                    :key="index"
                    :label="item.text"
                    :value="item.text">
                  </el-option>
                </el-select>
            </td>
            <td>
               <el-select v-model="sVirtualMachine_l" placeholder="请选择" @change="snodeClick">
                  <el-option
                    v-for="(item,index) in sVirtualMachines_l"
                    :key="index"
                    :label="item.text"
                    :value="item.text">
                  </el-option>
                </el-select>
            </td>
          </tr>
          <tr>
            <td><el-checkbox v-model="checked_so"  true-label="resource" false-label=''>服务器资源</el-checkbox></td>
            <td>
               <el-select v-model="sServiceDomainMoid_so" placeholder="请选择" @change="snodeClick">
                  <el-option
                    v-for="(item,index) in sServiceDomainMoids_so"
                    :key="index"
                    :label="item.text"
                    :value="item.text">
                  </el-option>
               </el-select>
            </td>
            <td>
               <el-select v-model="sPlatformDomainMoid_so" placeholder="请选择" @change="snodeClick">
                  <el-option
                    v-for="(item,index) in sPlatformDomainMoids_so"
                    :key="index"
                    :label="item.text"
                    :value="item.text">
                  </el-option>
               </el-select>
            </td>
            <td>
               <el-select v-model="sVirtualMachine_so" placeholder="请选择" @change="snodeClick">
                  <el-option
                    v-for="(item,index) in sVirtualMachines_so"
                    :key="index"
                    :label="item.text"
                    :value="item.text">
                  </el-option>
               </el-select>
            </td>
          </tr>
          <tr>
            <td><el-checkbox v-model="checked_st"  true-label="server" false-label=''>服务器状态</el-checkbox></td>
            <td>
               <el-select v-model="sServiceDomainMoid_st" placeholder="请选择" @change="snodeClick">
                  <el-option
                    v-for="(item,index) in sServiceDomainMoids_st"
                    :key="index"
                    :label="item.text"
                    :value="item.text">
                  </el-option>
               </el-select>
            </td>
            <td>
               <el-select v-model="sPlatformDomainMoid_st" placeholder="请选择" @change="snodeClick">
                  <el-option
                    v-for="(item,index) in sPlatformDomainMoids_st"
                    :key="index"
                    :label="item.text"
                    :value="item.text">
                  </el-option>
               </el-select>
            </td>
            <td>
               <el-select v-model="sVirtualMachine_st" placeholder="请选择" @change="snodeClick">
                  <el-option
                    v-for="(item,index) in sVirtualMachines_st"
                    :key="index"
                    :label="item.text"
                    :value="item.text">
                  </el-option>
               </el-select>
            </td>
          </tr>
          <tr>
            <td><el-checkbox v-model="checked_t" true-label="terminal" false-label=''>终端状态</el-checkbox></td>
            <td>
               <el-select v-model="sServiceDomainMoid_t" placeholder="请选择" @change="snodeClick">
                  <el-option
                    v-for="(item,index) in sServiceDomainMoids_t"
                    :key="index"
                    :label="item.text"
                    :value="item.text">
                  </el-option>
               </el-select>
            </td>
            <td>
               <el-select v-model="sPlatformDomainMoid_t" placeholder="请选择" @change="snodeClick">
                  <el-option
                    v-for="(item,index) in sPlatformDomainMoids_t"
                    :key="index"
                    :label="item.text"
                    :value="item.text">
                  </el-option>
               </el-select>
            </td>
          </tr>
        </table>
     </div>
     <nms-dialog title="重复" ref="repetitionDlg" @confirm="confirmDlg()">
        <div slot="content" class="warning-info">
          <tr>
            <td i="body" class="ui-dialog-body" style="padding: 26px 34px 0px;">
              <div i="content" class="ui-dialog-content" id="content:1555564649759" style="width: 490px; height: 180px;">
                <div class="floatleft">
                    <span>每周的</span>
                </div>
                <div class="clearboth"></div>
                <ul class="repeat_line">
                    <li class="week-container">
                      <el-checkbox v-model="moncheck" true-label="周一，" false-label='' @change="monCheck()">周一</el-checkbox>
                    </li>
                    <li class="week-container">
                      <el-checkbox v-model="tuecheck" true-label="周二，" false-label='' @change="tueCheck()">周二</el-checkbox>
                    </li>
                    <li class="week-container">
                      <el-checkbox v-model="wedcheck" true-label="周三，" false-label='' @change="wedCheck()">周三</el-checkbox>
                    </li>
                    <li class="week-container">
                      <el-checkbox v-model="thucheck" true-label="周四，" false-label='' @change="thuCheck()">周四</el-checkbox>
                    </li>
                    <li class="week-container">
                      <el-checkbox v-model="fricheck"  true-label="周五，" false-label='' @change="friCheck()">周五</el-checkbox>
                    </li>
                    <li class="week-container">
                      <el-checkbox v-model="satcheck" true-label="周六，" false-label='' @change="satCheck()">周六</el-checkbox>
                    </li>
                    <li class="week-container">
                      <el-checkbox v-model="suncheck" true-label="周日" false-label='' @change="sunCheck()">周日</el-checkbox>
                    </li>
                </ul>
                <div class="floatleft repeat_line">
                    <span style="margin-right: 22px;">结束日期</span>
                    <el-date-picker
                      size="mini"
                      v-model="value1"
                      type="date"
                      placeholder="选择日期"
                      format="yyyy/MM/dd"
                      value-format="yyyy/MM/dd"
                      style="padding-left: 30px;"
                      @change="updateDate">
                    </el-date-picker>
                </div>
                <div class="floatleft repeat_line">
                    <span class="floatleft">摘要:</span>
                    <span id="summaryContent">每周的{{ moncheck }}{{ tuecheck }}{{ wedcheck }}{{ thucheck }}{{ fricheck }}{{ satcheck }}{{ suncheck }}进行,直到{{ value1 }}</span>
                </div>
              </div>
            </td>
          </tr>
        </div>
     </nms-dialog>
     <nms-dialog title="提示" :width="'400px'" :height="'152px'" :close-btn="true" ref="OnCancelAddTimingTaskDialog" @confirm="OnCancelAddTimingTaskNotify()">
       <div slot="content">
         <div class="delTipsDiv">
            <span class="PromptImg"></span>
            <span>确定不保存定时任务？</span>
         </div>
       </div>
     </nms-dialog>
  </div>
</template>
<script>
  import NmsDialog from "components/common/nms-dialog";
  import {DateTime} from "../../../assets/js/common"
  import {} from "assets/js/diagnose";
  export default {
    components: { NmsDialog},
    name: "add-regular-inspection",
    data() {
      return {
        tabType: "inspectionItem", // tab标签类型
        checked_l: "",
        checked_so: "",
        checked_st: "",
        checked_t: "",

        critical: "",

        moncheck: "",
        tuecheck: "",
        wedcheck: "",
        thucheck: "",
        fricheck: "",
        satcheck: "",
        suncheck: "",

        value: "",
        value1: "",

        week:"",

        repetition: "",

        //License文件
        sServiceDomainMoid_l: "所有服务域",
        sServiceDomainMoids_l: [],
        sPlatformDomainMoid_l: "所有平台域",
        sPlatformDomainMoids_l: sPlatformDomainMoids,
        sVirtualMachine_l: "所有虚拟机房",
        sVirtualMachines_l: sVirtualMachines,

        //服务器资源
        sServiceDomainMoid_so: "所有服务域",
        sServiceDomainMoids_so: [],
        sPlatformDomainMoid_so: "所有平台域",
        sPlatformDomainMoids_so: sPlatformDomainMoids,
        sVirtualMachine_so: "所有虚拟机房",
        sVirtualMachines_so: sVirtualMachines,

        //服务器状态
        sServiceDomainMoid_st: "所有服务域",
        sServiceDomainMoids_st: [],
        sPlatformDomainMoid_st: "所有平台域",
        sPlatformDomainMoids_st: sPlatformDomainMoids,
        sVirtualMachine_st: "所有虚拟机房",
        sVirtualMachines_st: sVirtualMachines,

        //终端状态
        sServiceDomainMoid_t: "所有服务域",
        sServiceDomainMoids_t: [],
        sPlatformDomainMoid_t: "所有平台域",
        sPlatformDomainMoids_t: sPlatformDomainMoids
      };
    },
    activated: function() {
      this.sServiceDomainMoids_l = getsServiceDomainMoids();
      this.sServiceDomainMoids_so = getsServiceDomainMoids();
      this.sServiceDomainMoids_st = getsServiceDomainMoids();
      this.sServiceDomainMoids_t = getsServiceDomainMoids();
    },
    mounted: function() {
      let date = new DateTime();
      this.week = date.getWeek();
      console.log(this.week)
      if(this.week==="星期五") {
        this.fricheck=true
        this.fricheck="周五，"
      }else if(this.week==="星期一") {
        this.moncheck=true
        this.moncheck="周一，"
      }else if(this.week==="星期二") {
        this.tuecheck=true
        this.tuecheck="周二，"
      }else if(this.week==="星期三") {
        this.wedcheck=true
        this.wedcheck="周三，"
      }else if(this.week==="星期四") {
        this.thucheck=true
        this.thucheck="周四，"
      }else if(this.week==="星期六") {
        this.satcheck=true
        this.satcheck="周六，"
      }else if(this.week="星期日") {
        this.suncheck=true
        this.suncheck="周日"
      }
    },
    methods: {
      //重复
      recyclecheck: function() {
        console.log("recyclecheck");
        if(this.critical==true) {
          this.$refs.repetitionDlg.open();
        }
      },
      //编辑
      editCheck: function() {
        console.log("editCheck");
        this.$refs.repetitionDlg.open();
      },
      updateDate: function(val) {
        console.log("val:"+val)
        this.value1=val
        console.log("this.value1:"+this.value1)
        console.log("this.value1:"+typeof(this.value1))
        console.log("this.value1:"+(this.value1).length)
      },
      confirmDlg: function() {
        console.log("待使用...")
      },
      OnSaveTimingTask: function () {
        // 保存
        if (this.value==="") {
          //判断是否为空
          this.value=""
        }else {
          const d = new Date(this.value)
          const resDate = d.getFullYear() + '-' + this.p((d.getMonth() + 1)) + '-' + this.p(d.getDate())
          const resTime = this.p(d.getHours()) + ':' + this.p(d.getMinutes()) + ':' + this.p(d.getSeconds())
          this.value=resDate+" "+resTime
        }
        var cont=$("#summaryContent");
        this.repetition=cont.text()

        this.$router.push({
          name: 'inspectionhome',
          params: {
            //标签可见与不可见-判断标识
            path_name:"add-regular-inspection",
            //四种资源
            checked_l: this.checked_l,
            checked_so: this.checked_so,
            checked_st: this.checked_st,
            checked_t: this.checked_t,
            //巡检时间
            value: this.value,
            //“重复”里面的内容
            repetition: this.repetition,
            //License文件
            sServiceDomainMoid_l: this.sServiceDomainMoid_l,
            sPlatformDomainMoid_l: this.sPlatformDomainMoid_l,
            sVirtualMachine_l: this.sVirtualMachine_l,
            //服务器资源
            sServiceDomainMoid_so: this.sServiceDomainMoid_so,
            sPlatformDomainMoid_so: this.sPlatformDomainMoid_so,
            sVirtualMachine_so: this.sVirtualMachine_so,
            //服务器状态
            sServiceDomainMoid_st: this.sServiceDomainMoid_st,
            sPlatformDomainMoid_st: this.sPlatformDomainMoid_st,
            sVirtualMachine_st: this.sVirtualMachine_st,
            //终端状态
            sServiceDomainMoid_t: this.sServiceDomainMoid_t,
            sPlatformDomainMoid_t: this.sPlatformDomainMoid_t,
          }
        })
      },
      p(s) {
          return s < 10 ? '0' + s : s
      },
      OnCancelAddTimingTask: function () {
        this.$refs.OnCancelAddTimingTaskDialog.open();
      },
      OnCancelAddTimingTaskNotify: function () {
        this.$router.go(-1)
      }
    }
  };
</script>

<style scoped>
#inspectcontent {
  width: 1479px;
  height: 319px;
}
table {
  width: 468px;
  height: 296px;
}
td {
  padding-right: 19px;
}
tr {
  text-align: left;
  vertical-align: -webkit-baseline-middle;
}

.inspect-time-container {
  margin-top: 30px;
  overflow: hidden;
}
.add-inspection-title {
  float: left;
  width: 87px;
  font-size: 12px;
  color: #4e4e4e;
  position: relative;
  top: 4px;
  text-align: left;
}
.add-inspection-time {
  float: left;
  margin-right: 19px;
}
.inspect-item-container {
  margin-top: 43px;
}
.tradition-meeting-back > .normal-btn {
  float: right;
}
.tradition-meeting-back {
  overflow: hidden;
  height: 30px;
  line-height: 30px;
}
.ui-dialog-content {
  display: inline-block;
  position: relative;
  vertical-align: middle;
  zoom: 1;
  display: inline;
  padding: 0;
  overflow-y: auto;
}
.floatleft {
  float: left;
}
.clearboth {
  clear: both;
}
.repeat_line {
  padding-top: 27px;
}
.week-container {
  float: left;
  width: 65px;
}
#summaryContent {
    padding-left: 5px;
}
.inspect-time-show-container {
    /* display: none; */
    float: left;
    height: 24px;
    line-height: 30px;
    padding-left: 24px;
}
.inspect-time-show-container>li {
    float: left;
    font-size: 12px;
    color: #4e4e4e;
}
.inspect-time-show-container a {
    color: #007ac0;
    text-decoration: underline;
    cursor: pointer;
}
.inspect-time-show-container>li:first-child {
    margin-right: 11px;
}
.delTipsDiv {
    text-align: center;
    padding-top: 50px;
}
</style>
