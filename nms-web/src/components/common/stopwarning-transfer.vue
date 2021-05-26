<template>
  <div class="DlgWrapper">
    <tree-transfer
      :title="title"
      :from_data='from_data'
      :to_data='to_data'
      :defaultProps="{label:'label'}"
      @node-click="handleNodeClick"
      @addBtn='add' @removeBtn='remove'
      :mode='mode' height='380px'
      filter
      openAll
      :check-on-click-node='true'
      v-model="rightdata"
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
    name: "stopwarning-transfer",
    data() {
      return {
        mode: "transfer", // transfer addressList
        rightdata: [],
        changedata: [],
        changenode: [],
        title: ['全选', '已选']
      }
    },
    props: {
      from_data: {
        type: Array,
        required: true
      },
      to_data: {
        type: Array,
        default() {
          return []
        }
      }
    },
    methods: {
      handleNodeClick: function() {
        console.log('yes')
      },
      // 切换模式 现有树形穿梭框模式transfer 和通讯录模式addressList
      changeMode() {
        if (this.mode == "transfer") {
          this.mode = "addressList";
        } else {
          this.mode = "transfer";
        }
      },
      // 监听穿梭框组件添加
      add(fromData, toData, obj) {
        // 树形穿梭框模式transfer时，返回参数为左侧树移动后数据、右侧树移动后数据、移动的        {keys,nodes,halfKeys,halfNodes}对象
        // 通讯录模式addressList时，返回参数为右侧收件人列表、右侧抄送人列表、右侧密送人列表
        console.log("fromData >:", fromData);
        console.log("toData >:", toData);
        console.log("obj >:", obj);
        this.$emit('addData', toData);
      },
      // 监听穿梭框组件移除
      remove(fromData, toData, obj) {
        // 树形穿梭框模式transfer时，返回参数为左侧树移动后数据、右侧树移动后数据、移动的{keys,nodes,halfKeys,halfNodes}对象
        // 通讯录模式addressList时，返回参数为右侧收件人列表、右侧抄送人列表、右侧密送人列表
        console.log("fromData <:", fromData);
        console.log("toData <:", toData);
        console.log("obj <:", obj);
        this.$emit('addData', toData);
      }
    },
  }

</script>

<style scoped>
  .DlgWrapper {
    font-size: 12px;
    color: #4e4e4e;
    display: inline-block;
    margin: 22px 0px ;
    width: 700px;
  }
  input[type="text"] {
    font-size: 12px;
    color: #616060;
    border-bottom: 1px solid #949799;
    cursor: pointer;
    padding: 0 0 2px 1px;
  }
  /deep/ input.el-input__inner {
    width: 250px;
  }
</style>

