<template>
  <div>
    <div class="search-domain">
      <input type="text" v-model="filterText" placeholder="搜索"/>
      <span class="search-domain-icon"></span>
    </div>
    <el-tree :data="data" :props="defaultProps" node-key="moid"
             @node-click="handleNodeClick" ref="domainTree"
             :highlight-current="true"
             :default-expanded-keys="defaultExpandedKeys"
             :filter-node-method="filterNode"
             :style="{width: width + 'px', height: height + 'px', overflowX: 'scroll'}"/>
  </div>
</template>

<script>
    export default {
        name: "domain-tree",
        data () {
          return {
            defaultProps: {
              children: 'children',
              label: 'name'
            },
            defaultExpandedKeys: [],
            filterText: ''
          }
        },
        props: {
          data: {
            type: Array,
            required: true
          },
          width: {
            type: Number,
            default() {
              return 150
            }
          },
          height: {
            type: Number,
            default() {
              return 400
            }
          },
          nodeClick: {
            type: Function,
            default() {
              return function (data) {
                console.log('moid: ' + data.moid)
              }
            }
          }
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
