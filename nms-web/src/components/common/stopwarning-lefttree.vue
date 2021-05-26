<template>
    <div class= "leftPart">
        <div class="leftTree">
        <el-input
            placeholder="搜索"
            v-model="filterText"
            class="inputset">
        </el-input>
        <el-tree
            class="filter-tree"
            :data="from_data"
            :check-strictly="true"
            :props="defaultProps"
            default-expand-all
            node-key="id"
            @current-change="getCurrentNode"
            :check-on-click-node="true"
            :style="{width: 259 + 'px', height: 300 + 'px', overflowY: 'auto'}"
            ref="lefttree">
        </el-tree>
        </div>
    </div>
</template>

<script>
   export default {
    name: "stopwarning-lefttree",
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
      from_data: {
        type: Array,
        default() {
          return []
        }
      },
    },
    watch: {
      filterText(val) {
        this.$refs.lefttree.filter(val);
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
  .leftPart {
    width: 273px;
    height: 350px;
    margin-top: 22px;
    margin-left: 50px;
    border-style:solid;
    border-width:2px;
    border-color:#E8E8E8;
    float: left;
  }
  .leftTree {
    font-size: 15px;
    color: #4e4e4e;
    display: inline-block;
    margin: 22px 10px ;
    width: 100px;
  }
  .inputset {
    width: 250px;
  }
  input[type="text"] {
    font-size: 15px;
    color: #616060;
    border-bottom: 1px solid #949799;
    cursor: pointer;
    padding: 0 0 2px 1px;
  }
</style>
