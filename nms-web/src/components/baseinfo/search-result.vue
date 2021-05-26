<template>
  <div class="detail-style">
    <div class="detail-back">
      <span class="back-btn" @click="$router.go(-1)"></span>
      <span class="base-info-title">更多</span>
    </div>
    <div class="detail-line" slot="content">
      <el-tabs class="detail-tab" v-model="detailType" style="cursor:pointer">
        <el-tab-pane label="会议资源" name="meetingResource" style="cursor:default">
          <div v-if="this.detailType == 'meetingResource'" class="detail-div-pie">
            <div class="detail-chart">
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
          </div>
        </el-tab-pane>
        <el-tab-pane label="预约会议" name="meetingAppoint" style="cursor:default">
          <div v-show="this.detailType == 'meetingAppoint'" class="detail-div">
            <div class="detail-item">
              <el-select class="detail-select" v-model="tTerminalDomainMoid" placeholder="默认服务域" @change="serverClick">
                <el-option
                  v-for="(item,index) in tTerminalDomainMoids"
                  :key="index"
                  :label="item.name"
                  :value="item.moid">
                </el-option>
              </el-select>
              <el-select class="detail-select" v-model="tUserMoid" placeholder="全部用户域" @change="userClick">
                <el-option
                  v-for="(item,index) in tUserMoids"
                  :key="index"
                  :label="item.name"
                  :value="item.moid">
                </el-option>
              </el-select>
              <el-select class="timeSelect" v-model="timePeriodValue" value="" placeholder="最近一周" style="float:left; padding-top:6px; margin-right:10px">
                <el-option
                  v-for="(item,index) in timePeriods"
                  :key="index"
                  :label="item.label"
                  :value="item.value">
                </el-option>
              </el-select>
              <DateBox v-if="reSet" inputId="d1" v-model="startDate" style="width: 150px; float:left; margin-top: 5px" format="yyyy-MM-dd" :disabled="timePeriodValue !== 'selfdefine'"></DateBox>
              <div style="display: inline-block; width: 19px; float:left; margin-top: 5px">→</div>
              <DateBox v-if="reSet" inputId="d2" v-model="endDate" style="width: 150px; float:left; margin-top: 5px" format="yyyy-MM-dd" :disabled="timePeriodValue !== 'selfdefine'"></DateBox>
              <button class='search' style="float:left" @click="searchDomain()"></button>
              <button class="normal-btn" style="float:right" @click="onExport()">导出</button>
            </div>
            <div  class="detail-chart">
              <span class="res-chart-show" id="AppointMeeting">图表加载中...</span>
              <div class="res-chart-hide" id="AppointMeetingChart"/>
            </div>
          </div>
        </el-tab-pane>
        <el-tab-pane label="告警统计" name="warningCount" style="cursor:default">
          <div v-show="this.detailType == 'warningCount'" class="detail-div">
            <div class="detail-item">
              <el-select class="timeSelect" v-model="timePeriodValue" value="" placeholder="最近一周" style="float:left; padding-top:6px; margin-right:10px">
                <el-option
                  v-for="(item,index) in timePeriods"
                  :key="index"
                  :label="item.label"
                  :value="item.value">
                </el-option>
              </el-select>
              <DateBox v-if="reSet" inputId="d3" v-model="startDate" style="width: 150px; float:left; margin-top: 5px" format="yyyy-MM-dd" :disabled="timePeriodValue !== 'selfdefine'"></DateBox>
              <div style="display: inline-block; width: 19px; float:left; margin-top: 5px">→</div>
              <DateBox v-if="reSet" inputId="d4" v-model="endDate" style="width: 150px; float:left; margin-top: 5px" format="yyyy-MM-dd" :disabled="timePeriodValue !== 'selfdefine'"></DateBox>
              <button class='search' style="float:left" @click="searchDomain()"></button>
              <button class="normal-btn" style="float:right" @click="onExport()">导出</button>
            </div>
            <div  class="detail-chart">
              <span class="res-chart-show" id="CountWarning">图表加载中...</span>
              <div class="res-chart-hide" id="CountWarningChart"/>
            </div>
          </div>
        </el-tab-pane>
        <el-tab-pane label="会议数量" name="meetingNum" style="cursor:default">
          <div v-show="this.detailType == 'meetingNum'" class="detail-div">
            <div class="detail-item">
              <el-select class="detail-select" v-model="tTerminalDomainMoid" placeholder="默认服务域" @change="serverClick">
                <el-option
                  v-for="(item,index) in tTerminalDomainMoids"
                  :key="index"
                  :label="item.name"
                  :value="item.moid">
                </el-option>
              </el-select>
              <el-select class="detail-select" v-model="tUserMoid" placeholder="全部用户域" @change="userClick">
                <el-option
                  v-for="(item,index) in tUserMoids"
                  :key="index"
                  :label="item.name"
                  :value="item.moid">
                </el-option>
              </el-select>
              <el-select class="timeSelect" v-model="timePeriodValue" value="" placeholder="最近一周" style="float:left; padding-top:6px; margin-right:10px">
                <el-option
                  v-for="(item,index) in timePeriods"
                  :key="index"
                  :label="item.label"
                  :value="item.value">
                </el-option>
              </el-select>
              <DateBox v-if="reSet" inputId="d5" v-model="startDate" style="width: 150px; float:left; margin-top: 5px" format="yyyy-MM-dd" :disabled="timePeriodValue !== 'selfdefine'"></DateBox>
              <div style="display: inline-block; width: 19px; float:left; margin-top: 5px">→</div>
              <DateBox v-if="reSet" inputId="d6" v-model="endDate" style="width: 150px; float:left; margin-top: 5px" format="yyyy-MM-dd" :disabled="timePeriodValue !== 'selfdefine'"></DateBox>
              <button class='search' style="float:left" @click="searchDomain()"></button>
              <button class="normal-btn" style="float:right" @click="onExport()">导出</button>
            </div>
            <div class="detail-chart">
              <span class="res-chart-show" id="MeetingNum">图表加载中...</span>
              <div class="res-chart-hide" id="MeetingNumChart"/>
            </div>
          </div>
        </el-tab-pane>
        <el-tab-pane label="服务器数量" name="domainUse" style="cursor:default">
          <div v-show="this.detailType == 'domainUse'" class="detail-div">
            <div class="detail-item">
              <el-select class="detail-select" v-model="seviceDomain" value="" placeholder="所有服务域">
                <el-option
                  v-for="(item,index) in seviceDomains"
                  :key="index"
                  :label="item.name"
                  :value="item.moid">
                </el-option>
              </el-select>
              <el-select class="detail-select" v-model="platformDomain" value="" placeholder="所有平台域">
                <el-option
                  v-for="(item,index) in platformDomains"
                  :key="index"
                  :label="item.name"
                  :value="item.moid">
                </el-option>
              </el-select>
              <el-select class="detail-select" v-model="machineRoom" value="" placeholder="所有虚拟机房">
                <el-option
                  v-for="(item,index) in machineRooms"
                  :key="index"
                  :label="item.name"
                  :value="item.moid">
                </el-option>
              </el-select>
              <el-select class="timeSelect" v-model="timePeriodValue" value="" placeholder="最近一周" style="float:left; padding-top:6px; margin-right:10px">
                <el-option
                  v-for="(item,index) in timePeriods"
                  :key="index"
                  :label="item.label"
                  :value="item.value">
                </el-option>
              </el-select>
              <DateBox v-if="reSet" inputId="d7" v-model="startDate" style="width: 150px; float:left; margin-top: 5px" format="yyyy-MM-dd" :disabled="timePeriodValue !== 'selfdefine'"></DateBox>
              <div style="display: inline-block; width: 19px; float:left; margin-top: 5px">→</div>
              <DateBox v-if="reSet" inputId="d8" v-model="endDate" style="width: 150px; float:left; margin-top: 5px" format="yyyy-MM-dd" :disabled="timePeriodValue !== 'selfdefine'"></DateBox>
              <button class='search' style="float:left" @click="searchDomain()"></button>
              <button class="normal-btn" style="float:right" @click="onExport()">导出</button>
            </div>
            <div class="detail-chart">
              <span class="res-chart-show" id="ServiceNum">图表加载中...</span>
              <div class="res-chart-hide" id="ServiceNumChart"/>
            </div>
          </div>
        </el-tab-pane>
        <el-tab-pane label="终端数量" name="terminalUse" style="cursor:default">
          <div v-show="this.detailType == 'terminalUse'" class="detail-div">
            <div class="detail-item">
              <el-select class="detail-select" v-model="tTerminalDomainMoid" placeholder="默认服务域" @change="serverClick">
                <el-option
                  v-for="(item,index) in tTerminalDomainMoids"
                  :key="index"
                  :label="item.name"
                  :value="item.moid">
                </el-option>
              </el-select>
              <el-select class="detail-select" v-model="tUserMoid" placeholder="全部用户域" @change="userClick">
                <el-option
                  v-for="(item,index) in tUserMoids"
                  :key="index"
                  :label="item.name"
                  :value="item.moid">
                </el-option>
              </el-select>
              <el-select class="timeSelect" v-model="timePeriodValue" value="" placeholder="最近一周" style="float:left; padding-top:6px; margin-right:10px">
                <el-option
                  v-for="(item,index) in timePeriods"
                  :key="index"
                  :label="item.label"
                  :value="item.value">
                </el-option>
              </el-select>
              <DateBox v-if="reSet" inputId="d9" v-model="startDate" style="width: 150px; float:left; margin-top: 5px" format="yyyy-MM-dd" :disabled="timePeriodValue !== 'selfdefine'"></DateBox>
              <div style="display: inline-block; width: 19px; float:left; margin-top: 5px">→</div>
              <DateBox v-if="reSet" inputId="d0" v-model="endDate" style="width: 150px; float:left; margin-top: 5px" format="yyyy-MM-dd" :disabled="timePeriodValue !== 'selfdefine'"></DateBox>
              <button class='search' style="float:left" @click="searchDomain()"></button>
              <button class="normal-btn" style="float:right" @click="onExport()">导出</button>
            </div>
            <div class="detail-chart">
              <span class="res-chart-show" id="TerminalNum">图表加载中...</span>
              <div class="res-chart-hide" id="TerminalNumChart"/>
            </div>
          </div>
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>

<script>
  import ResUsageCircle from "../common/res-usage-circle";
  import ResUsageDetail from "../common/res-usage-detail";
  import api from '../../axios'
  import {setMyOption, } from 'assets/js/baseinfo'
  import NmsPagerTable from "../common/nms-pager-table";
  import {getTimePeriod, FormatTime, get_time, FormatChartTime, FormatDate, KeepTwoNum} from "../../assets/js/common";

  export default {
    name: "search-result",
    components: {
      NmsPagerTable,
      ResUsageDetail,
      ResUsageCircle,
    },
    data() {
      return {
        myChart: '',
        picInfo: '',
        reSet: true,
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
        CRPUsable: 0,

        timePeriods: getTimePeriod(),
        startDate: new Date(),
        endDate: new Date(),
        detailType: '',
        tTerminalDomainMoids: [],
        tTerminalDomainMoid: '',
        tUserMoids: [],
        tUserMoid: '',
        timePeriod: [],
        timePeriodValue: 'lastweek',
        searchMoid: '',
        timeRange: [],
        DomainTree: [],
        seviceDomains: [],
        seviceDomain: '',
        platformDomains: [],
        platformDomain: '',
        machineRooms: [],
        machineRoom: '',
        fromTime: '',
        untilTime: '',
        myOption: {
          backgroundColor: 'rgb(256,256,256)',
          yAxis: {
            name: '%',
            min: 0,
            max: 100,
            interval: 20,
            type: 'value',
            axisTick: {
              show: false
            },
            splitLine: {
              show: true,
              lineStyle: {
                type: 'dotted'
              }
            },
            axisLine: {
              symbolSize: [8, 12],
              lineStyle: {
              }
            },
          },
          grid: {
            top: 30,
            bottom: 20,
            containLabel: true
          },
          tooltip: {
            trigger: 'axis',
            textStyle: {
              align: 'left',
            }
          },
          xAxis: {
            type: 'time',
            boundaryGap: false,
            axisLabel: {
              rotate: 90,
              textStyle: {
                color: 'black',
                fontSize: 12,
                fontStyle: 'normal',
                fontWeight: 500
              },
            }
          },
          series: [],
          legend: {
            orient: 'horizontal',
            right: 100,
            top: 1,
            itemGap: 15,
            itemWidth: 20,
            itemHeight: 3,
            data: [],
          },
        },
        legendColor: ['#56b8e6', '#cf3e4f', '#e4c727', '#245bd7', '#63be20'],
        validData: [],
      }
    },
    activated: function () {
      if (this.$route.params.detailType) {
        this.detailType = this.$route.params.detailType
      } else {
        this.detailType = 'meetingResource'
      }
      if (this.detailType == 'meetingAppoint') {
        this.timePeriodValue = 'selfdefine'
        var time = parseInt(new Date().getTime());
        this.startDate = new Date()
        this.endDate = new Date(time + 60 * 60 * 1000 * 24 * 7);
      } else {
        this.startDate = get_time(this.timePeriodValue)
        this.endDate = new Date()
      }
      this.timePeriodValue = 'lastweek'
      this.reSet = false
      this.$nextTick(() => {
        this.reSet = true
      })
      this.searchMoid = ''
      if (this.detailType == 'meetingResource') {
        // 会议资源获取
        this.APsStarted = 0
        this.APsUsable = 0
        this.APStarted = 0
        this.APUsable = 0
        this.GAPStarted = 0
        this.GAPUsable = 0

        this.MPsStarted = 0
        this.MPsUsable = 0
        this.MPStarted = 0
        this.MPUsable = 0
        this.HMPStarted = 0
        this.HMPUsable = 0
        this.GMPStarted = 0
        this.GMPUsable = 0
        this.GHMPStarted = 0
        this.GHMPUsable = 0

        this.STerStarted = 0
        this.STerTotal = 0
        this.STerOnline = 0

        this.LMStarted = 0
        this.LMUsable = 0
        this.HLSStarted = 0
        this.HLSUsable = 0
        this.ASFStarted = 0
        this.ASFUsable = 0

        this.VRStarted = 0
        this.VRUsable = 0

        this.ViewersPercent = 0
        this.ViewersStarted = 0
        this.ViewersUsable = 0

        this.CRStarted = 0
        this.CRPUsable = 0

        api.getMeetingResourceData({params: {parentMoid: 'all'}}).then(res => {
          console.log(res)
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
        })
      } else if (this.detailType == 'meetingAppoint') {
        // 获取预约会议图表
        document.getElementById("AppointMeeting").style.display = "block";
        document.getElementById("AppointMeetingChart").style.display = "none";
        var appointStartTime = FormatTime(new Date())
        var appointStopTime = FormatTime(time + 60 * 60 * 1000 * 24 * 7)
        console.log(appointStopTime)
        console.log(appointStartTime)
        api.getAppointMeetingData({params: {parentMoid: 'all', startTime: appointStartTime, stopTime: appointStopTime}}).then(res => {
          console.log(res)
          this.myOption.yAxis.name = '个'
          this.myOption.yAxis.max = 10
          this.myOption.yAxis.interval = 5
          this.myOption.series = []
          this.myOption.legend.data = []
          this.validData = []
          if (res.success == 1) {
            if (res.datapoints.length > 0) {
              var maxValue = 0
              for (var j = res.datapoints.length - 1; j >= 0; j--) {
                if (res.datapoints[j][0] === null) {
                  continue
                }
                if (res.datapoints[j][0] > maxValue) {
                  maxValue = res.datapoints[j][0]
                }
                this.validData.push(res.datapoints[j])
              }
              this.validData.reverse()
              var day1 = (this.validData[this.validData.length - 1][1] - this.validData[0][1]) / 3600
              let maxLength = String(maxValue).length
              this.myOption.yAxis.max = Math.pow(10, maxLength)
              this.myOption.yAxis.interval = parseInt(parseFloat(Math.pow(10, maxLength) / 2).toFixed(0))
              this.myOption.series.push({
                type: 'line',
                name: '预约会议数量',
                symbol: 'none',
                data: this.validData.map(function(value) {
                  return {value: [value[1] * 1000, value[0]]};
                }),
                itemStyle: {
                  color: '#5eb9ef'
                },
                areaStyle: {
                  color: '#CCFFFF',
                  origin: 'start',
                },
              })
              if (day1 <= 24) {
                this.myOption.xAxis.axisLabel.formatter = function (value, index) {
                  var date = new Date(value);
                  return date.toTimeString().substr(0, 5);
                }
              } else {
                this.myOption.xAxis.axisLabel.formatter = function (value, index) {
                  return FormatDate(value)
                }
              }
            }
          }
          this.$nextTick(() => {
            this.myChart = this.$echarts.init(document.getElementById('AppointMeetingChart'));
            document.getElementById("AppointMeeting").style.display = "none";
            document.getElementById("AppointMeetingChart").style.display = "block";
            setMyOption(this.$echarts, 'AppointMeetingChart', this.myOption)
            this.picInfo = this.myChart.getDataURL()
          })
        })
      } else if (this.detailType == 'warningCount') {
        // 获取告警统计图表
        document.getElementById("CountWarning").style.display = "block";
        document.getElementById("CountWarningChart").style.display = "none";
        api.getWarningStatisticData({params: {parentMoid: 'all', startTime: '-1w', stopTime: ''}}).then(res => {
          console.log(res)
          this.myOption.yAxis.name = '个'
          this.myOption.yAxis.max = 10
          this.myOption.yAxis.interval = 5
          this.myOption.series = []
          this.myOption.legend.data = []
          this.validData = []
          if (res.success == 1) {
            var day1 = 0
            var day2 = 0
            var maxValue = 0
            if (res.data.server.length > 0) {
              for (var j = res.data.server[0].datapoints.length - 1; j >= 0; j--) {
                if (res.data.server[0].datapoints[j][0] === null) {
                  continue
                }
                if (res.data.server[0].datapoints[j][0] > maxValue) {
                  maxValue = res.data.server[0].datapoints[j][0]
                }
                this.validData.push(res.data.server[0].datapoints[j])
              }
              this.validData.reverse()
              day1 = (this.validData[this.validData.length - 1][1] - this.validData[0][1]) / 3600
              this.myOption.series.push({
                type: 'line',
                name: '服务器告警',
                symbol: 'none',
                data: this.validData.map(function(value) {
                  return {value: [value[1] * 1000, value[0]]};
                }),
                itemStyle: {
                  color: '#5eb9ef'
                },
                areaStyle: {
                  color: '#CCFFFF',
                  origin: 'start',
                },
              })
              this.myOption.legend.data.push({
                name: '服务器告警',
                icon: 'rect'
              })
            }
            if (res.data.terminal.length > 0) {
              this.validData = []
              for (var x = res.data.terminal[0].datapoints.length - 1; x >= 0; x--) {
                if (res.data.terminal[0].datapoints[x][0] === null) {
                  continue
                }
                if (res.data.terminal[0].datapoints[x][0] > maxValue) {
                  maxValue = res.data.terminal[0].datapoints[x][0]
                }
                this.validData.push(res.data.terminal[0].datapoints[x])
              }
              this.validData.reverse()
              day2 = (this.validData[this.validData.length - 1][1] - this.validData[0][1]) / 3600
              this.myOption.series.push({
                type: 'line',
                name: '终端告警',
                symbol: 'none',
                data: this.validData.map(function(value) {
                  return {value: [value[1] * 1000, value[0]]};
                }),
                itemStyle: {
                  color: '#09a206'
                },
                areaStyle: {
                  color: '#CCFFCC',
                  origin: 'start',
                },
              })
              this.myOption.legend.data.push({
                name: '终端告警',
                icon: 'rect'
              })
            }
            let maxLength = String(maxValue).length
            this.myOption.yAxis.max = Math.pow(10, maxLength)
            this.myOption.yAxis.interval = parseInt(parseFloat(Math.pow(10, maxLength) / 2).toFixed(0))
            if (day1 <= 24 && day2 <= 24) {
              this.myOption.xAxis.axisLabel.formatter = function (value, index) {
                var date = new Date(value);
                return date.toTimeString().substr(0, 5);
              }
            } else {
              this.myOption.xAxis.axisLabel.formatter = function (value, index) {
                return FormatDate(value)
              }
            }
          }
          this.$nextTick(() => {
            this.myChart = this.$echarts.init(document.getElementById('CountWarningChart'));
            document.getElementById("CountWarning").style.display = "none";
            document.getElementById("CountWarningChart").style.display = "block";
            setMyOption(this.$echarts, 'CountWarningChart', this.myOption)
            this.picInfo = this.myChart.getDataURL()
          })
        })
      } else if (this.detailType == 'meetingNum') {
        // 获取会议统计
        document.getElementById("MeetingNum").style.display = "block";
        document.getElementById("MeetingNumChart").style.display = "none";
        api.getMeetingStatisticData({params: {parentMoid: 'all', startTime: '-1w', stopTime: ''}}).then(res => {
          console.log(res)
          this.myOption.series = []
          this.myOption.legend.data = []
          this.validData = []
          this.myOption.yAxis.name = '个'
          this.myOption.yAxis.max = 10
          this.myOption.yAxis.interval = 5
          if (res.success == 1) {
            var day1 = 0
            var day2 = 0
            var maxValue = 0
            if (res.data.p2p.length > 0) {
              for (var j = res.data.p2p[0].datapoints.length - 1; j >= 0; j--) {
                if (res.data.p2p[0].datapoints[j][0] === null) {
                  continue
                }
                if (res.data.p2p[0].datapoints[j][0] > maxValue) {
                  maxValue = res.data.p2p[0].datapoints[j][0]
                }
                this.validData.push(res.data.p2p[0].datapoints[j])
              }
              this.validData.reverse()
              day1 = (this.validData[this.validData.length - 1][1] - this.validData[0][1]) / 3600
              this.myOption.series.push({
                type: 'line',
                name: '点对点会议',
                symbol: 'none',
                data: this.validData.map(function(value) {
                  return {value: [value[1] * 1000, value[0]]};
                }),
                itemStyle: {
                  color: '#5eb9ef'
                },
                areaStyle: {
                  color: '#CCFFFF',
                  origin: 'start',
                },
              })
              this.myOption.legend.data.push({
                name: '点对点会议',
                icon: 'rect'
              })
            }
            if (res.data.multi.length > 0) {
              this.validData = []
              for (var x = res.data.multi[0].datapoints.length - 1; x >= 0; x--) {
                if (res.data.multi[0].datapoints[x][0] === null) {
                  continue
                }
                if (res.data.multi[0].datapoints[x][0] > maxValue) {
                  maxValue = res.data.multi[0].datapoints[x][0]
                }
                this.validData.push(res.data.multi[0].datapoints[x])
              }
              this.validData.reverse()
              day2 = (this.validData[this.validData.length - 1][1] - this.validData[0][1]) / 3600
              this.myOption.series.push({
                type: 'line',
                name: '多点会议',
                symbol: 'none',
                data: this.validData.map(function(value) {
                  return {value: [value[1] * 1000, value[0]]};
                }),
                itemStyle: {
                  color: '#09a206'
                },
                areaStyle: {
                  color: '#CCFFCC',
                  origin: 'start',
                },
              })
              this.myOption.legend.data.push({
                name: '多点会议',
                icon: 'rect'
              })
            }
            let maxLength = String(maxValue).length
            this.myOption.yAxis.max = Math.pow(10, maxLength)
            this.myOption.yAxis.interval = parseInt(parseFloat(Math.pow(10, maxLength) / 2).toFixed(0))
            if (day1 <= 24 && day2 <= 24) {
              this.myOption.xAxis.axisLabel.formatter = function (value, index) {
                var date = new Date(value);
                return date.toTimeString().substr(0, 5);
              }
            } else {
              this.myOption.xAxis.axisLabel.formatter = function (value, index) {
                return FormatDate(value)
              }
            }
          }
          this.$nextTick(() => {
            this.myChart = this.$echarts.init(document.getElementById('MeetingNumChart'));
            document.getElementById("MeetingNum").style.display = "none";
            document.getElementById("MeetingNumChart").style.display = "block";
            setMyOption(this.$echarts, 'MeetingNumChart', this.myOption)
            this.picInfo = this.myChart.getDataURL()
          })
        })
      } else if (this.detailType == 'domainUse') {
        // 获取服务器数量图表
        document.getElementById("ServiceNum").style.display = "block";
        document.getElementById("ServiceNumChart").style.display = "none";
        api.getServerStatisticData({params: {parentMoid: 'all', startTime: '-1w', stopTime: ''}}).then(res => {
          console.log(res)
          this.myOption.series = []
          this.myOption.legend.data = []
          this.myOption.yAxis.name = '个'
          this.myOption.yAxis.max = 10
          this.myOption.yAxis.interval = 5
          this.validData = []
          if (res.success == 1) {
            var day1 = 0
            var day2 = 0
            var maxValue = 0
            if (res.data.online.length > 0) {
              for (var j = res.data.online[0].datapoints.length - 1; j >= 0; j--) {
                if (res.data.online[0].datapoints[j][0] === null) {
                  continue
                }
                if (res.data.online[0].datapoints[j][0] > maxValue) {
                  maxValue = res.data.online[0].datapoints[j][0]
                }
                this.validData.push(res.data.online[0].datapoints[j])
              }
              this.validData.reverse()
              day1 = (this.validData[this.validData.length - 1][1] - this.validData[0][1]) / 3600
              this.myOption.series.push({
                type: 'line',
                name: '在线服务器',
                symbol: 'none',
                data: this.validData.map(function(value) {
                  return {value: [value[1] * 1000, value[0]]};
                }),
                itemStyle: {
                  color: '#5eb9ef'
                },
                areaStyle: {
                  color: '#CCFFFF',
                  origin: 'start',
                },
              })
              this.myOption.legend.data.push({
                name: '在线服务器',
                icon: 'rect'
              })
            }
            if (res.data.offline.length > 0) {
              this.validData = []
              for (var x = res.data.offline[0].datapoints.length - 1; x >= 0; x--) {
                if (res.data.offline[0].datapoints[x][0] === null) {
                  continue
                }
                if (res.data.offline[0].datapoints[x][0] > maxValue) {
                  maxValue = res.data.offline[0].datapoints[x][0]
                }
                this.validData.push(res.data.offline[0].datapoints[x])
              }
              this.validData.reverse()
              day2 = (this.validData[this.validData.length - 1][1] - this.validData[0][1]) / 3600
              this.myOption.series.push({
                type: 'line',
                name: '离线服务器',
                symbol: 'none',
                data: this.validData.map(function(value) {
                  return {value: [value[1] * 1000, value[0]]};
                }),
                itemStyle: {
                  color: '#09a206'
                },
                areaStyle: {
                  color: '#CCFFCC',
                  origin: 'start',
                },
              })
              this.myOption.legend.data.push({
                name: '离线服务器',
                icon: 'rect'
              })
            }
            let maxLength = String(maxValue).length
            this.myOption.yAxis.max = Math.pow(10, maxLength)
            this.myOption.yAxis.interval = parseInt(parseFloat(Math.pow(10, maxLength) / 2).toFixed(0))
            if (day1 <= 24 && day2 <= 24) {
              this.myOption.xAxis.axisLabel.formatter = function (value, index) {
                var date = new Date(value);
                return date.toTimeString().substr(0, 5);
              }
            } else {
              this.myOption.xAxis.axisLabel.formatter = function (value, index) {
                return FormatDate(value)
              }
            }
          }
          this.$nextTick(() => {
            this.myChart = this.$echarts.init(document.getElementById('ServiceNumChart'));
            document.getElementById("ServiceNum").style.display = "none";
            document.getElementById("ServiceNumChart").style.display = "block";
            setMyOption(this.$echarts, 'ServiceNumChart', this.myOption)
            this.picInfo = this.myChart.getDataURL()
          })
        })
      } else if (this.detailType == 'terminalUse') {
        // 获取终端数量图表
        document.getElementById("TerminalNum").style.display = "block"
        document.getElementById("TerminalNumChart").style.display = "none"
        api.getTerminalStatisticData({params: {parentMoid: 'all', startTime: '-1w', stopTime: ''}}).then(res => {
          console.log(res)
          this.myOption.series = []
          this.myOption.legend.data = []
          this.validData = []
          this.myOption.yAxis.max = 10
          this.myOption.yAxis.interval = 5
          this.myOption.yAxis.name = '个'
          if (res.success == 1) {
            var day1 = 0
            var day2 = 0
            var maxValue = 0
            if (res.data.online.length > 0) {
              for (var j = res.data.online[0].datapoints.length - 1; j >= 0; j--) {
                if (res.data.online[0].datapoints[j][0] === null) {
                  continue
                }
                if (res.data.online[0].datapoints[j][0] > maxValue) {
                  maxValue = res.data.online[0].datapoints[j][0]
                }
                this.validData.push(res.data.online[0].datapoints[j])
              }
              this.validData.reverse()
              day1 = (this.validData[this.validData.length - 1][1] - this.validData[0][1]) / 3600
              this.myOption.series.push({
                type: 'line',
                name: '在线终端',
                symbol: 'none',
                data: this.validData.map(function(value) {
                  return {value: [value[1] * 1000, value[0]]};
                }),
                itemStyle: {
                  color: '#5eb9ef'
                },
                areaStyle: {
                  color: '#CCFFFF',
                  origin: 'start',
                },
              })
              this.myOption.legend.data.push({
                name: '在线终端',
                icon: 'rect'
              })
            }
            if (res.data.offline.length > 0) {
              this.validData = []
              for (var x = res.data.offline[0].datapoints.length - 1; x >= 0; x--) {
                if (res.data.offline[0].datapoints[x][0] === null) {
                  continue
                }
                if (res.data.offline[0].datapoints[x][0] > maxValue) {
                  maxValue = res.data.offline[0].datapoints[x][0]
                }
                this.validData.push(res.data.offline[0].datapoints[x])
              }
              this.validData.reverse()
              day2 = (this.validData[this.validData.length - 1][1] - this.validData[0][1]) / 3600
              this.myOption.series.push({
                type: 'line',
                name: '离线终端',
                symbol: 'none',
                data: this.validData.map(function(value) {
                  return {value: [value[1] * 1000, value[0]]};
                }),
                itemStyle: {
                  color: '#09a206'
                },
                areaStyle: {
                  color: '#CCFFCC',
                  origin: 'start',
                },
              })
              this.myOption.legend.data.push({
                name: '离线终端',
                icon: 'rect'
              })
            }
            let maxLength = String(maxValue).length
            this.myOption.yAxis.max = Math.pow(10, maxLength)
            this.myOption.yAxis.interval = parseInt(parseFloat(Math.pow(10, maxLength) / 2).toFixed(0))
            if (day1 <= 24 && day2 <= 24) {
              this.myOption.xAxis.axisLabel.formatter = function (value, index) {
                var date = new Date(value);
                return date.toTimeString().substr(0, 5);
              }
            } else {
              this.myOption.xAxis.axisLabel.formatter = function (value, index) {
                return FormatDate(value)
              }
            }
          }
          this.$nextTick(() => {
            this.myChart = this.$echarts.init(document.getElementById('TerminalNumChart'));
            document.getElementById("TerminalNum").style.display = "none"
            document.getElementById("TerminalNumChart").style.display = "block"
            setMyOption(this.$echarts, 'TerminalNumChart', this.myOption)
            this.picInfo = this.myChart.getDataURL()
          })
        })
      }
    },
    mounted: function () {
      // 获取下拉框域
      api.getUserDomainTree().then((res) => {
        console.log(res)
        this.tTerminalDomainMoids = []
        this.tUserMoids = []
        let serverCount = 0
        let userCount = 0
        this.warningUesrDomains = res.data
        this.warningUesrDomains.forEach(item => {
          if (item.type === "service" || item.type === "kernel") {
            this.tTerminalDomainMoids.unshift(item)
            serverCount++
          } else if (item.type === "user") {
            this.tUserMoids.unshift(item)
            userCount++
          }
        })
        if (serverCount == 0) {
          this.tTerminalDomainMoids.unshift({
            "moid": "",
            "parent_moid": "",
            "name": "无下级域",
            "type": "server"
          })
          this.tTerminalDomainMoid = ''
        } else {
          this.tTerminalDomainMoids.unshift({
            "moid": "all",
            "parent_moid": "",
            "name": "所有服务域",
            "type": "server"
          })
          this.tTerminalDomainMoid = 'all'
        }
        if (userCount == 0) {
          this.tUserMoids.unshift({
            "moid": "",
            "parent_moid": "",
            "name": "无下级域",
            "type": "user"
          })
          this.tUserMoid = ''
        } else {
          this.tUserMoids.unshift({
            "moid": "all",
            "parent_moid": "",
            "name": "所有用户域",
            "type": "user"
          })
          this.tUserMoid = 'all'
        }
      })
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
      })
    },
    methods: {
      onExport: function() {
        let aLink = document.createElement('a');
        let event = new MouseEvent('click');
        aLink.download = "导出图表.png";
        aLink.href = this.myChart.getDataURL();
        aLink.dispatchEvent(event);
      },
      searchDomain: function() {
        this.fromTime = ''
        this.untilTime = ''
        var nowDate = parseInt(new Date().getTime())
        if (this.timePeriodValue == 'lastweek') {
          this.fromTime = '-1w'
          this.untilTime = ''
          if (this.detailType == 'meetingAppoint') {
            this.startDate = new Date()
            this.endDate = new Date(nowDate + 60 * 60 * 1000 * 24 * 7)
          } else {
            this.endDate = new Date()
            this.startDate = new Date(nowDate - 60 * 60 * 1000 * 24 * 7)
          }
        } else if (this.timePeriodValue == 'lastmonth') {
          this.fromTime = '-1mon'
          this.untilTime = ''
          if (this.detailType == 'meetingAppoint') {
            this.startDate = new Date()
            this.endDate = new Date(nowDate + 60 * 60 * 1000 * 24 * 30)
          } else {
            this.endDate = new Date()
            this.startDate = new Date(nowDate - 60 * 60 * 1000 * 24 * 30)
          }
        } else if (this.timePeriodValue == 'lasthour') {
          this.fromTime = '-1h'
          this.untilTime = ''
          if (this.detailType == 'meetingAppoint') {
            this.startDate = new Date()
            this.endDate = new Date(nowDate + 60 * 60 * 1000)
          } else {
            this.endDate = new Date()
            this.startDate = new Date(nowDate - 60 * 60 * 1000)
          }
        } else if (this.timePeriodValue == 'lastday') {
          this.fromTime = '-1d'
          this.untilTime = ''
          if (this.detailType == 'meetingAppoint') {
            this.startDate = new Date()
            this.endDate = new Date()
          } else {
            this.endDate = new Date()
            this.startDate = new Date()
          }
        } else if (this.timePeriodValue == 'selfdefine') {
          var nowTime = new Date()
          if (this.endDate !== nowTime) {
            this.untilTime = '23:59' + FormatChartTime(this.endDate).substr(5, 13)
          } else {
            this.untilTime = FormatChartTime(this.endDate)
          }
          this.fromTime = FormatChartTime(this.startDate)
        }
        if (this.detailType == 'meetingAppoint') {
          // 获取预约会议图表
          document.getElementById("AppointMeetingChart").style.display = "none";
          document.getElementById("AppointMeeting").style.display = "block";
          var appointStopTime = FormatTime(this.endDate)
          var appointStartTime = FormatTime(this.startDate)
          if (this.tUserMoid == '') {
            this.errorDialog.open('用户域不能为空')
          } else {
            this.searchMoid = this.tUserMoid
          }
          api.getAppointMeetingData({params: {parentMoid: this.searchMoid, startTime: appointStartTime, stopTime: appointStopTime}}).then(res => {
            console.log(res)
            this.myOption.yAxis.name = '个'
            this.myOption.yAxis.max = 10
            this.myOption.yAxis.interval = 5
            this.myOption.series = []
            this.myOption.legend.data = []
            this.validData = []
            if (res.success == 1) {
              if (res.datapoints.length > 0) {
                var maxValue = 0
                for (var j = res.datapoints.length - 1; j >= 0; j--) {
                  if (res.datapoints[j][0] === null) {
                    continue
                  }
                  if (res.datapoints[j][0] > maxValue) {
                    maxValue = res.datapoints[j][0]
                  }
                  this.validData.push(res.datapoints[j])
                }
                this.validData.reverse()
                var day1 = (this.validData[this.validData.length - 1][1] - this.validData[0][1]) / 3600
                let maxLength = String(maxValue).length
                this.myOption.yAxis.max = Math.pow(10, maxLength)
                this.myOption.yAxis.interval = parseInt(parseFloat(Math.pow(10, maxLength) / 2).toFixed(0))
                this.myOption.series.push({
                  type: 'line',
                  name: '预约会议数量',
                  symbol: 'none',
                  data: this.validData.map(function(value) {
                    return {value: [value[1] * 1000, value[0]]};
                  }),
                  itemStyle: {
                    color: '#5eb9ef'
                  },
                  areaStyle: {
                    color: '#CCFFFF',
                    origin: 'start',
                  },
                })
                if (day1 <= 24) {
                  this.myOption.xAxis.axisLabel.formatter = function (value, index) {
                    var date = new Date(value);
                    return date.toTimeString().substr(0, 5);
                  }
                } else {
                  this.myOption.xAxis.axisLabel.formatter = function (value, index) {
                    return FormatDate(value)
                  }
                }
              }
            }
            this.$nextTick(() => {
              this.myChart = this.$echarts.init(document.getElementById('AppointMeetingChart'));
              document.getElementById("AppointMeeting").style.display = "none";
              document.getElementById("AppointMeetingChart").style.display = "block";
              setMyOption(this.$echarts, 'AppointMeetingChart', this.myOption)
              this.picInfo = this.myChart.getDataURL()
            })
          })
        } else if (this.detailType == 'warningCount') {
          // 获取告警统计图表
          document.getElementById("CountWarningChart").style.display = "none";
          document.getElementById("CountWarning").style.display = "block";
          api.getWarningStatisticData({params: {parentMoid: 'all', startTime: this.fromTime, stopTime: this.untilTime}}).then(res => {
            console.log(res)
            this.myOption.yAxis.name = '个'
            this.myOption.yAxis.max = 10
            this.myOption.yAxis.interval = 5
            this.myOption.series = []
            this.myOption.legend.data = []
            this.validData = []
            if (res.success == 1) {
              var day1 = 0
              var day2 = 0
              var maxValue = 0
              if (res.data.server.length > 0) {
                for (var j = res.data.server[0].datapoints.length - 1; j >= 0; j--) {
                  if (res.data.server[0].datapoints[j][0] === null) {
                    continue
                  }
                  if (res.data.server[0].datapoints[j][0] > maxValue) {
                    maxValue = res.data.server[0].datapoints[j][0]
                  }
                  this.validData.push(res.data.server[0].datapoints[j])
                }
                this.validData.reverse()
                day1 = (this.validData[this.validData.length - 1][1] - this.validData[0][1]) / 3600
                this.myOption.series.push({
                  type: 'line',
                  name: '服务器告警',
                  symbol: 'none',
                  data: this.validData.map(function(value) {
                    return {value: [value[1] * 1000, value[0]]};
                  }),
                  itemStyle: {
                    color: '#5eb9ef'
                  },
                  areaStyle: {
                    color: '#CCFFFF',
                    origin: 'start',
                  },
                })
                this.myOption.legend.data.push({
                  name: '服务器告警',
                  icon: 'rect'
                })
              }
              if (res.data.terminal.length > 0) {
                this.validData = []
                for (var x = res.data.terminal[0].datapoints.length - 1; x >= 0; x--) {
                  if (res.data.terminal[0].datapoints[x][0] === null) {
                    continue
                  }
                  if (res.data.terminal[0].datapoints[x][0] > maxValue) {
                    maxValue = res.data.terminal[0].datapoints[x][0]
                  }
                  this.validData.push(res.data.terminal[0].datapoints[x])
                }
                this.validData.reverse()
                day2 = (this.validData[this.validData.length - 1][1] - this.validData[0][1]) / 3600
                this.myOption.series.push({
                  type: 'line',
                  name: '终端告警',
                  symbol: 'none',
                  data: this.validData.map(function(value) {
                    return {value: [value[1] * 1000, value[0]]};
                  }),
                  itemStyle: {
                    color: '#09a206'
                  },
                  areaStyle: {
                    color: '#CCFFCC',
                    origin: 'start',
                  },
                })
                this.myOption.legend.data.push({
                  name: '终端告警',
                  icon: 'rect'
                })
              }
              let maxLength = String(maxValue).length
              this.myOption.yAxis.max = Math.pow(10, maxLength)
              this.myOption.yAxis.interval = parseInt(parseFloat(Math.pow(10, maxLength) / 2).toFixed(0))
              if (day1 <= 24 && day2 <= 24) {
                this.myOption.xAxis.axisLabel.formatter = function (value, index) {
                  var date = new Date(value);
                  return date.toTimeString().substr(0, 5);
                }
              } else {
                this.myOption.xAxis.axisLabel.formatter = function (value, index) {
                  return FormatDate(value)
                }
              }
            }
            this.$nextTick(() => {
              this.myChart = this.$echarts.init(document.getElementById('CountWarningChart'));
              document.getElementById("CountWarning").style.display = "none";
              document.getElementById("CountWarningChart").style.display = "block";
              setMyOption(this.$echarts, 'CountWarningChart', this.myOption)
              this.picInfo = this.myChart.getDataURL()
            })
          })
        } else if (this.detailType == 'meetingNum') {
          // 获取会议统计
          if (this.tUserMoid == '') {
            this.errorDialog.open('用户域不能为空')
          } else {
            this.searchMoid = this.tUserMoid
          }
          document.getElementById("MeetingNumChart").style.display = "none";
          document.getElementById("MeetingNum").style.display = "block";
          api.getMeetingStatisticData({params: {parentMoid: this.searchMoid, startTime: this.fromTime, stopTime: this.untilTime}}).then(res => {
            console.log(res)
            this.myOption.series = []
            this.myOption.legend.data = []
            this.validData = []
            this.myOption.yAxis.name = '个'
            this.myOption.yAxis.max = 10
            this.myOption.yAxis.interval = 5
            if (res.success == 1) {
              var day1 = 0
              var day2 = 0
              var maxValue = 0
              if (res.data.p2p.length > 0) {
                for (var j = res.data.p2p[0].datapoints.length - 1; j >= 0; j--) {
                  if (res.data.p2p[0].datapoints[j][0] === null) {
                    continue
                  }
                  if (res.data.p2p[0].datapoints[j][0] > maxValue) {
                    maxValue = res.data.p2p[0].datapoints[j][0]
                  }
                  this.validData.push(res.data.p2p[0].datapoints[j])
                }
                this.validData.reverse()
                day1 = (this.validData[this.validData.length - 1][1] - this.validData[0][1]) / 3600
                this.myOption.series.push({
                  type: 'line',
                  name: '点对点会议',
                  symbol: 'none',
                  data: this.validData.map(function(value) {
                    return {value: [value[1] * 1000, value[0]]};
                  }),
                  itemStyle: {
                    color: '#5eb9ef'
                  },
                  areaStyle: {
                    color: '#CCFFFF',
                    origin: 'start',
                  },
                })
                this.myOption.legend.data.push({
                  name: '点对点会议',
                  icon: 'rect'
                })
              }
              if (res.data.multi.length > 0) {
                this.validData = []
                for (var x = res.data.multi[0].datapoints.length - 1; x >= 0; x--) {
                  if (res.data.multi[0].datapoints[x][0] === null) {
                    continue
                  }
                  if (res.data.multi[0].datapoints[x][0] > maxValue) {
                    maxValue = res.data.multi[0].datapoints[x][0]
                  }
                  this.validData.push(res.data.multi[0].datapoints[x])
                }
                this.validData.reverse()
                day2 = (this.validData[this.validData.length - 1][1] - this.validData[0][1]) / 3600
                this.myOption.series.push({
                  type: 'line',
                  name: '多点会议',
                  symbol: 'none',
                  data: this.validData.map(function(value) {
                    return {value: [value[1] * 1000, value[0]]};
                  }),
                  itemStyle: {
                    color: '#09a206'
                  },
                  areaStyle: {
                    color: '#CCFFCC',
                    origin: 'start',
                  },
                })
                this.myOption.legend.data.push({
                  name: '多点会议',
                  icon: 'rect'
                })
              }
              let maxLength = String(maxValue).length
              this.myOption.yAxis.max = Math.pow(10, maxLength)
              this.myOption.yAxis.interval = parseInt(parseFloat(Math.pow(10, maxLength) / 2).toFixed(0))
              if (day1 <= 24 && day2 <= 24) {
                this.myOption.xAxis.axisLabel.formatter = function (value, index) {
                  var date = new Date(value);
                  return date.toTimeString().substr(0, 5);
                }
              } else {
                this.myOption.xAxis.axisLabel.formatter = function (value, index) {
                  return FormatDate(value)
                }
              }
            }
            this.$nextTick(() => {
              this.myChart = this.$echarts.init(document.getElementById('MeetingNumChart'));
              document.getElementById("MeetingNum").style.display = "none";
              document.getElementById("MeetingNumChart").style.display = "block";
              setMyOption(this.$echarts, 'MeetingNumChart', this.myOption)
              this.picInfo = this.myChart.getDataURL()
            })
          })
        } else if (this.detailType == 'domainUse') {
          if (this.machineRoom == '') {
            this.errorDialog.open('机房域不能为空')
          } else {
            this.searchMoid = this.machineRoom
          }
          document.getElementById("ServiceNumChart").style.display = "none";
          document.getElementById("ServiceNum").style.display = "block";
          // 获取服务器数量图表
          api.getServerStatisticData({params: {parentMoid: this.searchMoid, startTime: this.fromTime, stopTime: this.untilTime}}).then(res => {
            console.log(res)
            this.myOption.series = []
            this.myOption.legend.data = []
            this.myOption.yAxis.name = '个'
            this.myOption.yAxis.max = 10
            this.myOption.yAxis.interval = 5
            this.validData = []
            if (res.success == 1) {
              var day1 = 0
              var day2 = 0
              var maxValue = 0
              if (res.data.online.length > 0) {
                for (var j = res.data.online[0].datapoints.length - 1; j >= 0; j--) {
                  if (res.data.online[0].datapoints[j][0] === null) {
                    continue
                  }
                  if (res.data.online[0].datapoints[j][0] > maxValue) {
                    maxValue = res.data.online[0].datapoints[j][0]
                  }
                  this.validData.push(res.data.online[0].datapoints[j])
                }
                this.validData.reverse()
                day1 = (this.validData[this.validData.length - 1][1] - this.validData[0][1]) / 3600
                this.myOption.series.push({
                  type: 'line',
                  name: '在线服务器',
                  symbol: 'none',
                  data: this.validData.map(function(value) {
                    return {value: [value[1] * 1000, value[0]]};
                  }),
                  itemStyle: {
                    color: '#5eb9ef'
                  },
                  areaStyle: {
                    color: '#CCFFFF',
                    origin: 'start',
                  },
                })
                this.myOption.legend.data.push({
                  name: '在线服务器',
                  icon: 'rect'
                })
              }
              if (res.data.offline.length > 0) {
                this.validData = []
                for (var x = res.data.offline[0].datapoints.length - 1; x >= 0; x--) {
                  if (res.data.offline[0].datapoints[x][0] === null) {
                    continue
                  }
                  if (res.data.offline[0].datapoints[x][0] > maxValue) {
                    maxValue = res.data.offline[0].datapoints[x][0]
                  }
                  this.validData.push(res.data.offline[0].datapoints[x])
                }
                this.validData.reverse()
                day2 = (this.validData[this.validData.length - 1][1] - this.validData[0][1]) / 3600
                this.myOption.series.push({
                  type: 'line',
                  name: '离线服务器',
                  symbol: 'none',
                  data: this.validData.map(function(value) {
                    return {value: [value[1] * 1000, value[0]]};
                  }),
                  itemStyle: {
                    color: '#09a206'
                  },
                  areaStyle: {
                    color: '#CCFFCC',
                    origin: 'start',
                  },
                })
                this.myOption.legend.data.push({
                  name: '离线服务器',
                  icon: 'rect'
                })
              }
              let maxLength = String(maxValue).length
              this.myOption.yAxis.max = Math.pow(10, maxLength)
              this.myOption.yAxis.interval = parseInt(parseFloat(Math.pow(10, maxLength) / 2).toFixed(0))
              if (day1 <= 24 && day2 <= 24) {
                this.myOption.xAxis.axisLabel.formatter = function (value, index) {
                  var date = new Date(value);
                  return date.toTimeString().substr(0, 5);
                }
              } else {
                this.myOption.xAxis.axisLabel.formatter = function (value, index) {
                  return FormatDate(value)
                }
              }
            }
            this.$nextTick(() => {
              this.myChart = this.$echarts.init(document.getElementById('ServiceNumChart'));
              document.getElementById("ServiceNum").style.display = "none";
              document.getElementById("ServiceNumChart").style.display = "block";
              setMyOption(this.$echarts, 'ServiceNumChart', this.myOption)
              this.picInfo = this.myChart.getDataURL()
            })
          })
        } else if (this.detailType == 'terminalUse') {
          if (this.tUserMoid == '') {
            this.errorDialog.open('用户域不能为空')
          } else {
            this.searchMoid = this.tUserMoid
          }
          // 获取终端数量图表
          document.getElementById("TerminalNumChart").style.display = "none";
          document.getElementById("TerminalNum").style.display = "block";
          api.getTerminalStatisticData({params: {parentMoid: this.searchMoid, startTime: this.fromTime, stopTime: this.untilTime}}).then(res => {
            console.log(res)
            this.myOption.series = []
            this.myOption.legend.data = []
            this.validData = []
            this.myOption.yAxis.max = 10
            this.myOption.yAxis.interval = 5
            this.myOption.yAxis.name = '个'
            if (res.success == 1) {
              var day1 = 0
              var day2 = 0
              var maxValue = 0
              if (res.data.online.length > 0) {
                for (var j = res.data.online[0].datapoints.length - 1; j >= 0; j--) {
                  if (res.data.online[0].datapoints[j][0] === null) {
                    continue
                  }
                  if (res.data.online[0].datapoints[j][0] > maxValue) {
                    maxValue = res.data.online[0].datapoints[j][0]
                  }
                  this.validData.push(res.data.online[0].datapoints[j])
                }
                this.validData.reverse()
                day1 = (this.validData[this.validData.length - 1][1] - this.validData[0][1]) / 3600
                this.myOption.series.push({
                  type: 'line',
                  name: '在线终端',
                  symbol: 'none',
                  data: this.validData.map(function(value) {
                    return {value: [value[1] * 1000, value[0]]};
                  }),
                  itemStyle: {
                    color: '#5eb9ef'
                  },
                  areaStyle: {
                    color: '#CCFFFF',
                    origin: 'start',
                  },
                })
                this.myOption.legend.data.push({
                  name: '在线终端',
                  icon: 'rect'
                })
              }
              if (res.data.offline.length > 0) {
                this.validData = []
                for (var x = res.data.offline[0].datapoints.length - 1; x >= 0; x--) {
                  if (res.data.offline[0].datapoints[x][0] === null) {
                    continue
                  }
                  if (res.data.offline[0].datapoints[x][0] > maxValue) {
                    maxValue = res.data.offline[0].datapoints[x][0]
                  }
                  this.validData.push(res.data.offline[0].datapoints[x])
                }
                this.validData.reverse()
                day2 = (this.validData[this.validData.length - 1][1] - this.validData[0][1]) / 3600
                this.myOption.series.push({
                  type: 'line',
                  name: '离线终端',
                  symbol: 'none',
                  data: this.validData.map(function(value) {
                    return {value: [value[1] * 1000, value[0]]};
                  }),
                  itemStyle: {
                    color: '#09a206'
                  },
                  areaStyle: {
                    color: '#CCFFCC',
                    origin: 'start',
                  },
                })
                this.myOption.legend.data.push({
                  name: '离线终端',
                  icon: 'rect'
                })
              }
              let maxLength = String(maxValue).length
              this.myOption.yAxis.max = Math.pow(10, maxLength)
              this.myOption.yAxis.interval = parseInt(parseFloat(Math.pow(10, maxLength) / 2).toFixed(0))
              if (day1 <= 24 && day2 <= 24) {
                this.myOption.xAxis.axisLabel.formatter = function (value, index) {
                  var date = new Date(value);
                  return date.toTimeString().substr(0, 5);
                }
              } else {
                this.myOption.xAxis.axisLabel.formatter = function (value, index) {
                  return FormatDate(value)
                }
              }
            }
            this.$nextTick(() => {
              this.myChart = this.$echarts.init(document.getElementById('TerminalNumChart'));
              document.getElementById("TerminalNum").style.display = "none";
              document.getElementById("TerminalNumChart").style.display = "block";
              setMyOption(this.$echarts, 'TerminalNumChart', this.myOption)
              this.picInfo = this.myChart.getDataURL()
            })
          })
        }
      },
      serverClick: function() {

      },
      userClick: function() {

      }
    },
    watch: {
      detailType: function (newTab, oldTab) {
        document.getElementById("AppointMeetingChart").style.display = "none";
        document.getElementById("CountWarningChart").style.display = "none";
        document.getElementById("MeetingNumChart").style.display = "none";
        document.getElementById("ServiceNumChart").style.display = "none";
        document.getElementById("TerminalNumChart").style.display = "none";
        this.timePeriodValue = 'selfdefine'
        this.timePeriodValue = 'lastweek'
        this.startDate = get_time(this.timePeriodValue)
        this.endDate = new Date()
        this.searchMoid = ''
        api.getUserDomainTree().then((res) => {
          console.log(res)
          this.tTerminalDomainMoids = []
          this.tUserMoids = []
          let serverCount = 0
          let userCount = 0
          this.warningUesrDomains = res.data
          this.warningUesrDomains.forEach(item => {
            if (item.type === "service" || item.type === "kernel") {
              this.tTerminalDomainMoids.unshift(item)
              serverCount++
            } else if (item.type === "user") {
              this.tUserMoids.unshift(item)
              userCount++
            }
          })
          if (serverCount == 0) {
            this.tTerminalDomainMoids.unshift({
              "moid": "",
              "parent_moid": "",
              "name": "无下级域",
              "type": "server"
            })
            this.tTerminalDomainMoid = ''
          } else {
            this.tTerminalDomainMoids.unshift({
              "moid": "all",
              "parent_moid": "",
              "name": "所有服务域",
              "type": "server"
            })
            this.tTerminalDomainMoid = 'all'
          }
          if (userCount == 0) {
            this.tUserMoids.unshift({
              "moid": "",
              "parent_moid": "",
              "name": "无下级域",
              "type": "user"
            })
            this.tUserMoid = ''
          } else {
            this.tUserMoids.unshift({
              "moid": "all",
              "parent_moid": "",
              "name": "所有用户域",
              "type": "user"
            })
            this.tUserMoid = 'all'
          }
        })
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
        if (newTab == 'meetingResource') {
          api.getMeetingResourceData({params: {parentMoid: 'all'}}).then(res => {
            console.log(res)
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
          })
        } else if (newTab === "meetingAppoint") {
          document.getElementById("AppointMeeting").style.display = "block";
          // 获取预约会议图表
          this.timePeriodValue = 'selfdefine'
          var nowDate = parseInt(new Date().getTime())
          this.startDate = new Date()
          this.endDate = new Date(nowDate + 3600 * 1000 * 24 * 7);
          this.timePeriodValue = 'lastweek'
          var appointStopTime = FormatTime(this.endDate)
          var appointStartTime = FormatTime(this.startDate)
          console.log(this.endDate)
          console.log(this.startDate)
          api.getAppointMeetingData({params: {parentMoid: 'all', startTime: appointStartTime, stopTime: appointStopTime}}).then(res => {
            console.log(res)
            this.myOption.yAxis.name = '个'
            this.myOption.yAxis.max = 10
            this.myOption.yAxis.interval = 5
            this.myOption.series = []
            this.myOption.legend.data = []
            this.validData = []
            if (res.success == 1) {
              if (res.datapoints.length > 0) {
                var maxValue = 0
                for (var j = res.datapoints.length - 1; j >= 0; j--) {
                  if (res.datapoints[j][0] === null) {
                    continue
                  }
                  if (res.datapoints[j][0] > maxValue) {
                    maxValue = res.datapoints[j][0]
                  }
                  this.validData.push(res.datapoints[j])
                }
                this.validData.reverse()
                var day1 = (this.validData[this.validData.length - 1][1] - this.validData[0][1]) / 3600
                let maxLength = String(maxValue).length
                this.myOption.yAxis.max = Math.pow(10, maxLength)
                this.myOption.yAxis.interval = parseInt(parseFloat(Math.pow(10, maxLength) / 2).toFixed(0))
                this.myOption.series.push({
                  type: 'line',
                  name: '预约会议数量',
                  symbol: 'none',
                  data: this.validData.map(function(value) {
                    return {value: [value[1] * 1000, value[0]]};
                  }),
                  itemStyle: {
                    color: '#5eb9ef'
                  },
                  areaStyle: {
                    color: '#CCFFFF',
                    origin: 'start',
                  },
                })
                if (day1 <= 24) {
                  this.myOption.xAxis.axisLabel.formatter = function (value, index) {
                    var date = new Date(value);
                    return date.toTimeString().substr(0, 5);
                  }
                } else {
                  this.myOption.xAxis.axisLabel.formatter = function (value, index) {
                    return FormatDate(value)
                  }
                }
              }
            }
            this.$nextTick(() => {
              this.myChart = this.$echarts.init(document.getElementById('AppointMeetingChart'));
              document.getElementById("AppointMeeting").style.display = "none";
              document.getElementById("AppointMeetingChart").style.display = "block";
              setMyOption(this.$echarts, 'AppointMeetingChart', this.myOption)
              this.picInfo = this.myChart.getDataURL()
            })
          })
        } else if (newTab === "domainUse") {
          // 获取服务器数量图表
          document.getElementById("ServiceNum").style.display = "block";
          api.getServerStatisticData({params: {parentMoid: 'all', startTime: '-1w', stopTime: ''}}).then(res => {
            console.log(res)
            this.myOption.series = []
            this.myOption.legend.data = []
            this.myOption.yAxis.name = '个'
            this.myOption.yAxis.max = 10
            this.myOption.yAxis.interval = 5
            this.validData = []
            if (res.success == 1) {
              var day1 = 0
              var day2 = 0
              var maxValue = 0
              if (res.data.online.length > 0) {
                for (var j = res.data.online[0].datapoints.length - 1; j >= 0; j--) {
                  if (res.data.online[0].datapoints[j][0] === null) {
                    continue
                  }
                  if (res.data.online[0].datapoints[j][0] > maxValue) {
                    maxValue = res.data.online[0].datapoints[j][0]
                  }
                  this.validData.push(res.data.online[0].datapoints[j])
                }
                this.validData.reverse()
                day1 = (this.validData[this.validData.length - 1][1] - this.validData[0][1]) / 3600
                this.myOption.series.push({
                  type: 'line',
                  name: '在线服务器',
                  symbol: 'none',
                  data: this.validData.map(function(value) {
                    return {value: [value[1] * 1000, value[0]]};
                  }),
                  itemStyle: {
                    color: '#5eb9ef'
                  },
                  areaStyle: {
                    color: '#CCFFFF',
                    origin: 'start',
                  },
                })
                this.myOption.legend.data.push({
                  name: '在线服务器',
                  icon: 'rect'
                })
              }
              if (res.data.offline.length > 0) {
                this.validData = []
                for (var x = res.data.offline[0].datapoints.length - 1; x >= 0; x--) {
                  if (res.data.offline[0].datapoints[x][0] === null) {
                    continue
                  }
                  if (res.data.offline[0].datapoints[x][0] > maxValue) {
                    maxValue = res.data.offline[0].datapoints[x][0]
                  }
                  this.validData.push(res.data.offline[0].datapoints[x])
                }
                this.validData.reverse()
                day2 = (this.validData[this.validData.length - 1][1] - this.validData[0][1]) / 3600
                this.myOption.series.push({
                  type: 'line',
                  name: '离线服务器',
                  symbol: 'none',
                  data: this.validData.map(function(value) {
                    return {value: [value[1] * 1000, value[0]]};
                  }),
                  itemStyle: {
                    color: '#09a206'
                  },
                  areaStyle: {
                    color: '#CCFFCC',
                    origin: 'start',
                  },
                })
                this.myOption.legend.data.push({
                  name: '离线服务器',
                  icon: 'rect'
                })
              }
              let maxLength = String(maxValue).length
              this.myOption.yAxis.max = Math.pow(10, maxLength)
              this.myOption.yAxis.interval = parseInt(parseFloat(Math.pow(10, maxLength) / 2).toFixed(0))
              if (day1 <= 24 && day2 <= 24) {
                this.myOption.xAxis.axisLabel.formatter = function (value, index) {
                  var date = new Date(value);
                  return date.toTimeString().substr(0, 5);
                }
              } else {
                this.myOption.xAxis.axisLabel.formatter = function (value, index) {
                  return FormatDate(value)
                }
              }
            }
            this.$nextTick(() => {
              this.myChart = this.$echarts.init(document.getElementById('ServiceNumChart'));
              document.getElementById("ServiceNumChart").style.display = "block";
              document.getElementById("ServiceNum").style.display = "none";
              setMyOption(this.$echarts, 'ServiceNumChart', this.myOption)
              this.picInfo = this.myChart.getDataURL()
            })
          })
        } else if (newTab === "terminalUse") {
          document.getElementById("TerminalNum").style.display = "block";
          // 获取终端数量图表
          api.getTerminalStatisticData({params: {parentMoid: 'all', startTime: '-1w', stopTime: ''}}).then(res => {
            console.log(res)
            this.myOption.series = []
            this.myOption.legend.data = []
            this.validData = []
            this.myOption.yAxis.max = 10
            this.myOption.yAxis.interval = 5
            this.myOption.yAxis.name = '个'
            if (res.success == 1) {
              var day1 = 0
              var day2 = 0
              var maxValue = 0
              if (res.data.online.length > 0) {
                for (var j = res.data.online[0].datapoints.length - 1; j >= 0; j--) {
                  if (res.data.online[0].datapoints[j][0] === null) {
                    continue
                  }
                  if (res.data.online[0].datapoints[j][0] > maxValue) {
                    maxValue = res.data.online[0].datapoints[j][0]
                  }
                  this.validData.push(res.data.online[0].datapoints[j])
                }
                this.validData.reverse()
                day1 = (this.validData[this.validData.length - 1][1] - this.validData[0][1]) / 3600
                this.myOption.series.push({
                  type: 'line',
                  name: '在线终端',
                  symbol: 'none',
                  data: this.validData.map(function(value) {
                    return {value: [value[1] * 1000, value[0]]};
                  }),
                  itemStyle: {
                    color: '#5eb9ef'
                  },
                  areaStyle: {
                    color: '#CCFFFF',
                    origin: 'start',
                  },
                })
                this.myOption.legend.data.push({
                  name: '在线终端',
                  icon: 'rect'
                })
              }
              if (res.data.offline.length > 0) {
                this.validData = []
                for (var x = res.data.offline[0].datapoints.length - 1; x >= 0; x--) {
                  if (res.data.offline[0].datapoints[x][0] === null) {
                    continue
                  }
                  if (res.data.offline[0].datapoints[x][0] > maxValue) {
                    maxValue = res.data.offline[0].datapoints[x][0]
                  }
                  this.validData.push(res.data.offline[0].datapoints[x])
                }
                this.validData.reverse()
                day2 = (this.validData[this.validData.length - 1][1] - this.validData[0][1]) / 3600
                this.myOption.series.push({
                  type: 'line',
                  name: '离线终端',
                  symbol: 'none',
                  data: this.validData.map(function(value) {
                    return {value: [value[1] * 1000, value[0]]};
                  }),
                  itemStyle: {
                    color: '#09a206'
                  },
                  areaStyle: {
                    color: '#CCFFCC',
                    origin: 'start',
                  },
                })
                this.myOption.legend.data.push({
                  name: '离线终端',
                  icon: 'rect'
                })
              }
              let maxLength = String(maxValue).length
              this.myOption.yAxis.max = Math.pow(10, maxLength)
              this.myOption.yAxis.interval = parseInt(parseFloat(Math.pow(10, maxLength) / 2).toFixed(0))
              if (day1 <= 24 && day2 <= 24) {
                this.myOption.xAxis.axisLabel.formatter = function (value, index) {
                  var date = new Date(value);
                  return date.toTimeString().substr(0, 5);
                }
              } else {
                this.myOption.xAxis.axisLabel.formatter = function (value, index) {
                  return FormatDate(value)
                }
              }
            }
            this.$nextTick(() => {
              this.myChart = this.$echarts.init(document.getElementById('TerminalNumChart'));
              document.getElementById("TerminalNum").style.display = "none";
              document.getElementById("TerminalNumChart").style.display = "block";
              setMyOption(this.$echarts, 'TerminalNumChart', this.myOption)
              this.picInfo = this.myChart.getDataURL()
            })
          })
        } else if (newTab === "meetingNum") {
          document.getElementById("MeetingNum").style.display = "block";
          // 获取会议统计
          api.getMeetingStatisticData({params: {parentMoid: 'all', startTime: '-1w', stopTime: ''}}).then(res => {
            console.log(res)
            this.myOption.series = []
            this.myOption.legend.data = []
            this.validData = []
            this.myOption.yAxis.name = '个'
            this.myOption.yAxis.max = 10
            this.myOption.yAxis.interval = 5
            if (res.success == 1) {
              var day1 = 0
              var day2 = 0
              var maxValue = 0
              if (res.data.p2p.length > 0) {
                for (var j = res.data.p2p[0].datapoints.length - 1; j >= 0; j--) {
                  if (res.data.p2p[0].datapoints[j][0] === null) {
                    continue
                  }
                  if (res.data.p2p[0].datapoints[j][0] > maxValue) {
                    maxValue = res.data.p2p[0].datapoints[j][0]
                  }
                  this.validData.push(res.data.p2p[0].datapoints[j])
                }
                this.validData.reverse()
                day1 = (this.validData[this.validData.length - 1][1] - this.validData[0][1]) / 3600
                this.myOption.series.push({
                  type: 'line',
                  name: '点对点会议',
                  symbol: 'none',
                  data: this.validData.map(function(value) {
                    return {value: [value[1] * 1000, value[0]]};
                  }),
                  itemStyle: {
                    color: '#5eb9ef'
                  },
                  areaStyle: {
                    color: '#CCFFFF',
                    origin: 'start',
                  },
                })
                this.myOption.legend.data.push({
                  name: '点对点会议',
                  icon: 'rect'
                })
              }
              if (res.data.multi.length > 0) {
                this.validData = []
                for (var x = res.data.multi[0].datapoints.length - 1; x >= 0; x--) {
                  if (res.data.multi[0].datapoints[x][0] === null) {
                    continue
                  }
                  if (res.data.multi[0].datapoints[x][0] > maxValue) {
                    maxValue = res.data.multi[0].datapoints[x][0]
                  }
                  this.validData.push(res.data.multi[0].datapoints[x])
                }
                this.validData.reverse()
                day2 = (this.validData[this.validData.length - 1][1] - this.validData[0][1]) / 3600
                this.myOption.series.push({
                  type: 'line',
                  name: '多点会议',
                  symbol: 'none',
                  data: this.validData.map(function(value) {
                    return {value: [value[1] * 1000, value[0]]};
                  }),
                  itemStyle: {
                    color: '#09a206'
                  },
                  areaStyle: {
                    color: '#CCFFCC',
                    origin: 'start',
                  },
                })
                this.myOption.legend.data.push({
                  name: '多点会议',
                  icon: 'rect'
                })
              }
              let maxLength = String(maxValue).length
              this.myOption.yAxis.max = Math.pow(10, maxLength)
              this.myOption.yAxis.interval = parseInt(parseFloat(Math.pow(10, maxLength) / 2).toFixed(0))
              if (day1 <= 24 && day2 <= 24) {
                this.myOption.xAxis.axisLabel.formatter = function (value, index) {
                  var date = new Date(value);
                  return date.toTimeString().substr(0, 5);
                }
              } else {
                this.myOption.xAxis.axisLabel.formatter = function (value, index) {
                  return FormatDate(value)
                }
              }
            }
            this.$nextTick(() => {
              this.myChart = this.$echarts.init(document.getElementById('MeetingNumChart'));
              document.getElementById("MeetingNum").style.display = "none";
              document.getElementById("MeetingNumChart").style.display = "block";
              setMyOption(this.$echarts, 'MeetingNumChart', this.myOption)
              this.picInfo = this.myChart.getDataURL()
            })
          })
        } else if (newTab === "warningCount") {
          document.getElementById("CountWarning").style.display = "block";
          // 获取告警统计图表
          api.getWarningStatisticData({params: {parentMoid: 'all', startTime: '-1w', stopTime: ''}}).then(res => {
            console.log(res)
            this.myOption.yAxis.name = '个'
            this.myOption.yAxis.max = 10
            this.myOption.yAxis.interval = 5
            this.myOption.series = []
            this.myOption.legend.data = []
            this.validData = []
            if (res.success == 1) {
              var day1 = 0
              var day2 = 0
              var maxValue = 0
              if (res.data.server.length > 0) {
                for (var j = res.data.server[0].datapoints.length - 1; j >= 0; j--) {
                  if (res.data.server[0].datapoints[j][0] === null) {
                    continue
                  }
                  if (res.data.server[0].datapoints[j][0] > maxValue) {
                    maxValue = res.data.server[0].datapoints[j][0]
                  }
                  this.validData.push(res.data.server[0].datapoints[j])
                }
                this.validData.reverse()
                day1 = (this.validData[this.validData.length - 1][1] - this.validData[0][1]) / 3600
                this.myOption.series.push({
                  type: 'line',
                  name: '服务器告警',
                  symbol: 'none',
                  data: this.validData.map(function(value) {
                    return {value: [value[1] * 1000, value[0]]};
                  }),
                  itemStyle: {
                    color: '#5eb9ef'
                  },
                  areaStyle: {
                    color: '#CCFFFF',
                    origin: 'start',
                  },
                })
                this.myOption.legend.data.push({
                  name: '服务器告警',
                  icon: 'rect'
                })
              }
              if (res.data.terminal.length > 0) {
                this.validData = []
                for (var x = res.data.terminal[0].datapoints.length - 1; x >= 0; x--) {
                  if (res.data.terminal[0].datapoints[x][0] === null) {
                    continue
                  }
                  if (res.data.terminal[0].datapoints[x][0] > maxValue) {
                    maxValue = res.data.terminal[0].datapoints[x][0]
                  }
                  this.validData.push(res.data.terminal[0].datapoints[x])
                }
                this.validData.reverse()
                day2 = (this.validData[this.validData.length - 1][1] - this.validData[0][1]) / 3600
                this.myOption.series.push({
                  type: 'line',
                  name: '终端告警',
                  symbol: 'none',
                  data: this.validData.map(function(value) {
                    return {value: [value[1] * 1000, value[0]]};
                  }),
                  itemStyle: {
                    color: '#09a206'
                  },
                  areaStyle: {
                    color: '#CCFFCC',
                    origin: 'start',
                  },
                })
                this.myOption.legend.data.push({
                  name: '终端告警',
                  icon: 'rect'
                })
              }
              let maxLength = String(maxValue).length
              this.myOption.yAxis.max = Math.pow(10, maxLength)
              this.myOption.yAxis.interval = parseInt(parseFloat(Math.pow(10, maxLength) / 2).toFixed(0))
              if (day1 <= 24 && day2 <= 24) {
                this.myOption.xAxis.axisLabel.formatter = function (value, index) {
                  var date = new Date(value);
                  return date.toTimeString().substr(0, 5);
                }
              } else {
                this.myOption.xAxis.axisLabel.formatter = function (value, index) {
                  return FormatDate(value)
                }
              }
            }
            this.$nextTick(() => {
              this.myChart = this.$echarts.init(document.getElementById('CountWarningChart'));
              document.getElementById("CountWarning").style.display = "none";
              document.getElementById("CountWarningChart").style.display = "block";
              setMyOption(this.$echarts, 'CountWarningChart', this.myOption)
              this.picInfo = this.myChart.getDataURL()
            })
          })
        }
      },
      startDate: function(newTime, oldTime) {
        if ((this.endDate - newTime) < 0 && this.endDate !== null && FormatTime(newTime).substr(0, 10) !== FormatTime(this.endDate).substr(0, 10)) {
          this.startDate = oldTime
          this.errorDialog.open('起始时间不得超过截至时间')
          this.reSet = false
          this.$nextTick(() => {
            this.reSet = true
          })
        }
        if (this.detailType == 'meetingAppoint') {
          var nowtime = new Date()
          if ((this.startDate - nowtime) < 0 && FormatTime(nowtime).substr(0, 10) !== FormatTime(this.startDate).substr(0, 10)) {
            this.startDate = oldTime
            this.errorDialog.open('预约会议起始时间不得小于当前时间')
            this.reSet = false
            this.$nextTick(() => {
              this.reSet = true
            })
          }
        }
      },
      endDate: function(newTime, oldTime) {
        if ((newTime - this.startDate) < 0 && FormatTime(newTime).substr(0, 10) !== FormatTime(this.startDate).substr(0, 10)) {
          this.endDate = oldTime
          this.errorDialog.open('截至时间不得小于起始时间')
          this.reSet = false
          this.$nextTick(() => {
            this.reSet = true
          })
        }
      },
      // 下拉框服务域选择
      tTerminalDomainMoid: function(newDomain, oldDomain) {
        let userCount = 0
        if (newDomain == 'all') {
          this.tUserMoids = []
          this.warningUesrDomains.forEach(item => {
            if (item.type === "user") {
              this.tUserMoids.unshift(item)
              userCount++
            }
          })
          if (userCount == 0) {
            this.tUserMoids.unshift({
              "moid": "",
              "parent_moid": "",
              "name": "无下级域",
              "type": "user"
            })
            this.tUserMoid = ''
          } else {
            this.tUserMoids.unshift({
              "moid": "all",
              "parent_moid": "",
              "name": "所有用户域",
              "type": "user"
            })
            this.tUserMoid = 'all'
          }
        } else {
          let kernel = 0
          this.warningUesrDomains.forEach(domain => {
            if (domain.moid === newDomain && domain.type === 'kernel') {
              kernel = 1
            }
          })
          if (kernel == 0) {
            this.tUserMoids = []
            this.warningUesrDomains.forEach(user => {
              if (user.parent_moid === newDomain && user.type === 'user') {
                this.tUserMoids.push(user)
                userCount++
              }
            })
            if (userCount == 0) {
              this.tUserMoids.unshift({
                "moid": "",
                "parent_moid": "",
                "name": "无下级域",
                "type": "user"
              })
              this.tUserMoid = ''
            } else {
              this.tUserMoids.unshift({
                "moid": "all",
                "parent_moid": "",
                "name": "所有用户域",
                "type": "user"
              })
              this.tUserMoid = 'all'
            }
          } else {
            this.tUserMoids = []
            this.warningUesrDomains.forEach(item => {
              if (item.type === "user") {
                this.tUserMoids.unshift(item)
                userCount++
              }
            })
            if (userCount == 0) {
              this.tUserMoids.unshift({
                "moid": "",
                "parent_moid": "",
                "name": "无下级域",
                "type": "user"
              })
              this.tUserMoid = ''
            } else {
              this.tUserMoids.unshift({
                "moid": "all",
                "parent_moid": "",
                "name": "所有用户域",
                "type": "user"
              })
              this.tUserMoid = 'all'
            }
          }
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
    }
  }
</script>

<style scoped>
  /deep/ .el-tabs__content{
    width: 100%;
  }
  .detail-style {
    display: block;
  }
  .detail-back {
    width: 100%;
    float: left;
  }
  .detail-line {
    width: 100%;
    float: left;
  }
  .detail-tab{
    margin-top: 20px;
  }
  .timeSelect /deep/ .el-input{
    width: 95px;
  }
  /deep/ .el-tabs__item {
    height: 22px;
    line-height: 22px;
    font-size: 12px;
    font-weight: 500;
    position: relative;
    background-color: #373d41
  }
  /deep/ .el-tabs__item.is-active {
    /* color: #409EFF; */
    background-color: #53afe4;
    font-weight: 550;
  }
  /deep/ .el-tabs__nav-scroll{
    margin-bottom: 10px;
  }
  .base-info-title{
    font-size: 15px;
    font-weight: 550;
  }
  .detail-div-pie{
    float: left;
    width: 100%;
  }
  .detail-div{
    float: left;
  }
  .detail-select{
    margin-right: 16px;
    float: left;
    padding-top: 6px;
  }
  .detail-select-last{
    float: left;
    padding-top: 6px;
  }
  .detail-item{
    float: left;
    margin-bottom: 4px;
    width: 100%
  }
  .detail-chart{
    float: left;
    width: 100%;
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
  .circle-info-detail {
    float: left;
  }
  .circle-title{
    padding-top: 11px;
    padding-bottom: 8px;
    font-size: 13px;
    width: 100%;
    text-align: left;
    color: #000000;
    margin-left: 12px;
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
  .res-chart-hide{
    margin-top: 10px;
    height: 320px;
    display: none;
    width: 900px;
  }
  .res-chart-show{
    margin-top: 100px;
    text-align: center;
    height: 320px;
    font-size: 13px;
    display: none;
    width: 900px;
  }
.info {
    display: inline-block;
    width: 15px;
    height: 15px;
    cursor: pointer;
    background-image: url(../../assets/image/detail.png);
    margin-left: 11px;
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
</style>
