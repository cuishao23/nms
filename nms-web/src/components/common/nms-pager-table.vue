<template>
  <div style="width: 100%;margin-top: 8px">
    <el-table :data="curData" stripe style="width: 100%" border align="left" :highlight-current-row="highLight" ref="tbl"
              @selection-change="handleSelectionChange"
              @row-click="onSelect">
      <el-table-column type="index" :index="startIndex" width="50" label="序号" v-if="index"/>
      <el-table-column v-if="selection"
                       type="selection"
                       width="55">
      </el-table-column>
      <el-table-column v-for="(item, index) in fields" :key="index" :label="item.label" :prop="item.prop"
                       :show-overflow-tooltip="true">
        <template slot-scope="scope">
          <div v-if="item.prop ==='level' || item.prop === 'warning_level'">
            <span class="warning-critical"
                  v-if="scope.row.level === 'critical' ||scope.row.warning_level === 'critical'">严重</span>
            <span v-if="scope.row.level === 'important' || scope.row.warning_level === 'important'">重要</span>
            <span v-if="scope.row.level === 'normal' || scope.row.warning_level === 'normal'">一般</span>
            <span v-if="scope.row.level === 'none' || scope.row.warning_level === 'none'">无告警</span>
          </div>
          <div v-else-if="item.prop ==='resolve_time'">
            <span v-if="scope.row.resolve_time === null">未修复</span>
            <span v-else>{{scope.row.resolve_time}}</span>
          </div>
          <div v-else-if="item.opts != null">
            <a v-if="item.flag==='warning' && scope.row.server_type!==0 && scope.row.resolve_time === null && scope.row.server_type != null" @click.stop="item.opts[0].click(scope.row)">{{ item.opts[0].text }}</a>
            <a v-else-if="item.flag==='warning' && scope.row.resolve_time === null" v-for="(opt, oindex) in item.opts" @click.stop="opt.click(scope.row)" :key="oindex">{{ opt.text }}</a>
            <a v-else-if="item.flag!=='warning'" v-for="(opt, oindex) in item.opts" @click.stop="opt.click(scope.row)" :key="oindex">{{ opt.text }}</a>
          </div>
          <div v-else-if="item.prop === 'online'">
            <span v-if="scope.row.online === 'online'">在线</span>
            <span v-if="scope.row.online === 'offline'">离线</span>
            <span v-if="scope.row.online === 'conference'">会议中</span>
          </div>
          <div v-else-if="item.prop === 'log_type'">
            <span v-if="scope.row.log_type === 'logout'">注销</span>
            <span v-if="scope.row.log_type === 'diagnose'">设备诊断</span>
            <span v-if="scope.row.log_type === 'capture'">设备抓包</span>
            <span v-if="scope.row.log_type === 'log'">日志获取</span>
            <span v-if="scope.row.log_type === 'sus'">版本管理</span>
            <span v-if="scope.row.log_type === 'limitset'">阈值配置</span>
            <span v-if="scope.row.log_type === 'warningset'">告警配置</span>
            <span v-if="scope.row.log_type === 'terminaltype'">设备配置</span>
            <span v-if="scope.row.log_type === 'terminallimit'">权限配置</span>
          </div>
          <div v-else-if="item.prop === 'collaborate_mode'">
            <span v-if="scope.row.collaborate_mode === 'free'">自由模式</span>
            <span v-if="scope.row.collaborate_mode === 'admin'">管理方模式</span>
          </div>
          <div v-else-if="item.prop === 'cascadeType'">
            <span v-if="scope.row.cascadeType === 'up_meeting'">上级</span>
            <span v-if="scope.row.cascadeType === 'down_meeting'">下级</span>
          </div>
          <div v-else-if="item.prop === 'conf_type'">
            <span v-if="scope.row.conf_type === '0'">传统会议</span>
            <span v-if="scope.row.conf_type === '1'">端口会议</span>
            <span v-if="scope.row.conf_type === '2'">SFU纯转发会议</span>
            <span v-if="scope.row.conf_type === ''">未知会议</span>
          </div>
          <div v-else-if="item.flag === 'meeting_event' && item.prop === 'type'">
            <span v-if="scope.row.type == 'blunt'">卡顿</span>
            <span v-if="scope.row.type == 'lossrate'">丢包</span>
            <span v-if="scope.row.type == 'leave'">异常离会</span>
          </div>
          <div v-else-if="item.flag === 'meeting_event' && item.prop === 'note'">
            <span v-if="scope.row.type == 'leave' && scope.row.note == '1'">网络,接入或转发异常</span>
            <span v-if="scope.row.type == 'leave' && scope.row.note == '3'">RTD超时</span>
            <span v-if="scope.row.type == 'leave' && scope.row.note == '28'">mp掉线</span>
            <span v-if="scope.row.type == 'leave' && scope.row.note == '29'">申请解码资源失败</span>
            <span v-if="scope.row.type == 'leave' && scope.row.note == '30'">mtadp掉线</span>
            <span v-if="scope.row.type == 'leave' && scope.row.note == '31'">mpadp侧处理超时</span>
            <span v-if="scope.row.type == 'leave' && scope.row.note == '37'">CLIENT异常</span>
            <span v-if="scope.row.type == 'leave' && scope.row.note == '42'">sfu异常</span>
            <span v-if="scope.row.type == 'leave' && scope.row.note == '255'">未知错误</span>
            <span v-if="scope.row.type == 'lossrate' || scope.row.type == 'blunt'">{{ scope.row.note }}</span>
          </div>
          <div v-else-if="item.prop === 'leave_reason'">
            <span v-if="scope.row.leave_reason === '1'">网络,接入或转发异常</span>
            <span v-else-if="scope.row.leave_reason === '2'">正常挂断</span>
            <span v-else-if="scope.row.leave_reason === '3'">RTD超时</span>
            <span v-else-if="scope.row.leave_reason === '4'">DRQ</span>
            <span v-else-if="scope.row.leave_reason === '5'">类型不匹配</span>
            <span v-else-if="scope.row.leave_reason === '6'">终端忙</span>
            <span v-else-if="scope.row.leave_reason === '7'">终端主动挂断</span>
            <span v-else-if="scope.row.leave_reason === '8'">终端不可达</span>
            <span v-else-if="scope.row.leave_reason === '9'">终端本地挂断</span>
            <span v-else-if="scope.row.leave_reason === '10'">终端忙</span>
            <span v-else-if="scope.row.leave_reason === '11'">本端行政级别低，由远端自动发起重连</span>
            <span v-else-if="scope.row.leave_reason === '12'">呼叫下级MCU失败，该MCU正在召开其它会议</span>
            <span v-else-if="scope.row.leave_reason === '13'">呼叫下级MCU失败，该MCU已经被其它高级别MCU呼叫</span>
            <span v-else-if="scope.row.leave_reason === '14'">主叫方未注册</span>
            <span v-else-if="scope.row.leave_reason === '15'">被叫方未注册</span>
            <span v-else-if="scope.row.leave_reason === '16'">电话终端未接通</span>
            <span v-else-if="scope.row.leave_reason === '17'">终端入会加密模式和会议不符合</span>
            <span v-else-if="scope.row.leave_reason === '18'">终端入会超过会议最大终端数</span>
            <span v-else-if="scope.row.leave_reason === '19'">终端入会超过会议最大终端数</span>
            <span v-else-if="scope.row.leave_reason === '20'">会议为免打扰模式</span>
            <span v-else-if="scope.row.leave_reason === '21'">主席挂断</span>
            <span v-else-if="scope.row.leave_reason === '22'">会控挂断</span>
            <span v-else-if="scope.row.leave_reason === '23'">级联上级会议挂断</span>
            <span v-else-if="scope.row.leave_reason === '24'">会议结束挂断</span>
            <span v-else-if="scope.row.leave_reason === '25'">无终端，自动结会-1min</span>
            <span v-else-if="scope.row.leave_reason === '26'">无在线终端，自动结会-5min</span>
            <span v-else-if="scope.row.leave_reason === '27'">在线终端仅一个，自动结会-10min</span>
            <span v-else-if="scope.row.leave_reason === '28'">dssclient异常掉线</span>
            <span v-else-if="scope.row.leave_reason === '29'">申请解码资源失败</span>
            <span v-else-if="scope.row.leave_reason === '30'">mtadp掉线</span>
            <span v-else-if="scope.row.leave_reason === '31'">mpadp侧处理超时</span>
            <span v-else-if="scope.row.leave_reason === '32'">呼叫终端数超出License授权点数</span>
            <span v-else-if="scope.row.leave_reason === '33'">终端已入会</span>
            <span v-else-if="scope.row.leave_reason === '34'">终端权限认证失败</span>
            <span v-else-if="scope.row.leave_reason === '35'">当前终端注册在本平台域上的其他NU上</span>
            <span v-else-if="scope.row.leave_reason === '36'">国密加密认证失败</span>
            <span v-else-if="scope.row.leave_reason === '37'">CLIENT异常</span>
            <span v-else-if="scope.row.leave_reason === '38'">随机测试失败</span>
            <span v-else-if="scope.row.leave_reason === '39'">端口会议终端数量超过License授权点数</span>
            <span v-else-if="scope.row.leave_reason === '40'">终端在后台运行</span>
            <span v-else-if="scope.row.leave_reason === '41'">呼叫终端，该终端不支持此呼叫协议</span>
            <span v-else-if="scope.row.leave_reason === '42'">sfu异常</span>
            <span v-else-if="scope.row.leave_reason === '43'">终端注册类型和会议类型不匹配</span>
            <span v-else-if="scope.row.leave_reason === '44'">转发资源达到上限</span>
            <span v-else-if="scope.row.leave_reason === '45'">多设备强登入会</span>
            <span v-else-if="scope.row.leave_reason === '46'">此会议为不可见会议</span>
            <span v-else-if="scope.row.leave_reason === '255'">未知错误</span>
            <span v-else-if="scope.row.leave_reason === '0'">无异常</span>
            <span v-else-if="scope.row.leave_reason === ''"></span>
            <span v-else>未知错误</span>
          </div>
          <div v-else-if="item.prop === 'result'">
            <span v-if="scope.row.result === 'success'">成功</span>
            <span v-if="scope.row.result === 'fail'">失败</span>
          </div>
          <div v-else-if="item.prop === 'cpu' && scope.row.cpu !== null && scope.row.cpu !== ''">
            <span>{{ scope.row.cpu + '%'}}</span>
          </div>
          <div v-else-if="item.prop === 'memory' && scope.row.memory !== null && scope.row.memory !== ''">
            <span>{{ scope.row.memory + '%'}}</span>
          </div>
          <div v-else-if="item.prop === 'disk' && scope.row.disk !== null && scope.row.disk !== ''">
            <span>{{ scope.row.disk + '%'}}</span>
          </div>
          <div v-else-if="item.prop === 'port' && scope.row.port !== null && scope.row.port !== ''">
            <span>{{ scope.row.port + 'Mbps'}}</span>
          </div>
          <div v-else-if="item.prop === 'diskwritespeed' && scope.row.diskwritespeed !== null && scope.row.diskwritespeed !== ''">
            <span>{{ scope.row.diskwritespeed + 'MB/s'}}</span>
          </div>
          <div v-else-if="item.prop === 'rateofflow' && scope.row.rateofflow !== null && scope.row.rateofflow !== ''">
            <span>{{ scope.row.rateofflow + 'MB/s'}}</span>
          </div>
          <div v-else-if="item.prop === 'verLevel'">
            <span v-if="scope.row.verLevel == 0">强制</span>
            <span v-if="scope.row.verLevel == 1">建议</span>
            <span v-if="scope.row.verLevel == 2">普通</span>
          </div>
          <div v-else-if="item.prop === 'recomand' && item.flag === 'version'">
            <span v-if="scope.row.recomand === 1">是</span>
            <span v-if="scope.row.recomand === 0">否</span>
          </div>
          <div v-else-if="item.flag === 'license_file_status' && item.prop === 'auth_status'">
            <span v-if="scope.row.auth_status === 'normal'">正常</span>
            <span v-if="scope.row.auth_status === 'expired'">过期</span>
          </div>
          <div v-else-if="item.flag === 'version_level_tip' && item.prop === 'ver_level'">
            <span v-if="scope.row.ver_level == '0'">强制</span>
            <span v-if="scope.row.ver_level == '1'">建议</span>
            <span v-if="scope.row.ver_level == '2'">普通</span>
          </div>
          <div v-else-if="item.flag === 'inspect_server_unrepaires_warning' && item.prop === 'level'">
            <span v-if="scope.row.level == 'critical'">严重</span>
            <span v-if="scope.row.level == 'important'">重要</span>
            <span v-if="scope.row.level == 'normal'">一般</span>
          </div>
          <div v-else-if="item.flag === 'a1' && item.prop === 'inspects'">
            <span v-if="scope.row.license == '1'">License文件</span>
            <span v-if="scope.row.resource == '1'">会议资源</span>
            <span v-if="scope.row.server == '1'">服务器状态</span>
            <span v-if="scope.row.terminal == '1'">终端状态</span>
          </div>
          <div v-else-if="item.flag === 'release_attribute_tip' && item.prop === 'release_attribute'">
            <span v-if="scope.row.release_attribute == 0">无</span>
            <span v-if="scope.row.release_attribute == '1'">普通版本</span>
            <span v-if="scope.row.release_attribute == '2'">推荐版本</span>
            <span v-if="scope.row.release_attribute == '4'">灰度版本</span>
          </div>
          <div v-else-if="item.flag === 'diagnose_status' && item.prop === 'status'">
            <span v-if="scope.row.status == 0">未开始</span>
            <span v-if="scope.row.status == 1">正在执行...</span>
            <span v-if="scope.row.status == 2">已完成</span>
          </div>
          <div v-else-if="item.flag === 'online' && item.prop === 'online_state'">
            <span v-if="scope.row.online_state == 'online'">在线</span>
            <span v-if="scope.row.online_state == 'conference'">入会</span>
          </div>
          <div v-else-if="item.prop === 'online'">
            <div v-if="item.flag === 'serverDeviceOnline' && scope.row.device_ip === ''">
              <span></span>
            </div>
            <div v-else>
              <span v-if="scope.row.online === 'online'">在线</span>
              <span v-if="scope.row.online === 'offline'">离线</span>
              <span v-if="scope.row.online === 'conference'">会议中</span>
            </div>
          </div>
          <div v-else-if="item.flag === 'unctrl_ter' && item.prop === 'online'">
            <span v-if="scope.row.online == '1'">在线</span>
            <span v-if="scope.row.online == '0'">离线</span>
          </div>
          <div v-else-if="item.flag === 'terminalSatus' && item.prop === 'level'">
            <span v-if="scope.row.level == 'online'">在线</span>
            <span v-if="scope.row.level == 'offline'">离线</span>
          </div>
          <div v-else-if="item.prop === 'file_size'">
            <span v-html="formatter(scope.row.file_size, item.prop)"></span>
          </div>
          <div v-else-if="item.flag === 'terPers' && item.prop === 'status'">
            <span v-if="scope.row.status == '1'">开启</span>
            <span v-if="scope.row.status == '0'">关闭</span>
          </div>
          <div v-else-if="item.flag === 'per_type' && item.prop === 'type'">
            <span v-if="scope.row.type == ''">---</span>
            <span>{{ scope.row.type }}</span>
          </div>
          <div v-else-if="item.flag === 'per_version' && item.prop === 'version'">
            <span v-if="scope.row.version == ''">---</span>
            <span>{{ scope.row.version }}</span>
          </div>
          <div v-else-if="item.prop === 'SN'">
            <span v-if="scope.row.SN == ''">---</span>
          </div>
          <div v-else-if="item.flag === 'video_lostrate_tab' && item.prop === 'video_lostrate'">
            <span v-if="scope.row.video_lostrate == ''">---</span>
            <span v-else>{{ scope.row.video_lostrate }}%</span>
          </div>
          <div v-else-if="item.flag === 'audio_lostrate_tab' && item.prop === 'audio_lostrate'">
            <span v-if="scope.row.audio_lostrate == ''">---</span>
            <span v-else>{{ scope.row.audio_lostrate }}%</span>
          </div>
          <div v-else-if="item.flag === 'file_tag' && item.prop === 'file_size'">
            <span v-if="scope.row.file_size <= 0">---</span>
          </div>
          <div v-else>
            {{ scope.row[item.prop] }}
          </div>
        </template>
      </el-table-column>
    </el-table>
    <div class="pager" v-if="pager">
      <div class="goto-page">
        <input type="text" v-model.number="curPage" @keyup.enter="_gotoPage(curPage)" oninput = "value=value.replace(/[^\d]/g,'')"/><span>/</span><span>{{ totalPage }}</span>
      </div>
      <div class="pre-next-page">
        <div class="pre-page" @click="_prePage()"></div>
        <div class="next-page" @click="_nextPage()"></div>
      </div>
    </div>
    <nms-dialog title="提示" ref="isFirstDlg" width="400px" height="152px">
       <div slot="content">
         <div class="delTipsDiv">
            <span class="PromptImg"></span>
            <span>当前页为第一页</span>
         </div>
       </div>
    </nms-dialog>
    <nms-dialog title="提示" ref="isLastDlg" width="400px" height="152px">
      <div slot="content">
        <div class="delTipsDiv">
          <span class="PromptImg"></span>
          <span>当前页为最后一页</span>
        </div>
      </div>
    </nms-dialog>
    <nms-dialog title="提示" ref="wrongPageNum" width="400px" height="152px">
      <div slot="content">
        <div class="delTipsDiv">
          <span class="PromptImg"></span>
          <span>页码超过范围</span>
        </div>
      </div>
    </nms-dialog>
  </div>
</template>

<script>
  import NmsDialog from "./nms-dialog";
  import $ from 'jquery'

  export default {
    components: {NmsDialog},
    name: "nms-pager-table",
    data() {
      return {
        curPage: 1,
        startIndex: 1,
        currentSelect: null,
        highLight: true,
        curData: [],
        multipleSelection: null,
        a: false
      }
    },
    model: {
      prop: 'multipleSelection',
      event: 'multiSelect',

      prop: 'curPage',
      event: 'curPage'
    },
    created: function () {
      if (this.data != null && this.data.length > 0) {
        this.sliceData(1)
      } else {
        this.curPage = 1
      }
    },
    watch: {
      curPage: function (newPageNum, oldPageNum) {
        if (newPageNum > this.totalPage) {
          this.$refs.wrongPageNum.open()
          this.curPage=1
          this.$emit('curPage', this.curPage);
          this.startIndex = (this.curPage - 1) * this.perPage + 1
          return
        }
        this.curPage = newPageNum
        if(this.biaoZhi==2){
          this.$emit('curPage', this.curPage);
          this.startIndex = (newPageNum - 1) * this.perPage + 1
        }
      },
      data: function (newData, oldData) {
        if (this.biaoZhi == 2) {
          this.curPage=1
        }
        this.sliceData(this.curPage)

      },
    },
    methods: {
      formatter(row, value) {
        if (value == "file_size") {
          if (row < 1024) {
            return row + "B"
          } else if (row < 1024*1024) {
            return (Number(row) / 1024).toFixed(3) + "KB"
          } else if (row < 1024*1024*1024) {
            return (Number(row) / 1024 / 1024).toFixed(3) + "MB"
          } else {
            return (Number(row) / 1024 / 1024 / 1024).toFixed(3) + "GB"
          }
        }
      },
      sliceData: function (pageNum) {
        if (pageNum > this.totalPage || pageNum < 1) {
          return
        }
        let data = this.data
        if (data.length !== 0) {
          this.curData = data
          this.curPage = pageNum
        }
      },
      _prePage: function () {
        if (this.curPage === 1 || this.curPage === 0) {
          this.$refs.isFirstDlg.open()
          this.curPage=1
          this.$emit('curPage', this.curPage);
          this.startIndex = (this.curPage - 1) * this.perPage + 1
          return
        }
        let pageNum = this.curPage - 1
        this.$emit('curPage', pageNum);
        this.startIndex = (pageNum - 1) * this.perPage + 1
        if (this.prePage == null) {
          if (this.curPage > 1) {
            this.sliceData(this.curPage - 1)
          }
        } else {
          let data = this.prePage(pageNum)
          if (data !== null && data.length > 0) {
            this.curData = data
            this.curPage = pageNum
          }
        }
      },
      _nextPage: function () {
        if (this.curPage === this.totalPage) {
          this.$refs.isLastDlg.open()
          this.curPage=1
          this.$emit('curPage', this.curPage);
          this.startIndex = (this.curPage - 1) * this.perPage + 1
          return
        }
        let pageNum = this.curPage + 1
        this.$emit('curPage', pageNum);
        this.startIndex = (pageNum-1) * this.perPage + 1
        if (this.nextPage == null) {
          if (this.curPage < this.totalPage) {
            this.sliceData(this.curPage + 1)
          }
        } else {
          let data = this.nextPage(pageNum)
          if (data !== null && data.length > 0) {
            this.curData = data
            this.curPage = pageNum
          }
        }
      },
      _gotoPage: function (pageNum) {
        if (pageNum < 1 || pageNum > this.totalPage) {
          this.$refs.wrongPageNum.open()
          this.curPage=1
          this.$emit('curPage', this.curPage);
          this.startIndex = (this.curPage - 1) * this.perPage + 1
          return
        }else{
          this.$emit('curPage', this.curPage);
          this.startIndex = (pageNum - 1) * this.perPage + 1
        }
        if (this.gotoPage == null) {
          this.sliceData(pageNum)
        }
      },
      onSelect: function (row, event, column) {
        this.multipleSelection = row;
        this.$emit('multiSelect', this.multipleSelection)
        if (this.selection === true) {
          this.highLight = false
          this.$refs.tbl.toggleRowSelection(row)
        } else {
          if (this.currentSelect === row) {
            this.$refs.tbl.clearSelection()
            this.currentSelect = null
            this.highLight = false
          } else {
            this.currentSelect = row
            this.highLight = true
          }
        }
        if (this.rowClick != null) {
          this.rowClick(row)
        }
      },
      handleSelectionChange(val) {
        this.multipleSelection = val;
        this.$nextTick(() => {
          $('tbody tr', this.$el).each(function (index, ele) {
            let checkedTd = $('td.el-table-column--selection .is-checked', ele)
            if (checkedTd.length === 0) {
              $('td', ele).removeClass('td-black')
            } else {
              $('td', ele).addClass('td-black')
            }
          })
        })
        console.log('send multi select: ' + JSON.stringify(this.multipleSelection))
        this.$emit('multiSelect', this.multipleSelection)
        this.$store.commit('change',this.multipleSelection)
      }
    },
    props: {
      fields: {
        type: Array,
        required: true
      },
      totalPage: {
        type: Number
      },
      biaoZhi: {
        type: Number
      },
      perPage: {
        type: Number,
        default: function () {
          return 10
        }
      },
      pager: {
        type: Boolean,
        default: function () {
          return true
        }
      },
      index: {
        type: Boolean,
        default: function () {
          return true
        }
      },
      selection: {
        type: Boolean,
        default: function () {
          return false
        }
      },
      data: {
        type: Array,
        default: function () {
          return []
        }
      },
      rowClick: {
        type: Function
      },
      gotoPage: {
        type: Function
      },
      prePage: {
        type: Function
      },
      nextPage: {
        type: Function
      }
    }
  }
</script>

<style scoped>
  .pre-page, .next-page {
    width: 21px;
    height: 20px;
    cursor: pointer;
    position: relative;
    top: 1px;
  }

  .pager {
    float: right;
  }

  .goto-page {
    margin-right: 5px;
    float: left;
  }

  .goto-page input {
    width: 25px;
    padding-bottom: 0px;
  }

  .goto-page span {
    font-size: 11px;
    padding-left: 5px;
  }

  .pre-next-page {
    width: 42px;
    float: right;
  }

  .pre-page {
    float: left;
    background: url(../../assets/image/list_prepage.png);
  }

  .pre-page:hover {
    background: url(../../assets/image/list_prepage.png) -21px 0;
  }

  .pre-page:active {
    background: url(../../assets/image/list_prepage.png) -42px 0;
  }

  .next-page {
    float: right;
    background: url(../../assets/image/list_nextpage.png);
  }

  .next-page:hover {
    background: url(../../assets/image/list_nextpage.png) -21px 0;
  }

  .next-page:active {
    background: url(../../assets/image/list_nextpage.png) -42px 0;
  }

  .warning-critical {
    color: #ac1000;
  }

  .pager {
    position: fixed;
    bottom: 30px;
    right: 120px;
  }

  .note-content {
    font-size: 12px;
    color: #4e4e4e;
    white-space: nowrap;
    overflow: auto;
    height: 21px;
    line-height: 21px;
    background: url(../../assets/image/prompt.png) no-repeat;
    padding-left: 30px;
  }
  .el-table .cell.el-tooltip div {
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .delTipsDiv {
    text-align: center;
    padding-top: 50px;
  }
</style>
