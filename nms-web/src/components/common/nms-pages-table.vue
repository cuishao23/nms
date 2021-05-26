<template>
  <div style="width: 100%">
    <el-table :data="curData" style="width: 100%" border align="left" :highlight-current-row="highLight" ref="tbl"
              @selection-change="handleSelectionChange"
              @row-click="onSelect"
              stripe>
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
            <span v-if="scope.row.level === '' || scope.row.warning_level === ''">---</span>
          </div>
          <div v-else-if="item.opts != null">
            <a v-for="(opt, oindex) in item.opts" @click.stop="opt.click(scope.row)" :key="oindex">{{ opt.text}}</a>
          </div>
          <div v-else-if="item.prop === 'online'">
            <div v-if="item.flag==='serverDeviceOnline'&&scope.row.ip===''">
              <span></span>
            </div>
            <!-- <div v-if="item.flag==='frameOnline'">
              <span>---</span>
            </div> -->
            <div v-else>
              <span v-if="scope.row.online === 'online'">在线</span>
              <span v-else-if="scope.row.online === 'offline'">离线</span>
              <span v-else-if="scope.row.online === 'conference'">会议中</span>
              <span v-else>{{ scope.row[item.prop] }}</span>
            </div>
          </div>
          <!-- <div v-else-if="item.flag === 'frameIp' && item.prop === 'ip'">
            <span>---</span>
          </div> -->
          <div v-else-if="item.prop === 'belong_slot'">
            <span v-if="scope.row.belong_slot == ''">---</span>
            <span v-else>{{ scope.row[item.prop] }}</span>
          </div>
          <div v-else-if="item.prop === 'uptime'">
            <span v-if="scope.row.uptime == ''">---</span>
            <span v-else>{{ scope.row[item.prop] }}</span>
          </div>
          <div v-else-if="item.flag === 'perType' && item.prop === 'type'">
            <span>{{ scope.row.type }}</span>
          </div>
          <div v-else-if="item.prop === 'type'">
            <span v-if="scope.row.type === 'logout'">注销</span>
            <span v-if="scope.row.type === 'export'">导出数据</span>
            <span v-if="scope.row.type === 'backup'">备份数据</span>
            <span v-if="scope.row.type === 'limitset'">阈值设置</span>
            <span v-if="scope.row.type === 'clearset'">数据清理设置</span>
            <span v-if="scope.row.type === 'warningset'">告警设置</span>
            <span v-if="scope.row.type === 'susadd'">添加版本</span>
            <span v-if="scope.row.type === 'susedit'">编辑版本</span>
            <span v-if="scope.row.type === 'susdelete'">删除版本</span>
          </div>
          <div v-else-if="item.prop === 'result'">
            <span v-if="scope.row.result === 'success'">成功</span>
            <span v-if="scope.row.result === 'failed'">失败</span>
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
          <div v-else-if="item.flag === 'version_level_tip' && item.prop === 'ver_level'">
            <span v-if="scope.row.ver_level == '0'">强制</span>
            <span v-if="scope.row.ver_level == '1'">建议</span>
            <span v-if="scope.row.ver_level == '2'">普通</span>
          </div>
          <div v-else-if="item.flag === 'release_attribute_tip' && item.prop === 'release_attribute'">
            <span v-if="scope.row.release_attribute == 0">无</span>
            <span v-if="scope.row.release_attribute == '1'">普通版本</span>
            <span v-if="scope.row.release_attribute == '2'">推荐版本</span>
            <span v-if="scope.row.release_attribute == '4'">灰度版本</span>
          </div>
          <div v-else-if="item.flag === 'Peripheral' && item.prop === 'status'">
            <span v-if="scope.row.status == '0'">关闭</span>
            <span v-if="scope.row.status == '1'">开启</span>
          </div>
          <div v-else-if="item.flag === 'audio_video' && item.prop === 'meeting_audio_video_status'">
            <span v-if="scope.row.meeting_audio_video_status == '1'">正常</span>
            <span v-if="scope.row.meeting_audio_video_status == '0'">异常</span>
          </div>
          <div v-else-if="item.flag === 'audioCodec' && item.prop === 'audio_codec_start'">
            <span v-if="scope.row.audio_codec_start == '1'">是</span>
            <span v-if="scope.row.audio_codec_start == '0'">否</span>
          </div>
          <div v-else-if="item.flag === 'videoCodec' && item.prop === 'video_codec_start'">
            <span v-if="scope.row.video_codec_start == '1'">是</span>
            <span v-if="scope.row.video_codec_start == '0'">否</span>
          </div>
          <div v-else-if="item.flag === 'hwCodecStatus' && item.prop === 'hw_codec_status'">
            <span v-if="scope.row.hw_codec_status == '1'">是</span>
            <span v-if="scope.row.hw_codec_status == '0'">否</span>
          </div>
          <div v-else-if="item.flag === 'videoAbility' && item.prop === 'video_ability'">
            <span>{{scope.row.res + '@' + scope.row.framerate}}</span>
            <span>{{ scope.row.video_up_down_bitrate}}</span>
          </div>
          <div v-else-if="item.flag === 'videoPktsLoserate' && item.prop === 'video_pkts_loserate'">
            <span v-if="scope.row.video_pkts_loserate == null">---</span>
            <span v-else>{{ scope.row.video_pkts_loserate + '%'}}</span>
          </div>
          <div v-else-if="item.flag === 'audioPktsLoserate' && item.prop === 'audio_pkts_loserate'">
            <span v-if="scope.row.audio_pkts_loserate == null">---</span>
            <span v-else>{{ scope.row.audio_pkts_loserate + '%'}}</span>
          </div>
          <div v-else-if="item.flag === 'serverDeviceDisk' && item.prop === 'disk'">
            <span v-if="scope.row.disk == ''">---</span>
          </div>
          <div v-else-if="item.flag === 'videoFormat' && item.prop === 'video_format'">
            <span v-if="scope.row.video_format == null">---</span>
            <span v-else>{{ scope.row.video_format}}</span>
          </div>
          <div v-else-if="item.flag === 'audioFormat' && item.prop === 'audio_format'">
            <span v-if="scope.row.audio_format == null">---</span>
            <span v-else>{{ scope.row.audio_format}}</span>
          </div>
          <div v-else-if="item.prop === 'video_pkts_lose'">
            <span v-if="scope.row.video_pkts_lose == null">---</span>
            <span v-else>{{ scope.row.video_pkts_lose}}</span>
          </div>
          <div v-else-if="item.prop === 'audio_pkts_lose'">
            <span v-if="scope.row.audio_pkts_lose == null">---</span>
            <span v-else>{{ scope.row.audio_pkts_lose}}</span>
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
    name: "nms-pages-table",
    data() {
      return {
        curPage: 1,
        startIndex: 1,
        currentSelect: null,
        highLight: true,
        curData: [],
        multipleSelection: null
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
        } else if (newPageNum == 1) {
          this.curPage=1
          this.$emit('curPage', this.curPage);
          this.startIndex = (this.curPage - 1) * this.perPage + 1
          return
        }
        this.$emit('curPage', this.curPage);
        this.curPage = newPageNum
      },
      data: function (newData, oldData) {
        if (this.data != null && this.data.length > 0) {
          this.sliceData(1)
        } else {
          this.curPage = 1
        }
      }
    },
    methods: {
      sliceData: function (pageNum) {
        if (pageNum > this.totalPage || pageNum < 1) {
          return
        }
        let start = (pageNum - 1) * this.perPage
        let end = pageNum * this.perPage
        let data = this.data.slice(start, end)
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
        this.$store.commit('change',this.multipleSelection)
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
      perPage: {
        type: Number,
        default: function () {
          return 10
        }
      },
      disableFlag: {
        type: Number,
        default: function () {
          return 0
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

  .tbl-dlg {
    text-align: center;
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
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
