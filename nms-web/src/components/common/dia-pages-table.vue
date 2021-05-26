<template>
  <div style="width: 100%">
    <el-table :data="curData" style="width: 100%" border align="left" :highlight-current-row="highLight" ref="tbl"
              @selection-change="handleSelectionChange"
              @row-click="onSelect"
              :row-key="getRowKeys"
              stripe>
      <el-table-column type="index" :index="startIndex" width="50" label="序号" v-if="index"/>
      <el-table-column v-if="selection"
                       type="selection"
                       :reserve-selection="true"
                       :selectable='isDisabled'
                       width="55">
      </el-table-column>
      <el-table-column v-for="(item, index) in fields" :key="index" :label="item.label" :prop="item.prop"
                       :show-overflow-tooltip="true" :reserve-selection="true">
        <template slot-scope="scope">
          <div v-if="item.opts != null">
            <a v-for="(opt, oindex) in item.opts" @click.stop="opt.click(scope.row)" :key="oindex">{{ opt.text}}</a>
          </div>
          <div v-else>
            {{ scope.row[item.prop] }}
          </div>
        </template>
      </el-table-column>
    </el-table>
    <div class="pager" v-if="pager">
      <div class="goto-page">
        <input type="text" v-model.number="curPage" @keyup.enter="_gotoPage(curPage)"/><span>/</span><span>{{ totalPage }}</span>
      </div>
      <div class="pre-next-page">
        <div class="pre-page" @click="_prePage()"></div>
        <div class="next-page" @click="_nextPage()"></div>
      </div>
    </div>
    <nms-dialog title="提示" ref="isFirstDlg" width="300px" height="200px">
      <div slot="content" class="tbl-dlg">
        <p class="note-content">当前页为第一页</p>
      </div>
    </nms-dialog>
    <nms-dialog title="提示" ref="isLastDlg" width="300px" height="200px">
      <div slot="content" class="tbl-dlg">
        <p class="note-content">当前页为最后一页</p>
      </div>
    </nms-dialog>
    <nms-dialog title="提示" ref="wrongPageNum" width="300px" height="200px">
      <div slot="content" class="tbl-dlg">
        <p class="note-content">页码超过范围</p>
      </div>
    </nms-dialog>
  </div>
</template>

<script>
  import NmsDialog from "./nms-dialog";
  import $ from 'jquery'

  export default {
    components: {NmsDialog},
    name: "dia-pages-table",
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
      event: 'multiSelect'
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
        console.log('watch curPage: ' + newPageNum + ' ' + oldPageNum)
        let newPage = Number(newPageNum)
        if (Number.isInteger(newPage) && (newPage >= 1 && newPage <= this.totalPage)) {
          this.startIndex = (newPage - 1) * this.perPage + 1
        } else {
          this.curPage = oldPageNum
          this.$refs.wrongPageNum.open()
        }
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
      isDisabled(row, index) {
        console.log("this.disableFlag"+this.disableFlag)
        if (this.disableFlag == 1) {
          return 0
        } else {
          return 1
        }
      },
      // 保存选中的数据id,row-key就是要指定一个key标识这一行的数据
      getRowKeys(row){
        return row.id;
      },
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
        if (this.curPage === 1) {
          this.$refs.isFirstDlg.open()
          return
        }
        let pageNum = this.curPage - 1
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
          return
        }
        let pageNum = this.curPage + 1
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
        console.log("_gotoPage"+pageNum)
        if (pageNum < 1 || pageNum > this.totalPage) {
          this.$refs.wrongPageNum.open()
          return
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
</style>
