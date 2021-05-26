<template>
  <div class="chart-all">
    <div class="chart-block">
      <div class="chart-item">
        <span class="chart-title">今日会议质量</span>
      </div>
      <div class="chart-line">
        <div class="chart-pie" id="meetingState"/>
        <div class="chart-pie-detail">
          <span class="pie-number">{{ StartMeetingNum }}</span>
          <span class="pie-detail">正召开的会议</span>
          <span class="pie-number">{{ EndMeetingNum }}</span>
          <span class="pie-detail">已结束的会议</span>
        </div>
      </div>
    </div>
    <div class="chart-block">
      <div class="chart-item">
        <span class="chart-title">会议资源</span>
        <a class="chart-detail" @click="chartDetail('meetingResource')">更多</a>
      </div>
      <div class="chart-line">
        <div class="chart-circle-info">
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
          <div class="chart-circle" style="margin: 0 40px;">
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
        </div>
      </div>
    </div>

    <div class="chart-block">
      <div class="chart-item">
        <span class="chart-title">预约会议</span>
        <a class="chart-detail" @click="chartDetail('meetingAppoint')">更多</a>
      </div>
      <div class="chart-line">
        <div class="res-chart" id="appointChart"/>
      </div>
    </div>
    <div class="chart-block">
      <div class="chart-item">
        <span class="chart-title-short">告警统计</span>
        <div class="chart-title-tips">
          <span class="bluediv"></span>
          <span class="tips">服务器告警</span>
        </div>
        <div class="chart-title-tipslast">
          <div class="greendiv"></div>
          <span class="tips">终端告警</span>
        </div>
        <a class="chart-detail" @click="chartDetail('warningCount')">更多</a>
      </div>
      <div class="chart-line">
        <div class="res-chart" id="warnCountChart"/>
      </div>
    </div>
    <div class="chart-block">
      <div class="chart-item">
        <el-tabs class="chart-tabs" v-model="HardwareUse" @tab-click="HardwareClick">
          <el-tab-pane label="CPU使用率" name="cpuUse"></el-tab-pane>
          <el-tab-pane label="内存使用率" name="memoryUse"></el-tab-pane>
          <el-tab-pane label="磁盘使用寿命" name="diskAge"></el-tab-pane>
          <el-tab-pane label="磁盘使用率" name="diskUse"></el-tab-pane>
        </el-tabs>
        <a class="chart-detail" @click="chartDetail('hardWare')">更多</a>
      </div>
      <div class="chart-line">
        <div class="res-chart" id="cpuUsingChart"/>
        <div class="res-chart-hide" id="memoryUsingChart"/>
        <div class="res-chart-hide" id="diskAgeChart"/>
        <div class="res-chart-hide" id="diskUseChart"/>
      </div>
    </div>
    <div class="chart-block">
      <div class="chart-item">
        <el-tabs class="chart-tabs" v-model="BandWidth"  @tab-click="BandWidthClick">
          <el-tab-pane label="上行带宽" name="upBandWidth"></el-tab-pane>
          <el-tab-pane label="下行带宽" name="downBandWidth"></el-tab-pane>
        </el-tabs>
        <a class="chart-detail" @click="chartDetail('bandWidth')">更多</a>
      </div>
      <div class="chart-line">
        <div class="res-chart" id="upBandWidthChart"/>
        <div class="res-chart-hide" id="downBandWidthChart"/>
      </div>
    </div>
    <div class="chart-block">
      <div class="chart-item">
        <span class="chart-title-short">会议数量</span>
        <div class="chart-title-tips">
          <span class="bluediv"></span>
          <span class="tips">点对点会议</span>
        </div>
        <div class="chart-title-tipslast">
          <div class="greendiv"></div>
          <span class="tips">多点会议</span>
        </div>
        <a class="chart-detail" @click="chartDetail('meetingNum')">更多</a>
      </div>
      <div class="chart-line">
        <div class="res-chart" id="meetingNumChart"></div>
      </div>
    </div>
    <div class="chart-block">
      <div class="chart-item">
        <el-tabs class="chart-tabs-short" v-model="DomainUse" @tab-click="DomainClick">
          <el-tab-pane label="服务器数量" name="serviceUse"></el-tab-pane>
          <el-tab-pane label="终端数量" name= "deviceUse"></el-tab-pane>
        </el-tabs>
        <div class="chart-title-tipsonline" v-show="DomainUse=='serviceUse'">
          <span class="bluediv"></span>
          <span class="tips">在线</span>
        </div>
        <div class="chart-title-tipsoffline"  v-show="DomainUse=='serviceUse'">
          <div class="greendiv"></div>
          <span class="tips">离线</span>
        </div>
        <div class="chart-title-tipslinefirst"  v-show="DomainUse=='deviceUse'">
          <span class="bluediv"></span>
          <span class="tips">在线终端</span>
        </div>
        <div class="chart-title-tipsline"  v-show="DomainUse=='deviceUse'">
          <div class="greendiv"></div>
          <span class="tips">与会终端</span>
        </div>
        <a class="chart-detail" @click="chartDetail('domainUse')">更多</a>
      </div>
      <div class="chart-line">
        <div class="res-chart" id="serviceChart"></div>
        <div class="res-chart-hide" id="deviceChart"></div>
      </div>
    </div>
    <div class="chart-list">
      <div class="list-item">
        <el-tabs class="list-tabs" v-model="DomainWarn">
          <el-tab-pane label="服务器告警" name="serviceWarn"></el-tab-pane>
          <el-tab-pane label="终端告警" name="deviceWarn"></el-tab-pane>
        </el-tabs>
        <a class="chart-detail" @click="chartDetail('domainWarn')">更多</a>
      </div>
      <div class="list-line">
        <div class="list-warn" v-if="DomainWarn=='serviceWarn'">
          <nms-pager-table v-if='serverWarningList.length != 0' :data="serverWarningList" :fields="serverWarningFields" :pager="false"/>
          <div class="war-info-tip" v-if='serverWarningList.length == 0'>
            <span class="PromptImg"></span>
            <span>当前没有该级别未修复的服务器告警</span>
          </div>
        </div>
        <div class="list-warn" v-if="DomainWarn=='deviceWarn'">
          <nms-pager-table v-if='terminalWarningList.length != 0' :data="terminalWarningList" :fields="terminalWarningFields" :pager="false"/>
          <div class="war-info-tip" v-if='terminalWarningList.length == 0'>
            <span class="PromptImg"></span>
            <span>当前没有该级别未修复的终端告警</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import ResUsageCircle from "../common/res-usage-circle";
  import api from '../../axios'
  import {FormatTime, FormatTerminalTime, KeepTwoNum} from "../../assets/js/common";
  import {setMyOption, getServerWarningTblFields, getTerminalWarningTblFields} from 'assets/js/baseinfo'
  import NmsPagerTable from "../common/nms-pager-table";

  export default {
    components: {
      NmsPagerTable,
      ResUsageCircle,
    },
    name: "base-info",
    data() {
      return {
        screenWidth: document.body.clientWidth,
        deviceUse: false,
        pic: null,
        timer: '',
        graphite_data: [],
        graphite_url: '',
        graphite_time: '',
        graphite_target: '',
        graphite_format: '&format=json',
        from_time: '-62min',
        until_time: '',
        // 告警级别
        serverWarningLevel: [],
        terminalWarningLevel: [],
        server_criticalLevel: '',
        server_importantLevel: '',
        server_normalLevel: '',
        terminal_criticalLevel: '',
        terminal_importantLevel: '',
        terminal_normalLevel: '',
        // 标题栏选择项
        HardwareUse: 'cpuUse',
        BandWidth: 'upBandWidth',
        DomainUse: 'serviceUse',
        DomainWarn: 'serviceWarn',
        // 会议使用总量
        generalFeeling: 0,
        goodFeeling: 0,
        greatFeeling: 0,
        badFeeling: 0,
        StartMeetingNum: 0,
        EndMeetingNum: 0,
        // 告警列表
        serverWarningList: [],
        serverWarningFields: [],
        terminalWarningList: [],
        terminalWarningFields: [],
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
        // 图表数据
        cpuValue: [],
        myOption: {
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
          backgroundColor: 'rgb(256,256,256)',
          grid: {
            top: 30,
            bottom: 0,
            containLabel: true
          },
          tooltip: {
            trigger: 'axis',
            textStyle: {
              align: 'left',
            },
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
            bottom: 0,
            itemGap: 5,
            itemWidth: 10,
            itemHeight: 6,
            textStyle: {
              fontSize: 10,
            },
            formatter: function(name) {
              return name.length > 15 ? name.substr(0, 12) + "..." : name;
            },
            data: [],
          }
        },
        legendColor: ['#5eb9ef', '#09a206', '#f78600', '#db4c4c', '#ac5af2'],
        validData: [],
        meetingQualityOption: {
          // 注记显示手柄
          calculable: true,
          backgroundColor: 'rgb(256,256,256)',
          // 图形系列
          series: [
            {
                zlevel: 10,
                name: '今日会议质量',
                type: 'pie',
                radius: ['16%', '60%'],
                label: {
                  normal: {
                      fontSize: 13,
                      color: "#4e4e4e",
                  }
                },
                data: [
                ],
                labelLine: {
                  normal: {
                    length: 5
                  }
                }
            },
            {
              zlevel: 1,
              type: 'pie',
              radius: ['68%', '70%'],
              hoverAnimation: false,
              label: {
                normal: {
                    position: 'center',
                }
              },
              data: [
                { value: 25 },
              ],
              color: "#e8e8e8",
            },
            {
              zlevel: 2,
              type: 'pie',
              radius: ['8%', '20%'],
              hoverAnimation: false,
              label: {
                normal: {
                    position: 'center',
                }
              },
              data: [
                { value: 25 },
              ],
              color: "#F8F8FF",
            },
            {
              zlevel: 2,
              type: 'pie',
              radius: ['0%', '8%'],
              hoverAnimation: false,
              label: {
                normal: {
                    position: 'center',
                }
              },
              data: [
                { value: 25 },
              ],
              color: "#ffffff",
            },
          ],
          // 颜色调整
          color: ['#3fadef', '#b6d5e7', '#85cdf8', '#5eb9ef']
        }
      }
    },
    activated: function () {
      this.$nextTick(() => {
        this.CurentTime()
      })
      this.timer = setInterval(this.CurentTime, 180000);
      // 获取首页未修复告警
      api.getServerUnrepairedWarning().then(res => {
        console.log(res)
        if (res.success == 1) {
          if (res.data.length === 0) {
            this.serverWarningFields = []
            this.serverWarningList = []
          } else {
            this.serverWarningFields = getServerWarningTblFields()
            this.serverWarningList = res.data
          }
        }
      })
    },
    mounted: function () {
      this.$once('hook:beforeDestroy', () => {
        clearInterval(this.timer)
      })
    },
    methods: {
      DomainClick: function () {
        if (this.DomainUse === "serviceUse") {
          document.getElementById("deviceChart").style.display = "none";
          document.getElementById("serviceChart").style.display = "block";
        } else if (this.DomainUse === "deviceUse") {
          document.getElementById("serviceChart").style.display = "none";
          document.getElementById("deviceChart").style.display = "block";
        }
      },
      BandWidthClick: function () {
        if (this.BandWidth === "upBandWidth") {
          document.getElementById("downBandWidthChart").style.display = "none";
          document.getElementById("upBandWidthChart").style.display = "block";
        } else if (this.BandWidth === "downBandWidth") {
          document.getElementById("upBandWidthChart").style.display = "none";
          document.getElementById("downBandWidthChart").style.display = "block";
        }
      },
      HardwareClick: function () {
        if (this.HardwareUse === 'cpuUse') {
          document.getElementById("memoryUsingChart").style.display = "none";
          document.getElementById("diskAgeChart").style.display = "none";
          document.getElementById("diskUseChart").style.display = "none";
          document.getElementById("cpuUsingChart").style.display = "block";
        } else if (this.HardwareUse === 'memoryUse') {
          document.getElementById("cpuUsingChart").style.display = "none";
          document.getElementById("diskAgeChart").style.display = "none";
          document.getElementById("diskUseChart").style.display = "none";
          document.getElementById("memoryUsingChart").style.display = "block";
        } else if (this.HardwareUse === 'diskAge') {
          document.getElementById("cpuUsingChart").style.display = "none";
          document.getElementById("memoryUsingChart").style.display = "none";
          document.getElementById("diskUseChart").style.display = "none";
          document.getElementById("diskAgeChart").style.display = "block";
        } else if (this.HardwareUse === 'diskUse') {
          document.getElementById("cpuUsingChart").style.display = "none";
          document.getElementById("memoryUsingChart").style.display = "none";
          document.getElementById("diskAgeChart").style.display = "none";
          document.getElementById("diskUseChart").style.display = "block";
        }
      },
      chartDetail: function (data) {
        clearInterval(this.timer)
        console.log(data)
        if (data === 'domainWarn') {
          // 跳转后给设备告警目录标签添加一个模拟鼠标点击操作
          // document.getElementById("btn").click();
          if (this.DomainWarn === 'serviceWarn') {
            this.$router.push({
              name: 'unrepairedwarninginfo',
              params: {
                warningType: 'serverWarning'
              }
            })
          } else if (this.DomainWarn === 'deviceWarn') {
            this.$router.push({
              name: 'unrepairedwarninginfo',
              params: {
                warningType: 'terminalWarning'
              }
            })
          }
        } else if (data === 'hardWare') {
        //  document.getElementById("deviceInfo").click();
          this.$router.push({
            name: 'platformdeviceinfohome',
            params: {
            }
          })
        } else if (data === 'bandWidth') {
        //  document.getElementById("deviceInfo").click();
          this.$router.push({
            name: 'platformdeviceinfohome',
            params: {
            }
          })
        } else if (data === 'domainUse' && this.DomainUse === 'deviceUse') {
          this.$router.push({
            name: "baseinfosearch",
            params: {detailType: 'terminalUse'}
          })
        } else {
          this.$router.push({
            name: "baseinfosearch",
            params: {detailType: data}
          })
        }
      },
      CurentTime: function() {
        api.getMeetingQualityData().then(res => {
          console.log(res)
          this.meetingQualityOption.series[0].data = []
          if (res.success == 1 && JSON.stringify(res.data) !== '{}') {
            this.StartMeetingNum = res.data.realMeeting
            this.EndMeetingNum = res.data.historyMeeting
            this.greatFeeling = res.data.goodQality
            this.goodFeeling = res.data.betterQality
            this.generalFeeling = res.data.normalQality
            this.badFeeling = res.data.worseQality
            var totalNum = this.greatFeeling + this.goodFeeling + this.generalFeeling + this.badFeeling
            var Apercent = 0
            var Bpercent = 0
            var Cpercent = 0
            var Dpercent = 0
            if ((totalNum !== 0)) {
              Apercent = parseFloat(100 * this.greatFeeling / totalNum).toFixed(0)
              if (Apercent !== '0') {
                this.meetingQualityOption.series[0].data.push({ value: this.greatFeeling, name: ("体验优秀 " + Apercent + '%') })
              }
              Cpercent = parseFloat(100 * this.badFeeling / totalNum).toFixed(0)
              if (Cpercent !== '0') {
                this.meetingQualityOption.series[0].data.push({ value: this.badFeeling, name: ("体验不好 " + Cpercent + '%') })
              }
              Dpercent = parseFloat(100 * this.generalFeeling / totalNum).toFixed(0)
              if (Dpercent !== '0') {
                this.meetingQualityOption.series[0].data.push({ value: this.generalFeeling, name: ("体验一般 " + Dpercent + '%') })
              }
              Bpercent = parseFloat(100 * this.goodFeeling / totalNum).toFixed(0)
              if (Bpercent !== '0') {
                this.meetingQualityOption.series[0].data.push({ value: this.goodFeeling, name: ("体验良好 " + Bpercent + '%') })
              }
            }
          }
          this.$nextTick(() => {
            setMyOption(this.$echarts, 'meetingState', this.meetingQualityOption)
          })
        })
        // 会议资源获取接口
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
          }
        })
        var appointStopTime = FormatTime(new Date())
        var appointStartTime = FormatTime(new Date())
        // 获取预约会议图表
        api.getAppointMeetingData({params: {parentMoid: 'all', startTime: appointStartTime, stopTime: appointStopTime}}).then(res => {
          console.log(res)
          this.myOption.yAxis.name = '个'
          this.myOption.yAxis.max = 10
          this.myOption.yAxis.interval = 5
          this.myOption.grid.bottom = 45
          this.myOption.series = []
          this.myOption.legend.data = []
          this.validData = []
          if (res.success == 1) {
            var maxValue = 0
            if (res.datapoints.length > 0) {
              this.myOption.grid.bottom = 10
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
              this.myOption.xAxis.axisLabel.formatter = function (value, index) {
                var date = new Date(value);
                return date.toTimeString().substr(0, 5);
              }
            }
          }
          this.$nextTick(() => {
            setMyOption(this.$echarts, 'appointChart', this.myOption)
          })
        })
        // 获取告警统计图表
        api.getWarningStatisticData({params: {parentMoid: 'all', startTime: this.from_time, stopTime: this.until_time}}).then(res => {
          console.log(res)
          this.myOption.yAxis.name = '个'
          this.myOption.yAxis.max = 10
          this.myOption.yAxis.interval = 5
          this.myOption.grid.bottom = 45
          this.myOption.series = []
          this.myOption.legend.data = []
          this.validData = []
          if (res.success == 1) {
            var maxValue = 0
            if (res.data.server.length > 0) {
              this.myOption.grid.bottom = 10
              for (var j = res.data.server[0].datapoints.length - 1, k = 0; j >= 0 && k < 60; j--) {
                if (res.data.server[0].datapoints[j][0] === null) {
                  continue
                }
                if (res.data.server[0].datapoints[j][0] > maxValue) {
                  maxValue = res.data.server[0].datapoints[j][0]
                }
                this.validData.push(res.data.server[0].datapoints[j])
                k++
              }
              this.validData.reverse()
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
            }
            if (res.data.terminal.length > 0) {
              this.myOption.grid.bottom = 10
              this.validData = []
              for (var x = res.data.terminal[0].datapoints.length - 1, y = 0; x >= 0 && y < 60; x--) {
                if (res.data.terminal[0].datapoints[x][0] === null) {
                  continue
                }
                if (res.data.terminal[0].datapoints[x][0] > maxValue) {
                  maxValue = res.data.terminal[0].datapoints[x][0]
                }
                this.validData.push(res.data.terminal[0].datapoints[x])
                y++
              }
              this.validData.reverse()
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
            }
            let maxLength = String(maxValue).length
            this.myOption.yAxis.max = Math.pow(10, maxLength)
            this.myOption.yAxis.interval = parseInt(parseFloat(Math.pow(10, maxLength) / 2).toFixed(0))
            this.myOption.xAxis.axisLabel.formatter = function (value, index) {
              var date = new Date(value);
              return date.toTimeString().substr(0, 5);
            }
          }
          this.$nextTick(() => {
            setMyOption(this.$echarts, 'warnCountChart', this.myOption)
          })
        })
        // 获取会议统计
        api.getMeetingStatisticData({params: {parentMoid: 'all', startTime: this.from_time, stopTime: this.until_time}}).then(res => {
          console.log(res)
          this.myOption.series = []
          this.myOption.legend.data = []
          this.validData = []
          this.myOption.grid.bottom = 45
          this.myOption.yAxis.name = '个'
          this.myOption.yAxis.max = 10
          this.myOption.yAxis.interval = 5
          if (res.success == 1) {
            var maxValue = 0
            if (res.data.p2p.length > 0) {
              this.myOption.grid.bottom = 10
              for (var j = res.data.p2p[0].datapoints.length - 1, k = 0; j >= 0 && k < 60; j--) {
                if (res.data.p2p[0].datapoints[j][0] === null) {
                  continue
                }
                if (res.data.p2p[0].datapoints[j][0] > maxValue) {
                  maxValue = res.data.p2p[0].datapoints[j][0]
                }
                this.validData.push(res.data.p2p[0].datapoints[j])
                k++
              }
              this.validData.reverse()
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
            }
            if (res.data.multi.length > 0) {
              this.myOption.grid.bottom = 10
              this.validData = []
              for (var x = res.data.multi[0].datapoints.length - 1, y = 0; x >= 0 && y < 60; x--) {
                if (res.data.multi[0].datapoints[x][0] === null) {
                  continue
                }
                if (res.data.multi[0].datapoints[x][0] > maxValue) {
                  maxValue = res.data.multi[0].datapoints[x][0]
                }
                this.validData.push(res.data.multi[0].datapoints[x])
                y++
              }
              this.validData.reverse()
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
            }
            let maxLength = String(maxValue).length
            this.myOption.yAxis.max = Math.pow(10, maxLength)
            this.myOption.yAxis.interval = parseInt(parseFloat(Math.pow(10, maxLength) / 2).toFixed(0))
            this.myOption.xAxis.axisLabel.formatter = function (value, index) {
              var date = new Date(value);
              return date.toTimeString().substr(0, 5);
            }
          }
          this.$nextTick(() => {
            setMyOption(this.$echarts, 'meetingNumChart', this.myOption)
          })
        })
        // 获取服务器数量图表
        api.getServerStatisticData({params: {parentMoid: 'all', startTime: this.from_time, stopTime: this.until_time}}).then(res => {
          console.log(res)
          this.myOption.series = []
          this.myOption.legend.data = []
          this.myOption.grid.bottom = 45
          this.myOption.yAxis.name = '个'
          this.myOption.yAxis.max = 10
          this.myOption.yAxis.interval = 5
          this.validData = []
          if (res.success == 1) {
            var maxValue = 0
            if (res.data.online.length > 0) {
              this.myOption.grid.bottom = 10
              for (var j = res.data.online[0].datapoints.length - 1, k = 0; j >= 0 && k < 60; j--) {
                if (res.data.online[0].datapoints[j][0] === null) {
                  continue
                }
                if (res.data.online[0].datapoints[j][0] > maxValue) {
                  maxValue = res.data.online[0].datapoints[j][0]
                }
                this.validData.push(res.data.online[0].datapoints[j])
                k++
              }
              this.validData.reverse()
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
            }
            if (res.data.offline.length > 0) {
              this.myOption.grid.bottom = 10
              this.validData = []
              for (var x = res.data.offline[0].datapoints.length - 1, y = 0; x >= 0 && y < 60; x--) {
                if (res.data.offline[0].datapoints[x][0] === null) {
                  continue
                }
                if (res.data.offline[0].datapoints[x][0] > maxValue) {
                  maxValue = res.data.offline[0].datapoints[x][0]
                }
                this.validData.push(res.data.offline[0].datapoints[x])
                y++
              }
              this.validData.reverse()
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
            }
            let maxLength = String(maxValue).length
            this.myOption.yAxis.max = Math.pow(10, maxLength)
            this.myOption.yAxis.interval = parseInt(parseFloat(Math.pow(10, maxLength) / 2).toFixed(0))
            this.myOption.xAxis.axisLabel.formatter = function (value, index) {
              var date = new Date(value);
              return date.toTimeString().substr(0, 5);
            }
          }
          this.$nextTick(() => {
            setMyOption(this.$echarts, 'serviceChart', this.myOption)
          })
        })
        // 获取终端数量图表
        api.getTerminalStatisticData({params: {parentMoid: 'all', startTime: this.from_time, stopTime: this.until_time}}).then(res => {
          console.log(res)
          this.myOption.series = []
          this.myOption.legend.data = []
          this.validData = []
          var terminalOption = {
            backgroundColor: 'rgb(256,256,256)',
            yAxis: {
              name: '个',
              min: 0,
              max: 10,
              interval: 5,
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
              top: 28,
              bottom: 45,
              containLabel: true
            },
            tooltip: {
              trigger: 'axis',
              textStyle: {
                align: 'left',
              },
              formatter: function (params) {
                if (params.length == 2) {
                  let html = FormatTerminalTime(params[0].value[0]) + "<br>";
                  html += '<span style="display:inline-block;margin-right:5px;border-radius:10px;width:10px;height:10px;background-color:' + '#5eb9ef' + ';"></span>'
                  html += params[0].seriesName + ": " + params[0].value[1] + "<br>"
                  let onlinepercent = 0
                  if (params[0].value[2] == 0) {
                    onlinepercent = 0
                  } else {
                    onlinepercent = parseFloat(100 * params[0].value[1] / params[0].value[2]).toFixed(0)
                  }
                  html += '在线百分比' + ": " + onlinepercent + "%<br>"

                  html += '<span style="display:inline-block;margin-right:5px;border-radius:10px;width:10px;height:10px;background-color:' + '#09a206' + ';"></span>'
                  html += params[1].seriesName + ": " + params[1].value[1] + "<br>";
                  let meetingpercent = 0
                  if (params[0].value[1] == 0) {
                    meetingpercent = 0
                  } else {
                    meetingpercent = parseFloat(100 * params[1].value[1] / params[0].value[1]).toFixed(0)
                  }
                  html += '与会百分比' + ": " + meetingpercent + "%<br>";
                  return html;
                }
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
              bottom: 0,
              itemGap: 5,
              itemWidth: 11,
              itemHeight: 6,
              data: [],
            }
          }
          if (res.success == 1) {
            var maxValue = 0
            if (res.data.online.length > 0) {
              terminalOption.grid.bottom = 10
              for (var j = res.data.online[0].datapoints.length - 1, k = 0; j >= 0 && k < 60; j--) {
                if (res.data.online[0].datapoints[j][0] === null) {
                  continue
                }
                if (res.data.online[0].datapoints[j][0] > maxValue) {
                  maxValue = res.data.online[0].datapoints[j][0]
                }
                if (res.data.allline[0].datapoints[j][0] !== null) {
                  res.data.online[0].datapoints[j].push(res.data.allline[0].datapoints[j][0])
                  this.validData.push(res.data.online[0].datapoints[j])
                  k++
                }
              }
              this.validData.reverse()
              terminalOption.series.push({
                type: 'line',
                name: '在线终端',
                symbol: 'none',
                data: this.validData.map(function(value) {
                  return {value: [value[1] * 1000, value[0], value[2]]};
                }),
                itemStyle: {
                  color: '#5eb9ef'
                },
                areaStyle: {
                  color: '#CCFFFF',
                  origin: 'start',
                },
              })
            }
            if (res.data.meetingline.length > 0) {
              terminalOption.grid.bottom = 10
              this.validData = []
              for (var x = res.data.meetingline[0].datapoints.length - 1, y = 0; x >= 0 && y < 60; x--) {
                if (res.data.meetingline[0].datapoints[x][0] === null) {
                  continue
                }
                if (res.data.meetingline[0].datapoints[x][0] > maxValue) {
                  maxValue = res.data.meetingline[0].datapoints[x][0]
                }
                this.validData.push(res.data.meetingline[0].datapoints[x])
                y++
              }
              this.validData.reverse()
              terminalOption.series.push({
                type: 'line',
                name: '与会终端',
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
            }
            let maxLength = String(maxValue).length
            terminalOption.yAxis.max = Math.pow(10, maxLength)
            terminalOption.yAxis.interval = parseInt(parseFloat(Math.pow(10, maxLength) / 2).toFixed(0))
            terminalOption.xAxis.axisLabel.formatter = function (value, index) {
              var date = new Date(value);
              return date.toTimeString().substr(0, 5);
            }
          }
          this.$nextTick(() => {
            setMyOption(this.$echarts, 'deviceChart', terminalOption)
          })
        })
        // 获取cpu使用率图表
        api.getCpuUsageData().then(res => {
          console.log(res)
          this.myOption.series = []
          this.myOption.legend.data = []
          this.myOption.grid.bottom = 45
          if (res.success == 1) {
            if (res.data.length > 0) {
              for (var i = 0; i < res.data.length; i++) {
                if (res.data[i].name !== '') {
                  this.validData = []
                  for (var j = res.data[i].datapoints.length - 1, k = 0; j >= 0 && k < 60; j--) {
                    if (res.data[i].datapoints[j][0] === null) {
                      continue
                    }
                    this.validData.push(res.data[i].datapoints[j])
                    k++
                  }
                  this.validData.reverse()
                  this.myOption.yAxis.name = '%'
                  this.myOption.yAxis.max = 100
                  this.myOption.yAxis.interval = 50
                  this.myOption.series.push({
                    type: 'line',
                    name: res.data[i].name,
                    symbol: 'none',
                    data: this.validData.map(function(value) {
                      return {value: [value[1] * 1000, value[0]]};
                    }),
                    itemStyle: {
                      color: this.legendColor[i]
                    }
                  })
                  this.myOption.legend.data.push(
                    {
                      name: res.data[i].name,
                      icon: 'rect'
                    },
                  )
                  this.myOption.xAxis.axisLabel.formatter = function (value, index) {
                    var date = new Date(value);
                    return date.toTimeString().substr(0, 5);
                  }
                }
              }
            }
          }
          this.$nextTick(() => {
            setMyOption(this.$echarts, 'cpuUsingChart', this.myOption)
          })
        })
        // 获取内存使用率图表
        api.getMemUsageData().then(res => {
          console.log(res)
          this.myOption.series = []
          this.myOption.legend.data = []
          this.myOption.grid.bottom = 45
          if (res.success == 1) {
            if (res.data.length > 0) {
              for (var i = 0; i < res.data.length; i++) {
                if (res.data[i].name !== '') {
                  this.validData = []
                  for (var j = res.data[i].datapoints.length - 1, k = 0; j >= 0 && k < 60; j--) {
                    if (res.data[i].datapoints[j][0] === null) {
                      continue
                    }
                    this.validData.push(res.data[i].datapoints[j])
                    k++
                  }
                  this.validData.reverse()
                  this.myOption.yAxis.name = '%'
                  this.myOption.yAxis.max = 100
                  this.myOption.yAxis.interval = 50
                  this.myOption.series.push({
                    type: 'line',
                    name: res.data[i].name,
                    symbol: 'none',
                    data: this.validData.map(function(value) {
                      return {value: [value[1] * 1000, value[0]]};
                    }),
                    itemStyle: {
                      color: this.legendColor[i]
                    }
                  })
                  this.myOption.legend.data.push(
                    {
                      name: res.data[i].name,
                      icon: 'rect'
                    },
                  )
                  this.myOption.xAxis.axisLabel.formatter = function (value, index) {
                    var date = new Date(value);
                    return date.toTimeString().substr(0, 5);
                  }
                }
              }
            }
          }
          this.$nextTick(() => {
            setMyOption(this.$echarts, 'memoryUsingChart', this.myOption)
          })
        })
        // 获取上行带宽图表
        api.getNetcardUpData().then(res => {
          console.log(res)
          this.myOption.series = []
          this.myOption.legend.data = []
          this.myOption.grid.bottom = 45
          if (res.success == 1) {
            if (res.data.length > 0) {
              var maxValue = 0
              for (var i = 0; i < res.data.length; i++) {
                if (res.data[i].name !== '') {
                  this.validData = []
                  for (var j = res.data[i].datapoints.length - 1, k = 0; j >= 0 && k < 60; j--) {
                    if (res.data[i].datapoints[j][0] === null) {
                      continue
                    }
                    if (res.data[i].datapoints[j][0] > maxValue) {
                      maxValue = res.data[i].datapoints[j][0]
                    }
                    this.validData.push(res.data[i].datapoints[j])
                    k++
                  }
                  this.validData.reverse()
                  this.myOption.yAxis.name = 'Mbps'
                  if (maxValue <= 1) {
                    this.myOption.yAxis.max = 1
                    this.myOption.yAxis.interval = 0.5
                  } else {
                    let maxLength = String(maxValue).length
                    this.myOption.yAxis.max = Math.pow(10, maxLength)
                    this.myOption.yAxis.interval = parseInt(parseFloat(Math.pow(10, maxLength) / 2).toFixed(0))
                  }
                  this.myOption.series.push({
                    type: 'line',
                    name: res.data[i].name,
                    symbol: 'none',
                    data: this.validData.map(function(value) {
                      return {value: [value[1] * 1000, value[0]]};
                    }),
                    itemStyle: {
                      color: this.legendColor[i]
                    }
                  })
                  this.myOption.legend.data.push(
                    {
                      name: res.data[i].name,
                      icon: 'rect'
                    },
                  )
                  this.myOption.xAxis.axisLabel.formatter = function (value, index) {
                    var date = new Date(value);
                    return date.toTimeString().substr(0, 5);
                  }
                }
              }
            }
          }
          this.$nextTick(() => {
            setMyOption(this.$echarts, 'upBandWidthChart', this.myOption)
          })
        })
        // 获取下行带宽图表
        api.getNetcardDownData().then(res => {
          console.log(res)
          this.myOption.series = []
          this.myOption.legend.data = []
          this.myOption.grid.bottom = 45
          if (res.success == 1) {
            if (res.data.length > 0) {
              var maxValue = 0
              for (var i = 0; i < res.data.length; i++) {
                if (res.data[i].name !== '') {
                  this.validData = []
                  for (var j = res.data[i].datapoints.length - 1, k = 0; j >= 0 && k < 60; j--) {
                    if (res.data[i].datapoints[j][0] === null) {
                      continue
                    }
                    if (res.data[i].datapoints[j][0] > maxValue) {
                      maxValue = res.data[i].datapoints[j][0]
                    }
                    this.validData.push(res.data[i].datapoints[j])
                    k++
                  }
                  this.validData.reverse()
                  this.myOption.yAxis.name = 'Mbps'
                  if (maxValue <= 1) {
                    this.myOption.yAxis.max = 1.0
                    this.myOption.yAxis.interval = 0.5
                  } else {
                    let maxLength = String(maxValue).length
                    this.myOption.yAxis.max = Math.pow(10, maxLength)
                    this.myOption.yAxis.interval = parseInt(parseFloat(Math.pow(10, maxLength) / 2).toFixed(0))
                  }
                  this.myOption.series.push({
                    type: 'line',
                    name: res.data[i].name,
                    symbol: 'none',
                    data: this.validData.map(function(value) {
                      return {value: [value[1] * 1000, value[0]]};
                    }),
                    itemStyle: {
                      color: this.legendColor[i]
                    }
                  })
                  this.myOption.legend.data.push(
                    {
                      name: res.data[i].name,
                      icon: 'rect'
                    },
                  )
                  this.myOption.xAxis.axisLabel.formatter = function (value, index) {
                    var date = new Date(value);
                    return date.toTimeString().substr(0, 5);
                  }
                }
              }
            }
          }
          this.$nextTick(() => {
            setMyOption(this.$echarts, 'downBandWidthChart', this.myOption)
          })
        })
        // 获取磁盘寿命图表
        api.getDiskAgeStatisticData({params: {parentMoid: 'all'}}).then(res => {
          console.log(res)
          if (res.success == 1) {
            var option = {
              backgroundColor: 'rgb(256,256,256)',
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
                  symbolSize: [8, 12],
                  lineStyle: {
                  }
                },
              },
              grid: {
                top: 20,
                bottom: 15,
                containLabel: true
              },
              tooltip: {
                trigger: 'axis',
                textStyle: {
                  align: 'left',
                },
                formatter: function (params) {
                  var tip = '磁盘: ' + params[0].name + '<br/>' + '已消耗: ' + params[0].data + '%';
                  return tip
                }
              },
              series: [
                {
                  name: [],
                  id: [],
                  type: 'bar',
                  data: [],
                  barWidth: 10,
                  itemStyle: {
                    normal: {
                      color: "#0f97e5",

                    }
                  }
                },
              ],
            }
            res.data.forEach(item => {
              option.series[0].name.push(item.name)
              option.series[0].id.push({'total': item.total, 'used': item.used})
              option.series[0].data.push(item.age)
              option.yAxis.data.push(item.name)
            })
            this.$nextTick(() => {
              setMyOption(this.$echarts, 'diskAgeChart', option)
            })
          }
        })
        // 获取磁盘使用率图表
        api.getDiskUsageStatisticData({params: {parentMoid: 'all'}}).then(res => {
          console.log(res)
          if (res.success == 1) {
            var option = {
              backgroundColor: 'rgb(256,256,256)',
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
                textStyle: {
                  align: 'left',
                },
                formatter: function (params) {
                  console.log(params)
                  var tip = '总量: ' + params[0].data.total + 'G' + '<br/>' + '已使用: ' + params[0].data.used + 'G' + '<br/>' + '使用率: ' + params[0].data.value + '%';
                  return tip
                }
              },
              series: [
                {
                  name: [],
                  id: [],
                  type: 'bar',
                  data: [],
                  barWidth: 10,
                  itemStyle: {
                    normal: {
                      color: "#0f97e5",

                    }
                  }
                },
              ],
            }
            res.data.forEach(item => {
              option.series[0].name.push(item.name)
              option.series[0].data.push({value: item.userate, total: item.total, used: item.used})
              option.yAxis.data.push(item.name)
            })
            this.$nextTick(() => {
              setMyOption(this.$echarts, 'diskUseChart', option)
            })
          }
        })
      }
    },
    watch: {
      DomainWarn: function (newTab, oldTab) {
        if (newTab === "serviceWarn") {
          this.serverWarningFields = []
          this.serverWarningList = []
          api.getServerUnrepairedWarning().then(res => {
            console.log(res)
            if (res.success == 1) {
              if (res.data.length === 0) {
                this.serverWarningFields = []
                this.serverWarningList = []
              } else {
                this.serverWarningFields = getServerWarningTblFields()
                this.serverWarningList = res.data
              }
            }
          })
        } else if (newTab === "deviceWarn") {
          this.terminalWarningFields = []
          this.terminalWarningList = []
          api.getTerminalUnrepairedWarning().then(res => {
            console.log(res)
            if (res.success == 1) {
              if (res.data.length === 0) {
                this.terminalWarningFields = []
                this.terminalWarningList = []
              } else {
                this.terminalWarningFields = getTerminalWarningTblFields()
                this.terminalWarningList = res.data
              }
            }
          })
        }
      },
    }
  }
</script>

<style scoped>

  .chart-all {
    width: 100%;
    height: 100%;
  }
  .chart-mid {
    width: 90%;
    height: 90%;
  }
  .chart-block {
    border-style: solid;
    border-width: 1px;
    border-color: #e2e4e6;
    float: left;
    width: 45%;
    height: 20%;
    margin-right: 12px;
    margin-top: 12px;
    text-align:center
  }
  .chart-list {
    border-style: solid;
    border-width: 1px;
    border-color: #e2e4e6;
    float: left;
    width: 91%;
    height: 263px;
    margin-top: 12px;
  }
  .chart-title {
    height: 40px;
    width: 94%;
    font-size: 12px;
    font-weight: 550;
    margin-top: 5px;
    display: block;
    text-align:left;
    padding-left: 20px;
  }
  .chart-title-short{
    float: right;
    height: 40px;
    width: 67%;
    font-size: 12px;
    font-weight: 550;
    margin-top: 5px;
    display: block;
    text-align:left;
    padding-left: 20px;
  }
  .chart-title-tips {
    height: 30px;
    width: 100px;
    font-size: 12px;
    font-weight: 500;
    margin-top: 5px;
    display: block;
    text-align:left;
  }
  .chart-title-tipslast {
    height: 30px;
    width: 80px;
    font-size: 12px;
    font-weight: 500;
    margin-top: 5px;
    display: block;
    text-align:left;
  }
  .chart-title-tipsonline {
    height: 30px;
    width: 60px;
    font-size: 12px;
    font-weight: 500;
    margin-top: 5px;
    margin-left: 7%;
    display: block;
    text-align:left;
  }
  .chart-title-tipsoffline {
    height: 30px;
    width: 60px;
    font-size: 12px;
    font-weight: 500;
    margin-top: 5px;
    display: block;
    text-align:left;
  }
  .chart-title-tipslinefirst {
    height: 30px;
    width: 80px;
    font-size: 12px;
    margin-left: 1%;
    font-weight: 500;
    margin-top: 5px;
    display: block;
    text-align:left;
  }
  .chart-title-tipsline {
    height: 30px;
    width: 80px;
    font-size: 12px;
    font-weight: 500;
    margin-top: 5px;
    display: block;
    text-align:left;
  }
  .bluediv{
    margin-top: 5px;
    height: 6px;
    width: 11px;
    background-color: #5eb9ef;
    margin-right: 1px;
    float: left;
  }
  .tips {
    padding-left: 5px;
    height: 20px;
    float: left;
  }
  .tips-line {
    width: 40%;
    padding-left: 5px;
    height: 20px;
    float: left;
  }
  .greendiv{
    margin-top: 4px;
    height: 6px;
    width: 11px;
    background-color: #09a206;
    margin-right: 1px;
    float: left;
  }
  .chart-item {
    background-color: #f5f6f7;
    height: 28px;
    width: 100%;
    display: flex;
  }
  .list-item {
    background-color: #f5f6f7;
    height: 28px;
    width: 100%;
    display: flex;
  }
  .list-warn{
    margin-top: 16px;
    margin-left: 16px;
    margin-right: 16px;
  }
  .chart-tabs {
    height: 28px;
    width: 92%;
    display:block;
    margin-left: 10px;
  }
  .chart-tabs-short {
    height: 28px;
    width: 67%;
    margin-left: 10px;
  }
  .list-tabs {
    height: 28px;
    width: 96%;
    margin-left: 10px;
  }
  .chart-detail{
    height: 23px;
    width: 30px;
    text-decoration:underline;
    font-size: 12px;
    color: #0f97e5;
    cursor: pointer;
    margin-top: 5px;
    float: right;
  }
  /deep/ .el-tabs__item {
    background-color: white;
    padding: 0px;
    height: 28px;
    box-sizing: border-box;
    line-height: 28px;
    display: inline-block;
    list-style: none;
    font-size: 10px;
    font-weight: 500;
    min-width: 60px;
    color: #4e4e4e;
    position: relative;
    background-color: #f5f6f7;
    margin-left: 10px;
  }
  /deep/ .el-tabs__item.is-active {
    /* color: #409EFF; */
    background-color: #f5f6f7;
    font-weight: 550;
    border-bottom: 2px solid #4E4E4E;
  }
  .chart-line{
    height: 190px;
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  .list-line{
    width: 100%;
    height: 207px;
  }
  .res-chart {
    height: 180px;
    width: 400px;
  }
  .res-chart-hide{
    height: 180px;
    display: none;
    width: 400px;
  }
  .chart-pie{
    height: 164px;
    width: 80%;
    margin-top: 1%;
  }
  .chart-pie-detail{
    width: 20%;
    font-size: 11px;
    color: #8e8e8e;
    margin-top: 15%;
    margin-bottom: 15%;
    margin-right: 5%;
  }
  .pie-detail{
    text-align: right;
    font-size: 8px;
    color: #8e8e8e;
    display: block;
  }
  .pie-number{
    margin-top: 10px;
    color: #5eb9ef;
    font-size: 20px;
    display: block;
    text-align: right;
  }
  .chart-circle-info{
    float: left;
    position: relative;
    /* margin-top: 48px; */
    margin-bottom: 70px;
    height: 90px;
    /* width: 25%; */
    /* border-right: 1px solid #e9e9e9; */
  }
  .chart-circle-right{
    float: left;
    position: relative;
    margin-top: 48px;
    margin-bottom: 70px;
    height: 67px;
    width: 25%;
  }
  /* .circle-block{
    width: 100%;
    text-align: center;
  } */
  /* .circle-title{
    padding-top: 10px;
    font-size: 14px;
    width: 100%;
    text-align: center;
    color: #4e4e4e;
  } */
  /* .circle-detail{
    width: 100%;
    text-align: center;
    font-size: 3px;
    color: #4e4e4e
  }
  .circle-detail-block {
    padding-top: 5px;
    display: block;
  } */
  .detail-block {
    font-size: 24px;
    color: #5eb9ef;
    margin-right: 2px;
  }
  .chart-circle{
    float: left;
    /* margin-top: 56px; */
    /* width: 200px; */
    height: 120px;
    /* margin-right: 10px; */
  }
  .circle-block{
    width: 100px;
    /* height: 120px; */
    float: left;
  }
  .circle-info{
    width: 110px;
    height: 120px;
    /* float: left; */
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
  .info {
    display: inline-block;
    width: 15px;
    height: 15px;
    cursor: pointer;
    background-image: url(../../assets/image/detail.png);
    margin-left: 8px;
 }
 h4 {
   float: left;
   font-size: 13px;
   font-weight: normal;
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
 .el-button.is-circle {
    border-radius: 50%;
    padding: 0 5px;
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
.circle-info-detail {
  float: left;
}
.war-info-tip {
  padding-top: 80px;
}
</style>
