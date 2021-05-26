<template>
    <div class= "rightPart">
      <span class="rightTitle">已选</span>
      <div class="rightTree">
        <el-tree
           class="filter-tree"
            :data="to_data"
            :check-strictly="true"
            :props="defaultProps"
            default-expand-all
            node-key="id"
            @current-change="getCurrentNode"
            check-on-click-node
            :style="{width: 259 + 'px', height: 304 + 'px', overflowY: 'auto'}"
            ref="righttree">
        </el-tree>
      </div>
    </div>
</template>

<script>
   export default {
    name: "stopwarning-righttree",
    data() {
      return {
        filterText: '',
        defaultProps: {
          children: 'children',
          label: 'label'
        }
      }
    },
    props: {
      to_data: {
        type: Array,
        default() {
          return []
        }
      }
    },
    methods: {
      getCurrentNode: function(data) {
        console.log(data)
        this.$emit('sendData', data);
      },
    },
  }

</script>

<style scoped>
  /deep/ .el-tree-node.is-current > .el-tree-node__content{
    background-color: white;
  }
  /deep/ .el-tree-node:hover > .el-tree-node__content{
    background-color: white;
  }
  /deep/ .el-tree-node.is-current > .el-tree-node__content .el-tree-node__label{
    background-color: #1e94da;
    color: white;
  }
  .rightTitle {
    font-size: 15px;
    padding: 10px 0 0 20px;
    display: inline-block;
    color: #4e4e4e;
    height: 42px;
    width: 270px;
    border-bottom: 2px solid #E8E8E8;
  }
  .rightPart {
    width: 273px;
    height: 350px;
    margin-top: 22px;
    border-style:solid;
    border-width:2px;
    border-color:#E8E8E8;
    float: left;
  }
  .rightTree {
    font-size: 15px;
    color: #4e4e4e;
    display: inline-block;
    margin: 0px 10px ;
    width: 100px;
  }
</style>
