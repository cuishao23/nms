<template>
  <div>
    <div class="search-domain">
      <input type="text" v-model="filterText" style="width:305px" placeholder="请输入用户域"/>
      <span class="search-domain-icon"></span>
    </div>
    <el-tree :data="data" :props="defaultProps" node-key="moid"
             @check-change="handleNodeClick" ref="domainTree"
             :highlight-current="true"
             :default-expanded-keys="defaultExpandedKeys"
             :filter-node-method="filterNode"
             :default-expand-all="true"
             show-checkbox
             :style="{width: width + 'px', height: height + 'px', overflowX: 'scroll'}"/>
  </div>
</template>

<script>
    export default {
        name: "userdomain-tree",
        data () {
          return {
            defaultProps: {
              children: 'children',
              label: 'name'
            },
            defaultExpandedKeys: [],
            filterText: '',
            cNodes: [],
          }
        },
        props: {
          // give: {type:string},
          data: {
            type: Array,
            required: true
          },
          width: {
            type: Number,
            default() {
              return 330
            }
          },
          height: {
            type: Number,
            default() {
              return 330
            }
          },
          nodeClick: {
            type: Function,
            default() {
              return function (data) {
                console.log('data: ' + data)
                console.log('moid: ' + data.moid)
              }
            }
          }
        },
      model: {
        event: 'returnBack'
      },
      watch: {
        filterText: function(val) {
          this.$refs.domainTree.filter(val);
        }
      },
      mounted: function () {
        if (this.data.length > 0) {
          this.defaultExpandedKeys = [this.data[0].moid]
        }
      },
      methods: {
        handleNodeClick: function(data) {
          this.nodeClick(data)
          this.cNodes=this.$refs.domainTree.getCheckedNodes()
          this.$emit('returnBack', this.cNodes);
        },
        filterNode: function(value, data) {
          if (!value) return true;
          return data.name.indexOf(value) !== -1;
        },
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
</style>
