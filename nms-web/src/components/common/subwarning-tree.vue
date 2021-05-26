<template>
  <el-tree :data="data" :props="defaultProps" node-key="code"
           @node-click="handleNodeClick" ref="tree"
           :default-checked-keys="defaultCodes"
           :highlight-current="true"
           :show-checkbox="showCheckbox"
           :default-expanded-keys="defaultExpandedKeys"
           :filter-node-method="filterNode"
  />
</template>

<script>
  export default {
    name: "subwarning-tree",
    data() {
      return {
        checkAll: true,
        isIndeterminate: true,

        defaultProps: {
          children: 'children',
          label: 'name',
        },
        defaultExpandedKeys: [],
        defaultCodes: []
      }
    },
    props: {
      data: {
        type: Array,
        required: true
      },
      nodeClick: {
        type: Function,
        default() {
          return function (data) {
            console.log('level: ' + data.level)
            console.log('level: ' + data.code)
          }
        }
      },
      showCheckbox: {
        type: Boolean,
        default() {
          return false
        }
      }
    },
    mounted: function () {
      if (this.data.length > 0) {
        //告警类型初始化默认全选
        console.log("data: " + JSON.stringify(this.data))
        this.defaultCodes = []
        for (var i = 0; i < this.data.length; i++) {
          for (var j = 0; j < this.data[i].children.length; j++) {
            this.defaultCodes.push(this.data[i].children[j].code)
          }
        }
      }
    },
    methods: {
      handleCheckAllChange(val) {
        this.isIndeterminate = false;
      },
      handleCheckedWarningsChange(value) {
        let checkedCount = value.length;
        this.checkAll = checkedCount === this.warnings.length;
        this.isIndeterminate = checkedCount > 0 && checkedCount < this.warnings.length;
      },
      handleNodeClick: function (data) {
        console.log('data:' + data[0].code)
        this.nodeClick(data)
      },
      filterNode: function (value, data) {
        if (!value) return true;
        return data.name.indexOf(value) !== -1;
      },
    }
  }
</script>

<style scoped>

</style>
