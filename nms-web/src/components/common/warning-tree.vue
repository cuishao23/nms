<template>
  <div class="ui-dialog-body">
    <div>
      <span id="codeSetDlgTitle">告警级别</span>
      <el-checkbox :indeterminate="isIndeterminate" v-model="checkAll" @change="handleCheckAllChange" style="margin-right:30px">全选</el-checkbox>
      <el-checkbox-group v-model="checkedWarings"  @change="handleCheckedWarningsChange" style="display: inline-block;">
         <el-checkbox  v-for="(warning,index) in warnings" :label="warning" :key="warning" @change="getValue(index,warning)">{{ warning }}</el-checkbox>
      </el-checkbox-group>
    </div>
    <el-tree :data="data" :props="defaultProps" node-key="code"
             ref="tree"
             :current-node-key="currentnodekey"
             @check="handleNodeCheck"
             show-checkbox
             :default-expand-all="false"
             :default-checked-keys="defaultCodes"
             :highlight-current="true"
             :default-expanded-keys="defaultExpandedKeys"
             :filter-node-method="filterNode"
             :style="{width: width + 'px', height: height + 'px', overflowY: 'auto'}"/>
  </div>
</template>

<script>
    import api from '../../axios';
    const warningOptions = ['严重', '重要', '一般'];
    export default {
      name: "warning-tree",
      data () {
        return {
          checkAll: false,
          isIndeterminate: true,
          checkedWarings: [],
          warnings: warningOptions,
          warning: '',
          senddata: [],
          defaultProps: {
            children: 'children',
            label: 'name',
          },
          defaultExpandedKeys: [],
          defaultCodes: [],
          currentnodekey: "",
          subwarningCode: [],

          // 比较依据
          imtWarn: [],
          imtNum: 0,
          ctlWarn: [],
          ctlNum: 0,
          nmlWarn: [],
          nmlNum: 0,
          // 当前选择
          imt: [],
          ctl: [],
          nml: [],

        }
      },
      props: {
        data: {
          type: Array,
          required: true
        },
        flash: {
          type: Boolean,
          default() {
            return false
          }
        },
        width: {
          type: Number,
          default() {
            return 500
          }
        },
        height: {
          type: Number,
          default() {
            return 380
          }
        },
      },
      mounted: function () {
        if (this.data.length > 0) {
          for (var i = 0; i < this.data.length; i++) {
            for (var j = 0; j < this.data[i].children.length; j++) {
              if (this.data[i].children[j].level === "important") {
                this.imt.push(this.data[i].children[j].code)
                this.imtWarn.push(this.data[i].children[j].code)
                this.imtNum++
              } else if (this.data[i].children[j].level === "critical") {
                // 用来记录当前勾选的严重类别告警项
                this.ctl.push(this.data[i].children[j].code)
                // 用来记录严重类别告警项
                this.ctlWarn.push(this.data[i].children[j].code)
                this.ctlNum++
              } else if (this.data[i].children[j].level === "normal") {
 
                this.nmlWarn.push(this.data[i].children[j].code)
                this.nmlNum++
              }
            }
          }
          api.getSubWarningCode().then((res) => {
            console.log(res)
            console.log(this.data)
            this.imt = []
            this.ctl = []
            this.nml = []
            if (res.success == 1) {
              let checkKeys = []
              let checkTotal = 0
              let imtcheck = 0
              let ctlcheck = 0
              let nmlcheck = 0
              let count = 0
              this.subwarningCode = res.subwarningcode;
              this.subwarningCode.forEach(item => {
                count = 0
                if (count == 0) {
                  this.data[0].children.forEach(warn => {
                    if (warn.code === item.code) {
                      checkKeys.push(item.code)
                      checkTotal++
                      if (warn.level === "important") {
                        this.imt.push(item.code)
                        imtcheck++
                      } else if (warn.level === "critical") {
                        this.ctl.push(item.code)
                        ctlcheck++
                      } else if (warn.level === "normal") {
                        this.nml.push(item.code)
                        nmlcheck++
                      }
                      count = 1
                    }
                  })
                }
                if (count == 0) {
                  this.data[1].children.forEach(warn => {
                    if (warn.code === item.code) {
                      checkKeys.push(item.code)
                      checkTotal++
                      if (warn.level === "important") {
                        this.imt.push(item.code)
                        imtcheck++
                      } else if (warn.level === "critical") {
                        this.ctl.push(item.code)
                        ctlcheck++
                      } else if (warn.level === "normal") {
                        this.nml.push(item.code)
                        nmlcheck++
                      }
                      count = 1
                    }
                  })
                }
                if (count == 0) {
                  this.data[2].children.forEach(warn => {
                    if (warn.code === item.code) {
                      checkKeys.push(item.code)
                      checkTotal++
                      if (warn.level === "important") {
                        this.imt.push(item.code)
                        imtcheck++
                      } else if (warn.level === "critical") {
                        this.ctl.push(item.code)
                        ctlcheck++
                      } else if (warn.level === "normal") {
                        this.nml.push(item.code)
                        nmlcheck++
                      }
                      count = 1
                    }
                  })
                }
                if (count == 0) {
                  this.data[3].children.forEach(warn => {
                    if (warn.code === item.code) {
                      checkKeys.push(item.code)
                      checkTotal++
                      if (warn.level === "important") {
                        this.imt.push(item.code)
                        imtcheck++
                      } else if (warn.level === "critical") {
                        this.ctl.push(item.code)
                        ctlcheck++
                      } else if (warn.level === "normal") {
                        this.nml.push(item.code)
                        nmlcheck++
                      }
                      count = 1
                    }
                  })
                }
              })
              this.defaultCodes = checkKeys
              this.$refs.tree.setCheckedKeys(checkKeys);
              if (checkTotal == (this.imtNum + this.ctlNum + this.nmlNum)) {
                this.checkAll = true
              } else {
                this.checkedWarings = []
                if (imtcheck == this.imtNum) {
                  this.checkedWarings.push("重要")
                } else if (ctlcheck == this.ctlNum) {
                  this.checkedWarings.push("严重")
                } else if (nmlcheck == this.nmlNum) {
                  this.checkedWarings.push("一般")
                }
                this.checkAll = false
              }
            }
          })
        }
      },
      watch: {
        flash: function(newstate, oldstate) {
          this.imt = []
          this.ctl = []
          this.nml = []
          console.log(newstate)
          if (newstate === true) {
            if (this.data.length > 0) {
              api.getSubWarningCode().then((res) => {
                console.log(res)
                console.log(this.data)
                if (res.success == 1) {
                  let checkKeys = []
                  let checkTotal = 0
                  let imtcheck = 0
                  let ctlcheck = 0
                  let nmlcheck = 0
                  let count = 0
                  this.subwarningCode = res.subwarningcode;
                  this.subwarningCode.forEach(item => {
                    count = 0
                    if (count == 0) {
                      this.data[0].children.forEach(warn => {
                        if (warn.code === item.code) {
                          checkKeys.push(item.code)
                          checkTotal++
                          if (warn.level === "important") {
                            this.imt.push(item.code)
                            imtcheck++
                          } else if (warn.level === "critical") {
                            this.ctl.push(item.code)
                            ctlcheck++
                          } else if (warn.level === "normal") {
                            this.nml.push(item.code)
                            nmlcheck++
                          }
                          count = 1
                        }
                      })
                    }
                    if (count == 0) {
                      this.data[1].children.forEach(warn => {
                        if (warn.code === item.code) {
                          checkKeys.push(item.code)
                          checkTotal++
                          if (warn.level === "important") {
                            this.imt.push(item.code)
                            imtcheck++
                          } else if (warn.level === "critical") {
                            this.ctl.push(item.code)
                            ctlcheck++
                          } else if (warn.level === "normal") {
                            this.nml.push(item.code)
                            nmlcheck++
                          }
                          count = 1
                        }
                      })
                    }
                    if (count == 0) {
                      this.data[2].children.forEach(warn => {
                        if (warn.code === item.code) {
                          checkKeys.push(item.code)
                          checkTotal++
                          if (warn.level === "important") {
                            this.imt.push(item.code)
                            imtcheck++
                          } else if (warn.level === "critical") {
                            this.ctl.push(item.code)
                            ctlcheck++
                          } else if (warn.level === "normal") {
                            this.nml.push(item.code)
                            nmlcheck++
                          }
                          count = 1
                        }
                      })
                    }
                    if (count == 0) {
                      this.data[3].children.forEach(warn => {
                        if (warn.code === item.code) {
                          checkKeys.push(item.code)
                          checkTotal++
                          if (warn.level === "important") {
                            this.imt.push(item.code)
                            imtcheck++
                          } else if (warn.level === "critical") {
                            this.ctl.push(item.code)
                            ctlcheck++
                          } else if (warn.level === "normal") {
                            this.nml.push(item.code)
                            nmlcheck++
                          }
                          count = 1
                        }
                      })
                    }
                  })
                  this.defaultCodes = checkKeys
                  this.$refs.tree.setCheckedKeys(checkKeys);
                  if (checkTotal == (this.imtNum + this.ctlNum + this.nmlNum)) {
                    this.checkAll = true
                    this.warnings = ['严重', '重要', '一般']
                    this.checkedWarings = this.warnings
                  } else {
                    this.checkAll = false
                    this.checkedWarings = []
                    console.log(imtcheck)
                    console.log(this.imtNum)
                    console.log(ctlcheck)
                    console.log(this.ctlNum)
                    console.log(nmlcheck)
                    console.log(this.nmlNum)
                    if (imtcheck == this.imtNum) {
                      this.checkedWarings.push("重要")
                    }
                    if (ctlcheck == this.ctlNum) {
                      this.checkedWarings.push("严重")
                    }
                    if (nmlcheck == this.nmlNum) {
                      this.checkedWarings.push("一般")
                    }
                    console.log(this.checkedWarings)
                  }
                }
              })
            }
          }
        },
        // 全选状态变化时触发
        checkAll: function(newstate, oldstate) {
          console.log(newstate)
          if (newstate === true) {
            this.warnings = ['严重', '重要', '一般']
            this.checkedWarings = this.warnings
            this.$refs.tree.setCheckedNodes(this.data);
            this.senddata = this.$refs.tree.getCheckedNodes(this.data);
            this.$emit('sendWarningdata', this.senddata);
            this.defaultCodes = this.$refs.tree.getCheckedKeys(this.data)
            console.log(this.defaultCodes)
            this.defaultCodes.splice(this.defaultCodes.indexOf(4), 1)
            this.defaultCodes.splice(this.defaultCodes.indexOf(3), 1)
            this.defaultCodes.splice(this.defaultCodes.indexOf(2), 1)
            this.defaultCodes.splice(this.defaultCodes.indexOf(1), 1)
            this.nml = this.nmlWarn
            this.imt = this.imtWarn
            this.ctl = this.ctlWarn
          } else {
              if (this.ctl.length == 0) {
                this.imt = this.imtWarn
              } else if (this.nml.length == 0) {
                this.nml = this.nmlWarn
              }
              else {
                this.warnings = ['严重', '重要', '一般']
              this.nml = []
              this.imt = []
              this.ctl = []
              }           
          }
        },
      },
      methods: {
        // 点击全选触发,点击严重级别不触发
        handleCheckAllChange(val) {
          console.log(val)
          this.warnings = ['严重', '重要', '一般']
          this.checkedWarings = val ? this.warnings : [];
          this.checkAll = val;
          this.isIndeterminate = false;
          if (this.checkAll == false) {
            console.log(this.checkAll);
            this.$refs.tree.setCheckedKeys([]);
            // 只有点击取消勾选才能清空defaultCodes
            this.defaultCodes = []
            this.$emit('sendWarningdata', []);
          }
        },
        // 点击严重级别触发，点击全选不会触发
        handleCheckedWarningsChange(value) {
          console.log('value')
          console.log(value)
          let checkedCount = value.length;
          this.checkAll = checkedCount === this.warnings.length;
          // this.isIndeterminate = ((checkedCount > 0) && (checkedCount < this.warnings.length));
        },

        getValue(index, warning) {
          console.group('getValue')
          let cod = this.checkedWarings.indexOf(warning)
          let reference = null
          let select = null
          if (warning === '严重'){
            reference = this.ctlWarn
            select = this.ctl

          } else if (warning === '重要'){
            reference = this.imtWarn
            select = this.imt

          } else {
            reference = this.nmlWarn
            select = this.nml
          }
          if (cod === -1){
            console.log('清空 ' + warning)
              for (var i = 0; i < this.defaultCodes.length; i++) {
                if (reference.indexOf(this.defaultCodes[i]) !== -1) {
                  this.defaultCodes[i] = ''
                }
              }
            select.length = 0
          }else{
            console.log('添加 ' + warning)
            this.defaultCodes = Array.from(new Set(this.defaultCodes.concat(reference)))
            reference.map((v, i)=>select[i]=v)
          }

          this.$refs.tree.setCheckedKeys(this.defaultCodes);
          this.senddata = this.$refs.tree.getCheckedNodes(this.data);
          this.$emit('sendWarningdata', this.senddata);
          console.log("实时更新:" + this.defaultCodes)
          console.groupEnd()
        },

        handleNodeCheck: function(data, obj) {
          // tree型点击结点回调函数
          console.group('handleNodeCheck')
          console.log(data)
          console.log(obj)
          let checked = 0
          if (data.children) {
            data.children.forEach(warn => {
              checked = 0
              obj.checkedNodes.forEach(item => {
                if (warn.code == item.code) {
                  checked = 1
                }
              })
              if (checked == 1) {
                this.defaultCodes.push(warn.code)
                switch (warn.level) {
                  case "normal":
                    this.nml.push(warn.code)
                    let nmlIndex = this.checkedWarings.indexOf('一般')
                    if (nmlIndex === -1 && this.nml.length === this.nmlNum) {
                      this.checkedWarings.push("一般")
                    }
                    if (this.checkedWarings.length === 3) {
                      this.checkAll = true
                    }
                    break
                  case "important":
                    this.imt.push(warn.code)
                    let imtIndex = this.checkedWarings.indexOf('重要')
                    if (imtIndex === -1 && this.imt.length === this.imtNum) {
                      this.checkedWarings.push("重要")
                    }
                    if (this.checkedWarings.length === 3) {
                      this.checkAll = true
                    }
                    break
                  case "critical":
                    this.ctl.push(warn.code)
                    let ctlIndex = this.checkedWarings.indexOf('严重')
                    if (ctlIndex === -1 && this.ctl.length === this.ctlNum) {
                      this.checkedWarings.push("严重")
                    }
                    if (this.checkedWarings.length === 3) {
                      this.checkAll = true
                    }
                    break
                  default:
                    break
                }
              } else {
                for (var i = 0; i < this.defaultCodes.length; i++) {
                  if (this.defaultCodes[i] == warn.code) {
                    this.defaultCodes.splice(i, 1)
                    console.log(this.defaultCodes[i])
                    // this.$refs.tree.setCheckedKeys(this.defaultCodes);
                  }
                }
                switch (warn.level) {
                  case "normal":
                    this.nml.splice(this.nml.indexOf(warn.code), 1)
                    let nmlIndex = this.checkedWarings.indexOf('一般')
                    if (nmlIndex === -1) {
                      this.checkAll = false
                    } else {
                      console.log(this.checkedWarings)
                      this.checkedWarings.splice(nmlIndex, 1)
                      // 删除勾选值会带动告警值变化，须重新赋值（组件问题）
                      this.warnings = ['严重', '重要', '一般']
                      this.checkAll = false
                    }
                    break
                  case "important":
                    this.imt.splice(this.imt.indexOf(warn.code), 1)
                    let imtIndex = this.checkedWarings.indexOf('重要')
                    if (imtIndex === -1) {
                      this.checkAll = false
                    } else {
                      console.log(this.checkedWarings)
                      this.checkedWarings.splice(imtIndex, 1)
                      this.warnings = ['严重', '重要', '一般']
                      this.checkAll = false
                    }
                    break
                  case "critical":
                    this.ctl.splice(this.ctl.indexOf(warn.code), 1)
                    let ctlIndex = this.checkedWarings.indexOf('严重')
                    if (ctlIndex === -1) {
                      this.checkAll = false
                    } else {
                      console.log(this.checkedWarings)
                      this.checkedWarings.splice(ctlIndex, 1)
                      this.warnings = ['严重', '重要', '一般']
                      this.checkAll = false
                    }
                    break
                  default:
                    break
                }
              }
            })
          } else {
            checked = 0
            obj.checkedNodes.forEach(item => {
              if (data.code == item.code) {
                checked = 1
              }
            })
            if (checked == 1) {
              this.defaultCodes.push(data.code)
              console.log(this.checkedWarings)
              switch (data.level) {
                case "normal":
                  this.nml.push(data.code)
                  let nmlIndex = this.checkedWarings.indexOf('一般')
                  if (nmlIndex === -1 && this.nml.length === this.nmlNum) {
                    this.checkedWarings.push("一般")
                    console.log(this.checkedWarings)
                  }
                  if (this.checkedWarings.length === 3) {
                    this.checkAll = true
                  }
                  break
                case "important":
                  this.imt.push(data.code)
                  let imtIndex = this.checkedWarings.indexOf('重要')
                  if (imtIndex === -1 && this.imt.length === this.imtNum) {
                    this.checkedWarings.push("重要")
                    console.log(this.checkedWarings)
                  }
                  if (this.checkedWarings.length === 3) {
                    this.checkAll = true
                  }
                  break
                case "critical":
                  this.ctl.push(data.code)
                  let ctlIndex = this.checkedWarings.indexOf('严重')
                  if (ctlIndex === -1 && this.ctl.length === this.ctlNum) {
                    this.checkedWarings.push("严重")
                    console.log(this.checkedWarings)
                  }
                  if (this.checkedWarings.length === 3) {
                    this.checkAll = true
                  }
                  break
                default:
                  break
              }
            } else {
              for (var i = 0; i < this.defaultCodes.length; i++) {
                if (this.defaultCodes[i] == data.code) {
                  this.defaultCodes.splice(i, 1)
                  console.log(this.defaultCodes[i])
                  // this.$refs.tree.setCheckedKeys(this.defaultCodes);
                }
              }
              console.log(this.checkedWarings)
              switch (data.level) {
                case "normal":
                  this.nml.splice(this.nml.indexOf(data.code), 1)
                  let nmlIndex = this.checkedWarings.indexOf('一般')
                  if (nmlIndex === -1) {
                    this.checkAll = false
                  } else {
                    console.log(this.checkedWarings)
                    this.checkedWarings.splice(nmlIndex, 1)
                    // 删除勾选值会带动告警值变化，须重新赋值（组件问题）
                    this.warnings = ['严重', '重要', '一般']
                    this.checkAll = false
                  }
                  break
                case "important":
                  this.imt.splice(this.imt.indexOf(data.code), 1)                   
                  let imtIndex = this.checkedWarings.indexOf('重要')
                  if (imtIndex === -1) {
                    this.checkAll = false
                  } else {
                    console.log(this.checkedWarings)
                    this.checkedWarings.splice(imtIndex, 1)
                    this.warnings = ['严重', '重要', '一般']
                    this.checkAll = false
                  }
                  break
                case "critical":
                  this.ctl.splice(this.ctl.indexOf(data.code), 1)                   
                  let ctlIndex = this.checkedWarings.indexOf('严重')
                  if (ctlIndex === -1) {
                    this.checkAll = false
                  } else {
                    console.log(this.checkedWarings)
                    this.checkedWarings.splice(ctlIndex, 1)
                    this.warnings = ['严重', '重要', '一般']
                    this.checkAll = false
                  }
                  break
                default:
                  break
              }
            }
          }

          this.senddata = this.$refs.tree.getCheckedNodes(this.data);
          this.$emit('sendWarningdata', this.senddata);
          console.groupEnd()
        },
        filterNode: function(value, data) {
          if (!value) return true;
          return data.name.indexOf(value) !== -1;
        }
      }
    }
</script>

<style scoped>
  .search-domain {
    display: flex;
    justify-content: flex-start;
  }

  .search-domain-icon:active {
    background: url(../../assets/image/search.png) -40px 0;
  }

  .search-domain-icon:hover {
    background: url(../../assets/image/search.png) -20px 0;
  }
  .search-domain-icon {
    display: block;
    width: 20px;
    height: 20px;
    background: url(../../assets/image/search.png) 0 0;
    cursor: pointer;
    position: relative;
    top: 0px;
    right: 15px;
  }
  #codeSetDlgTitle{
    font-size: 12px;
    color: #8b8b8b;
    float: left;
    padding-right: 30px;
  }
  .ui-dialog-body{
    padding: 30px;
    text-align: center;
  }
</style>
