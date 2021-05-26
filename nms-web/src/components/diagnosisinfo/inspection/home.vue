<template>
  <el-tabs v-model="tabType" style="cursor:pointer" @tab-click="handleClick">
    <el-tab-pane label="即时巡检" name="inspectionItem" style="cursor:default">
      <div id="inspectcontent">
        <table style="border-collapse:separate;border-spacing:0px 25px;">
          <tr>
            <td><el-checkbox v-model="checked_l"  true-label="license" false-label=''>License文件</el-checkbox></td>
            <td>
               <el-select v-model="lServiceDomainMoid" placeholder="请选择">
                  <el-option
                    v-for="(item,index) in lServiceDomainMoids"
                    :key="index"
                    :label="item.name"
                    :value="item.moid">
                  </el-option>
                </el-select>
            </td>
          </tr>
          <tr>
            <td><el-checkbox v-model="checked_so"  true-label="resource" false-label=''>会议资源</el-checkbox></td>
            <td>
               <el-select v-model="mServiceDomainMoid" placeholder="请选择">
                  <el-option
                    v-for="(item,index) in mServiceDomainMoids"
                    :key="index"
                    :label="item.name"
                    :value="item.moid">
                  </el-option>
               </el-select>
            </td>
            <td>
               <el-select v-model="mPlatformDomainMoid" placeholder="请选择">
                  <el-option
                    v-for="(item,index) in mPlatformDomainMoids"
                    :key="index"
                    :label="item.name"
                    :value="item.moid">
                  </el-option>
               </el-select>
            </td>
            <td>
               <el-select v-model="mMachineRoomMoid" placeholder="请选择">
                  <el-option
                    v-for="(item,index) in mMachineRoomMoids"
                    :key="index"
                    :label="item.name"
                    :value="item.moid">
                  </el-option>
               </el-select>
            </td>
          </tr>
          <tr>
            <td><el-checkbox v-model="checked_st"  true-label="server" false-label=''>服务器状态</el-checkbox></td>
            <td>
               <el-select v-model="sServiceDomainMoid" placeholder="请选择">
                  <el-option
                    v-for="(item,index) in sServiceDomainMoids"
                    :key="index"
                    :label="item.name"
                    :value="item.moid">
                  </el-option>
               </el-select>
            </td>
            <td>
               <el-select v-model="sPlatformDomainMoid" placeholder="请选择">
                  <el-option
                    v-for="(item,index) in sPlatformDomainMoids"
                    :key="index"
                    :label="item.name"
                    :value="item.moid">
                  </el-option>
               </el-select>
            </td>
            <td>
               <el-select v-model="sMachineRoomMoid" placeholder="请选择">
                  <el-option
                    v-for="(item,index) in sMachineRoomMoids"
                    :key="index"
                    :label="item.name"
                    :value="item.moid">
                  </el-option>
               </el-select>
            </td>
          </tr>
          <tr>
            <td><el-checkbox v-model="checked_t" true-label="terminal" false-label=''>终端状态</el-checkbox></td>
            <td>
               <el-select v-model="tTerminalDomainMoid" placeholder="请选择">
                  <el-option
                    v-for="(item,index) in tTerminalDomainMoids"
                    :key="index"
                    :label="item.name"
                    :value="item.moid">
                  </el-option>
               </el-select>
            </td>
            <td>
               <el-select v-model="tUserMoid" placeholder="请选择">
                  <el-option
                    v-for="(item,index) in tUserMoids"
                    :key="index"
                    :label="item.name"
                    :value="item.moid">
                  </el-option>
               </el-select>
            </td>
          </tr>
        </table>
        <div><button style="float:left;" id="btnBeginInspect" class="normal-btn"  @click="StartRealTimeInspect()">开始巡检</button></div>
      </div>
      <div class="grab-msg" v-show="inspect_info">
        <el-select v-model="selectType" class="grab-select" placeholder="请选择" style="float: left;">
          <el-option
            v-for="(item,index) in selectTypes"
            :key="index"
            :label="item.text"
            :value="item.value">
          </el-option>
        </el-select>
        <span class="time_msg">巡检时间<span class="obj">{{ grab_start }}</span></span>
        <button class="normal-btn export" @click="onExport()" style="float: right">导出</button>
      </div>
      <div class="license-list" v-show="lince">
        <div v-if="licenseList.length === 0" class="no-info-tip">
          没有巡检数据！
        </div>
        <div v-if="licenseList.length > 0">
          <nms-pager-table :data="licenseList" :fields="licenseFields" :total-page="licenseTotalPage" :biao-zhi="cage" v-model="curPage"/>
        </div>
      </div>
      <div class="resource-list" v-show="resou">
        <!-- <res-info :res-list="resList" style="width: 1506px;"></res-info> -->
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
      </div>
      <div class="server-list" v-show="ser">
        <div v-if="serverList.length === 0" class="no-info-tip">
          没有巡检数据！
        </div>
        <div v-if="serverList.length > 0">
          <nms-pager-table :data="serverList" :fields="serverFields" :total-page="serverTotalPage" :biao-zhi="cage" v-model="curPage"/>
        </div>
      </div>
      <div class="rterminal-list" v-show="ter">
        <div v-if="terminalList.length === 0" class="no-info-tip">
          没有巡检数据！
        </div>
        <div v-if="terminalList.length > 0">
          <nms-pager-table :data="terminalList" :fields="terminalListFields" :total-page="terminalListTotalPage" :biao-zhi="cage" v-model="curPage"/>
        </div>
      </div>
    </el-tab-pane>
    <el-tab-pane label="定时巡检" name="regularInspection" style="cursor:default">
      <div>
        <button style="position: absolute;top:0;right:0;" id="btnAddTask" class="normal-btn" @click="OnAddTimingTask()">添加定时巡检</button>
      </div>
      <div id="timingInspectInfo">
        <div class="inspect-task-container"><nms-pager-table :data="inspectTaskList" :fields="inspectTaskListFields" :total-page="inspectTaskListTotalPage" :biao-zhi="cage" v-model="curPage"/></div>
        <div class="timingTaskEmptyTip" v-if="inspectTaskList.length==0">
          <span class="PromptImg"></span>
          <span class="warningNotifyNone">未进行定时巡检，请设置右上角<a class="warningNotifyAdd" v-on:click="OnAddTimingTask()">添加定时巡检</a>按钮开始定时巡检吧！</span>
        </div>
      </div>
      <nms-dialog title="提示" :width="'400px'" :height="'152px'" :close-btn="true" ref="OnDelTaskDialog" @confirm="OnDelTaskDialogNotify()">
       <div slot="content">
         <div class="delTipsDiv">
            <span class="PromptImg"></span>
            <span>真的删除巡检任务吗？</span>
         </div>
       </div>
      </nms-dialog>
      <nms-big-dialog title="添加" :width="'730px'" :height="'460px'" ref="addInspectDlg" @confirm="onSign()" @cancel="cancelSign()" @close="closeSign()">
        <div slot="content" class="main-dia">
          <div class="inspect-time-container">
                <div class="add-inspection-title">巡检时间</div>
                <DateBox inputId="d1" v-model="startDate" style="width: 110px;float:left;height:24px" format="yyyy-MM-dd"></DateBox>
                <el-select v-model="hour" placeholder="请选择" class="select-time">
                  <el-option
                    v-for="(item,index) in hours"
                    :key="index"
                    :label="item.text"
                    :value="item.value">
                  </el-option>
                </el-select>
                <el-select v-model="minute" placeholder="请选择" class="select-time">
                  <el-option
                    v-for="(item,index) in minutes"
                    :key="index"
                    :label="item.text"
                    :value="item.value">
                  </el-option>
                </el-select>
                <el-select v-model="second" placeholder="请选择" class="select-time">
                  <el-option
                    v-for="(item,index) in seconds"
                    :key="index"
                    :label="item.text"
                    :value="item.value">
                  </el-option>
                </el-select>
                <div style="float:left;padding-top:4px;padding-left:35px">
                  <el-checkbox v-model="critical" @change="recyclecheck()">重复</el-checkbox>
                </div>
                <ul class="inspect-time-show-container" v-if="value1.length > 0 && critical && postShow">
                    <li><p id="inspect-time-show">{{ value }}日开始,每周的{{ moncheck }}{{ tuecheck }}{{ wedcheck }}{{ thucheck }}{{ fricheck }}{{ satcheck }}{{ suncheck }}{{ hourValue }}:{{ minuteValue }}:{{ secondValue }}进行,直到{{ value1 }}</p></li>
                    <li><a @click="editCheck()">编辑</a></li>
                </ul>
                <ul class="inspect-time-show-container" v-if="editShow">
                    <li><p id="inspect-time-show">{{ value }}日开始,每周的{{ moncheck }}{{ tuecheck }}{{ wedcheck }}{{ thucheck }}{{ fricheck }}{{ satcheck }}{{ suncheck }}{{ hourValue }}:{{ minuteValue }}:{{ secondValue }}进行,直到{{ value1 }}</p></li>
                    <li><a @click="editCheck()">编辑</a></li>
                </ul>
          </div>
          <div id="inspectcontent-timer" class="inspect-item-container">
              <div class="add-inspection-title">巡检项</div>
              <table style="border-collapse: collapse;border-spacing: 0; height: 196px;">
                <tr>
                  <td><el-checkbox v-model="checked_l"  true-label="license" false-label=''>License文件</el-checkbox></td>
                  <td>
                    <el-select v-model="lServiceDomainMoid" placeholder="请选择">
                        <el-option
                          v-for="(item,index) in lServiceDomainMoids"
                          :key="index"
                          :label="item.name"
                          :value="item.moid">
                        </el-option>
                      </el-select>
                  </td>
                </tr>
                <tr>
                  <td><el-checkbox v-model="checked_so"  true-label="resource" false-label=''>会议资源</el-checkbox></td>
                  <td>
                    <el-select v-model="mServiceDomainMoid" placeholder="请选择">
                        <el-option
                          v-for="(item,index) in mServiceDomainMoids"
                          :key="index"
                          :label="item.name"
                          :value="item.moid">
                        </el-option>
                    </el-select>
                  </td>
                  <td>
                    <el-select v-model="mPlatformDomainMoid" placeholder="请选择">
                        <el-option
                          v-for="(item,index) in mPlatformDomainMoids"
                          :key="index"
                          :label="item.name"
                          :value="item.moid">
                        </el-option>
                    </el-select>
                  </td>
                  <td>
                    <el-select v-model="mMachineRoomMoid" placeholder="请选择">
                        <el-option
                          v-for="(item,index) in mMachineRoomMoids"
                          :key="index"
                          :label="item.name"
                          :value="item.moid">
                        </el-option>
                    </el-select>
                  </td>
                </tr>
                <tr>
                  <td><el-checkbox v-model="checked_st"  true-label="server" false-label=''>服务器状态</el-checkbox></td>
                  <td>
                    <el-select v-model="sServiceDomainMoid" placeholder="请选择">
                        <el-option
                          v-for="(item,index) in sServiceDomainMoids"
                          :key="index"
                          :label="item.name"
                          :value="item.moid">
                        </el-option>
                    </el-select>
                  </td>
                  <td>
                    <el-select v-model="sPlatformDomainMoid" placeholder="请选择">
                        <el-option
                          v-for="(item,index) in sPlatformDomainMoids"
                          :key="index"
                          :label="item.name"
                          :value="item.moid">
                        </el-option>
                    </el-select>
                  </td>
                  <td>
                    <el-select v-model="sMachineRoomMoid" placeholder="请选择">
                        <el-option
                          v-for="(item,index) in sMachineRoomMoids"
                          :key="index"
                          :label="item.name"
                          :value="item.moid">
                        </el-option>
                    </el-select>
                  </td>
                </tr>
                <tr>
                  <td><el-checkbox v-model="checked_t" true-label="terminal" false-label=''>终端状态</el-checkbox></td>
                  <td>
                    <el-select v-model="tTerminalDomainMoid" placeholder="请选择">
                        <el-option
                          v-for="(item,index) in tTerminalDomainMoids"
                          :key="index"
                          :label="item.name"
                          :value="item.moid">
                        </el-option>
                    </el-select>
                  </td>
                  <td>
                    <el-select v-model="tUserMoid" placeholder="请选择">
                        <el-option
                          v-for="(item,index) in tUserMoids"
                          :key="index"
                          :label="item.name"
                          :value="item.moid">
                        </el-option>
                    </el-select>
                  </td>
                </tr>
              </table>
          </div>
        </div>
      </nms-big-dialog>
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
                      <el-checkbox v-model="moncheck" true-label="周一，" false-label=''>周一</el-checkbox>
                    </li>
                    <li class="week-container">
                      <el-checkbox v-model="tuecheck" true-label="周二，" false-label=''>周二</el-checkbox>
                    </li>
                    <li class="week-container">
                      <el-checkbox v-model="wedcheck" true-label="周三，" false-label=''>周三</el-checkbox>
                    </li>
                    <li class="week-container">
                      <el-checkbox v-model="thucheck" true-label="周四，" false-label=''>周四</el-checkbox>
                    </li>
                    <li class="week-container">
                      <el-checkbox v-model="fricheck"  true-label="周五，" false-label=''>周五</el-checkbox>
                    </li>
                    <li class="week-container">
                      <el-checkbox v-model="satcheck" true-label="周六，" false-label=''>周六</el-checkbox>
                    </li>
                    <li class="week-container">
                      <el-checkbox v-model="suncheck" true-label="周日" false-label=''>周日</el-checkbox>
                    </li>
                </ul>
                <div class="floatleft repeat_line">
                    <span style="margin-right: 16px;">结束日期</span>
                    <DateBox inputId="d1" v-model="endDate" style="width: 110px;height:24px" format="yyyy-MM-dd"></DateBox>
                </div>
                <div class="floatleft repeat_line" style="width:365px">
                    <span class="floatleft">摘要:</span>
                    <span id="summaryContent">每周的{{ moncheck }}{{ tuecheck }}{{ wedcheck }}{{ thucheck }}{{ fricheck }}{{ satcheck }}{{ suncheck }}进行,直到{{ value1 }}</span>
                </div>
              </div>
            </td>
          </tr>
        </div>
     </nms-dialog>
    </el-tab-pane>
  </el-tabs>
</template>

<script>
    import NmsDialog from "components/common/nms-dialog";
    import NmsBigDialog from "components/common/nms-big-dialog";
    import {getLicenseFields,getServerFields,getTerminalFields,getInspectionResInfo,getInspectTaskListFields,getHours,getMinutes,getSeconds} from "../../../assets/js/diagnose";
    import api from "../../../axios";
    import NmsPagerTable from "../../common/nms-pager-table";
    import ResInfo from "../../common/res-info";
    import {Upexcele}  from '../../../common/commonFunction'
    import {DateTime,FormatTime,get_time,FormatDateTime,KeepTwoNum,UnFormatTime} from "../../../assets/js/common";
    import ResUsageCircle from "../../common/res-usage-circle";
    export default {
        components:{NmsDialog, NmsPagerTable, ResInfo, NmsBigDialog, ResUsageCircle},
        name: "inspectionhome",
        inject: ['reload'],
        data () {
          return {
            tabType: 'inspectionItem',// tab标签类型
            isShow: false,
            areShow: true,
            sign: "", // 用去区分编辑/添加定时巡检的标志符

            perPage: 10, // 表格每页显示数量
            curPage: 1,
            cage: 1,
            //***************即时巡检************
            checked_l: "license",
            checked_so: "resource",
            checked_st: "server",
            checked_t: "terminal",

            warningDomains: [],
            warningUesrDomains: [],
            s: [],
            p: [],
            m: [],
            top_main: "",
            tm: [],
            tu: [],

            lince: false,
            resou: false,
            ser: false,
            ter: false,
            //License文件
            lServiceDomainMoid: "",
            lServiceDomainMoids: [],

            licenseList: [],
            licenseFields: [],
            licenseTotalPage: 1,

            //会议资源
            mServiceDomainMoid: "",
            mServiceDomainMoids: [],
            mPlatformDomainMoid: "",
            mPlatformDomainMoids: [],
            mMachineRoomMoid: "",
            mMachineRoomMoids: [],

            resData: [],
            resList: [],

            //服务器状态
            sServiceDomainMoid: "",
            sServiceDomainMoids: [],
            sPlatformDomainMoid: "",
            sPlatformDomainMoids: [],
            sMachineRoomMoid: "",
            sMachineRoomMoids: [],

            serverList: [],
            serverFields: [],
            serverTotalPage: 1,

            //终端状态
            tTerminalDomainMoid: "",
            tTerminalDomainMoids: [],
            tUserMoid: "",
            tUserMoids: [],

            terminalList: [],
            terminalListFields: [],
            terminalListTotalPage: 1,

            selectType: "",
            selectTypes: [],
            grab_start: "",

            inspect_data: {},
            // 巡检任务id
            taskid: '',
            inspect_info: false,

            //***************定时巡检************
            critical: false,

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

            inspectTaskList: [],
            inspectTaskListFields: getInspectTaskListFields(),
            inspectTaskListTotalPage: 1,

            startDate: new Date(),
            endDate: new Date(),
            hour: "00",
            hours: getHours(),
            minute: "00",
            minutes: getMinutes(),
            second: "00",
            seconds: getSeconds(),

            hourValue: "",
            minuteValue: "",
            secondValue: "",
            end_time: "",

            monday: 0,
            tuesday: 0,
            wednesday: 0,
            thursday: 0,
            friday: 0,
            saturday: 0,
            sunday: 0,

            postShow: true,
            editShow: false,

            edit_task_id: "",

            lv_show : false,
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
            CRPUsable: 0
          }
        },
        activated: function () {
          // platform
          api.getPlatformDomainTree().then((res) => {
            this.mServiceDomainMoids = []
            this.mPlatformDomainMoids = []
            this.mMachineRoomMoids = []
            this.lServiceDomainMoids = []
            this.sServiceDomainMoids = []
            this.sPlatformDomainMoids = []
            this.sMachineRoomMoids = []
            this.s=[]
            this.p=[]
            this.m=[]
            console.log("res.data "+JSON.stringify(res.data))
            this.warningDomains = res.data
            this.warningDomains.forEach(i=>{
              if(i.type=="service" || i.type=="kernel"){
                this.mServiceDomainMoids.push(i)
                this.lServiceDomainMoids.push(i)
                this.sServiceDomainMoids.push(i)
                this.s.push(i)
                if(i.type=="kernel"){
                  this.top_main=i.moid
                }
              }else if(i.type=="platform"){
                this.mPlatformDomainMoids.push(i)
                this.sPlatformDomainMoids.push(i)
                this.p.push(i)
              }else if(i.type=="machine_room"){
                this.mMachineRoomMoids.push(i)
                this.sMachineRoomMoids.push(i)
                this.m.push(i)
              }
            })
            this.lServiceDomainMoids.unshift({
              "moid": "all",
              "parent_moid": "",
              "name": "所有服务域",
              "type": "server"
            })
            this.lServiceDomainMoid = "all"
            this.mServiceDomainMoids.unshift({
              "moid": "all",
              "parent_moid": "",
              "name": "所有服务域",
              "type": "server"
            })
            this.mPlatformDomainMoids.unshift({
              "moid": "all",
              "parent_moid": "",
              "name": "所有平台域",
              "type": "platform"
            })
            this.mMachineRoomMoids.unshift({
              "moid": "all",
              "parent_moid": "",
              "name": "所有虚拟机房",
              "type": "machine_room"
            })
            this.mServiceDomainMoid = "all"
            this.mPlatformDomainMoid = "all"
            this.mMachineRoomMoid = "all"
            this.sServiceDomainMoids.unshift({
              "moid": "all",
              "parent_moid": "",
              "name": "所有服务域",
              "type": "server"
            })
            this.sPlatformDomainMoids.unshift({
              "moid": "all",
              "parent_moid": "",
              "name": "所有平台域",
              "type": "platform"
            })
            this.sMachineRoomMoids.unshift({
              "moid": "all",
              "parent_moid": "",
              "name": "所有虚拟机房",
              "type": "machine_room"
            })
            this.sServiceDomainMoid = "all"
            this.sPlatformDomainMoid = "all"
            this.sMachineRoomMoid = "all"
          })
          // user
          api.getUserDomainTree().then((res) => {
            this.tTerminalDomainMoids=[]
            this.tUserMoids=[]
            this.tm=[]
            this.tu=[]
            this.warningUesrDomains = res.data
            this.warningUesrDomains.forEach(i=>{
              if(i.type=="service" || i.type=="kernel"){
                this.tTerminalDomainMoids.push(i)
                this.tm.push(i)
              }else if(i.type=="user"){
                this.tUserMoids.push(i)
                this.tu.push(i)
              }
            })
            this.tTerminalDomainMoids.unshift({
              "moid": "all",
              "parent_moid": "",
              "name": "所有服务域",
              "type": "server"
            })
            this.tUserMoids.unshift({
              "moid": "all",
              "parent_moid": "",
              "name": "所有用户域",
              "type": "user"
            })
            this.tTerminalDomainMoid = "all"
            this.tUserMoid = "all"
          })

        },
        mounted: function() {
          this.updateType();

          this.value = FormatDateTime(this.startDate)
          this.hourValue = this.hour
          this.minuteValue = this.minute
          this.secondValue = this.second

          this.getStartWeek()
        },
        watch: {
          hour: function(val) {
            this.hourValue = val
          },
          minute: function(val) {
            this.minuteValue = val
          },
          second: function(val) {
            this.secondValue = val
          },
          startDate: function(val) {
            this.value = FormatDateTime(val)
          },
          endDate: function(val) {
            this.value1 = FormatDateTime(val)
          },
          tabType: function(val) {
            if(val=="regularInspection"){
              this.getTimerInspectInfo()
            }
            // checked updata
            this.checked_l="license",
            this.checked_so="resource",
            this.checked_st="server",
            this.checked_t="terminal"
            // platform updata
            this.mServiceDomainMoids = []
            this.mPlatformDomainMoids = []
            this.mMachineRoomMoids = []
            this.lServiceDomainMoids = []
            this.sServiceDomainMoids = []
            this.sPlatformDomainMoids = []
            this.sMachineRoomMoids = []
            this.warningDomains.forEach(i=>{
              if(i.type=="service" || i.type=="kernel"){
                this.mServiceDomainMoids.push(i)
                this.lServiceDomainMoids.push(i)
                this.sServiceDomainMoids.push(i)
              }else if(i.type=="platform"){
                this.mPlatformDomainMoids.push(i)
                this.sPlatformDomainMoids.push(i)
              }else if(i.type=="machine_room"){
                this.mMachineRoomMoids.push(i)
                this.sMachineRoomMoids.push(i)
              }
            })
            this.lServiceDomainMoids.unshift({
              "moid": "all",
              "parent_moid": "",
              "name": "所有服务域",
              "type": "server"
            })
            this.lServiceDomainMoid = "all"
            this.mServiceDomainMoids.unshift({
              "moid": "all",
              "parent_moid": "",
              "name": "所有服务域",
              "type": "server"
            })
            this.mPlatformDomainMoids.unshift({
              "moid": "all",
              "parent_moid": "",
              "name": "所有平台域",
              "type": "platform"
            })
            this.mMachineRoomMoids.unshift({
              "moid": "all",
              "parent_moid": "",
              "name": "所有虚拟机房",
              "type": "machine_room"
            })
            this.mServiceDomainMoid = "all"
            this.mPlatformDomainMoid = "all"
            this.mMachineRoomMoid = "all"
            this.sServiceDomainMoids.unshift({
              "moid": "all",
              "parent_moid": "",
              "name": "所有服务域",
              "type": "server"
            })
            this.sPlatformDomainMoids.unshift({
              "moid": "all",
              "parent_moid": "",
              "name": "所有平台域",
              "type": "platform"
            })
            this.sMachineRoomMoids.unshift({
              "moid": "all",
              "parent_moid": "",
              "name": "所有虚拟机房",
              "type": "machine_room"
            })
            this.sServiceDomainMoid = "all"
            this.sPlatformDomainMoid = "all"
            this.sMachineRoomMoid = "all"
            // user updata
            this.tTerminalDomainMoids=[]
            this.tUserMoids=[]
            this.warningUesrDomains.forEach(i=>{
              if(i.type=="service" || i.type=="kernel"){
                this.tTerminalDomainMoids.push(i)
              }else if(i.type=="user"){
                this.tUserMoids.push(i)
              }
            })
            this.tTerminalDomainMoids.unshift({
              "moid": "all",
              "parent_moid": "",
              "name": "所有服务域",
              "type": "server"
            })
            this.tUserMoids.unshift({
              "moid": "all",
              "parent_moid": "",
              "name": "所有用户域",
              "type": "user"
            })
            this.tTerminalDomainMoid = "all"
            this.tUserMoid = "all"
          },
          $route(now, old) {
            console.log("now:"+now.path)
            console.log("old:"+old.path)
            if (old.path==='/inspection/addregular') {
              this.isShow=false
              this.areShow=true
            }
            else if (old.path==='/inspection/inspection') {
              this.isShow=true
              this.areShow=false
            }
          },
          // License文件
          mServiceDomainMoid: function (val) {
            if(val=="all"){
              this.mServiceDomainMoids = []
              this.mPlatformDomainMoids = []
              this.mMachineRoomMoids = []
              this.mServiceDomainMoids = [].concat(this.s)
              this.mPlatformDomainMoids = [].concat(this.p)
              this.mMachineRoomMoids = [].concat(this.m)
              this.mServiceDomainMoids.unshift({
                  "moid": "all",
                  "parent_moid": "",
                  "name": "所有服务域",
                  "type": "server"
                })
                this.mPlatformDomainMoids.unshift({
                  "moid": "all",
                  "parent_moid": "",
                  "name": "所有平台域",
                  "type": "platform"
                })
                this.mMachineRoomMoids.unshift({
                  "moid": "all",
                  "parent_moid": "",
                  "name": "所有虚拟机房",
                  "type": "machine_room"
              })
              this.mServiceDomainMoid = "all"
              this.mPlatformDomainMoid = "all"
              this.mMachineRoomMoid = "all"
            }else if(val==this.top_main){
              this.mPlatformDomainMoids = []
              this.mMachineRoomMoids = []
              this.mPlatformDomainMoids = [].concat(this.p)
              this.mMachineRoomMoids = [].concat(this.m)
              this.mPlatformDomainMoids.unshift({
                  "moid": "all",
                  "parent_moid": "",
                  "name": "所有平台域",
                  "type": "platform"
              })
              this.mMachineRoomMoids.unshift({
                  "moid": "all",
                  "parent_moid": "",
                  "name": "所有虚拟机房",
                  "type": "machine_room"
              })
              this.mPlatformDomainMoid = "all"
              this.mMachineRoomMoid = "all"
            }else{
              this.mPlatformDomainMoids = []
              this.mMachineRoomMoids = []
              this.p.forEach(j=>{
                if(val==j.parent_moid){
                  this.mPlatformDomainMoids.push(j)
                  this.m.forEach(k=>{
                    if(j.moid==k.parent_moid){
                      this.mMachineRoomMoids.push(k)
                    }
                  })
                }
              })
              this.mPlatformDomainMoids.unshift({
                "moid": "all",
                "parent_moid": "",
                "name": "所有平台域",
                "type": "platform"
              })
              this.mPlatformDomainMoid="all"
              if(this.mMachineRoomMoids.length==0){
                this.mMachineRoomMoids.unshift({
                  "moid": "all",
                  "parent_moid": "",
                  "name": "无下级域",
                  "type": "machine_room"
                })
              }else{
                this.mMachineRoomMoids.unshift({
                  "moid": "all",
                  "parent_moid": "",
                  "name": "所有虚拟机房",
                  "type": "machine_room"
                })
              }
              this.mMachineRoomMoid="all"
            }
          },
          // 会议资源
          // 服务器状态
          sServiceDomainMoid: function (val) {
            if(val=="all"){
              this.sServiceDomainMoids = []
              this.sPlatformDomainMoids = []
              this.sMachineRoomMoids = []
              this.sServiceDomainMoids = [].concat(this.s)
              this.sPlatformDomainMoids = [].concat(this.p)
              this.sMachineRoomMoids = [].concat(this.m)
              this.sServiceDomainMoids.unshift({
                  "moid": "all",
                  "parent_moid": "",
                  "name": "所有服务域",
                  "type": "server"
                })
                this.sPlatformDomainMoids.unshift({
                  "moid": "all",
                  "parent_moid": "",
                  "name": "所有平台域",
                  "type": "platform"
                })
                this.sMachineRoomMoids.unshift({
                  "moid": "all",
                  "parent_moid": "",
                  "name": "所有虚拟机房",
                  "type": "machine_room"
              })
              this.sServiceDomainMoid = "all"
              this.sPlatformDomainMoid = "all"
              this.sMachineRoomMoid = "all"
            }else if(val==this.top_main){
              this.sPlatformDomainMoids = []
              this.sMachineRoomMoids = []
              this.sPlatformDomainMoids = [].concat(this.p)
              this.sMachineRoomMoids = [].concat(this.m)
              this.sPlatformDomainMoids.unshift({
                  "moid": "all",
                  "parent_moid": "",
                  "name": "所有平台域",
                  "type": "platform"
              })
              this.sMachineRoomMoids.unshift({
                  "moid": "all",
                  "parent_moid": "",
                  "name": "所有虚拟机房",
                  "type": "machine_room"
              })
              this.sPlatformDomainMoid = "all"
              this.sMachineRoomMoid = "all"
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
                "moid": "all",
                "parent_moid": "",
                "name": "所有平台域",
                "type": "platform"
              })
              this.sPlatformDomainMoid="all"
              if(this.sMachineRoomMoids.length==0){
                this.sMachineRoomMoids.unshift({
                  "moid": "all",
                  "parent_moid": "",
                  "name": "无下级域",
                  "type": "machine_room"
                })
              }else{
                this.sMachineRoomMoids.unshift({
                  "moid": "all",
                  "parent_moid": "all",
                  "name": "所有虚拟机房",
                  "type": "machine_room"
                })
              }
              this.sMachineRoomMoid="all"
            }
          },
          // 终端状态
          tTerminalDomainMoid: function (val) {
            if(val=="all"){
                this.tTerminalDomainMoids = []
                this.tUserMoids = []
                this.tTerminalDomainMoids = [].concat(this.tm)
                this.tUserMoids = [].concat(this.tu)
                this.tTerminalDomainMoids.unshift({
                  "moid": "all",
                  "parent_moid": "",
                  "name": "所有服务域",
                  "type": "server"
                })
                this.tUserMoids.unshift({
                  "moid": "all",
                  "parent_moid": "",
                  "name": "所有用户域",
                  "type": "user"
                })
                this.tTerminalDomainMoid = "all"
                this.tUserMoid = "all"
              }else if(val==this.top_main){
                this.tUserMoids = []
                this.tUserMoids = [].concat(this.tu)
                this.tUserMoids.unshift({
                  "moid": "all",
                  "parent_moid": "",
                  "name": "所有用户域",
                  "type": "user"
                })
                this.tUserMoid = "all"
              }else{
                this.tUserMoids=[]
                this.tu.forEach(j=>{
                  if(val==j.parent_moid){
                    this.tUserMoids.push(j)
                  }
                })
                if(this.tUserMoids.length==0){
                  this.tUserMoids.unshift({
                    "moid": "all",
                    "parent_moid": "",
                    "name": "无下级域",
                    "type": "user"
                  })
                }else{
                  this.tUserMoids.unshift({
                    "moid": "all",
                    "parent_moid": "",
                    "name": "所有用户域",
                    "type": "user"
                  })
                }
                this.tUserMoid="all"
              }
          },
          selectType: function(val) {
            if(this.taskid !="") {
              if(val=="license") {
                this.getLicense()
                this.lince = true
                this.resou = false
                this.ser = false
                this.ter = false
              }else if(val=="resource"){
                this.getResource()
                this.lince = false
                this.resou = true
                this.ser = false
                this.ter = false
              }else if(val=="server"){
                this.getServer()
                this.lince = false
                this.resou = false
                this.ser = true
                this.ter = false
              }else if(val=="terminal"){
                this.getTerminal()
                this.lince = false
                this.resou = false
                this.ser = false
                this.ter = true
              }
            }
          },
          curPage: function (newPageNum, oldPageNum) {
            this.cage = 1
            if (this.tabType=="inspectionItem") {
              if (this.selectType == "server") {
                api.getInspectServer(this.taskid,{params:{page:newPageNum}}).then((res) => {
                  console.log("server信息： "+JSON.stringify(res))
                  if(res.success==1){
                    this.serverList = res.data.server_list
                    this.serverFields = getServerFields(this.serDetail)
                    this.serverTotalPage = Math.ceil(res.data.max_page)
                  }
                }).catch(error => {
                  console.log(error)
                });
              } else if (this.selectType == "terminal") {
                api.getInspectTerminal(this.taskid,{params:{page:newPageNum}}).then((res) => {
                  console.log("terminal信息： "+JSON.stringify(res))
                  if(res.success==1){
                    this.terminalList = res.data.terminal_list
                    this.terminalListFields = getTerminalFields(this.terDetail)
                    this.terminalListTotalPage = Math.ceil(res.data.max_page)
                  }
                }).catch(error => {
                  console.log(error)
                });
              } else if (this.selectType == "license") {
                api.getInspectLicense(this.taskid,{params:{page:newPageNum}}).then((res) => {
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
            } else if (this.tabType=="regularInspection") {
              api.getInspectTasks({params:{page:newPageNum}}).then((res) => {
                if(res.success==1){
                  this.inspectTaskList = res.data.inspect_tasks
                  this.inspectTaskListFields = getInspectTaskListFields(this.OnDelTask,this.OnEditTask,this.OnViewTask)
                  this.inspectTaskListTotalPage = Math.ceil(res.data.max_page)
                }
              }).catch(error => {
                console.log(error)
              });
            }
          }
        },
        methods: {
          // 页面刷新保存tab状态
          updateType() {
            let type = this.$route.query.type;
            if(type === '1') {
                this.tabType = 'inspectionItem';
            }else if(type === '2') {
                this.tabType = 'regularInspection';
            }
          },
          handleClick(tab) {
              let queryType;
              if(tab.name == 'inspectionItem') {
                  queryType = 1;
              }else if(tab.name == 'regularInspection') {
                  queryType = 2;
              }
            this.$router.push({
                path: '/inspection/home',
                query: {
                    type: queryType || 1
                }
            });
          },
          getStartWeek: function () {
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
          // 开始巡检
          StartRealTimeInspect: function () {
            if (this.checked_l == "" && this.checked_so == "" && this.checked_st == "" && this.checked_t == "") {
              this.errorDialog.open("请至少勾选一项巡检条件")
            } else {
              this.selectTypes = []
              if(this.checked_l){
                let dic = {}
                dic["text"] = "License文件"
                dic["value"] = this.checked_l
                this.selectTypes.push(dic)
              }
              if(this.checked_so){
                let dic = {}
                dic["text"] = "会议资源"
                dic["value"] = this.checked_so
                this.selectTypes.push(dic)
              }
              if(this.checked_st){
                let dic = {}
                dic["text"] = "服务器状态"
                dic["value"] = this.checked_st
                this.selectTypes.push(dic)
              }
              if(this.checked_t){
                let dic = {}
                dic["text"] = "终端状态"
                dic["value"] = this.checked_t
                this.selectTypes.push(dic)
              }
              this.selectType = this.selectTypes[0]["value"]

              this.grab_start = FormatTime(new Date());
              this.inspect_data["inspect_range"] = {}
              this.inspect_data["inspect_recycle"] = {}
              if(this.checked_l){
                this.inspect_data["inspect_range"][this.checked_l] = {}
                this.inspect_data["inspect_range"][this.checked_l]["service_domain_moid"] = this.lServiceDomainMoid
              }
              if(this.checked_so){
                this.inspect_data["inspect_range"][this.checked_so] = {}
                this.inspect_data["inspect_range"][this.checked_so]["service_domain_moid"] = this.mServiceDomainMoid
                this.inspect_data["inspect_range"][this.checked_so]["platform_domain_moid"] = this.mPlatformDomainMoid
                this.inspect_data["inspect_range"][this.checked_so]["virtual_machine_room_moid"] = this.mMachineRoomMoid
              }
              if(this.checked_st){
                this.inspect_data["inspect_range"][this.checked_st] = {}
                this.inspect_data["inspect_range"][this.checked_st]["service_domain_moid"] = this.sServiceDomainMoid
                this.inspect_data["inspect_range"][this.checked_st]["platform_domain_moid"] = this.sPlatformDomainMoid
                this.inspect_data["inspect_range"][this.checked_st]["virtual_machine_room_moid"] = this.sMachineRoomMoid
              }
              if(this.checked_t){
                this.inspect_data["inspect_range"][this.checked_t] = {}
                this.inspect_data["inspect_range"][this.checked_t]["service_domain_moid"] = this.tTerminalDomainMoid
                this.inspect_data["inspect_range"][this.checked_t]["user_domain_moid"] = this.tUserMoid
              }
              if (this.tabType=="inspectionItem") {
                this.inspect_data["task_flag"] = 0
              }else if (this.tabType=="regularInspection") {
                this.inspect_data["task_flag"] = 1
                this.inspect_data["inspect_recycle"]["end_time"] = this.end_time
                this.inspect_data["inspect_recycle"]["monday"] = this.monday
                this.inspect_data["inspect_recycle"]["tuesday"] = this.tuesday
                this.inspect_data["inspect_recycle"]["wednesday"] = this.wednesday
                this.inspect_data["inspect_recycle"]["thursday"] = this.thursday
                this.inspect_data["inspect_recycle"]["friday"] = this.friday
                this.inspect_data["inspect_recycle"]["saturday"] = this.saturday
                this.inspect_data["inspect_recycle"]["sunday"] = this.sunday
              }
              this.inspect_data["start_time"] = this.value+" "+this.hour+":"+this.minute+":"+this.second
              console.log("this.inspect_data="+JSON.stringify(this.inspect_data))

              api.addInspectTask(this.inspect_data).then((res) => {
                console.log("巡检反馈： "+JSON.stringify(res))
                if(res.success==1){
                  this.taskid=res.taskid
                  if(this.tabType=="inspectionItem"){
                    console.log("即时巡检")
                    this.inspect_info = true
                    this.selectType = this.selectTypes[0]["value"]
                    if(this.selectType=="license") {
                      this.getLicense()
                      this.lince = true
                    }else if(this.selectType=="resource") {
                      this.getResource()
                      this.resou = true
                    }else if(this.selectType=="server") {
                      this.getServer()
                      this.ser = true
                    }else if(this.selectType=="terminal") {
                      this.getTerminal()
                      this.ter = true
                    }
                  }else if(this.tabType=="regularInspection") {
                    console.log("定时巡检")
                    this.getTimerInspectInfo()
                  }
                }
              }).catch(error => {
                console.log(error)
              });
            }
          },
          // License文件
          getLicense() {
            api.getInspectLicense(this.taskid).then((res) => {
              console.log("license信息： "+JSON.stringify(res))
              if(res.success==1){
                this.licenseList = res.data.license_list
                this.licenseFields = getLicenseFields()
                this.licenseTotalPage = Math.ceil(res.data.max_page)
              }
            }).catch(error => {
              console.log(error)
            });
          },
          // 会议资源
          getResource() {
            api.getInspectResource(this.taskid).then((res) => {
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
            api.getInspectServer(this.taskid).then((res) => {
              console.log("server信息： "+JSON.stringify(res))
              if(res.success==1){
                this.serverList = res.data.server_list
                this.serverFields = getServerFields(this.serDetail)
                this.serverTotalPage = Math.ceil(res.data.max_page)
              }
            }).catch(error => {
              console.log(error)
            });
          },
          serDetail: function(data) {
            this.$router.push({name: 'physicsdetail', params: {device_moid: data.device_moid,taskid: data.taskid, inspect_time: this.grab_start}})
          },
          // 终端状态
          getTerminal() {
            api.getInspectTerminal(this.taskid).then((res) => {
              console.log("terminal信息： "+JSON.stringify(res))
              if(res.success==1){
                this.terminalList = res.data.terminal_list
                this.terminalListFields = getTerminalFields(this.terDetail)
                this.terminalListTotalPage = Math.ceil(res.data.max_page)
              }
            }).catch(error => {
              console.log(error)
            });
          },
          terDetail: function(data) {
            this.$router.push({name: 'terminaldetail', params: {device_moid: data.device_moid,taskid: data.taskid}})
          },
          // 导出
          onExport: function (){
            api.downloadInspect({params:{taskid:this.taskid},responseType: 'blob'})
            .then((res) => {
              Upexcele(res, '巡检信息.xls')
            }).catch(error => {
              console.log(error)
            });
          },
          //**********************定时巡检方法************************//
          getTimerInspectInfo: function() {
            api.getInspectTasks().then((res) => {
              console.log("定时巡检初始信息反馈： "+JSON.stringify(res))
              if(res.success==1){
                this.inspectTaskList = res.data.inspect_tasks
                this.inspectTaskListFields = getInspectTaskListFields(this.OnDelTask,this.OnEditTask,this.OnViewTask)
                this.inspectTaskListTotalPage = Math.ceil(res.data.max_page)
                this.checked_l = "license"
                this.checked_so = "resource"
                this.checked_st = "server"
                this.checked_t = "terminal"
                this.lServiceDomainMoid = "all"
                this.mServiceDomainMoid = "all"
                this.mPlatformDomainMoid = "all"
                this.mMachineRoomMoid = "all"
                this.sServiceDomainMoid = "all"
                this.sPlatformDomainMoid = "all"
                this.sMachineRoomMoid = "all"
                this.tTerminalDomainMoid = "all"
                this.tUserMoid = "all"
                this.critical = false
                this.startDate = new Date()
                this.endDate = new Date()
                this.hour = "00"
                this.minute = "00"
                this.second = "00"
                this.moncheck = ""
                this.tuecheck = ""
                this.wedcheck = ""
                this.thucheck = ""
                this.fricheck = ""
                this.satcheck = ""
                this.suncheck = ""
                this.getStartWeek()
              }
            }).catch(error => {
              console.log(error)
            });
          },
          // 日期编辑
          editCheck: function() {
            this.$refs.repetitionDlg.open();
          },
          //添加
          OnAddTimingTask: function () {
            this.sign = "add"
            this.editShow=false
            this.postShow=true
            this.$refs.addInspectDlg.open()
          },
          onSign: function () {
            if (this.sign === "edit" && this.critical) {
              this.verEdit()
            } else if (this.sign === "add" && this.critical) {
              this.addInspect()
            } else {
              this.errorDialog.open('请点击"重复"按钮添加结束时间')
            }
          },
          // 发定时巡检消息
          addInspect: function () {
            this.end_time=this.value1+" "+this.hour+":"+this.minute+":"+this.second
            console.log("end_time"+this.end_time)
            if(this.moncheck){
              this.monday = 1
            }
            if(this.tuecheck){
              this.tuesday = 1
            }
            if(this.wedcheck){
              this.wednesday = 1
            }
            if(this.thucheck){
              this.thursday = 1
            }
            if(this.fricheck){
              this.friday = 1
            }
            if(this.satcheck){
              this.saturday = 1
            }
            if(this.suncheck){
              this.sunday = 1
            }
            this.StartRealTimeInspect()
          },
          //编辑
          OnEditTask: function (rowData) {
            console.log("编辑的数据="+JSON.stringify(rowData))
            this.edit_task_id=rowData.id
            this.sign="edit"
            this.editShow=true
            this.postShow=false
            this.$refs.addInspectDlg.open()
            // 参数整理
            if (rowData.recycle.monday == 1) {
              this.moncheck = "周一，"
            }
            if (rowData.recycle.tuesday == 1) {
              this.tuecheck = "周二，"
            }
            if (rowData.recycle.wednesday == 1) {
              this.wedcheck = "周三，"
            }
            if (rowData.recycle.thursday == 1) {
              this.thucheck = "周四，"
            }
            if (rowData.recycle.friday == 1) {
              this.fricheck = "周五，"
            }
            if (rowData.recycle.saturday == 1) {
              this.satcheck = "周六，"
            }
            if (rowData.recycle.sunday == 1) {
              this.suncheck = "周日"
            }
            this.critical=true
            this.value1 = rowData.recycle.end_time
            if (this.value1 != "") {
              this.endDate = UnFormatTime(this.value1)
            }
            this.startDate=new Date(Date.parse(rowData.start_time.replace(/-/g,   "/")))
            this.hour=rowData.start_time.split(" ")[1].split(":")[0]
            this.minute=rowData.start_time.split(" ")[1].split(":")[1]
            this.second=rowData.start_time.split(" ")[1].split(":")[2]
            if(rowData.license==1){
              this.checked_l="license"
              console.log("this.top_main="+this.top_main)
              if(rowData.inspect_range.license.service_domain_moid==this.top_main){
                this.lServiceDomainMoid="all"
              }else {
                this.lServiceDomainMoid=rowData.inspect_range.license.service_domain_moid
              }
            }else {
              this.checked_l=""
            }

            if(rowData.resource==1){
              this.checked_so="resource"
              if(rowData.inspect_range.resource.service_domain_moid==this.top_main){
                this.mServiceDomainMoid="all"
              }else {
                this.mServiceDomainMoid=rowData.inspect_range.resource.service_domain_moid
              }
              this.mPlatformDomainMoid=rowData.inspect_range.resource.platform_domain_moid
              this.mMachineRoomMoid=rowData.inspect_range.resource.virtual_machine_room_moid
            }else {
              this.checked_so=""
            }

            if(rowData.server==1){
              this.checked_st="server"
              if(rowData.inspect_range.server.service_domain_moid==this.top_main){
                this.sServiceDomainMoid="all"
              }else {
                this.sServiceDomainMoid=rowData.inspect_range.server.service_domain_moid
              }
              this.sPlatformDomainMoid=rowData.inspect_range.server.platform_domain_moid
              this.sMachineRoomMoid=rowData.inspect_range.server.virtual_machine_room_moid
            }else {
              this.checked_st=""
            }

            if(rowData.terminal==1){
              this.checked_t="terminal"
              if(rowData.inspect_range.terminal.service_domain_moid==this.top_main){
                this.tTerminalDomainMoid="all"
              }else {
                this.tTerminalDomainMoid=rowData.inspect_range.terminal.service_domain_moid
              }
              this.tUserMoid=rowData.inspect_range.terminal.user_domain_moid
            }else {
              this.checked_t=""
            }
            console.log("this.startDate="+this.startDate)
            console.log("this.hour="+this.hour)
            console.log("this.minute="+this.minute)
            console.log("this.second="+this.second)
            console.log("this.mServiceDomainMoid="+this.mServiceDomainMoid)
            console.log("this.mPlatformDomainMoid="+this.mPlatformDomainMoid)
            console.log("this.mMachineRoomMoid="+this.mMachineRoomMoid)
          },
          verEdit: function () {
            this.inspect_data["inspect_range"] = {}
            this.inspect_data["inspect_recycle"] = {}
            if(this.checked_l){
              this.inspect_data["inspect_range"][this.checked_l] = {}
              this.inspect_data["inspect_range"][this.checked_l]["service_domain_moid"] = this.lServiceDomainMoid
            }
            if(this.checked_so){
              this.inspect_data["inspect_range"][this.checked_so] = {}
              this.inspect_data["inspect_range"][this.checked_so]["service_domain_moid"] = this.mServiceDomainMoid
              this.inspect_data["inspect_range"][this.checked_so]["platform_domain_moid"] = this.mPlatformDomainMoid
              this.inspect_data["inspect_range"][this.checked_so]["virtual_machine_room_moid"] = this.mMachineRoomMoid
            }
            if(this.checked_st){
              this.inspect_data["inspect_range"][this.checked_st] = {}
              this.inspect_data["inspect_range"][this.checked_st]["service_domain_moid"] = this.sServiceDomainMoid
              this.inspect_data["inspect_range"][this.checked_st]["platform_domain_moid"] = this.sPlatformDomainMoid
              this.inspect_data["inspect_range"][this.checked_st]["virtual_machine_room_moid"] = this.sMachineRoomMoid
            }
            if(this.checked_t){
              this.inspect_data["inspect_range"][this.checked_t] = {}
              this.inspect_data["inspect_range"][this.checked_t]["service_domain_moid"] = this.tTerminalDomainMoid
              this.inspect_data["inspect_range"][this.checked_t]["user_domain_moid"] = this.tUserMoid
            }
            if(this.moncheck){
              this.monday = 1
            }
            if(this.tuecheck){
              this.tuesday = 1
            }
            if(this.wedcheck){
              this.wednesday = 1
            }
            if(this.thucheck){
              this.thursday = 1
            }
            if(this.fricheck){
              this.friday = 1
            }
            if(this.satcheck){
              this.saturday = 1
            }
            if(this.suncheck){
              this.sunday = 1
            }
            this.inspect_data["inspect_recycle"]["end_time"] = this.value1
            this.inspect_data["inspect_recycle"]["monday"] = this.monday
            this.inspect_data["inspect_recycle"]["tuesday"] = this.tuesday
            this.inspect_data["inspect_recycle"]["wednesday"] = this.wednesday
            this.inspect_data["inspect_recycle"]["thursday"] = this.thursday
            this.inspect_data["inspect_recycle"]["friday"] = this.friday
            this.inspect_data["inspect_recycle"]["saturday"] = this.saturday
            this.inspect_data["inspect_recycle"]["sunday"] = this.sunday
            this.inspect_data["start_time"] = this.value+" "+this.hour+":"+this.minute+":"+this.second
            console.log("this.inspect_data="+JSON.stringify(this.inspect_data))
            api.updateInspectTask(this.edit_task_id, this.inspect_data).then((res) => {
              console.log("编辑结果反馈="+JSON.stringify(res))
              if(res.success==1){
                api.getInspectTasks().then((res) => {
                  if(res.success==1){
                    this.inspectTaskList = res.data.inspect_tasks
                    this.inspectTaskListFields = getInspectTaskListFields(this.OnDelTask,this.OnEditTask,this.OnViewTask)
                    this.inspectTaskListTotalPage = Math.ceil(res.data.max_page)
                    this.cage = 2
                  }
                }).catch(error => {
                  console.log(error)
                });
              }
            }).catch(error => {
              console.log(error)
            });
          },
          //删除
          OnDelTask: function (rowData) {
            this.taskid = rowData.id
            api.delInspectTask(this.taskid).then((res) => {
              if(res.success==1){
                api.getInspectTasks().then((res) => {
                  if(res.success==1){
                    if (res.data.inspect_tasks.length == 0) {
                      this.reload()
                    } else {
                      this.inspectTaskList = res.data.inspect_tasks
                      this.inspectTaskListFields = getInspectTaskListFields(this.OnDelTask,this.OnEditTask,this.OnViewTask)
                      this.inspectTaskListTotalPage = Math.ceil(res.data.max_page)
                      this.cage = 2
                    }
                  }
                }).catch(error => {
                  console.log(error)
                });
              }
            }).catch(error => {
              console.log(error)
            });
            // this.$refs.OnDelTaskDialog.open();
          },
          OnDelTaskDialogNotify: function () {
            this.isShow=false
            this.areShow=true
          },
          //详情
          OnViewTask: function (rowData) {
            console.log("详情的数据="+JSON.stringify(rowData))
            this.taskid = rowData.id
            console.log("ID="+this.taskid)
            this.$router.push({
              name: 'inspectionresult',
              params: rowData
            })
          },
          // 弹框取消按钮
          cancelSign: function () {
            // this.reload()
          },
          closeSign: function() {
            this.critical = false
            this.moncheck = ""
            this.tuecheck = ""
            this.wedcheck = ""
            this.thucheck = ""
            this.fricheck = ""
            this.satcheck = ""
            this.suncheck = ""

            this.hour = "00"
            this.minute = "00"
            this.second = "00"
            this.startDate = new Date()
            this.endDate = new Date()
          },
          // 重复
          recyclecheck: function() {
            console.log("this.critical="+this.critical)
            if(this.critical==true) {
              this.value1=FormatDateTime(this.endDate)
              console.log("this.value1="+this.value1)
              this.$refs.repetitionDlg.open();
            }
          },
          confirmDlg: function() {
            if (FormatTime(this.startDate) >= FormatTime(this.endDate)) {
              this.errorDialog.open("开始时间不能大于结束时间，请重新选择结束时间！")
            }
          },
        }
    }
</script>

<style scoped>
#inspectcontent {
  width: 1479px;
  height: 260px;
  border-bottom: 1px dotted #c0c0c0;
}
#inspectcontent-timer {
  height: 260px;
  border-bottom: 1px dotted #c0c0c0;
}
table {
  width: 468px;
}
td {
    padding-right: 19px;
}
tr {
  text-align: left;
  vertical-align: 10%;
}
.timingTaskEmptyTip {
    margin: 198px auto 0 auto;
    text-align: center;
    /* font-size: 14px; */
    color: #2c3e50;
}
.btnAddTask {
  float: right;
}
tbody td {
    padding-right: 0px;
}
tbody tr {
  vertical-align: text-top;
}
.inspect-task-container {
    margin-top: 29px;
    font-size: 12px;
}
.itemName {
    float: left;
    width: 79px;
}
.startTime {
    margin-right: 24px;
}
.itemValue {
    color: #4e4e4e;
    display: inline-block;
    /* padding-top: 5px; */
}
.repeatItem {
    min-width: 400px;
}
/* table {
    border-collapse: collapse;
    border-spacing: 0;
} */
.operations {
    position: absolute;
    right: 0;
    bottom: 10px;
}
.delTipsDiv {
    text-align: center;
    padding-top: 50px;
}
.grab-msg{
  font: 14px "Microsoft Yahei", arial;
  margin-top: 10px;
  margin-bottom: 10px;
  float: left;
  height: 24px;
  width: 100%;
}
.time_msg{
  float: none;
  text-align: left;
  width: 25%;
  margin-right: 10px;
}
/deep/ .res-info-list {
  width: 1506px;
}
.inspect-time-container {
  overflow: hidden;
}
.inspect-item-container {
  margin-top: 43px;
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
.inspect-time-show-container {
    float: left;
    line-height: 30px;
    padding-left: 24px;
    padding-left: 87px;
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
.inspect-time-show-container p {
  text-align: left;
  width: 357px;
}
.inspect-time-show-container>li:first-child {
    margin-right: 11px;
}
.main-dia {
  padding-left: 40px;
  padding-top: 40px;
}
.select-time {
  float: left;
  padding-left: 16px
}
/deep/ .el-select.select-time div.el-input {
  width: 50px;
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
.repeat_line {
  padding-top: 27px;
}
#summaryContent {
    padding-left: 5px;
}
.no-info-tip {
  float: left;
}
.warningNotifyAdd{
  color: #007ac0;
  text-decoration: underline
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
/* .circle-info-detail {
  float: left;
} */
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
