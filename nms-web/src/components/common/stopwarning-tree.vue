<template>
  <div class="allPart" v-if="reset">
    <stopwarning-lefttree :from_data="stopwarningDomain" @sendData="sendLeftData($event)"></stopwarning-lefttree>
    <div class="midButton">
      <button class="one_image" id='allmove' @click="allmove"></button>
      <button class="one_image" id='rightmove' @click="rightmove"></button>
      <button class="one_image" id='leftmove' @click="leftmove"></button>
      <button class="one_image" id='allback' @click="allback"></button>
    </div>
    <stopwarning-righttree :to_data="stopedwarningDomain" @sendData="sendRightData($event)"></stopwarning-righttree>
  </div>
</template>

<script>
import StopwarningLefttree from "./stopwarning-lefttree";
import StopwarningRighttree from "./stopwarning-righttree";
import api from '../../axios';
   export default {
    components: {StopwarningLefttree, StopwarningRighttree},
    name: "stopwarning-tree",
    data() {
      return {
        reset: true, // 刷新穿梭框组件
        Domaintree: [], // 获取后端总列表，需要再处理转化成树
        warningAllList: [], // 获取后端所有已选列表

        leftNodes: [], // 当前点击选中的左侧节点
        rightNodes: [], // 当前点击选中的右侧节点

        stopwarningDomain: [], // 记录当前穿梭框左侧的树
        stopedwarningDomain: [], // 记录当前穿梭框右侧的树
        allwarningDomain: [], // 记录总树，方便全移时直接赋给上面俩参数

        tempLeft: [], // 记录当前穿梭框左侧的节点列表
        tempRight: [], // 记录当前穿梭框右侧需要传递后端的节点列表
        tempAll: [], // 记录总节点列表，方便全移时直接赋给上面俩参数
      }
    },
    props: {
      confirm: {
        type: Number,
        default() {
          return 0
        }
      },
    },
    mounted: function () {
        this.$nextTick(() => {
            // 初始化暂停告警列表，分别记录两组树及节点属性列表
            this.getStopWarning()
            // 获得当前所有暂停告警列表并存入allwarningDomain，以备全移时直接获取
            this.getallStopWarning()
        })
    },
    watch: {
      // 确定时向后端发送告警
      confirm: function (newtype, oldtype) {
        console.log(newtype)
        if (newtype == 1) {
          api.setStopWarning({moid: this.tempRight}).then(res => {
            console.log(res)
            if (res.success == 1) {
              this.$emit('reSet', '1')
            }
            this.$nextTick(() => {
                this.getStopWarning()
            })
          })
        }
      }
    },
    methods: {
      // 初始化调用
      getStopWarning: function() {
          this.tempLeft = []
          this.tempRight = []
          this.tempAll = []
          api.getStopWarningInfo({params: {newPageNum: 1}}).then((res) => {
            console.log(res)
            if (res.success == 1) {
                this.warningAllList = res.allWarnings
                api.getDomainTree().then((res) => {
                    this.stopedwarningDomain = []
                    this.stopwarningDomain = []
                    console.log(res)
                    if (res.success === 1) {
                        let aa = []
                        let bb = []
                        res.data.forEach(item => {
                          if (item.type == "user") {
                            aa.push(item)
                          } else {
                            bb.push(item)
                          }
                        })
                        this.Domaintree = bb.concat(aa)
                        this.Domaintree.forEach(item => {
                          if (item.type == "machine_room" || item.type == "user") {
                            this.tempAll.push(item.moid)
                            if (this.warningAllList.length == 0) {
                              this.tempLeft.push(item.moid)
                            } else {
                              this.warningAllList.forEach(warn => {
                                if (warn.moid !== item.moid) {
                                  this.tempLeft.push(item.moid)
                                } else if (warn.moid == item.moid) {
                                  this.tempRight.push(item.moid)
                                }
                              })
                            }
                          }
                        })
                        let serverId = 1
                        let domainId = 1
                        let roomId = 1
                        let send = 0
                        let machine = 0
                        let roomcount = 0
                        this.Domaintree.forEach(item => {
                            if (item.type === "kernel" && item.parent_moid === '-1') {
                                // 记录左侧的告警列表
                                let Topchildren = { id: '', pid: '', label: '', moid: '', type: '', children: [] }
                                Topchildren.label = item.name
                                Topchildren.id = 1
                                Topchildren.pid = 0
                                Topchildren.moid = item.moid
                                Topchildren.type = item.type
                                // 记录右侧的告警列表
                                let Topchildren0 = { id: '', pid: '', label: '', moid: '', type: '', children: [] }
                                Topchildren0.label = item.name
                                Topchildren0.id = 1
                                Topchildren0.pid = 0
                                Topchildren0.moid = item.moid
                                Topchildren0.type = item.type
                                this.Domaintree.forEach(service => {
                                    send = 0
                                    if (service.parent_moid === item.moid) {
                                        let Servicechildren = { id: '', pid: '', label: '', moid: '', type: '', children: [] }
                                        Servicechildren.label = service.name
                                        Servicechildren.id = Topchildren.id + '-' + serverId
                                        Servicechildren.pid = Topchildren.id
                                        Servicechildren.moid = service.moid
                                        Servicechildren.type = service.type

                                        let Servicechildren0 = { id: '', pid: '', label: '', moid: '', type: '', children: [] }
                                        Servicechildren0.label = service.name
                                        Servicechildren0.id = Topchildren.id + '-' + serverId
                                        Servicechildren0.pid = Topchildren.id
                                        Servicechildren0.moid = service.moid
                                        Servicechildren0.type = service.type
                                        this.Domaintree.forEach(domain => {
                                            send = 0
                                            machine = 0
                                            if (domain.parent_moid === service.moid) {
                                                let Domainchildren = { id: '', pid: '', label: '', moid: '', type: '', children: [] }
                                                Domainchildren.label = domain.name
                                                Domainchildren.id = Servicechildren.id + '-' + domainId
                                                Domainchildren.pid = Servicechildren.id
                                                Domainchildren.moid = domain.moid
                                                Domainchildren.type = domain.type
                                                let Domainchildren0 = { id: '', pid: '', label: '', moid: '', type: '', children: [] }
                                                Domainchildren0.label = domain.name
                                                Domainchildren0.id = Servicechildren.id + '-' + domainId
                                                Domainchildren0.pid = Servicechildren.id
                                                Domainchildren0.moid = domain.moid
                                                Domainchildren0.type = domain.type
                                                roomcount = 0
                                                this.Domaintree.forEach(room => {
                                                    send = 0
                                                    let Roomchildren = { id: '', pid: '', label: '', moid: '', type: '', children: [] }
                                                    let Roomchildren0 = { id: '', pid: '', label: '', moid: '', type: '', children: [] }
                                                    if (room.parent_moid === domain.moid) {
                                                        roomcount++
                                                        Roomchildren.label = room.name
                                                        Roomchildren.id = Domainchildren.id + '-' + roomId
                                                        Roomchildren.pid = Domainchildren.id
                                                        Roomchildren.moid = room.moid
                                                        Roomchildren.type = room.type
                                                        Roomchildren0.label = room.name
                                                        Roomchildren0.id = Domainchildren.id + '-' + roomId
                                                        Roomchildren0.pid = Domainchildren.id
                                                        Roomchildren0.moid = room.moid
                                                        Roomchildren0.type = room.type
                                                        this.warningAllList.forEach(item => {
                                                            if (item.moid === room.moid) {
                                                                send = 1
                                                                machine = 1 // 用户域同节点可能还有机房域
                                                                Domainchildren0.children.push(Roomchildren0)
                                                            }
                                                        })
                                                        if (send === 0) {
                                                            Domainchildren.children.push(Roomchildren)
                                                        }
                                                        roomId++
                                                    }
                                                })
                                                if (roomcount === 0 && (Domainchildren.type == 'service' || Domainchildren.type == 'platform')) {
                                                    // 去除没有用户域或机房的服务域和机房域
                                                    console.log(Domainchildren)
                                                } else {
                                                    this.warningAllList.forEach(item => {
                                                        if (item.moid === domain.moid) {
                                                            send = 1
                                                        }
                                                    })
                                                    if (send === 0) {
                                                      if (machine === 0) {
                                                        Servicechildren.children.push(Domainchildren)
                                                        if (Domainchildren0.children.length > 0) {
                                                          Servicechildren0.children.push(Domainchildren0)
                                                        }
                                                      } else if (machine === 1) {
                                                        Servicechildren0.children.push(Domainchildren0)
                                                        if (Domainchildren.children.length > 0) {
                                                          Servicechildren.children.push(Domainchildren)
                                                        }
                                                      }
                                                    } else if (send === 1) {
                                                      Servicechildren0.children.push(Domainchildren0)
                                                      if (Domainchildren.children.length > 0) {
                                                        Servicechildren.children.push(Domainchildren)
                                                      }
                                                    }
                                                    domainId++
                                                }
                                            }
                                        })
                                        if (Servicechildren.children.length === 0 && Servicechildren0.children.length === 0 && (Servicechildren.type == 'service' || Servicechildren.type == 'platform')) {
                                            console.log(Servicechildren)
                                        } else {
                                            if (Servicechildren0.children.length > 0) {
                                                Topchildren0.children.push(Servicechildren0)
                                            }
                                            if (Servicechildren.children.length > 0) {
                                                Topchildren.children.push(Servicechildren)
                                            }
                                            serverId++
                                        }
                                    }
                                })
                                if (Topchildren.children.length > 0) {
                                    this.stopwarningDomain.push(Topchildren)
                                } else {
                                    this.stopwarningDomain = []
                                }
                                if (Topchildren0.children.length > 0) {
                                    this.stopedwarningDomain.push(Topchildren0)
                                } else {
                                    this.stopedwarningDomain = []
                                }
                            }
                        })
                    }
                })
            }
        })
      },
      // 单移时调用
      addStopWarning: function() {
        this.leftNodes = []
        this.rightNodes = []
        api.getDomainTree().then((res) => {
            this.stopedwarningDomain = []
            this.stopwarningDomain = []
            console.log(res)
            if (res.success === 1) {
                let aa = []
                let bb = []
                res.data.forEach(item => {
                  if (item.type == "user") {
                    aa.push(item)
                  } else {
                    bb.push(item)
                  }
                })
                this.Domaintree = bb.concat(aa)
                let serverId = 1
                let domainId = 1
                let roomId = 1
                let send = 0
                let machine = 0
                let roomcount = 0
                this.Domaintree.forEach(item => {
                    if (item.type === "kernel" && item.parent_moid === '-1') {
                        let Topchildren = { id: '', pid: '', label: '', moid: '', type: '', children: [] }
                        Topchildren.label = item.name
                        Topchildren.id = 1
                        Topchildren.pid = 0
                        Topchildren.moid = item.moid
                        Topchildren.type = item.type

                        let Topchildren0 = { id: '', pid: '', label: '', moid: '', type: '', children: [] }
                        Topchildren0.label = item.name
                        Topchildren0.id = 1
                        Topchildren0.pid = 0
                        Topchildren0.moid = item.moid
                        Topchildren0.type = item.type
                        this.Domaintree.forEach(service => {
                            send = 0
                            if (service.parent_moid === item.moid) {
                                let Servicechildren = { id: '', pid: '', label: '', moid: '', type: '', children: [] }
                                Servicechildren.label = service.name
                                Servicechildren.id = Topchildren.id + '-' + serverId
                                Servicechildren.pid = Topchildren.id
                                Servicechildren.moid = service.moid
                                Servicechildren.type = service.type

                                let Servicechildren0 = { id: '', pid: '', label: '', moid: '', type: '', children: [] }
                                Servicechildren0.label = service.name
                                Servicechildren0.id = Topchildren.id + '-' + serverId
                                Servicechildren0.pid = Topchildren.id
                                Servicechildren0.moid = service.moid
                                Servicechildren0.type = service.type
                                this.Domaintree.forEach(domain => {
                                    send = 0
                                    machine = 0
                                    if (domain.parent_moid === service.moid) {
                                        let Domainchildren = { id: '', pid: '', label: '', moid: '', type: '', children: [] }
                                        Domainchildren.label = domain.name
                                        Domainchildren.id = Servicechildren.id + '-' + domainId
                                        Domainchildren.pid = Servicechildren.id
                                        Domainchildren.moid = domain.moid
                                        Domainchildren.type = domain.type
                                        let Domainchildren0 = { id: '', pid: '', label: '', moid: '', type: '', children: [] }
                                        Domainchildren0.label = domain.name
                                        Domainchildren0.id = Servicechildren.id + '-' + domainId
                                        Domainchildren0.pid = Servicechildren.id
                                        Domainchildren0.moid = domain.moid
                                        Domainchildren0.type = domain.type
                                        roomcount = 0
                                        this.Domaintree.forEach(room => {
                                            send = 0
                                            let Roomchildren = { id: '', pid: '', label: '', moid: '', type: '', children: [] }
                                            let Roomchildren0 = { id: '', pid: '', label: '', moid: '', type: '', children: [] }
                                            if (room.parent_moid === domain.moid) {
                                                roomcount++
                                                Roomchildren.label = room.name
                                                Roomchildren.id = Domainchildren.id + '-' + roomId
                                                Roomchildren.pid = Domainchildren.id
                                                Roomchildren.moid = room.moid
                                                Roomchildren.type = room.type
                                                Roomchildren0.label = room.name
                                                Roomchildren0.id = Domainchildren.id + '-' + roomId
                                                Roomchildren0.pid = Domainchildren.id
                                                Roomchildren0.moid = room.moid
                                                Roomchildren0.type = room.type
                                                this.tempRight.forEach(item => {
                                                    if (item === room.moid) {
                                                        send = 1
                                                        machine = 1 // 用户域同节点可能还有机房域
                                                        Domainchildren0.children.push(Roomchildren0)
                                                    }
                                                })
                                                if (send === 0) {
                                                    Domainchildren.children.push(Roomchildren)
                                                }
                                                roomId++
                                            }
                                        })
                                        if (roomcount === 0 && (Domainchildren.type == 'service' || Domainchildren.type == 'platform')) {
                                            console.log(Domainchildren)
                                        } else {
                                            this.tempRight.forEach(item => {
                                                if (item === domain.moid) {
                                                    send = 1
                                                }
                                            })
                                            if (send === 0) {
                                              if (machine == 0) {
                                                Servicechildren.children.push(Domainchildren)
                                                if (Domainchildren0.children.length > 0) {
                                                    Servicechildren0.children.push(Domainchildren0)
                                                }
                                              } else if (machine === 1) {
                                                Servicechildren0.children.push(Domainchildren0)
                                                if (Domainchildren.children.length > 0) {
                                                    Servicechildren.children.push(Domainchildren)
                                                }
                                              }
                                            } else if (send === 1) {
                                              Servicechildren0.children.push(Domainchildren0)
                                              if (Domainchildren.children.length > 0) {
                                                  Servicechildren.children.push(Domainchildren)
                                              }
                                            }
                                            domainId++
                                        }
                                    }
                                })
                                if (Servicechildren.children.length === 0 && Servicechildren0.children.length === 0 && (Servicechildren.type == 'service' || Servicechildren.type == 'platform')) {
                                    console.log(Servicechildren)
                                } else {
                                    if (Servicechildren0.children.length > 0) {
                                        Topchildren0.children.push(Servicechildren0)
                                    }
                                    if (Servicechildren.children.length > 0) {
                                        Topchildren.children.push(Servicechildren)
                                    }
                                    serverId++
                                }
                            }
                        })
                        if (Topchildren.children.length > 0) {
                            this.stopwarningDomain.push(Topchildren)
                        } else {
                            this.stopwarningDomain = []
                        }
                        if (Topchildren0.children.length > 0) {
                            this.stopedwarningDomain.push(Topchildren0)
                        } else {
                            this.stopedwarningDomain = []
                        }
                    }
                })
            }
        })
      },
      // 全移时调用
      getallStopWarning: function() {
          api.getStopWarningInfo({params: {newPageNum: 1}}).then((res) => {
            console.log(res)
            if (res.success == 1) {
                this.warningAllList = res.allWarnings
                api.getDomainTree().then((res) => {
                    this.allwarningDomain = []
                    console.log(res)
                    if (res.success === 1) {
                        let aa = []
                        let bb = []
                        res.data.forEach(item => {
                          if (item.type == "user") {
                            aa.push(item)
                          } else {
                            bb.push(item)
                          }
                        })
                        this.Domaintree = bb.concat(aa)
                        let serverId = 1
                        let domainId = 1
                        let roomId = 1
                        let roomcount = 0
                        this.Domaintree.forEach(item => {
                            if (item.type === "kernel" && item.parent_moid === '-1') {
                                let Topchildren = { id: '', pid: '', label: '', moid: '', type: '', children: [] }
                                Topchildren.label = item.name
                                Topchildren.id = 1
                                Topchildren.pid = 0
                                Topchildren.moid = item.moid
                                Topchildren.type = item.type

                                this.Domaintree.forEach(service => {
                                    if (service.parent_moid === item.moid) {
                                        let Servicechildren = { id: '', pid: '', label: '', moid: '', type: '', children: [] }
                                        Servicechildren.label = service.name
                                        Servicechildren.id = Topchildren.id + '-' + serverId
                                        Servicechildren.pid = Topchildren.id
                                        Servicechildren.moid = service.moid
                                        Servicechildren.type = service.type
                                        this.Domaintree.forEach(domain => {
                                            if (domain.parent_moid === service.moid) {
                                                let Domainchildren = { id: '', pid: '', label: '', moid: '', type: '', children: [] }
                                                Domainchildren.label = domain.name
                                                Domainchildren.id = Servicechildren.id + '-' + domainId
                                                Domainchildren.pid = Servicechildren.id
                                                Domainchildren.moid = domain.moid
                                                Domainchildren.type = domain.type
                                                roomcount = 0
                                                this.Domaintree.forEach(room => {
                                                    let Roomchildren = { id: '', pid: '', label: '', moid: '', type: '', children: [] }
                                                    if (room.parent_moid === domain.moid) {
                                                        roomcount++
                                                        Roomchildren.label = room.name
                                                        Roomchildren.id = Domainchildren.id + '-' + roomId
                                                        Roomchildren.pid = Domainchildren.id
                                                        Roomchildren.moid = room.moid
                                                        Roomchildren.type = room.type
                                                        Domainchildren.children.push(Roomchildren)
                                                        roomId++
                                                    }
                                                })
                                                if (roomcount === 0 && (Domainchildren.type == 'service' || Domainchildren.type == 'platform')) {
                                                    console.log(Domainchildren)
                                                } else {
                                                    Servicechildren.children.push(Domainchildren)
                                                    domainId++
                                                }
                                            }
                                        })
                                        if (Servicechildren.children.length === 0 && (Servicechildren.type == 'service' || Servicechildren.type == 'platform')) {
                                            console.log(Servicechildren)
                                        } else {
                                            Topchildren.children.push(Servicechildren)
                                            serverId++
                                        }
                                    }
                                })
                                if (Topchildren.children.length > 0) {
                                    this.allwarningDomain.push(Topchildren)
                                } else {
                                    this.allwarningDomain = []
                                }
                            }
                        })
                    }
                })
            }
        })
      },
      // 获取左侧树组件传递参数
      sendLeftData: function(data) {
        console.log(data)
        this.leftNodes = []
        this.leftNodes.push(data)
      },
      // 获取右侧树组件传递参数
      sendRightData: function(data) {
        console.log(data)
        this.rightNodes = []
        this.rightNodes.push(data)
      },
      // 全部右移按键触发
      allmove: function() {
        if (this.stopwarningDomain.length > 0) {
          // 若之前有选中告警则清空
          this.leftNodes = []
          this.rightNodes = []
          // 将树列表重新分配
          this.stopwarningDomain = []
          this.stopedwarningDomain = this.allwarningDomain
          // 将节点属性列表重新分配
          this.tempLeft = []
          this.tempRight = this.tempAll
        }
      },
      // 全部左移按键触发
      allback: function() {
        if (this.stopedwarningDomain.length > 0) {
          this.leftNodes = []
          this.rightNodes = []
          this.stopedwarningDomain = []
          this.stopwarningDomain = this.allwarningDomain
          this.tempLeft = this.tempAll
          this.tempRight = []
        }
      },
      // 单个右移按键触发
      rightmove: function() {
        if (this.leftNodes.length > 0) {
          if (this.leftNodes[0].children.length > 0) {
            // 点击包含子节点的父节点域不触发
          } else {
            if (this.leftNodes[0].type == "user" || this.leftNodes[0].type == "machine_room") {
              if (this.tempLeft.length == 1) {
                this.tempLeft = []
                this.tempRight = this.tempAll
              } else {
                for (var i = 0; i < this.tempLeft.length; i++) {
                  if (this.tempLeft[i] == this.leftNodes[0].moid) {
                    this.tempLeft[i] = ''
                    var exist = 0
                    this.tempRight.forEach(warn => {
                      if (warn == this.leftNodes[0].moid) {
                        exist = 1
                      }
                    })
                    if (exist == 0) {
                      this.tempRight.push(this.leftNodes[0].moid)
                    }
                  }
                }
                this.tempLeft = this.tempLeft.filter(item => {
                  if (item !== '') {
                    return item
                  }
                })
              }
              this.$nextTick(() => {
                this.addStopWarning()
              })
            }
          }
        }
      },
      // 单个左移按键触发
      leftmove: function() {
        console.log(this.tempRight)
        if (this.rightNodes.length > 0) {
          console.log(this.rightNodes)
          if (this.rightNodes[0].children.length > 0) {

          } else {
            if (this.rightNodes[0].type == "user" || this.rightNodes[0].type == "machine_room") {
              if (this.tempRight.length == 1) {
                this.tempRight = []
                this.tempLeft = this.tempAll
              } else {
                for (var i = 0; i < this.tempRight.length; i++) {
                  if (this.tempRight[i] == this.rightNodes[0].moid) {
                    this.tempRight[i] = ''
                    var exist = 0
                    this.tempLeft.forEach(warn => {
                      if (warn == this.rightNodes[0].moid) {
                        exist = 1
                      }
                    })
                    if (exist == 0) {
                      this.tempLeft.push(this.rightNodes[0].moid)
                    }
                  }
                }
                this.tempRight = this.tempRight.filter(item => {
                  if (item !== '') {
                    return item
                  }
                })
              }
              this.$nextTick(() => {
                this.addStopWarning()
              })
            }
          }
        }
      },
    },
  }

</script>

<style scoped>
  .one_image {
    cursor: pointer;
    margin-right: 5px;
    width: 50px;
    margin-bottom: 20px;
    vertical-align: middle;
  }
  #allmove {
    width: 30px;
    height: 30px;
    background: url("../../assets/image/allmove.png") 0 0;
  }
  #allmove:hover {
    background: url("../../assets/image/allmove.png") -30px 0;
  }
  #allback {
    width: 30px;
    height: 30px;
    background: url("../../assets/image/allback.png") 0 0;
  }
  #allback:hover {
    background: url("../../assets/image/allback.png") -30px 0;
  }
  #rightmove {
    width: 30px;
    height: 30px;
    background: url("../../assets/image/rightmove.png") 0 0;
  }
  #rightmove:hover {
    background: url("../../assets/image/rightmove.png") -30px 0;
  }
  #leftmove {
    width: 30px;
    height: 30px;
    background: url("../../assets/image/leftmove.png") 0 0;
  }
  #leftmove:hover {
    background: url("../../assets/image/leftmove.png") -30px 0;
  }
  .allPart{
    width: 100%;
    height: 100%;
    display:inline-block
  }
  .midButton {
    padding-top: 107px;
    padding-left: 22px;
    padding-right: 22px;
    width: 75px;
    height: 405px;
    float: left;
  }
</style>
