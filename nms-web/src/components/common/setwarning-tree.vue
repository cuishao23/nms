<template>
  <el-tree :data="data" :props="defaultProps" node-key="code"
           @check-change="getCheckedKeys" ref="tree"
           :default-checked-keys="defaultCodes"
           :highlight-current="true"
           show-checkbox
           :default-expanded-keys="defaultExpandedKeys"
           :filter-node-method="filterNode"
           :style="{width: width + 'px', height: height + 'px'}"
  />
</template>

<script>
  export default {
    name: "setwarning-tree",
    data() {
      return {
        checkAll: true,
        isIndeterminate: true,

        defaultProps: {
          children: 'children',
          label: 'name',
        },
        defaultExpandedKeys: [],
        defaultCodes: [],
        sendNodes: [],
        changeNodes: ''
      }
    },
    props: {
      warningcheck: {
        type: Array,
        default() {
          return []
        }
      },
      data: {
        type: Array,
        required: true
      },
      width: {
        type: Number,
        default() {
          return 460
        }
      },
      height: {
        type: Number,
        default() {
          return 410
        }
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
      },
      checkClear: {
        type: Boolean,
        default() {
          return false
        }
      }
    },
    mounted: function () {
      this.$refs.tree.setCheckedKeys([]);
      console.log(this.warningcheck)
      console.log(this.data)
      if (this.data.length > 0) {
        let checkKeys = []
        if (this.warningcheck.length > 0) {
          this.warningcheck.forEach(item => {
            if (item !== '') {
              checkKeys.push(item)
            }
          })
          this.$refs.tree.setCheckedKeys(checkKeys);
          console.log(checkKeys)
        }
      }
    },
    watch: {
      warningcheck: function(newcheck, oldcheck) {
        let checkKeys = []
        this.$refs.tree.setCheckedKeys([]);
        if (newcheck.length > 0) {
          newcheck.forEach(item => {
            if (item !== '') {
              checkKeys.push(item)
            }
          })
          this.$refs.tree.setCheckedKeys(checkKeys);
          console.log(checkKeys)
        }
      },
      checkClear: function(newstate, oldstate) {
        console.log(newstate)
        if (newstate === true) {
          this.$refs.tree.setCheckedKeys([]);
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
        console.log(data.name)
        this.nodeClick(data)
      },
      getCheckedKeys: function() {
        this.sendNodes = this.$refs.tree.getCheckedKeys();
        console.log(this.sendNodes);
        this.$emit('getnodes', this.sendNodes);
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
