<template>
  <div class="DlgWrapper">
    <div class="frame-name-container">
      <p class="leftP">机架名称</p>
      <input class="rightinput" type="text" value="" id="">
    </div>
    <tree-transfer
      :title="title"
      :from_data='fromData'
      :to_data='toData'
      :defaultProps="{label:'label'}"
      @addBtn='add' @removeBtn='remove'
      :mode='mode' height='380px'
      filter
      openAll
      placeholder="搜索">
    </tree-transfer>
  </div>
</template>

<script>
   import treeTransfer from 'el-tree-transfer'; // 引入
   export default {
    components: {
      treeTransfer, // 注册
    },
    name: "nms-transfer",
    data(){
      return {
        mode: "transfer", // transfer addressList
        fromData:[
          {
            id: "1",
            pid: 0,
            label: "电视墙",
            children: [
              {
                id: "1-1",
                pid: "1",
                label: "cuixin",
                children: []
              }
            ]
          },
          {
            id: "2",
            pid: 0,
            label: "机框",
            children: [
              {
                id: '2-1',
                pid: '2',
                label: 'jd6000',
                children: []
              }
            ]
          },
          {
            id: "3",
            pid: 0,
            label: "x86",
            children: []
          },
          {
            id: "4",
            pid: 0,
            label: "JDS6000",
            children: [
              {
                id: '4-1',
                pid: '4',
                label: 'jds6000',
                children: []
              }
            ]
          },
        ],
        toData:[],
        title: ['未选','已选']
      }
    },
    methods:{
      // 切换模式 现有树形穿梭框模式transfer 和通讯录模式addressList
      changeMode() {
        if (this.mode == "transfer") {
          this.mode = "addressList";
        } else {
          this.mode = "transfer";
        }
      },
      // 监听穿梭框组件添加
      add(fromData,toData,obj){
        // 树形穿梭框模式transfer时，返回参数为左侧树移动后数据、右侧树移动后数据、移动的        {keys,nodes,halfKeys,halfNodes}对象
        // 通讯录模式addressList时，返回参数为右侧收件人列表、右侧抄送人列表、右侧密送人列表
        console.log("fromData >:", fromData);
        console.log("toData >:", toData);
        console.log("obj >:", obj);
      },
      // 监听穿梭框组件移除
      remove(fromData,toData,obj){
        // 树形穿梭框模式transfer时，返回参数为左侧树移动后数据、右侧树移动后数据、移动的{keys,nodes,halfKeys,halfNodes}对象
        // 通讯录模式addressList时，返回参数为右侧收件人列表、右侧抄送人列表、右侧密送人列表
        console.log("fromData <:", fromData);
        console.log("toData <:", toData);
        console.log("obj <:", obj);
      }
    },
  }

</script>

<style scoped>
  .DlgWrapper {
    font-size: 12px;
    color: #4e4e4e;
    display: inline-block;
    margin: 0px 28px;
  }
  .frame-name-container {
    overflow: hidden;
    margin-top: 26px;
    margin-bottom: 25px;
  }
  .leftP {
    float: left;
    width: 90px;
    text-align: left;
  }
 .DlgWrapper .rightinput {
    width: 530px;
  }
  input[type="text"] {
    font-size: 12px;
    color: #616060;
    border-bottom: 1px solid #949799;
    cursor: pointer;
    padding: 0 0 2px 1px;
  }
</style>

